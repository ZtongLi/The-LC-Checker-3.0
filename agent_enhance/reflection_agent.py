"""
反思纠错 Agent (Reflection Agent)

接收 Phase 3+4 合并后的不符点列表，让 LLM 以"审核专家复核"的角色，
按 4 个维度逐项检查，输出修正后的最终不符点列表。
"""

import logging
from typing import Dict, List, Any, Optional

from agent_enhance.llm_client import AgentLLMClient
from agent_enhance.output_checker import OutputChecker, REFLECTION_SCHEMA
from agent_enhance.prompts.reflection_prompt import get_reflection_prompt

logger = logging.getLogger(__name__)


class ReflectionAgent:
    """
    反思纠错 Agent
    
    4 维度检查标准：
    1. 字段匹配准确性 - 不符点涉及的字段值是否真实存在差异
    2. UCP 条款引用正确性 - 引用的条款是否适用
    3. 严重程度合理性 - 严重/一般/轻微的判定是否合理
    4. 遗漏检查 - 是否有应检未检的不符点
    """
    
    def __init__(
        self,
        llm_client: AgentLLMClient,
        output_checker: OutputChecker,
        max_loop: int = 5
    ):
        """
        初始化 Reflection Agent
        
        Args:
            llm_client: LLM 客户端
            output_checker: 输出校验器
            max_loop: 最大重试次数
        """
        self.llm_client = llm_client
        self.output_checker = output_checker
        self.max_loop = max_loop
    
    def reflect(
        self,
        discrepancies: List[Dict[str, Any]],
        lc: Dict[str, Any],
        invoice: Dict[str, Any],
        bl: Dict[str, Any],
        insurance: Dict[str, Any],
        presentation_date: str = ""
    ) -> List[Dict[str, Any]]:
        """
        完整反思流程
        
        Args:
            discrepancies: 待反思的不符点列表
            lc: 信用证数据
            invoice: 发票数据
            bl: 提单数据
            insurance: 保险单数据
            presentation_date: 交单日期
            
        Returns:
            修正后的不符点列表
        """
        if not discrepancies:
            logger.info("No discrepancies to reflect on")
            return []
        
        # 构建反思 prompt
        system_prompt, user_prompt = get_reflection_prompt(
            discrepancies,
            lc,
            invoice,
            bl,
            insurance,
            presentation_date
        )
        
        try:
            # 调用 LLM + 校验
            reflection_result = self.llm_client.call_json(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                schema=REFLECTION_SCHEMA,
                temperature=0.1,
                max_loop=self.max_loop
            )
            
            # 应用反思结果
            final_discrepancies = self._apply_reflection(
                discrepancies,
                reflection_result
            )
            
            logger.info(f"Reflection complete: {len(discrepancies)} -> {len(final_discrepancies)} discrepancies")
            
            return final_discrepancies
            
        except Exception as e:
            logger.error(f"Reflection failed: {e}, returning original discrepancies")
            return discrepancies
    
    def _apply_reflection(
        self,
        original: List[Dict[str, Any]],
        reflection_result: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        应用反思结果到原始不符点列表
        
        action 类型：
        - keep: 保留原不符点
        - remove: 删除原不符点
        - modify: 修改原不符点
        - add: 添加新不符点
        
        Args:
            original: 原始不符点列表
            reflection_result: 反思结果列表
            
        Returns:
            修正后的不符点列表
        """
        result = []
        removed_indices = set()
        modified_indices = {}  # index -> modified item
        
        # 首先处理所有反思指令
        for reflection in reflection_result:
            action = reflection.get("action", "keep")
            
            if action == "remove":
                idx = reflection.get("original_index")
                if idx is not None and 0 <= idx < len(original):
                    removed_indices.add(idx)
                    logger.debug(f"Removing discrepancy at index {idx}: {reflection.get('reason', '')}")
                    
            elif action == "modify":
                idx = reflection.get("original_index")
                if idx is not None and 0 <= idx < len(original):
                    modified_item = original[idx].copy()
                    # 应用修改
                    if "severity" in reflection:
                        modified_item["severity"] = reflection["severity"]
                    if "description" in reflection:
                        modified_item["description"] = reflection["description"]
                    if "ucp_reference" in reflection:
                        modified_item["ucp_reference"] = reflection["ucp_reference"]
                    if "field" in reflection:
                        modified_item["field"] = reflection["field"]
                    
                    modified_indices[idx] = modified_item
                    logger.debug(f"Modifying discrepancy at index {idx}: {reflection.get('reason', '')}")
                    
            elif action == "add":
                new_item = {
                    "document": reflection.get("document", ""),
                    "field": reflection.get("field", ""),
                    "description": reflection.get("description", ""),
                    "ucp_reference": reflection.get("ucp_reference", ""),
                    "severity": reflection.get("severity", "一般"),
                }
                # 添加标记
                new_item["reflection_note"] = reflection.get("reflection_note", "由反思 Agent 添加")
                result.append(new_item)
                logger.debug(f"Adding new discrepancy: {new_item['description'][:50]}...")
        
        # 构建最终结果
        for i, item in enumerate(original):
            if i in removed_indices:
                continue  # 跳过被删除的
            elif i in modified_indices:
                result.append(modified_indices[i])  # 使用修改后的版本
            else:
                result.append(item)  # 保留原样
        
        return result
    
    def quick_check(
        self,
        discrepancy: Dict[str, Any],
        lc: Dict[str, Any],
        invoice: Dict[str, Any],
        bl: Dict[str, Any],
        insurance: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        对单个不符点进行快速反思检查
        
        Args:
            discrepancy: 单个不符点
            lc: 信用证数据
            invoice: 发票数据
            bl: 提单数据
            insurance: 保险单数据
            
        Returns:
            包含检查结果的字典
        """
        system_prompt = """你是信用证审核专家。请对提供的不符点进行快速复核，判断其准确性。

请从以下角度评估：
1. 该不符点是否真实存在？
2. 引用的 UCP 条款是否正确？
3. 严重程度判定是否合理？

只返回简短的判断结果，JSON格式：
{
    "valid": true/false,
    "confidence": "高/中/低",
    "issue": "如有问题，简要说明"
}"""
        
        user_prompt = f"""不符点详情：
- 涉及单据: {discrepancy.get('document', '')}
- 字段: {discrepancy.get('field', '')}
- 描述: {discrepancy.get('description', '')}
- 引用条款: {discrepancy.get('ucp_reference', '')}
- 严重程度: {discrepancy.get('severity', '')}

信用证关键信息：
- 金额: {lc.get('amount', '')} {lc.get('currency', '')}
- 货物: {lc.get('goods_description', '')[:100]}...

请快速评估此不符点是否准确。"""
        
        try:
            answer = self.llm_client.call(system_prompt, user_prompt, temperature=0.1)
            # 简单解析
            import json
            if '"valid": true' in answer.lower():
                return {"valid": True, "confidence": "中", "issue": ""}
            else:
                return {"valid": False, "confidence": "中", "issue": answer[:200]}
        except Exception as e:
            logger.error(f"Quick check failed: {e}")
            return {"valid": True, "confidence": "低", "issue": "检查失败，保留原判"}
