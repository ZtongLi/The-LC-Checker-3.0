"""
Knowledge Agent 的 Prompt 模板

用于向 ChromaDB 检索术语后，构建系统化的知识增强 prompt
"""

from typing import Tuple, List


SYSTEM_PROMPT = """你是信用证领域的知识专家（Knowledge Agent）。

你的任务是：为审核员提供准确的术语解释和条款引用。

你需要基于以下知识库检索结果，组织成清晰、准确的知识摘要：
1. 术语的标准定义
2. UCP600/ISBP 相关条款
3. 实务中的常见处理方式

注意：
- 只使用提供的检索结果，不要编造条款
- 如果检索结果不足，明确说明"信息不足"
- 保持简洁，重点突出对审核判断有用的信息
"""


def get_knowledge_prompt(term: str, retrieved_knowledge: str) -> Tuple[str, str]:
    """
    获取术语解释的 Prompt
    
    Args:
        term: 术语
        retrieved_knowledge: 检索到的知识
        
    Returns:
        (system_prompt, user_prompt) 元组
    """
    user_prompt = f"""请为以下术语提供审核所需的知识解释：

术语：{term}

检索到的知识：
{retrieved_knowledge}

请按以下格式组织回答：
1. 术语定义（1-2句话）
2. UCP/ISBP 相关条款（如有）
3. 审核要点（1-2点）
"""
    return SYSTEM_PROMPT, user_prompt


def get_term_explanation_prompt(terms_with_knowledge: List[Tuple[str, str]]) -> Tuple[str, str]:
    """
    获取多个术语解释的 Prompt
    
    Args:
        terms_with_knowledge: [(term, knowledge), ...] 列表
        
    Returns:
        (system_prompt, user_prompt) 元组
    """
    knowledge_text = "\n\n".join([
        f"【{term}】\n{knowledge}"
        for term, knowledge in terms_with_knowledge
    ])
    
    user_prompt = f"""请为以下术语提供审核所需的知识解释：

{knowledge_text}

请按以下格式组织回答：

📚 术语解释：
1. "术语1" = 定义，参见 UCP600 Article X
2. "术语2" = 定义，参见 ISBP 745 Para X
...
"""
    return SYSTEM_PROMPT, user_prompt
