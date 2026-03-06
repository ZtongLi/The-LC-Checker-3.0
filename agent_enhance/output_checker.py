"""
结构化输出校验器

对 LLM 的每次输出进行严格的 JSON Schema 校验，校验失败则触发重试。
对应 KDR-Agent 的 jsonchecker.py
"""

import json
import re
import logging
from typing import Dict, Any, List, Union, Optional
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


# 不符点 Schema 定义
DISCREPANCY_SCHEMA = {
    "type": "object",
    "required": ["document", "field", "description", "ucp_reference", "severity"],
    "properties": {
        "document": {"type": "string"},
        "field": {"type": "string"},
        "description": {"type": "string"},
        "ucp_reference": {"type": "string"},
        "severity": {"type": "string", "enum": ["严重", "一般", "轻微"]},
        # 可选字段
        "lc_requirement": {"type": "string"},
        "doc_shows": {"type": "string"},
        "uncertain": {"type": "boolean"},
        "suggestion": {"type": "string"}
    }
}

# 反思输出 Schema 定义
REFLECTION_SCHEMA = {
    "type": "object",
    "required": ["action"],
    "properties": {
        "action": {"type": "string", "enum": ["keep", "remove", "modify", "add"]},
        "original_index": {"type": "integer"},
        "document": {"type": "string"},
        "field": {"type": "string"},
        "description": {"type": "string"},
        "ucp_reference": {"type": "string"},
        "severity": {"type": "string"},
        "reason": {"type": "string"},
        "reflection_note": {"type": "string"}
    }
}


@dataclass
class DiscrepancySchema:
    """不符点数据结构"""
    document: str
    field: str
    description: str
    ucp_reference: str
    severity: str  # 严重/一般/轻微
    lc_requirement: Optional[str] = None
    doc_shows: Optional[str] = None
    uncertain: bool = False
    suggestion: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        result = {
            "document": self.document,
            "field": self.field,
            "description": self.description,
            "ucp_reference": self.ucp_reference,
            "severity": self.severity
        }
        if self.lc_requirement:
            result["lc_requirement"] = self.lc_requirement
        if self.doc_shows:
            result["doc_shows"] = self.doc_shows
        if self.uncertain:
            result["uncertain"] = self.uncertain
        if self.suggestion:
            result["suggestion"] = self.suggestion
        return result


@dataclass
class ReflectionSchema:
    """反思输出数据结构"""
    action: str  # keep/remove/modify/add
    original_index: Optional[int] = None
    document: Optional[str] = None
    field: Optional[str] = None
    description: Optional[str] = None
    ucp_reference: Optional[str] = None
    severity: Optional[str] = None
    reason: Optional[str] = None
    reflection_note: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        result = {"action": self.action}
        if self.original_index is not None:
            result["original_index"] = self.original_index
        if self.document:
            result["document"] = self.document
        if self.field:
            result["field"] = self.field
        if self.description:
            result["description"] = self.description
        if self.ucp_reference:
            result["ucp_reference"] = self.ucp_reference
        if self.severity:
            result["severity"] = self.severity
        if self.reason:
            result["reason"] = self.reason
        if self.reflection_note:
            result["reflection_note"] = self.reflection_note
        return result


class OutputChecker:
    """
    结构化输出校验器
    
    功能：
    1. 解析 LLM 输出的 JSON
    2. 校验字段类型和必填项
    3. 自动修复常见 JSON 格式问题
    4. 支持重试机制
    """
    
    def __init__(self, schema: Dict[str, Any], use_json_repair: bool = True):
        """
        初始化校验器
        
        Args:
            schema: JSON Schema 定义
            use_json_repair: 是否使用 json_repair 库进行修复
        """
        self.schema = schema
        self.use_json_repair = use_json_repair
        
        # 尝试导入 json_repair
        self.json_repair = None
        if use_json_repair:
            try:
                import json_repair
                self.json_repair = json_repair
                logger.debug("json_repair library loaded")
            except ImportError:
                logger.warning("json_repair not installed, using standard json parser")
    
    def check(self, data: Dict[str, Any]) -> bool:
        """
        校验单个 JSON 对象是否符合 Schema
        
        Args:
            data: 待校验的字典
            
        Returns:
            是否通过校验
        """
        # 检查必填字段
        required = self.schema.get("required", [])
        for field in required:
            if field not in data:
                logger.warning(f"Missing required field: {field}")
                return False
            if data[field] is None or data[field] == "":
                logger.warning(f"Required field is empty: {field}")
                return False
        
        # 检查字段类型
        properties = self.schema.get("properties", {})
        for field, value in data.items():
            if field in properties:
                expected_type = properties[field].get("type")
                if expected_type and not self._check_type(value, expected_type):
                    logger.warning(f"Field {field} type mismatch: expected {expected_type}, got {type(value)}")
                    return False
                
                # 检查枚举值
                enum_values = properties[field].get("enum")
                if enum_values and value not in enum_values:
                    logger.warning(f"Field {field} value not in enum: {value}")
                    return False
        
        return True
    
    def check_list(self, data_list: List[Dict[str, Any]]) -> bool:
        """
        校验 JSON 数组中每个元素是否都符合 Schema
        
        Args:
            data_list: 待校验的列表
            
        Returns:
            是否全部通过校验
        """
        if not isinstance(data_list, list):
            logger.warning(f"Expected list, got {type(data_list)}")
            return False
        
        for i, item in enumerate(data_list):
            if not isinstance(item, dict):
                logger.warning(f"Item {i} is not a dict: {type(item)}")
                return False
            if not self.check(item):
                logger.warning(f"Item {i} failed validation")
                return False
        
        return True
    
    def parse_and_validate(self, raw_text: str) -> Optional[Union[Dict, List]]:
        """
        解析文本 -> 校验 -> 返回结果
        
        流程：
        1. 从文本中提取 JSON
        2. 尝试解析
        3. 使用 json_repair 修复常见问题
        4. 校验 Schema
        
        Args:
            raw_text: 原始文本（可能包含 markdown 代码块等）
            
        Returns:
            解析校验后的数据，失败返回 None
        """
        # 1. 提取 JSON 文本
        json_text = self._extract_json(raw_text)
        
        # 2. 尝试解析
        try:
            data = json.loads(json_text)
        except json.JSONDecodeError as e:
            logger.warning(f"Standard JSON parse failed: {e}")
            
            # 3. 尝试使用 json_repair 修复
            if self.json_repair:
                try:
                    repaired = self.json_repair.repair_json(json_text)
                    data = json.loads(repaired)
                    logger.debug("JSON repaired successfully")
                except Exception as e2:
                    logger.error(f"JSON repair failed: {e2}")
                    return None
            else:
                return None
        
        # 4. 校验
        if isinstance(data, list):
            if self.check_list(data):
                return data
        elif isinstance(data, dict):
            if self.check(data):
                return data
        
        return None
    
    def _extract_json(self, text: str) -> str:
        """
        从文本中提取 JSON 部分
        
        支持：
        1. Markdown 代码块 ```json ... ```
        2. Markdown 代码块 ``` ... ```
        3. 纯 JSON 文本
        """
        # 尝试匹配 markdown 代码块
        patterns = [
            r'```json\s*(.*?)\s*```',  # ```json ... ```
            r'```\s*(.*?)\s*```',       # ``` ... ```
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.DOTALL)
            if match:
                return match.group(1).strip()
        
        # 尝试直接找 JSON 数组或对象
        # 找方括号包裹的内容
        bracket_match = re.search(r'\[.*\]', text, re.DOTALL)
        if bracket_match:
            return bracket_match.group(0)
        
        # 找花括号包裹的内容
        brace_match = re.search(r'\{.*\}', text, re.DOTALL)
        if brace_match:
            return brace_match.group(0)
        
        # 返回原文本
        return text.strip()
    
    def _check_type(self, value: Any, expected_type: str) -> bool:
        """检查值的类型是否符合预期"""
        type_map = {
            "string": str,
            "integer": int,
            "number": (int, float),
            "boolean": bool,
            "array": list,
            "object": dict
        }
        
        if expected_type not in type_map:
            return True  # 未知类型，跳过检查
        
        expected = type_map[expected_type]
        return isinstance(value, expected)


# 便捷函数
def validate_discrepancies(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    校验不符点列表，过滤掉无效项
    
    Args:
        data: 不符点列表
        
    Returns:
        过滤后的有效列表
    """
    checker = OutputChecker(DISCREPANCY_SCHEMA)
    valid = []
    
    for item in data:
        if checker.check(item):
            valid.append(item)
        else:
            logger.warning(f"Invalid discrepancy item filtered: {item}")
    
    return valid


def validate_reflections(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    校验反思输出列表，过滤掉无效项
    
    Args:
        data: 反思输出列表
        
    Returns:
        过滤后的有效列表
    """
    checker = OutputChecker(REFLECTION_SCHEMA)
    valid = []
    
    for item in data:
        if checker.check(item):
            valid.append(item)
        else:
            logger.warning(f"Invalid reflection item filtered: {item}")
    
    return valid
