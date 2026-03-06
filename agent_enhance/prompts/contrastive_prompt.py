"""
正反对比 Prompt 模板

将正反例格式化为可直接注入审核 prompt 的文本
对应 KDR-Agent 的 define_sample_min.json 的注入逻辑
"""

from typing import Tuple, List, Dict, Any


SYSTEM_PROMPT_WITH_CONTRASTIVE = """你是资深的信用证审核专家。请对以下单据进行全面审核，识别所有不符点。

{contrastive_examples}

【审核原则】
1. 严格对照 UCP600 和 ISBP 745 条款
2. 参考正反对比样本，避免常见误判
3. 对不确定的判断，标注"存疑"
4. 输出结构化 JSON 格式

{knowledge_context}

请仔细分析单据，识别所有不符点。

【强制检查清单——以下每项必须逐一核对，不得跳过】
1. 单据份数：信用证要求的每种单据份数（triplicate/full set/3/3等）是否与实际提交份数一致？
2. 贸易术语：发票上的贸易术语（FOB/CIF/CFR/EXW等）是否与信用证完全一致？
3. 受益人/被保险人名称：所有单据中的名称是否与信用证严格一致？（缩写不等于全称：Co.,Ltd.≠Company Limited, Corp.≠Company Limited, Ltd≠Limited）
4. 金额：发票金额是否超出信用证金额？保险金额是否满足110%要求？
5. 货物描述：型号、规格、数量是否完全一致？
6. 装运条款：是否存在分批装运违规？装运日期是否超期？
7. 保险条款：险别是否完全覆盖信用证要求的所有风险？是否有排除条款与要求矛盾？

宁可多报，不可漏报。如果存在疑问，报为不符点并标注存疑。

对于每个不符点，请提供：
- 涉及单据名称
- 不符字段
- 不符点描述
- 引用 UCP600 条款
- 严重程度（严重/一般/轻微）

以 JSON 数组格式输出，每个不符点为一个对象。"""


def get_contrastive_system_prompt(
    contrastive_text: str,
    knowledge_context: str = ""
) -> str:
    """
    获取包含正反例的系统 Prompt
    
    Args:
        contrastive_text: 格式化后的正反例文本
        knowledge_context: 知识上下文（可选）
        
    Returns:
        系统 Prompt
    """
    knowledge_section = ""
    if knowledge_context:
        knowledge_section = f"\n{knowledge_context}\n"
    
    return SYSTEM_PROMPT_WITH_CONTRASTIVE.format(
        contrastive_examples=contrastive_text,
        knowledge_context=knowledge_section
    )


def get_contrastive_user_prompt(
    lc: Dict[str, Any],
    invoice: Dict[str, Any],
    bl: Dict[str, Any],
    insurance: Dict[str, Any],
    presentation_date: str = ""
) -> str:
    """
    获取包含单据信息的用户 Prompt
    
    Args:
        lc: 信用证数据
        invoice: 发票数据
        bl: 提单数据
        insurance: 保险单数据
        presentation_date: 交单日期
        
    Returns:
        用户 Prompt
    """
    lines = []
    lines.append("请审核以下单据：\n")
    
    # 信用证信息
    lines.append("=" * 60)
    lines.append("【信用证信息】")
    lines.append("=" * 60)
    lines.append(f"交单日期: {presentation_date}")
    lines.append(f"信用证号: {lc.get('lc_no', '')}")
    lines.append(f"开证行: {lc.get('issuing_bank', '')}")
    lines.append(f"受益人: {lc.get('beneficiary', {}).get('name', '') if isinstance(lc.get('beneficiary'), dict) else lc.get('beneficiary', '')}")
    lines.append(f"申请人: {lc.get('applicant', '')}")
    lines.append(f"金额: {lc.get('currency', '')} {lc.get('amount', '')}")
    lines.append(f"金额容差: {lc.get('amount_tolerance', '')}")
    lines.append(f"最迟装运日: {lc.get('shipment', {}).get('latest_date', '')}")
    lines.append(f"有效期: {lc.get('expiry_date', '')}")
    lines.append(f"货物描述: {lc.get('goods_description', '')}")
    lines.append(f"数量: {lc.get('quantity', '')}")
    lines.append(f"贸易术语: {lc.get('trade_terms', '')}")
    lines.append(f"装货港: {lc.get('shipment', {}).get('loading_port', '')}")
    lines.append(f"卸货港: {lc.get('shipment', {}).get('discharge_port', '')}")
    lines.append(f"所需单据: {', '.join(lc.get('required_documents', []))}")
    lines.append(f"保险要求: {lc.get('insurance_coverage', '')}")
    lines.append(f"特别条款: {lc.get('special_conditions', '')}")
    
    # 发票信息
    lines.append("\n" + "=" * 60)
    lines.append("【商业发票信息】")
    lines.append("=" * 60)
    lines.append(f"出具人: {invoice.get('issued_by', '')}")
    lines.append(f"发票号: {invoice.get('invoice_no', '')}")
    lines.append(f"日期: {invoice.get('date', '')}")
    lines.append(f"金额: {invoice.get('currency', '')} {invoice.get('total_amount', '')}")
    lines.append(f"货物描述: {invoice.get('goods_description', '')}")
    lines.append(f"数量: {invoice.get('quantity', '')}")
    
    # 提单信息
    lines.append("\n" + "=" * 60)
    lines.append("【提单信息】")
    lines.append("=" * 60)
    lines.append(f"托运人: {bl.get('shipper', '')}")
    lines.append(f"收货人: {bl.get('consignee', '')}")
    lines.append(f"装货港: {bl.get('loading_port', '')}")
    lines.append(f"卸货港: {bl.get('discharge_port', '')}")
    lines.append(f"装船日期: {bl.get('shipped_on_board_date', '')}")
    lines.append(f"货物描述: {bl.get('goods_description', '')}")
    lines.append(f"清洁提单: {'是' if bl.get('clean_on_board', True) else '否'}")
    if bl.get('remarks'):
        lines.append(f"批注: {bl.get('remarks')}")
    
    # 保险单信息
    lines.append("\n" + "=" * 60)
    lines.append("【保险单信息】")
    lines.append("=" * 60)
    insured = insurance.get('insured', '')
    if isinstance(insured, list):
        insured = ', '.join(insured)
    lines.append(f"被保险人: {insured}")
    lines.append(f"险别: {insurance.get('coverage', '')}")
    lines.append(f"保险金额: {insurance.get('sum_insured', '')}")
    lines.append(f"起运地: {insurance.get('from_location', '')}")
    lines.append(f"目的地: {insurance.get('to_location', '')}")
    lines.append(f"赔付地: {insurance.get('claim_payable_at', '')}")
    
    lines.append("\n" + "=" * 60)
    lines.append("【输出要求】")
    lines.append("=" * 60)
    lines.append("""请以 JSON 数组格式输出所有发现的不符点。每个不符点对象包含以下字段：
{
    "document": "单据名称（如：商业发票、提单、保险单）",
    "field": "不符的字段名称",
    "description": "不符点详细描述",
    "ucp_reference": "引用的 UCP600 条款（如：UCP600 Article 18(b)）",
    "severity": "严重程度：严重/一般/轻微",
    "lc_requirement": "信用证要求（可选）",
    "doc_shows": "单据实际显示内容（可选）",
    "uncertain": false,
    "suggestion": "修改建议（可选）"
}

如果没有发现不符点，请返回空数组 []。
只输出 JSON，不要添加其他说明文字。""")
    
    return "\n".join(lines)


def format_contrastive_examples_for_audit(
    positive_cases: List[Dict[str, Any]],
    negative_cases: List[Dict[str, Any]],
    boundary_cases: List[Dict[str, Any]]
) -> str:
    """
    将正反例格式化为审核可用的文本格式
    
    Args:
        positive_cases: 正例列表
        negative_cases: 反例列表
        boundary_cases: 边界案例列表
        
    Returns:
        格式化后的文本
    """
    lines = []
    lines.append("=" * 60)
    lines.append("【正反对比学习样本 —— 供 AI 审核参考】")
    lines.append("=" * 60)
    
    # 正例
    if positive_cases:
        lines.append("\n📌 正例（应判为不符点的场景）：")
        lines.append("-" * 40)
        for i, case in enumerate(positive_cases, 1):
            lines.append(f"\n【案例 {i}】{case.get('scenario', '')}")
            lc_field = case.get('lc_field', {})
            doc_field = case.get('doc_field', {})
            lines.append(f"  L/C要求: {lc_field.get('field', 'N/A')} = {lc_field.get('value', 'N/A')}")
            lines.append(f"  单据显示: {doc_field.get('document', 'N/A')}.{doc_field.get('field', 'N/A')} = {doc_field.get('value', 'N/A')}")
            lines.append(f"  判断结果: ✅ 构成不符点（{case.get('severity', '一般')}）")
            lines.append(f"  依据条款: {case.get('ucp_reference', 'N/A')}")
            lines.append(f"  说明: {case.get('explanation', '')}")
    
    # 反例
    if negative_cases:
        lines.append("\n\n📌 反例（不应判为不符点的场景 —— 常见误判）：")
        lines.append("-" * 40)
        for i, case in enumerate(negative_cases, 1):
            lines.append(f"\n【案例 {i}】{case.get('scenario', '')}")
            lc_field = case.get('lc_field', {})
            doc_field = case.get('doc_field', {})
            lines.append(f"  L/C要求: {lc_field.get('field', 'N/A')} = {lc_field.get('value', 'N/A')}")
            lines.append(f"  单据显示: {doc_field.get('document', 'N/A')}.{doc_field.get('field', 'N/A')} = {doc_field.get('value', 'N/A')}")
            lines.append(f"  判断结果: ❌ 不构成不符点")
            lines.append(f"  说明: {case.get('explanation', '')}")
    
    # 边界案例
    if boundary_cases:
        lines.append("\n\n📌 边界案例（需特别注意的判断标准）：")
        lines.append("-" * 40)
        for i, case in enumerate(boundary_cases, 1):
            lines.append(f"\n【案例 {i}】{case.get('scenario', '')}")
            lines.append(f"  判断标准: {case.get('criteria', '')}")
            lines.append(f"  依据条款: {case.get('ucp_reference', 'N/A')}")
            lines.append(f"  说明: {case.get('explanation', '')}")
    
    lines.append("\n" + "=" * 60)
    lines.append("【请 AI 审核员参考以上案例，对当前单据进行准确判断】")
    lines.append("=" * 60)
    
    return "\n".join(lines)
