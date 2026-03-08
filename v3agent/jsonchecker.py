"""
✅ 验证模块 - JSON 结构校验
"""

import json
import re
import logging
from typing import Dict, Any, List, Union, Optional

logger = logging.getLogger(__name__)


DISCREPANCY_SCHEMA = {
    "type": "object",
    "required": ["document", "field", "description", "ucp_reference", "severity"],
    "properties": {
        "document": {"type": "string"},
        "field": {"type": "string"},
        "description": {"type": "string"},
        "ucp_reference": {"type": "string"},
        "severity": {"type": "string", "enum": ["严重", "一般", "轻微"]},
        "lc_requirement": {"type": "string"},
        "doc_shows": {"type": "string"},
        "uncertain": {"type": "boolean"},
        "suggestion": {"type": "string"}
    }
}

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


class JSONChecker:
    """JSON 结构校验器"""
    
    def __init__(self, schema: Dict[str, Any], use_json_repair: bool = True):
        self.schema = schema
        self.use_json_repair = use_json_repair
        
        self.json_repair = None
        if use_json_repair:
            try:
                import json_repair
                self.json_repair = json_repair
            except ImportError:
                pass
    
    def check(self, data: Dict[str, Any]) -> bool:
        """校验单个 JSON 对象"""
        required = self.schema.get("required", [])
        for field in required:
            if field not in data:
                return False
            if data[field] is None or data[field] == "":
                return False
        
        properties = self.schema.get("properties", {})
        for field, value in data.items():
            if field in properties:
                expected_type = properties[field].get("type")
                if expected_type and not self._check_type(value, expected_type):
                    return False
                
                enum_values = properties[field].get("enum")
                if enum_values and value not in enum_values:
                    return False
        
        return True
    
    def check_list(self, data_list: List[Dict[str, Any]]) -> bool:
        """校验 JSON 数组"""
        if not isinstance(data_list, list):
            return False
        
        for item in data_list:
            if not isinstance(item, dict):
                return False
            if not self.check(item):
                return False
        
        return True
    
    def parse_and_validate(self, raw_text: str) -> Optional[Union[Dict, List]]:
        """解析并校验"""
        json_text = self._extract_json(raw_text)
        
        try:
            data = json.loads(json_text)
        except json.JSONDecodeError:
            if self.json_repair:
                try:
                    repaired = self.json_repair.repair_json(json_text)
                    data = json.loads(repaired)
                except Exception:
                    return None
            else:
                return None
        
        if isinstance(data, list):
            if self.check_list(data):
                return data
        elif isinstance(data, dict):
            if self.check(data):
                return data
        
        return None
    
    def _extract_json(self, text: str) -> str:
        """提取 JSON"""
        patterns = [
            r'```json\s*(.*?)\s*```',
            r'```\s*(.*?)\s*```',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.DOTALL)
            if match:
                return match.group(1).strip()
        
        bracket_match = re.search(r'\[.*\]', text, re.DOTALL)
        if bracket_match:
            return bracket_match.group(0)
        
        brace_match = re.search(r'\{.*?\}', text, re.DOTALL)
        if brace_match:
            return brace_match.group(0)
        
        return text.strip()
    
    def _check_type(self, value: Any, expected_type: str) -> bool:
        """检查类型"""
        type_map = {
            "string": str,
            "integer": int,
            "number": (int, float),
            "boolean": bool,
            "array": list,
            "object": dict
        }
        
        if expected_type not in type_map:
            return True
        
        return isinstance(value, type_map[expected_type])
