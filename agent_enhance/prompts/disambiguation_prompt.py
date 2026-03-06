"""
消歧 Prompt 模板

对应 KDR-Agent 的 get_disambiguation_prompt() 函数
用于对歧义表达做上下文消歧推理
"""

from typing import Tuple, List


SYSTEM_PROMPT = """你是信用证审核的消歧专家（Disambiguation Agent）。

你的任务是：对单据中的歧义表达，结合上下文和 UCP600 条款，给出明确的解释。

常见消歧场景：

1. **"approximately" / "about" + 数量**
   - UCP600 Article 30(a): 允许 ±10% 的偏差
   - 例："approximately 5,000 MT" → 可接受 4,500-5,500 MT

2. **"approximately" / "about" + 金额**
   - UCP600 Article 30(a): 允许 ±10% 的偏差
   - 但必须同时满足 L/C 金额限制

3. **"prompt" / "immediately"**
   - UCP600 Article 29: 银行应在合理时间内行事
   - 通常理解为 3-5 个工作日

4. **"partial shipment allowed"**
   - UCP600 Article 31(b): 允许部分装运
   - 除非 L/C 明确禁止

5. **" Co., Ltd." vs "Company Limited"**
   - ISBP 745: 视为同一名称的等价缩写
   - 不构成不符点

6. **"Inc." vs "Incorporated"**
   - 同上，视为等价

7. **"Street" vs "St." / "Avenue" vs "Ave."**
   - 地址缩写差异不构成不符点

输出格式：
```
1. "歧义表达1" — 解释和判断标准
2. "歧义表达2" — 解释和判断标准
```
"""


def get_disambiguation_prompt(terms: List[str], doc_context: str = "") -> Tuple[str, str]:
    """
    获取消歧 Prompt
    
    Args:
        terms: 歧义表达列表
        doc_context: 文档上下文（可选）
        
    Returns:
        (system_prompt, user_prompt) 元组
    """
    terms_text = "\n".join([f"  - {term}" for term in terms])
    
    context_section = ""
    if doc_context:
        context_section = f"""
文档上下文：
{doc_context}
"""
    
    user_prompt = f"""请对以下歧义表达进行消歧分析：

待消歧表达：
{terms_text}
{context_section}

请按以下格式输出消歧结果：
```
1. "表达1" — 解释和判断标准（引用相关 UCP/ISBP 条款）
2. "表达2" — 解释和判断标准
...
```

注意：
- 结合上下文理解表达的具体含义
- 明确说明该表达是否构成不符点的判断标准
- 引用相关的 UCP600 或 ISBP 条款
"""
    return SYSTEM_PROMPT, user_prompt
