"""
KDR-Agent V3 - 信用证智能审核系统

基于多智能体架构的增强版信用证单据审核系统。
"""

from .main import (
    ReviewOrchestrator,
    ReviewResult,
    PlannerAgent,
    KnowledgeAgent,
    ReflectionAgent,
    review_documents
)
from .arguments import get_config, ConfigManager
from .tool import LLMClient, PromptBuilder, ContrastiveExampleManager
from .jsonchecker import JSONChecker

__version__ = "3.0.0"

__all__ = [
    "ReviewOrchestrator",
    "ReviewResult",
    "PlannerAgent",
    "KnowledgeAgent",
    "ReflectionAgent",
    "LLMClient",
    "PromptBuilder",
    "ContrastiveExampleManager",
    "JSONChecker",
    "get_config",
    "ConfigManager",
    "review_documents",
]
