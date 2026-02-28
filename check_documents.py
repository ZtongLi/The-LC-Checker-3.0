import json
import os
from datetime import datetime, timedelta
from openai import OpenAI
import chromadb
from sentence_transformers import SentenceTransformer

# ============================================================
# 第一部分：加载模型和数据库
# ============================================================
print("正在加载系统...\n")

# 加载 Embedding 模型
embed_model = SentenceTransformer("BAAI/bge-m3")

# 连接 ChromaDB 向量数据库
chroma_client = chromadb.PersistentClient(path="/root/lc-checker/chroma_db")
collection = chroma_client.get_collection("ucp600")

# 连接本地 Ollama 大模型
llm_client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

print("系统加载完成！\n")


# ============================================================
# 第二部分：工具函数
# ============================================================
def parse_date(date_str):
    """将各种日期格式统一解析为 datetime 对象"""
    if not date_str:
        return None
    formats = ["%Y-%m-%d", "%Y/%m/%d", "%d/%m/%Y", "%B %d, %Y", "%b %d, %Y"]
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    return None


def rag_query(question, top_k=3):
    """RAG 检索：根据问题检索相关 UCP600 条款"""
    query_embedding = embed_model.encode([question]).tolist()
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=min(top_k, collection.count()),
    )
    context = ""
    for i in range(len(results["ids"][0])):
        article = results["metadatas"][0][i].get("article", "未知")
        content = results["documents"][0][i]
        context += f"\n{'='*50}\n{article}：\n{content}\n"
    return context


def ai_judge(question, context):
    """调用大模型进行语义判断"""
    system_prompt = """你是一位资深的信用证审单专家，精通 UCP600 和 ISBP745。
请根据提供的 UCP600 条款原文，判断单据是否存在不符点。

回答要求：
1. 只回答 JSON 格式
2. 格式为：{"has_discrepancy": true/false, "description": "不符点描述", "ucp_reference": "条款引用", "severity": "严重/一般/轻微"}
3. 如果没有不符点，description 填写"相符"
4. 必须严格依据条款原文判断，不得臆测"""

    user_prompt = f"""以下是相关 UCP600 条款：
{context}

请判断以下情况是否构成不符点：
{question}

请以 JSON 格式回答。"""

    response = llm_client.chat.completions.create(
        model="qwen2.5:14b",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.1,
    )
    
    # 尝试解析 AI 返回的 JSON
    answer = response.choices[0].message.content.strip()
    try:
        # 移除可能的 markdown 代码块标记
        if answer.startswith("```"):
            answer = answer.split("\n", 1)[1]
            answer = answer.rsplit("```", 1)[0]
        return json.loads(answer)
    except json.JSONDecodeError:
        return {
            "has_discrepancy": None,
            "description": answer,
            "ucp_reference": "AI 返回格式异常",
            "severity": "待人工确认"
        }


# ============================================================
# 第三部分：第一层 — 程序自动精确对比
# ============================================================
def check_rule_based(lc, invoice, bl, insurance, presentation_date):
    """基于规则的精确对比，返回不符点列表和相符项列表"""
    discrepancies = []
    compliant_items = []

    # ----------------------------------------------------------
    # 1. 商业发票金额 vs 信用证金额
    # ----------------------------------------------------------
    lc_amount = lc.get("amount", 0)
    inv_amount = invoice.get("total_amount", 0)
    tolerance_str = lc.get("amount_tolerance", "+/- 0%")
    
    # 解析容差百分比
    try:
        tolerance_pct = float(tolerance_str.replace("+/-", "").replace("%", "").strip()) / 100
    except ValueError:
        tolerance_pct = 0
    
    max_allowed = lc_amount * (1 + tolerance_pct)
    
    if inv_amount > max_allowed:
        discrepancies.append({
            "document": "商业发票",
            "field": "金额",
            "lc_requirement": f"{lc.get('currency', '')} {lc_amount:,.2f}（容差 {tolerance_str}，最大允许 {max_allowed:,.2f}）",
            "doc_shows": f"{invoice.get('currency', '')} {inv_amount:,.2f}",
            "description": f"发票金额超��信用证允许的最大金额，超出 {inv_amount - max_allowed:,.2f}",
            "ucp_reference": "UCP600 Article 18(b)",
            "severity": "严重"
        })
    else:
        compliant_items.append("商业发票 — 金额在信用证允许范围内")

    # ----------------------------------------------------------
    # 2. 币种一致性
    # ----------------------------------------------------------
    lc_currency = lc.get("currency", "")
    inv_currency = invoice.get("currency", "")
    
    if lc_currency and inv_currency and lc_currency != inv_currency:
        discrepancies.append({
            "document": "商业发票",
            "field": "币种",
            "lc_requirement": lc_currency,
            "doc_shows": inv_currency,
            "description": f"发票币种 {inv_currency} 与信用证币种 {lc_currency} 不一致",
            "ucp_reference": "UCP600 Article 18(a)",
            "severity": "严重"
        })
    else:
        compliant_items.append(f"商业发票 — 币种一致（{lc_currency}）")

    # ----------------------------------------------------------
    # 3. 装船日期 vs 最迟装运日
    # ----------------------------------------------------------
    latest_shipment = parse_date(lc.get("latest_shipment_date", ""))
    onboard_date = parse_date(bl.get("onboard_date", ""))
    
    if latest_shipment and onboard_date:
        if onboard_date > latest_shipment:
            days_late = (onboard_date - latest_shipment).days
            discrepancies.append({
                "document": "提单",
                "field": "装船日期",
                "lc_requirement": f"最迟 {lc.get('latest_shipment_date', '')}",
                "doc_shows": bl.get("onboard_date", ""),
                "description": f"装船日期晚于信用证最迟装运日 {days_late} 天",
                "ucp_reference": "UCP600 Article 20(c)",
                "severity": "严重"
            })
        else:
            compliant_items.append("提单 — 装船日期在规定期限内")

        # ----------------------------------------------------------
    # 4. 装货港一致性（改进匹配逻辑）
    # ----------------------------------------------------------
    lc_loading_port = lc.get("loading_port", "").lower().strip()
    bl_loading_port = bl.get("port_of_loading", "").lower().strip()
    
    if lc_loading_port and bl_loading_port:
        # 提取核心城市名（去掉国家名后取第一部分）
        def extract_city(port_str):
            """提取港口名称中的核心城市名"""
            parts = [p.strip() for p in port_str.replace("，", ",").split(",")]
            return parts[0] if parts else port_str
        
        lc_city = extract_city(lc_loading_port)
        bl_city = extract_city(bl_loading_port)
        
        # 判断核心城市名是否匹配
        if lc_city in bl_city or bl_city in lc_city or lc_city == bl_city:
            compliant_items.append("提单 — 装货港一致")
        else:
            discrepancies.append({
                "document": "提单",
                "field": "装货港",
                "lc_requirement": lc.get("loading_port", ""),
                "doc_shows": bl.get("port_of_loading", ""),
                "description": "提单装货港与信用证规定不一致",
                "ucp_reference": "UCP600 Article 20(a)(iii)",
                "severity": "严重"
            })

    # ----------------------------------------------------------
    # 5. 卸货港一致性（改进匹配逻辑）
    # ----------------------------------------------------------
    lc_discharge_port = lc.get("discharge_port", "").lower().strip()
    bl_discharge_port = bl.get("port_of_discharge", "").lower().strip()
    
    if lc_discharge_port and bl_discharge_port:
        lc_city_d = extract_city(lc_discharge_port)
        bl_city_d = extract_city(bl_discharge_port)
        
        if lc_city_d in bl_city_d or bl_city_d in lc_city_d or lc_city_d == bl_city_d:
            compliant_items.append("提单 — 卸货港一致")
        else:
            discrepancies.append({
                "document": "提单",
                "field": "卸货港",
                "lc_requirement": lc.get("discharge_port", ""),
                "doc_shows": bl.get("port_of_discharge", ""),
                "description": "提单卸货港与信用证规定不一致",
                "ucp_reference": "UCP600 Article 20(a)(iii)",
                "severity": "严重"
            })

    # ----------------------------------------------------------
    # 6. 清洁提单检查
    # ----------------------------------------------------------
    clean_onboard = bl.get("clean_onboard", True)
    if not clean_onboard:
        discrepancies.append({
            "document": "提单",
            "field": "清洁提单",
            "lc_requirement": "清洁已装船提单（Clean On Board）",
            "doc_shows": "不清洁提单（有批注）",
            "description": "提单包含不清洁批注，不符合清洁已装船要求",
            "ucp_reference": "UCP600 Article 27(a)",
            "severity": "严重"
        })
    else:
        compliant_items.append("提单 — 清洁已装船")

    # ----------------------------------------------------------
    # 7. 保险金额检查（至少 110% CIF 价值）
    # ----------------------------------------------------------
    ins_amount = insurance.get("insurance_amount", 0)
    ins_currency = insurance.get("currency", "")
    
    # 先检查保险币种是否一致
    if lc_currency and ins_currency and lc_currency != ins_currency:
        discrepancies.append({
            "document": "保险单",
            "field": "币种",
            "lc_requirement": lc_currency,
            "doc_shows": ins_currency,
            "description": f"保险币种 {ins_currency} 与信用证币种 {lc_currency} 不一致",
            "ucp_reference": "UCP600 Article 28(f)(ii)",
            "severity": "严重"
        })
    else:
        min_insurance = round(inv_amount * 1.10, 2)
        if round(ins_amount, 2) < round(min_insurance, 2):
            pct = (ins_amount / inv_amount * 100) if inv_amount > 0 else 0
            discrepancies.append({
                "document": "保险单",
                "field": "保险金额",
                "lc_requirement": f"至少 {lc_currency} {min_insurance:,.2f}（发票金额的 110%）",
                "doc_shows": f"{ins_currency} {ins_amount:,.2f}（仅为发票金额的 {pct:.1f}%）",
                "description": f"保险金额不足，差额 {min_insurance - ins_amount:,.2f}",
                "ucp_reference": "UCP600 Article 28(f)(ii)",
                "severity": "严重"
            })
        else:
            compliant_items.append("保险单 — 保险金额充足（≥110% CIF）")

    # ----------------------------------------------------------
    # 8. 保险单日期 vs 装船日期
    # ----------------------------------------------------------
    ins_date = parse_date(insurance.get("issue_date", ""))
    
    if ins_date and onboard_date:
        if ins_date > onboard_date:
            discrepancies.append({
                "document": "保险单",
                "field": "签发日期",
                "lc_requirement": f"不晚于装运日期 {bl.get('onboard_date', '')}",
                "doc_shows": insurance.get("issue_date", ""),
                "description": "保险单签发日期晚于装运日期",
                "ucp_reference": "UCP600 Article 28(e)",
                "severity": "严重"
            })
        else:
            compliant_items.append("保险单 — 签发日期早于装运日期")

    # ----------------------------------------------------------
    # 9. 交单期限检查
    # ----------------------------------------------------------
    pres_date = parse_date(presentation_date)
    expiry_date = parse_date(lc.get("expiry_date", ""))
    
    if pres_date and onboard_date:
        # 检查是否超过装运后 21 天
        pres_str = lc.get("presentation_period", "")
        # 默认 21 天，如果有特别规定则解析
        max_days = 21
        if "15 days" in pres_str.lower():
            max_days = 15
        
        deadline_from_shipment = onboard_date + timedelta(days=max_days)
        
        if pres_date > deadline_from_shipment:
            days_late = (pres_date - deadline_from_shipment).days
            discrepancies.append({
                "document": "交单",
                "field": "交单期限",
                "lc_requirement": f"装运日后 {max_days} 天内（不晚于 {deadline_from_shipment.strftime('%Y-%m-%d')}）",
                "doc_shows": presentation_date,
                "description": f"交单日期超过装运日后 {max_days} 天期限，迟 {days_late} 天",
                "ucp_reference": "UCP600 Article 14(c)",
                "severity": "严重"
            })
        else:
            compliant_items.append(f"交单 — 在装运日后 {max_days} 天内")
    
    if pres_date and expiry_date:
        if pres_date > expiry_date:
            discrepancies.append({
                "document": "交单",
                "field": "信用证有效期",
                "lc_requirement": f"信用证到期日 {lc.get('expiry_date', '')}",
                "doc_shows": presentation_date,
                "description": "交单日期超过信用证到期日，信用证已失效",
                "ucp_reference": "UCP600 Article 6(d)(i)",
                "severity": "严重"
            })
        else:
            compliant_items.append("交单 — 在信用证有效期内")

    # ----------------------------------------------------------
    # 10. 转运检查
    # ----------------------------------------------------------
    transhipment_allowed = lc.get("transhipment", "").lower()
    bl_raw = bl.get("raw_text", "").lower()
    
    if "not allowed" in transhipment_allowed:
        if "transhipment" in bl_raw or "transshipment" in bl_raw:
            # 检查提单原文中是否有转运标记
            if "transhipment at" in bl_raw or "transshipment at" in bl_raw:
                discrepancies.append({
                    "document": "提单",
                    "field": "转运",
                    "lc_requirement": "不允许转运",
                    "doc_shows": "提单显示有转运",
                    "description": "信用证规定不允许转运，但提单显示货物将在途中转运",
                    "ucp_reference": "UCP600 Article 20(c)",
                    "severity": "严重"
                })
    
    # ----------------------------------------------------------
    # 11. 货物数量对比：发票 vs 提单
    # ----------------------------------------------------------
    inv_goods = invoice.get("goods", [])
    if inv_goods:
        inv_qty = inv_goods[0].get("quantity", 0)
        inv_unit = inv_goods[0].get("unit", "")
        
        # 尝试从提单中提取数量
        bl_goods_desc = bl.get("goods_description", "")
        bl_gross_weight = bl.get("gross_weight", "")
        
        # 提取提单中的数量数字
        import re
        bl_numbers = re.findall(r'([\d,]+(?:\.\d+)?)\s*(?:' + re.escape(inv_unit) + '|MT|WMT|Metric Tons?|Units?|Pieces?|PCS|CBM|Cubic Meters?)', bl_goods_desc, re.IGNORECASE)
        
        if bl_numbers:
            bl_qty_str = bl_numbers[0].replace(",", "")
            try:
                bl_qty = float(bl_qty_str)
                
                # 计算差异百分比
                if inv_qty > 0:
                    diff_pct = abs(bl_qty - inv_qty) / inv_qty * 100
                    
                    # 判断是否允许溢短装
                    tolerance_str = lc.get("amount_tolerance", "+/- 0%")
                    try:
                        tolerance_pct_val = float(tolerance_str.replace("+/-", "").replace("%", "").strip())
                    except ValueError:
                        tolerance_pct_val = 0
                    
                    # 如果差异超过容差且超过 1%
                    if diff_pct > max(tolerance_pct_val, 1) and bl_qty != inv_qty:
                        discrepancies.append({
                            "document": "多个单据",
                            "field": "货物数量",
                            "lc_requirement": f"{inv_qty:,.0f} {inv_unit}（发票数量）",
                            "doc_shows": f"{bl_qty:,.0f} {inv_unit}（提单数量）",
                            "description": f"发票数量与提单数量不一致，差异 {diff_pct:.1f}%",
                            "ucp_reference": "UCP600 Article 14(d) / Article 30(b)",
                            "severity": "严重"
                        })
                    else:
                        compliant_items.append("多个单据 — 货物数量一致")
            except ValueError:
                pass
       
    # ----------------------------------------------------------
    # 12. 受益人名称一致性（跨单据严格对比）
    # ----------------------------------------------------------
    beneficiary_name = lc.get("beneficiary", {}).get("name", "").strip()
    inv_issued_by = invoice.get("issued_by", "").strip()
    bl_shipper = bl.get("shipper", "").strip()
    ins_insured = insurance.get("insured", "").strip()
    
    # 定义缩写等价表
    def normalize_company_name(name):
        """标准化公司名称，用于严格对比"""
        return name.lower().strip()
    
    def names_strictly_match(name1, name2):
        """严格匹配：完全相同才算一致"""
        n1 = normalize_company_name(name1)
        n2 = normalize_company_name(name2)
        # 如果一个名称完整包含另一个，算匹配
        if n1 in n2 or n2 in n1:
            return True
        return n1 == n2
    
    # 检查发票出票人 vs 受益人
    if beneficiary_name and inv_issued_by:
        if not names_strictly_match(beneficiary_name, inv_issued_by):
            discrepancies.append({
                "document": "商业发票",
                "field": "出票人名称",
                "lc_requirement": f"受益人：{beneficiary_name}",
                "doc_shows": f"发票出票人：{inv_issued_by}",
                "description": "发票出票人名称与信用证受益人名称不完全一致",
                "ucp_reference": "UCP600 Article 18(a)",
                "severity": "轻微"
            })
    
    # 检查提单托运人 vs 受益人
    if beneficiary_name and bl_shipper:
        if not names_strictly_match(beneficiary_name, bl_shipper):
            discrepancies.append({
                "document": "提单",
                "field": "托运人名称",
                "lc_requirement": f"受益人：{beneficiary_name}",
                "doc_shows": f"提单托运人：{bl_shipper}",
                "description": "提单托运人名称与信用证受益人名称不完全一致",
                "ucp_reference": "UCP600 Article 14(k)",
                "severity": "轻微"
            })
    
    # 检查保险被保险人 vs 受益人
    if beneficiary_name and ins_insured:
        if not names_strictly_match(beneficiary_name, ins_insured):
            discrepancies.append({
                "document": "保险单",
                "field": "被保险人名称",
                "lc_requirement": f"受益人：{beneficiary_name}",
                "doc_shows": f"保险被保险人：{ins_insured}",
                "description": "保险单被保险人名称与信用证受益人名称不完全一致",
                "ucp_reference": "UCP600 Article 14(d)",
                "severity": "轻微"
            })

    # ----------------------------------------------------------
    # 13. 数量单位表述一致性
    # ----------------------------------------------------------
    if inv_goods:
        inv_unit_str = inv_goods[0].get("unit", "").strip()
        lc_goods_desc = lc.get("goods_description", "")
        
        # 常见的不一致缩写对
        unit_variants = {
            "cbm": ["cubic meters", "cubic meter", "cu.m", "m3"],
            "mt": ["metric tons", "metric ton", "m/t"],
            "wmt": ["wet metric tons", "wet metric ton"],
            "pcs": ["pieces", "piece"],
            "kgs": ["kilograms", "kilogram", "kg"],
            "units": ["unit"],
        }
        
        inv_unit_lower = inv_unit_str.lower()
        
        # 检查发票单位是否是缩写，而信用证用的是全称（或反过来）
        for abbrev, full_forms in unit_variants.items():
            if inv_unit_lower == abbrev or inv_unit_lower in full_forms:
                # 检查信用证中用的是哪种写法
                lc_lower = lc_goods_desc.lower()
                inv_is_abbrev = (inv_unit_lower == abbrev)
                lc_has_abbrev = (abbrev in lc_lower)
                lc_has_full = any(f in lc_lower for f in full_forms)
                
                if inv_is_abbrev and lc_has_full and not lc_has_abbrev:
                    discrepancies.append({
                        "document": "商业发票",
                        "field": "数量单位表述",
                        "lc_requirement": f"信用证使用全称",
                        "doc_shows": f"发票使用缩写 '{inv_unit_str}'",
                        "description": f"发票数量单位 '{inv_unit_str}' 为缩写，信用证中使用全称，表述不一致",
                        "ucp_reference": "ISBP745 Paragraph A7",
                        "severity": "轻微"
                    })
                    break
                elif not inv_is_abbrev and lc_has_abbrev and not lc_has_full:
                    discrepancies.append({
                        "document": "商业发票",
                        "field": "数量单位表述",
                        "lc_requirement": f"信用证使用缩写",
                        "doc_shows": f"发票使用全称 '{inv_unit_str}'",
                        "description": f"发票数量单位 '{inv_unit_str}' 为全称，信用证中使用缩写，表述不一致",
                        "ucp_reference": "ISBP745 Paragraph A7",
                        "severity": "轻微"
                    })
                    break

        # ----------------------------------------------------------
    # 14. 保险单起运地/目的地 vs 提单装卸港
    # ----------------------------------------------------------
    ins_from = insurance.get("from", "").lower().strip()
    ins_to = insurance.get("to", "").lower().strip()
    bl_loading = bl.get("port_of_loading", "").lower().strip()
    bl_discharge = bl.get("port_of_discharge", "").lower().strip()
    
    if ins_from and bl_loading:
        ins_from_city = extract_city(ins_from)
        bl_loading_city = extract_city(bl_loading)
        
        if ins_from_city not in bl_loading_city and bl_loading_city not in ins_from_city and ins_from_city != bl_loading_city:
            discrepancies.append({
                "document": "保险单",
                "field": "起运地",
                "lc_requirement": f"提单装货港：{bl.get('port_of_loading', '')}",
                "doc_shows": f"保险单起运地：{insurance.get('from', '')}",
                "description": "保险单起运地与提单装货港不一致",
                "ucp_reference": "UCP600 Article 28(h)",
                "severity": "一般"
            })
    
    if ins_to and bl_discharge:
        ins_to_city = extract_city(ins_to)
        bl_discharge_city = extract_city(bl_discharge)
        
        if ins_to_city not in bl_discharge_city and bl_discharge_city not in ins_to_city and ins_to_city != bl_discharge_city:
            discrepancies.append({
                "document": "保险单",
                "field": "目的地",
                "lc_requirement": f"提单卸货港：{bl.get('port_of_discharge', '')}",
                "doc_shows": f"保险单目的地：{insurance.get('to', '')}",
                "description": "保险单目的地与提单卸货港不一致",
                "ucp_reference": "UCP600 Article 28(h)",
                "severity": "一般"
            })

        # ----------------------------------------------------------
    # 15. 发票数量 vs 信用证货物描述中的数量（加强对比）
    # ----------------------------------------------------------
    if inv_goods:
        inv_qty = inv_goods[0].get("quantity", 0)
        inv_unit = inv_goods[0].get("unit", "")
        lc_goods_desc = lc.get("goods_description", "")
        
        # 从信用证货物描述中提取数量
        import re
        lc_numbers = re.findall(r'([\d,]+(?:\.\d+)?)\s*(?:' + re.escape(inv_unit) + '|MT|WMT|Wet Metric Tons?|Metric Tons?|Units?|Pieces?|PCS|CBM|Cubic Meters?)', lc_goods_desc, re.IGNORECASE)
        
        if lc_numbers:
            lc_qty_str = lc_numbers[0].replace(",", "")
            try:
                lc_qty = float(lc_qty_str)
                
                if inv_qty > 0 and lc_qty > 0 and inv_qty != lc_qty:
                    diff_pct = abs(inv_qty - lc_qty) / lc_qty * 100
                    
                    # 检查是否在容差范围内
                    tolerance_str = lc.get("amount_tolerance", "+/- 0%")
                    try:
                        tolerance_pct_val = float(tolerance_str.replace("+/-", "").replace("%", "").strip())
                    except ValueError:
                        tolerance_pct_val = 0
                    
                    if diff_pct > tolerance_pct_val:
                        discrepancies.append({
                            "document": "商业发票",
                            "field": "货物数量",
                            "lc_requirement": f"信用证：{lc_qty:,.0f} {inv_unit}",
                            "doc_shows": f"发票：{inv_qty:,.0f} {inv_unit}",
                            "description": f"发票数量与信用证规定数量不一致，差异 {diff_pct:.1f}%",
                            "ucp_reference": "UCP600 Article 30(b)",
                            "severity": "严重" if diff_pct > 5 else "一般"
                        })
            except ValueError:
                pass

    return discrepancies, compliant_items


# ============================================================
# 第四部分：第二层 — AI 语义对比
# ============================================================
def check_ai_semantic(lc, invoice, bl, insurance):
    """AI 语义对比，处理需要自然语言理解的字段"""
    ai_discrepancies = []

    # ----------------------------------------------------------
    # 1. 货物描述对比：发票 vs 信用证
    # ----------------------------------------------------------
    lc_goods = lc.get("goods_description", "")
    inv_goods = invoice.get("goods", [{}])[0].get("description", "") if invoice.get("goods") else ""
    
    if lc_goods and inv_goods:
        question = f"""信用证货物描述为："{lc_goods}"
商业发票货物描述为："{inv_goods}"
根据 UCP600 Article 18(c)，商业发票的货物描述必须与信用证一致（correspond with）。
请判断这两个描述是否一致，是否存在遗漏或矛盾。"""
        
        context = rag_query("商业发票货物描述必须与信用证一致")
        result = ai_judge(question, context)
        
        if result.get("has_discrepancy"):
            ai_discrepancies.append({
                "document": "商业发票",
                "field": "货物描述",
                "lc_requirement": lc_goods,
                "doc_shows": inv_goods,
                "description": result.get("description", ""),
                "ucp_reference": result.get("ucp_reference", "UCP600 Article 18(c)"),
                "severity": result.get("severity", "严重")
            })

    # ----------------------------------------------------------
    # 2. 货物描述对比：提单 vs 信用证
    # ----------------------------------------------------------
    bl_goods = bl.get("goods_description", "")
    
    if lc_goods and bl_goods:
        question = f"""信用证货物描述为："{lc_goods}"
提单货物描述为："{bl_goods}"
根据 UCP600 Article 14(d)，提单中的货物描述可以不与信用证完全相同，但不得矛盾。
请判断提单的货物描述是否与信用证矛盾。"""
        
        context = rag_query("提单货物描述不得与信用证矛盾")
        result = ai_judge(question, context)
        
        if result.get("has_discrepancy"):
            ai_discrepancies.append({
                "document": "提单",
                "field": "货物描述",
                "lc_requirement": lc_goods,
                "doc_shows": bl_goods,
                "description": result.get("description", ""),
                "ucp_reference": result.get("ucp_reference", "UCP600 Article 14(d)"),
                "severity": result.get("severity", "严重")
            })

    # ----------------------------------------------------------
    # 3. 发票抬头 vs 信用证申请人
    # ----------------------------------------------------------
    lc_applicant = lc.get("applicant", {}).get("name", "")
    inv_issued_to = invoice.get("issued_to", "")
    
    if lc_applicant and inv_issued_to and lc_applicant != inv_issued_to:
        question = f"""信用证申请人为："{lc_applicant}"
商业发票抬头（issued to）为："{inv_issued_to}"
请判断这两个名称是否指同一公司。如果名称不同，是否构成不符点。"""
        
        context = rag_query("商业发票必须以申请人为抬头")
        result = ai_judge(question, context)
        
        if result.get("has_discrepancy"):
            ai_discrepancies.append({
                "document": "商业发票",
                "field": "抬头（申请人）",
                "lc_requirement": lc_applicant,
                "doc_shows": inv_issued_to,
                "description": result.get("description", ""),
                "ucp_reference": result.get("ucp_reference", "UCP600 Article 18(a)"),
                "severity": result.get("severity", "严重")
            })

    # ----------------------------------------------------------
    # 4. 保险险别对比
    # ----------------------------------------------------------
    lc_docs = lc.get("required_documents", [])
    ins_coverage = insurance.get("coverage", "")
    
    # 从信用证要求的单据中提取保险要求
    lc_insurance_req = ""
    for doc in lc_docs:
        if "insurance" in doc.lower() or "保险" in doc:
            lc_insurance_req = doc
            break
    
    if lc_insurance_req and ins_coverage:
        question = f"""信用证对保险的要求为："{lc_insurance_req}"
保险单显示的险别为："{ins_coverage}"
请判断保险单的险别是否涵盖了信用证要求的所有险别。"""
        
        context = rag_query("保险单必须承保信用证要求的险别")
        result = ai_judge(question, context)
        
        if result.get("has_discrepancy"):
            ai_discrepancies.append({
                "document": "保险单",
                "field": "险别",
                "lc_requirement": lc_insurance_req,
                "doc_shows": ins_coverage,
                "description": result.get("description", ""),
                "ucp_reference": result.get("ucp_reference", "UCP600 Article 28(a)"),
                "severity": result.get("severity", "严重")
            })

    return ai_discrepancies


# ============================================================
# 第五部分：生成审核报告
# ============================================================
def generate_report(case, rule_discrepancies, ai_discrepancies, compliant_items):
    """生成标准化审核报告"""
    lc = case["letter_of_credit"]
    all_discrepancies = rule_discrepancies + ai_discrepancies
    
    report = []
    report.append("=" * 70)
    report.append("              信用证单据审核报告")
    report.append("=" * 70)
    report.append("")
    report.append(f"  案例编号：{case.get('case_id', '')}")
    report.append(f"  案例描述：{case.get('case_description', '')}")
    report.append(f"  信用证号：{lc.get('lc_number', '')}")
    report.append(f"  开 证 行：{lc.get('issuing_bank', '')}")
    report.append(f"  申 请 人：{lc.get('applicant', {}).get('name', '')}")
    report.append(f"  受 益 人：{lc.get('beneficiary', {}).get('name', '')}")
    report.append(f"  信用证金额：{lc.get('currency', '')} {lc.get('amount', 0):,.2f}")
    report.append(f"  交 单 日：{case.get('presentation_date', '')}")
    report.append(f"  审核日期：{datetime.now().strftime('%Y-%m-%d %H:%M')}")
    report.append("")
    
    if all_discrepancies:
        report.append(f"  ⚠️  审核结果：发现 {len(all_discrepancies)} 处不符点")
    else:
        report.append(f"  ✅  审核结果：所有单据相符")
    
    report.append("")
    
    # 输出不符点
    if all_discrepancies:
        for i, d in enumerate(all_discrepancies, 1):
            report.append("-" * 70)
            report.append(f"  不符点 #{i}")
            report.append("-" * 70)
            report.append(f"  涉及单据：{d.get('document', '')}")
            report.append(f"  不符字段：{d.get('field', '')}")
            report.append(f"  信用证要求：{d.get('lc_requirement', '')}")
            report.append(f"  单据显示：{d.get('doc_shows', '')}")
            report.append(f"  差异说明：{d.get('description', '')}")
            report.append(f"  依据条款：{d.get('ucp_reference', '')}")
            severity = d.get('severity', '一般')
            stars = {"严重": "★★★", "一般": "★★", "轻微": "★"}.get(severity, "★★")
            report.append(f"  严重程度：{stars} {severity}")
            report.append("")
    
    # 输出相符项目
    if compliant_items:
        report.append("-" * 70)
        report.append("  相符项目（已通过审核）")
        report.append("-" * 70)
        for item in compliant_items:
            report.append(f"  ✓ {item}")
        report.append("")
    
    # 审核结论
    report.append("=" * 70)
    if not all_discrepancies:
        report.append("  审核结论：所有单据与信用证条款完全相符，建议承付。")
    elif any(d.get("severity") == "严重" for d in all_discrepancies):
        report.append("  审核结论：单据存在严重不符点，建议拒绝承付或联系申请人。")
    else:
        report.append("  审核结论：单据存在轻微不符点，建议联系申请人确认是否接受。")
    report.append("=" * 70)
    
    return "\n".join(report)


# ============================================================
# 第六部分：主程序 — 逐个案例审核
# ============================================================
def main():
    # 加载测试数据
    data_path = "/root/lc-checker/test_data/test_cases.json"
    print(f"正在加载测试数据：{data_path}\n")
    
    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    cases = data["cases"]
    print(f"共加载 {len(cases)} 组测试案例\n")
    
    # 创建报告输出目录
    report_dir = "/root/lc-checker/reports"
    os.makedirs(report_dir, exist_ok=True)
    
    # 统计结果
    total_expected = 0
    total_found = 0
    total_correct = 0
    
    for case in cases:
        case_id = case["case_id"]
        print(f"\n{'#' * 70}")
        print(f"# 正在审核：{case_id} — {case.get('case_description', '')}")
        print(f"{'#' * 70}\n")
        
        lc = case["letter_of_credit"]
        invoice = case["commercial_invoice"]
        bl = case["bill_of_lading"]
        insurance = case["insurance_policy"]
        presentation_date = case.get("presentation_date", "")
        expected = case.get("expected_result", {})
        
        # 第一层：程序精确对比
        print("  [第一层] 程序精确对比...")
        rule_discrepancies, compliant_items = check_rule_based(
            lc, invoice, bl, insurance, presentation_date
        )
        print(f"  → 发现 {len(rule_discrepancies)} 个不符点\n")
        
        # 第二层：AI 语义对比
        print("  [第二层] AI 语义对比...")
        ai_discrepancies = check_ai_semantic(lc, invoice, bl, insurance)
        print(f"  → 发现 {len(ai_discrepancies)} 个不符点\n")
        
        # 生成报告
        report = generate_report(case, rule_discrepancies, ai_discrepancies, compliant_items)
        print(report)
        
        # 保存报告到文件
        report_path = os.path.join(report_dir, f"{case_id}_report.txt")
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"\n  报告已保存：{report_path}")
        
        # 与标准答案对比
        expected_count = len(expected.get("discrepancies", []))
        found_count = len(rule_discrepancies) + len(ai_discrepancies)
        total_expected += expected_count
        total_found += found_count
        
        print(f"\n  标准答案：{expected_count} 个不符点")
        print(f"  系统发现：{found_count} 个不符点")
        print(f"  预期结果：{'有不符点' if expected.get('has_discrepancies') else '无不符点'}")
        print(f"  系统判断：{'有不符点' if found_count > 0 else '无不符点'}")
        
        # 判断大方向是否正确
        if expected.get("has_discrepancies") == (found_count > 0):
            print(f"  ✅ 大方向判断正确")
            total_correct += 1
        else:
            print(f"  ❌ 大方向判断错误")
    
    # 输出总结
    print(f"\n\n{'=' * 70}")
    print(f"                    审核总结")
    print(f"{'=' * 70}")
    print(f"  总案例数：{len(cases)}")
    print(f"  大方向正确：{total_correct}/{len(cases)}（{total_correct/len(cases)*100:.1f}%）")
    print(f"  标准答案总不符点：{total_expected}")
    print(f"  系统发现总不符点：{total_found}")
    print(f"  报告保存路径：{report_dir}/")
    print(f"{'=' * 70}")


if __name__ == "__main__":
    main()