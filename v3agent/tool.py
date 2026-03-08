"""
🛠️ 工具模块 - Prompt生成 & API封装
"""

import os
import json
import logging
from typing import Dict, Any, List, Union, Optional
from dataclasses import dataclass

from .arguments import get_config, LLMConfig
from .jsonchecker import JSONChecker

logger = logging.getLogger(__name__)


class LLMClient:
    """统一 LLM 调用客户端"""
    
    def __init__(self, config: Optional[LLMConfig] = None):
        if config is None:
            config = get_config().llm
        self.config = config
        self._client = None
    
    def _get_client(self):
        """获取 OpenAI 客户端"""
        if self._client is None:
            try:
                from openai import OpenAI
                self._client = OpenAI(
                    base_url=self.config.base_url,
                    api_key=self.config.api_key,
                    timeout=self.config.timeout
                )
            except ImportError:
                raise ImportError("openai package is required")
        return self._client
    
    def call(self, system_prompt: str, user_prompt: str, 
             temperature: float = 0.1, max_tokens: Optional[int] = None) -> str:
        """单次 LLM 调用"""
        client = self._get_client()
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        response = client.chat.completions.create(
            model=self.config.model_name,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        return response.choices[0].message.content.strip()
    
    def call_json(self, system_prompt: str, user_prompt: str,
                  schema: Dict[str, Any], temperature: float = 0.1,
                  max_loop: int = 5, max_tokens: Optional[int] = None) -> Union[Dict, List]:
        """调用 LLM 并校验 JSON"""
        checker = JSONChecker(schema)
        last_error = None
        
        for attempt in range(max_loop):
            try:
                answer = self.call(system_prompt, user_prompt, temperature, max_tokens)
                result = checker.parse_and_validate(answer)
                
                if result is not None:
                    return result
                    
            except Exception as e:
                last_error = str(e)
                if attempt < max_loop - 1:
                    user_prompt = f"""{user_prompt}

【重要提示】你之前的输出格式不正确，请严格按照 JSON 格式输出。"""
        
        raise ValueError(f"Failed after {max_loop} attempts: {last_error}")


class PromptBuilder:
    """Prompt 构建器"""
    
    @staticmethod
    def get_planner_prompt(field_summary: str) -> tuple:
        """Planner Agent Prompt"""
        system_prompt = """你是信用证审核专家。扫描单据字段，识别专业术语和潜在风险。

请从以下维度分析：
1. **陌生术语**：保险险别、贸易术语、特殊条款等
2. **歧义表达**：约数词（approximately, about）、模糊表述等
3. **关键风险字段**：金额容差、日期要求、单据份数等

输出格式（使用 # 分隔）：
**陌生术语**: term1#term2#term3
**歧义表达**: term4#term5
**关键风险**: field1#field2

如果没有某类内容，输出 "无"。"""

        user_prompt = f"请分析以下单据字段：\n\n{field_summary}"
        return system_prompt, user_prompt
    
    @staticmethod
    def get_knowledge_prompt(term: str, retrieved_docs: List[str]) -> tuple:
        """Knowledge Agent Prompt"""
        system_prompt = """你是 UCP600 信用证条款专家。请根据参考文档解释专业术语。

要求：
1. 解释简洁准确，不超过 200 字
2. 如与 UCP600 条款相关，请指明具体条款号
3. 说明该术语在信用证审核中的注意要点"""

        docs_text = "\n\n".join([f"参考 {i+1}:\n{doc}" for i, doc in enumerate(retrieved_docs[:3])])
        user_prompt = f"术语：{term}\n\n{docs_text}\n\n请解释该术语。"
        return system_prompt, user_prompt
    
    @staticmethod
    def get_disambiguation_prompt(terms: List[str], doc_context: str = "") -> tuple:
        """消歧 Prompt"""
        system_prompt = """你是信用证条款解读专家。对歧义表达进行上下文消歧。

说明：
1. 该表达在信用证中的常见含义
2. 单据中应如何体现
3. 潜在审核风险点"""

        terms_text = "\n".join([f"- {term}" for term in terms])
        context_text = f"\n\n文档上下文：\n{doc_context}" if doc_context else ""
        user_prompt = f"歧义表达：\n{terms_text}{context_text}\n\n请逐一解释。"
        return system_prompt, user_prompt
    
    @staticmethod
    def get_contrastive_system_prompt(contrastive_examples: str = "", knowledge_context: str = "") -> str:
        """增强版审核 System Prompt"""
        base_prompt = """你是信用证审核专家，精通 UCP600 规则。请审核单据，识别所有不符点。

输出要求（JSON 格式）：
[
  {
    "document": "单据名称",
    "field": "字段名",
    "description": "差异描述",
    "ucp_reference": "UCP600 条款",
    "severity": "严重/一般/轻微"
  }
]

没有发现不符点时返回空数组 []。"""
        
        if knowledge_context:
            base_prompt += f"\n\n{knowledge_context}"
        
        if contrastive_examples:
            base_prompt += f"\n\n{contrastive_examples}"
        
        return base_prompt
    
    @staticmethod
    def get_contrastive_user_prompt(lc: Dict, invoice: Dict, bl: Dict, 
                                    insurance: Dict, presentation_date: str) -> str:
        """增强版审核 User Prompt"""
        lines = ["请审核以下单据，识别不符点：\n"]
        
        lines.append("【信用证】")
        lines.append(f"信用证号：{lc.get('lc_number', 'N/A')}")
        lines.append(f"金额：{lc.get('currency', '')} {lc.get('amount', 0)}")
        lines.append(f"货物描述：{lc.get('goods_description', 'N/A')}")
        lines.append(f"最迟装运日：{lc.get('shipment', {}).get('latest_date', 'N/A')}")
        
        lines.append("\n【商业发票】")
        lines.append(f"出具人：{invoice.get('issued_by', 'N/A')}")
        lines.append(f"金额：{invoice.get('currency', '')} {invoice.get('total_amount', 0)}")
        
        lines.append("\n【提单】")
        lines.append(f"托运人：{bl.get('shipper', 'N/A')}")
        lines.append(f"装货港：{bl.get('loading_port', 'N/A')}")
        lines.append(f"卸货港：{bl.get('discharge_port', 'N/A')}")
        lines.append(f"装船日期：{bl.get('shipped_on_board_date', 'N/A')}")
        
        lines.append("\n【保险单】")
        lines.append(f"险别：{insurance.get('coverage', 'N/A')}")
        
        lines.append(f"\n【交单日期】{presentation_date}")
        lines.append("\n请以 JSON 格式输出不符点列表。")
        
        return "\n".join(lines)
    
    @staticmethod
    def get_reflection_prompt(discrepancies: List[Dict], lc: Dict, invoice: Dict,
                              bl: Dict, insurance: Dict, presentation_date: str) -> tuple:
        """Reflection Agent Prompt"""
        system_prompt = """你是资深信用证审核专家。请复核以下不符点列表。

4 维度检查：
1. 字段匹配准确性
2. UCP 条款引用正确性
3. 严重程度合理性
4. 遗漏检查

输出格式（JSON 数组）：
{
  "action": "keep/remove/modify/add",
  "original_index": 0,
  "document": "单据名",
  "field": "字段名",
  "description": "描述",
  "severity": "严重/一般/轻微",
  "reason": "修改理由"
}"""

        disc_text = []
        for i, d in enumerate(discrepancies):
            disc_text.append(f"[{i}] {d.get('document', '')}/{d.get('field', '')}: {d.get('description', '')}")
        
        user_prompt = f"待复核不符点：\n\n{chr(10).join(disc_text)}"
        return system_prompt, user_prompt


@dataclass
class SelectedExamples:
    """选中的案例集合"""
    positive: List[Dict] = None
    negative: List[Dict] = None
    boundary: List[Dict] = None
    
    def __post_init__(self):
        if self.positive is None:
            self.positive = []
        if self.negative is None:
            self.negative = []
        if self.boundary is None:
            self.boundary = []


class ContrastiveExampleManager:
    """正反对比样本管理器"""
    
    def __init__(self, data_dir: str = "contrastive_data"):
        self.data_dir = data_dir
        self.positive_cases: List[Dict] = []
        self.negative_cases: List[Dict] = []
        self.boundary_cases: List[Dict] = []
        
        self.positive_by_category: Dict[str, List[Dict]] = {}
        self.negative_by_category: Dict[str, List[Dict]] = {}
        self.boundary_by_category: Dict[str, List[Dict]] = {}
        
        self._load_data()
    
    def _load_data(self):
        """加载数据"""
        try:
            positive_path = os.path.join(self.data_dir, "positive_cases.json")
            if os.path.exists(positive_path):
                with open(positive_path, 'r', encoding='utf-8') as f:
                    self.positive_cases = json.load(f)
                self._index_by_category(self.positive_cases, self.positive_by_category)
            
            negative_path = os.path.join(self.data_dir, "negative_cases.json")
            if os.path.exists(negative_path):
                with open(negative_path, 'r', encoding='utf-8') as f:
                    self.negative_cases = json.load(f)
                self._index_by_category(self.negative_cases, self.negative_by_category)
            
            boundary_path = os.path.join(self.data_dir, "boundary_cases.json")
            if os.path.exists(boundary_path):
                with open(boundary_path, 'r', encoding='utf-8') as f:
                    self.boundary_cases = json.load(f)
                self._index_by_category(self.boundary_cases, self.boundary_by_category)
                
        except Exception as e:
            logger.error(f"Failed to load contrastive data: {e}")
    
    def _index_by_category(self, cases: List[Dict], index: Dict):
        """按类别索引"""
        for case in cases:
            category = case.get("category", "general")
            if category not in index:
                index[category] = []
            index[category].append(case)
    
    def select_relevant(self, lc: Dict, invoice: Dict, bl: Dict, insurance: Dict) -> SelectedExamples:
        """智能选择相关案例"""
        selected = SelectedExamples()
        
        # 金额容差
        if lc.get("amount_tolerance") and lc.get("amount_tolerance") != "+/- 0%":
            self._add_from_category(selected, "amount_tolerance", "positive")
        
        # 约数词
        goods_desc = lc.get("goods_description", "")
        quantity = lc.get("quantity", "")
        if any(w in f"{goods_desc} {quantity}".lower() for w in ["approximately", "about"]):
            self._add_from_category(selected, "approximate_quantity", "boundary")
        
        # 保险
        if insurance.get("coverage") or lc.get("insurance_coverage"):
            self._add_from_category(selected, "insurance_coverage", "positive")
        
        # 港口
        if lc.get("shipment", {}).get("loading_port") and bl.get("loading_port"):
            self._add_from_category(selected, "port_matching", "negative")
        
        # 货物描述
        if lc.get("goods_description"):
            self._add_from_category(selected, "goods_description_diff", "positive")
        
        # 日期
        if lc.get("shipment", {}).get("latest_date") and bl.get("shipped_on_board_date"):
            self._add_from_category(selected, "late_shipment", "positive")
        
        return selected
    
    def _add_from_category(self, selected: SelectedExamples, category: str, 
                          case_type: str, max_items: int = 2):
        """添加案例"""
        if case_type == "positive":
            cases = self.positive_by_category.get(category, [])
            for case in cases[:max_items]:
                if case not in selected.positive:
                    selected.positive.append(case)
        elif case_type == "negative":
            cases = self.negative_by_category.get(category, [])
            for case in cases[:max_items]:
                if case not in selected.negative:
                    selected.negative.append(case)
        elif case_type == "boundary":
            cases = self.boundary_by_category.get(category, [])
            for case in cases[:max_items]:
                if case not in selected.boundary:
                    selected.boundary.append(case)
    
    def format_for_prompt(self, selected: SelectedExamples, max_positive: int = 5,
                         max_negative: int = 5, max_boundary: int = 3) -> str:
        """格式化为 Prompt 文本"""
        if not selected.positive and not selected.negative and not selected.boundary:
            return ""
        
        lines = ["=" * 60, "【正反对比学习样本】", "=" * 60]
        
        if selected.positive:
            lines.append("\n📌 正例（应判为不符点）：")
            for i, case in enumerate(selected.positive[:max_positive], 1):
                lines.append(f"\n【案例 {i}】{case.get('scenario', '')}")
                lines.append(f"  结果: ✅ 不符点（{case.get('severity', '一般')}）")
        
        if selected.negative:
            lines.append("\n\n📌 反例（不应判为不符点）：")
            for i, case in enumerate(selected.negative[:max_negative], 1):
                lines.append(f"\n【案例 {i}】{case.get('scenario', '')}")
                lines.append(f"  结果: ❌ 不构成不符点")
        
        lines.append("\n" + "=" * 60)
        return "\n".join(lines)
