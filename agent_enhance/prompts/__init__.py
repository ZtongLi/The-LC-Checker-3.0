"""
Prompt 模板子模块

该模块包含所有 Agent 使用的 Prompt 模板。
所有 Prompt 均抽离为独立的 Python 文件，使用函数返回格式化后的 prompt 字符串。
"""

from agent_enhance.prompts.planner_prompt import get_planner_prompt
from agent_enhance.prompts.knowledge_prompt import get_knowledge_prompt
from agent_enhance.prompts.disambiguation_prompt import get_disambiguation_prompt
from agent_enhance.prompts.contrastive_prompt import get_contrastive_system_prompt, get_contrastive_user_prompt
from agent_enhance.prompts.reflection_prompt import get_reflection_prompt

__all__ = [
    "get_planner_prompt",
    "get_knowledge_prompt",
    "get_disambiguation_prompt",
    "get_contrastive_system_prompt",
    "get_contrastive_user_prompt",
    "get_reflection_prompt",
]
