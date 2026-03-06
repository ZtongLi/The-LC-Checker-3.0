"""
The-LC-Checker V3 多智能体增强模块

该模块提供了增强版信用证审核功能，包括：
- Planner Agent: 识别单据中的专业术语和歧义表达
- Knowledge Agent: 通过知识库检索和上下文消歧增强理解
- Reflection Agent: 反思纠错，提升审核准确性
- OutputChecker: 结构化输出校验
- ContrastiveExampleManager: 正反对比样本管理
"""

# 核心 Agent
from agent_enhance.planner_agent import PlannerAgent, PlannerResult
from agent_enhance.knowledge_agent import KnowledgeAgent
from agent_enhance.reflection_agent import ReflectionAgent

# 工具类
from agent_enhance.output_checker import OutputChecker, DiscrepancySchema, ReflectionSchema
from agent_enhance.contrastive_examples import ContrastiveExampleManager, SelectedExamples
from agent_enhance.llm_client import AgentLLMClient

__all__ = [
    # Agents
    "PlannerAgent",
    "PlannerResult",
    "KnowledgeAgent",
    "ReflectionAgent",
    # Tools
    "OutputChecker",
    "DiscrepancySchema",
    "ReflectionSchema",
    "ContrastiveExampleManager",
    "SelectedExamples",
    "AgentLLMClient",
]

__version__ = "3.0.0"
