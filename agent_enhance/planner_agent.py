"""
规划 Agent (Planner Agent)

在正式 AI 审核前，扫描所有 4 份单据的结构化字段数据，
识别其中的专业术语和歧义表达，决定后续哪些术语需要做知识增强。
"""

import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field

from agent_enhance.llm_client import AgentLLMClient
from agent_enhance.prompts.planner_prompt import get_planner_prompt

logger = logging.getLogger(__name__)


@dataclass
class PlannerResult:
    """Planner Agent 的输出结果"""
    unfamiliar_terms: List[str] = field(default_factory=list)    # 陌生术语
    ambiguous_terms: List[str] = field(default_factory=list)     # 歧义表达
    key_risk_fields: List[str] = field(default_factory=list)     # 关键风险字段
    raw_output: str = ""                                          # 原始输出
    
    def is_empty(self) -> bool:
        """检查结果是否为空"""
        return (len(self.unfamiliar_terms) == 0 and 
                len(self.ambiguous_terms) == 0 and 
                len(self.key_risk_fields) == 0)


class PlannerAgent:
    """
    规划 Agent
    
    职责：
    1. 扫描 4 份单据的关键字段
    2. 识别专业术语（如保险险别、贸易术语等）
    3. 识别歧义表达（如 "approximately", "about" 等）
    4. 标记关键风险字段
    """
    
    def __init__(self, llm_client: AgentLLMClient, max_terms: int = 10):
        """
        初始化 Planner Agent
        
        Args:
            llm_client: LLM 客户端
            max_terms: 最大识别术语数量
        """
        self.llm_client = llm_client
        self.max_terms = max_terms
    
    def analyze(
        self,
        lc: Dict[str, Any],
        invoice: Dict[str, Any],
        bl: Dict[str, Any],
        insurance: Dict[str, Any]
    ) -> PlannerResult:
        """
        分析全部单据字段
        
        Args:
            lc: 信用证数据
            invoice: 发票数据
            bl: 提单数据
            insurance: 保险单数据
            
        Returns:
            PlannerResult 分析结果
        """
        # 构建字段摘要
        field_summary = self._build_field_summary(lc, invoice, bl, insurance)
        
        # 获取 prompt
        system_prompt, user_prompt = get_planner_prompt(field_summary)
        
        try:
            # 调用 LLM
            answer = self.llm_client.call(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                temperature=0.2  # 低温度，更确定
            )
            
            # 解析输出
            result = self._parse_planner_output(answer)
            result.raw_output = answer
            
            logger.info(f"Planner analysis complete: {len(result.unfamiliar_terms)} unfamiliar terms, "
                       f"{len(result.ambiguous_terms)} ambiguous terms, "
                       f"{len(result.key_risk_fields)} risk fields")
            
            return result
            
        except Exception as e:
            logger.error(f"Planner analysis failed: {e}")
            return PlannerResult(raw_output=str(e))
    
    def _build_field_summary(
        self,
        lc: Dict[str, Any],
        invoice: Dict[str, Any],
        bl: Dict[str, Any],
        insurance: Dict[str, Any]
    ) -> str:
        """
        将 4 份单据关键字段拼接为摘要文本
        """
        lines = []
        lines.append("=" * 60)
        lines.append("【单据字段摘要】")
        lines.append("=" * 60)
        
        # 信用证字段
        lines.append("\n【信用证 (L/C)】")
        lc_fields = [
            ("货物描述", lc.get("goods_description", "")),
            ("数量", lc.get("quantity", "")),
            ("金额", f"{lc.get('amount', '')} {lc.get('currency', '')}"),
            ("金额容差", lc.get("amount_tolerance", "")),
            ("受益人", self._extract_name(lc.get("beneficiary", {}))),
            ("最迟装运日", lc.get("shipment", {}).get("latest_date", "")),
            ("装货港", lc.get("shipment", {}).get("loading_port", "")),
            ("卸货港", lc.get("shipment", {}).get("discharge_port", "")),
            ("贸易术语", lc.get("trade_terms", "")),
            ("要求保险", lc.get("insurance_coverage", "")),
        ]
        for label, value in lc_fields:
            if value:
                lines.append(f"  {label}: {value}")
        
        # 商业发票字段
        lines.append("\n【商业发票 (Commercial Invoice)】")
        inv_fields = [
            ("出具人", invoice.get("issued_by", "")),
            ("货物描述", invoice.get("goods_description", "")),
            ("数量", invoice.get("quantity", "")),
            ("金额", f"{invoice.get('total_amount', '')} {invoice.get('currency', '')}"),
        ]
        for label, value in inv_fields:
            if value:
                lines.append(f"  {label}: {value}")
        
        # 提单字段
        lines.append("\n【提单 (Bill of Lading)】")
        bl_fields = [
            ("托运人", bl.get("shipper", "")),
            ("收货人", bl.get("consignee", "")),
            ("装货港", bl.get("loading_port", "")),
            ("卸货港", bl.get("discharge_port", "")),
            ("装船日期", bl.get("shipped_on_board_date", "")),
            ("货物描述", bl.get("goods_description", "")),
            ("清洁提单", "是" if bl.get("clean_on_board", True) else "否"),
            ("批注", bl.get("remarks", "")),
        ]
        for label, value in bl_fields:
            if value:
                lines.append(f"  {label}: {value}")
        
        # 保险单字段
        lines.append("\n【保险单 (Insurance Policy)】")
        ins_fields = [
            ("被保险人", self._format_insured(insurance.get("insured", ""))),
            ("险别", insurance.get("coverage", "")),
            ("保险金额", insurance.get("sum_insured", "")),
            ("起运地", insurance.get("from_location", "")),
            ("目的地", insurance.get("to_location", "")),
        ]
        for label, value in ins_fields:
            if value:
                lines.append(f"  {label}: {value}")
        
        return "\n".join(lines)
    
    def _extract_name(self, beneficiary) -> str:
        """提取受益人名称"""
        if isinstance(beneficiary, dict):
            return beneficiary.get("name", "")
        return str(beneficiary)
    
    def _format_insured(self, insured) -> str:
        """格式化被保险人字段"""
        if isinstance(insured, list):
            return ", ".join(insured)
        return str(insured)
    
    def _parse_planner_output(self, answer: str) -> PlannerResult:
        """
        解析 LLM 回答中的术语列表
        
        期望格式：
        **陌生术语**: term1#term2#term3
        **歧义表达**: term4#term5
        **关键风险**: field1#field2
        """
        result = PlannerResult()
        
        # 解析陌生术语
        unfamiliar_match = self._extract_section(answer, "陌生术语", "unfamiliar")
        if unfamiliar_match:
            result.unfamiliar_terms = [t.strip() for t in unfamiliar_match.split("#") if t.strip()]
        
        # 解析歧义表达
        ambiguous_match = self._extract_section(answer, "歧义表达", "ambiguous")
        if ambiguous_match:
            result.ambiguous_terms = [t.strip() for t in ambiguous_match.split("#") if t.strip()]
        
        # 解析关键风险
        risk_match = self._extract_section(answer, "关键风险", "key risk", "risk")
        if risk_match:
            result.key_risk_fields = [t.strip() for t in risk_match.split("#") if t.strip()]
        
        # 限制数量
        result.unfamiliar_terms = result.unfamiliar_terms[:self.max_terms]
        result.ambiguous_terms = result.ambiguous_terms[:self.max_terms]
        result.key_risk_fields = result.key_risk_fields[:self.max_terms]
        
        return result
    
    def _extract_section(self, text: str, *keywords: str) -> Optional[str]:
        """从文本中提取特定部分"""
        import re
        
        for keyword in keywords:
            # 尝试匹配 **关键词**: value 格式
            pattern = rf"\*\*{keyword}\*\*[:：]\s*(.+?)(?=\n\*\*|$)"
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                return match.group(1).strip()
            
            # 尝试匹配 关键词: value 格式
            pattern = rf"{keyword}[:：]\s*(.+?)(?=\n\w+[:：]|$)"
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                return match.group(1).strip()
        
        return None
