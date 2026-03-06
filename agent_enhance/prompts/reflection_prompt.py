"""
Reflection Agent 的 Prompt 模板

对应 KDR-Agent 的 get_reflection_prompt() 函数
构建 4 维度反思 prompt，要求逐项审视已有的不符点列表
"""

from typing import Tuple, List, Dict, Any


SYSTEM_PROMPT = """你是资深的信用证审核复核专家（Reflection Agent）。

你的任务是：对 AI 初审发现的不符点进行复核，从 4 个维度检查每个不符点的准确性。

## 4 维度检查标准

### 1. 字段匹配准确性（对应实体边界是否准确）
- 不符点涉及的信用证字段值和单据字段值是否真的存在差异？
- 是否是 OCR 提取错误导致的误判？
- 是否将相似但不相同的值错误判断为不符？

### 2. UCP 条款引用正确性（对应实体类型是否准确）
- 引用的 UCP600 条款是否真的适用于该不符点？
- 例如：保险金额问题应引用 Article 28(f)(ii) 而非 Article 18
- 是否遗漏了更准确的条款引用？

### 3. 严重程度合理性（边界+类型同时准确）
- "严重/一般/轻微"的判定是否合理？
- 缩写差异是否该降为轻微？
- 金额超限是否确实严重？
- 是否考虑了行业惯例和商业实践？

### 4. 遗漏检查（是否遗漏实体）
- 是否有应检未检的不符点？
- 保险起运地/目的地是否与提单一致？
- 单据份数是否满足要求？（这是高频漏报项！信用证要求 triplicate/full set 时必须逐一核对）
- 贸易术语是否与信用证一致？（FOB/CIF/CFR/EXW 等任何差异都是不符点）
- 名称是否完全一致？（缩写形式与全称的差异也是不符点）
- 背书是否正确？

## 输出格式

对每个不符点，判断采取以下哪种 action：
- **keep**: 保留该不符点（经复核确认无误）
- **remove**: 删除该不符点（仅当你有100%把握确定这是误判时才使用！）
  【删除门槛极高】只有以下情况才可以 remove：
  (a) 字段值完全相同，根本不存在差异（如日期格式不同但实际日期相同）
  (b) 有明确的 UCP600 条款或 ISBP 惯例支持"不构成不符"
  (c) 纯粹的大小写/标点/空格差异（且不影响含义）
  【绝对不能删除的情况】：
  - 名称缩写差异（Co.,Ltd. vs Company Limited, Corp. vs Company Limited）
  - 金额/数量差异（无论多小）
  - 贸易术语差异（FOB vs CIF 等）
  - 单据份数差异
  - 险别/保险条款差异
  如果不确定，选择 keep 而不是 remove。宁可多报，不可漏报。
- **modify**: 修改该不符点（部分正确，需要调整 severity/description 等）
- **add**: 添加新不符点（原列表遗漏了应检项目）

以 JSON 数组格式输出，每个对象包含：
```json
{
    "action": "keep/remove/modify/add",
    "original_index": 0,  // 对于 keep/remove/modify，指定原列表索引
    "document": "单据名称",  // 对于 add，或需要修改时
    "field": "字段名称",
    "description": "不符点描述",
    "ucp_reference": "UCP600 Article X",
    "severity": "严重/一般/轻微",
    "reason": "采取此 action 的理由",
    "reflection_note": "复核备注"
}
```

注意：
- 必须为原列表中的每个不符点都做出判断（keep/remove/modify）
- 如果添加新不符点，使用 action: "add"
- 输出必须是合法的 JSON 数组，可以被 Python json.loads() 解析
"""


def get_reflection_prompt(
    discrepancies: List[Dict[str, Any]],
    lc: Dict[str, Any],
    invoice: Dict[str, Any],
    bl: Dict[str, Any],
    insurance: Dict[str, Any],
    presentation_date: str = ""
) -> Tuple[str, str]:
    """
    获取反思 Prompt
    
    Args:
        discrepancies: 不符点列表
        lc: 信用证数据
        invoice: 发票数据
        bl: 提单数据
        insurance: 保险单数据
        presentation_date: 交单日期
        
    Returns:
        (system_prompt, user_prompt) 元组
    """
    # 格式化不符点列表
    disc_text = "\n\n".join([
        f"【不符点 {i+1}】\n"
        f"  单据: {d.get('document', '')}\n"
        f"  字段: {d.get('field', '')}\n"
        f"  描述: {d.get('description', '')}\n"
        f"  引用条款: {d.get('ucp_reference', '')}\n"
        f"  严重程度: {d.get('severity', '')}"
        for i, d in enumerate(discrepancies)
    ])
    
    # 格式化单据摘要
    doc_summary = f"""信用证关键信息：
- 金额: {lc.get('currency', '')} {lc.get('amount', '')} (容差: {lc.get('amount_tolerance', '')})
- 货物: {lc.get('goods_description', '')[:100]}...
- 装货港: {lc.get('shipment', {}).get('loading_port', '')}
- 卸货港: {lc.get('shipment', {}).get('discharge_port', '')}
- 最迟装运日: {lc.get('shipment', {}).get('latest_date', '')}
- 保险要求: {lc.get('insurance_coverage', '')}

发票信息：
- 出具人: {invoice.get('issued_by', '')}
- 金额: {invoice.get('currency', '')} {invoice.get('total_amount', '')}
- 货物: {invoice.get('goods_description', '')[:100]}...

提单信息：
- 托运人: {bl.get('shipper', '')}
- 装货港: {bl.get('loading_port', '')}
- 卸货港: {bl.get('discharge_port', '')}
- 装船日期: {bl.get('shipped_on_board_date', '')}

保险单信息：
- 被保险人: {insurance.get('insured', '')}
- 险别: {insurance.get('coverage', '')}
- 保险金额: {insurance.get('sum_insured', '')}
- 起运地: {insurance.get('from_location', '')}
- 目的地: {insurance.get('to_location', '')}
"""
    
    user_prompt = f"""请对以下 {len(discrepancies)} 个不符点进行复核：

{disc_text}

单据摘要：
{doc_summary}

交单日期: {presentation_date}

请从 4 个维度（字段匹配准确性、UCP条款引用正确性、严重程度合理性、遗漏检查）逐一审视每个不符点，
并按要求的 JSON 格式输出复核结果。

注意：
1. 不要遗漏原列表中的任何一个不符点
2. 如有明显遗漏的不符点，使用 "add" action 添加
3. 确保输出是合法的 JSON 数组"""
    
    return SYSTEM_PROMPT, user_prompt
