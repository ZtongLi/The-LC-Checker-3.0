import json
import os
from datetime import datetime, timedelta
from openai import OpenAI
import chromadb
from sentence_transformers import SentenceTransformer

# ============================================================
# 第一部分：加载模型和数据库
# ============================================================
print("=" * 70)
print("  信用证智能审单系统 V2 — AI 驱动架构")
print("=" * 70)
print("\n正在加载系统...\n")

# 加载 Embedding 模型
embed_model = SentenceTransformer("BAAI/bge-m3")

# 工作目录配置
WORK_DIR = os.environ.get("WORK_DIR", os.path.dirname(os.path.abspath(__file__)))
CHROMA_DB_PATH = os.path.join(WORK_DIR, "chroma_db")

# 连接 ChromaDB
try:
    chroma_client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
    collection = chroma_client.get_collection("ucp600")
except Exception as e:
    print(f"警告：无法连接 ChromaDB ({e})，知识库检索功能将不可用")
    chroma_client = None
    collection = None

# LLM 客户端配置（优先使用环境变量）
llm_client = OpenAI(
    base_url=os.environ.get("OPENAI_API_BASE", "http://localhost:11434/v1"),
    api_key=os.environ.get("OPENAI_API_KEY", "ollama")
)

print("系统加载完成！\n")


# ============================================================
# 第二部分：动态 RAG 查询配置
# ============================================================

# 文档类型到相关条款的映射（用于限定检索范围）
DOCUMENT_ARTICLE_MAP = {
    "letter_of_credit": ["article_02", "article_06", "article_07", "article_10", "article_14", "article_30"],
    "commercial_invoice": ["article_14", "article_18", "article_03", "article_30"],
    "bill_of_lading": [
        "article_14",      # 单据审核标准
        "article_20",      # 提单核心条款
        "article_19",      # 多式联运
        "article_21",      # 不可转让海运单
        "article_22",      # 租船合同提单
        "article_26",      # 货装舱面、托运人装载
        "article_27",      # 清洁运输单据
        "article_31",      # 分批装运
        "article_06",      # 截止日
    ],
    "insurance_policy": ["article_14", "article_28", "article_30"],
}

# 字段级查询模板（用于针对性检索）
FIELD_QUERY_TEMPLATES = {
    # 提单特有字段
    "bl_clean_onboard": "清洁运输单据的要求 Article 27",
    "bl_shippers_load": "托运人装载和计数条款的接受 Article 26",
    "bl_on_deck": "货装舱面条款 Article 26",
    "bl_transshipment": "提单转运规定 Article 20",
    "bl_charter_party": "租船合同提单 Article 22",
    
    # 通用字段
    "amount_tolerance": "信用证金额容差规定 Article 30",
    "partial_shipment": "部分发运规定 Article 31",
    "installment": "分期支款规定 Article 32",
    "latest_shipment": "最迟装运日 Article 06",
    "presentation_period": "交单期限 Article 14",
    "original_documents": "正本单据要求 Article 17",
    "transferable": "可转让信用证 Article 38",
}

# 通用查询模板（用于全面检索）
BASE_QUERIES = [
    "商业发票货物描述必须与信用证一致",
    "提单装货港卸货港必须与信用证一致",
    "保险单必须承保信用证要求的险别",
    "审核单据的标准，单据之间不得互相矛盾",
    "分批装运和转运的规定",
    "提单必须是清洁已装船提单"
]


def rag_retrieve(query, top_k=8):
    """
    RAG 检索：返回最相关的 UCP600 条款
    增加 top_k（原来是 5，现在是 8）以支持"宁多勿漏"原则
    """
    if collection is None:
        return "\n--- 知识库未加载 ---\n暂时无法检索 UCP600 条款\n"
    
    query_embedding = embed_model.encode([query]).tolist()
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=min(top_k, collection.count()),
    )
    context = ""
    for i in range(len(results["ids"][0])):
        article = results["metadatas"][0][i].get("article", "未知")
        content = results["documents"][0][i]
        context += f"\n--- {article} ---\n{content}\n"
    return context


def generate_dynamic_queries(lc, invoice, bl, insurance):
    """
    根据单据内容动态生成查询
    这是动态 RAG 的核心：看着单据查，而非闭着眼睛查
    """
    queries = []
    
    # 分析提单内容（海运单据是重点）
    bl_text = bl.get("raw_text", "").lower() if bl.get("raw_text") else ""
    
    # 检查是否为租船提单
    if any(term in bl_text for term in ["charter party", "租船", "charter"]):
        queries.append("租船合同提单的特殊审核要求 Article 22")
    
    # 检查是否有托运人装载批注
    if any(term in bl_text for term in ["shipper's load", "shipper's count", "托运人装载"]):
        queries.append("托运人装载和计数批注对清洁提单的影响 Article 26")
    
    # 检查是否有舱面货批注
    if any(term in bl_text for term in ["on deck", "舱面", "甲板"]):
        queries.append("货装舱面条款 Article 26")
    
    # 检查是否有转运
    if any(term in bl_text for term in ["transshipment", "转运", "transhipment"]):
        queries.append("提单转运规定 Article 20")
    
    # 检查是否有不清洁批注
    if any(term in bl_text for term in ["dirty", "unclean", "stained", "damaged", "破损", "污渍"]):
        queries.append("清洁运输单据的要求 Article 27")
    
    # 分析信用证关键条款
    partial_shipment = lc.get("partial_shipment", "").lower()
    transshipment = lc.get("transhipment", "").lower()
    
    if "not allowed" in partial_shipment or "prohibited" in partial_shipment:
        queries.append("禁止分批装运时的单据要求 Article 31")
    
    if "not allowed" in transshipment or "prohibited" in transshipment:
        queries.append("禁止转运时的提单要求 Article 20")
    
    # 分析金额容差
    tolerance_str = lc.get("amount_tolerance", "")
    if tolerance_str and tolerance_str != "+/- 0%":
        queries.append("信用证金额容差规定 Article 30")
    
    # 分析保险单据
    ins_coverage = insurance.get("coverage", "") if insurance else ""
    if ins_coverage:
        queries.append("保险单据承保范围要求 Article 28")
    
    # 分析发票
    inv_amount = invoice.get("total_amount", 0) if invoice else 0
    lc_amount = lc.get("amount", 0)
    if inv_amount > lc_amount:
        queries.append("发票金额超过信用证金额的处理 Article 18")
    
    return queries


def retrieve_comprehensive_context(lc, invoice, bl, insurance):
    """
    综合检索：结合基础查询 + 动态查询 + 文档类型限定
    确保"宁多勿漏"
    """
    all_context = ""
    seen = set()
    
    # 1. 基础通用查询（确保覆盖面）
    print("  [RAG] 执行基础查询...")
    for q in BASE_QUERIES:
        ctx = rag_retrieve(q, top_k=5)
        for line in ctx.split("\n---"):
            if line.strip() and line.strip() not in seen:
                seen.add(line.strip())
                all_context += line + "\n"
    
    # 2. 动态查询（基于单据内容）
    print("  [RAG] 生成动态查询...")
    dynamic_queries = generate_dynamic_queries(lc, invoice, bl, insurance)
    for q in dynamic_queries:
        print(f"    - {q}")
        ctx = rag_retrieve(q, top_k=6)
        for line in ctx.split("\n---"):
            if line.strip() and line.strip() not in seen:
                seen.add(line.strip())
                all_context += line + "\n"
    
    # 3. 文档类型限定检索（扩大检索范围，宁多勿漏）
    print("  [RAG] 执行文档类型限定检索...")
    doc_type_queries = {
        "提单相关": "提单 Bill of Lading 要求 Article 20",
        "发票相关": "商业发票 Commercial Invoice 要求 Article 18",
        "保险相关": "保险单据 Insurance Document 要求 Article 28",
    }
    for desc, q in doc_type_queries.items():
        ctx = rag_retrieve(q, top_k=4)
        for line in ctx.split("\n---"):
            if line.strip() and line.strip() not in seen:
                seen.add(line.strip())
                all_context += line + "\n"
    
    print(f"  [RAG] 共检索到 {len(seen)} 个唯一条款")
    return all_context


def parse_date(date_str):
    """解析日期"""
    if not date_str:
        return None
    formats = ["%Y-%m-%d", "%Y/%m/%d", "%d/%m/%Y", "%B %d, %Y", "%b %d, %Y"]
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    return None


# ============================================================
# 第三部分：第一层 — 规则引擎（只做精确计算）
# ============================================================
def check_calculations(lc, invoice, bl, insurance, presentation_date):
    """只做 AI 不擅长的精确计算"""
    discrepancies = []
    compliant_items = []

    lc_amount = lc.get("amount", 0)
    lc_currency = lc.get("currency", "")
    inv_amount = invoice.get("total_amount", 0)
    inv_currency = invoice.get("currency", "")
    ins_amount = insurance.get("insurance_amount", 0)
    ins_currency = insurance.get("currency", "")

    # 解析容差
    tolerance_str = lc.get("amount_tolerance", "+/- 0%")
    try:
        tolerance_pct = float(tolerance_str.replace("+/-", "").replace("%", "").strip()) / 100
    except ValueError:
        tolerance_pct = 0

    # ① 发票金额 vs 信用证金额
    max_allowed = lc_amount * (1 + tolerance_pct)
    if inv_amount > round(max_allowed, 2):
        discrepancies.append({
            "document": "商业发票",
            "field": "金额",
            "lc_requirement": f"{lc_currency} {lc_amount:,.2f}（容差 {tolerance_str}，最大 {max_allowed:,.2f}）",
            "doc_shows": f"{inv_currency} {inv_amount:,.2f}",
            "description": f"发票金额超出信用证允许的最大金额，超出 {inv_amount - max_allowed:,.2f}",
            "ucp_reference": "UCP600 Article 18(b)",
            "severity": "严重"
        })
    else:
        compliant_items.append("商业发票 — 金额在信用证允许范围内")

    # ② 币种精确匹配
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

    # ③ 保险金额计算（只有币种一致时才算）
    if lc_currency == ins_currency or not ins_currency:
        min_insurance = round(inv_amount * 1.10, 2)
        if round(ins_amount, 2) < min_insurance:
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
            compliant_items.append("保险单 — 保险金额充足（≥110%）")

    # ④ 装船日期 vs 最迟装运日
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

    # ⑤ 交单期限计算
    pres_date = parse_date(presentation_date)
    expiry_date = parse_date(lc.get("expiry_date", ""))

    if pres_date and onboard_date:
        pres_str = lc.get("presentation_period", "")
        max_days = 21
        if "15 days" in pres_str.lower():
            max_days = 15
        deadline = onboard_date + timedelta(days=max_days)
        if pres_date > deadline:
            discrepancies.append({
                "document": "交单",
                "field": "交单期限",
                "lc_requirement": f"装运日后 {max_days} 天内（不晚于 {deadline.strftime('%Y-%m-%d')}）",
                "doc_shows": presentation_date,
                "description": f"交单日期超过装运日后 {max_days} 天期限",
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
                "lc_requirement": f"到期日 {lc.get('expiry_date', '')}",
                "doc_shows": presentation_date,
                "description": "交单日期超过信用证到期日",
                "ucp_reference": "UCP600 Article 6(d)(i)",
                "severity": "严重"
            })
        else:
            compliant_items.append("交单 — 在信用证有效期内")

    # ⑥ 保险单日期 vs 装船日期
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

    # ⑦ 单据份数检查
    required_docs = lc.get("required_documents", "")
    if isinstance(required_docs, list):
        required_docs_text = " ".join(str(d) for d in required_docs)
    else:
        required_docs_text = str(required_docs)
    req_lower = required_docs_text.lower()

    # 检查发票份数
    inv_copies_required = 0
    if "triplicate" in req_lower or "3/3" in req_lower.replace(" ", ""):
        inv_copies_required = 3
    elif "duplicate" in req_lower or "2/2" in req_lower.replace(" ", ""):
        inv_copies_required = 2
    # 也检查 lc 的其他字段
    for field_val in [str(lc.get("documents_required", "")), str(lc.get("document_requirements", ""))]:
        fv_lower = field_val.lower()
        if "invoice" in fv_lower:
            if "triplicate" in fv_lower or "3/3" in fv_lower:
                inv_copies_required = 3
            elif "duplicate" in fv_lower or "2/2" in fv_lower:
                inv_copies_required = 2

    if inv_copies_required > 0:
        import re as _re_inv
        inv_originals = invoice.get("number_of_originals", invoice.get("copies", 0))
        if isinstance(inv_originals, str):
            nums = _re_inv.findall(r'\d+', str(inv_originals))
            inv_originals = int(nums[0]) if nums else 0
        # 如果字段里没有，从 raw_text 提取
        if not inv_originals or inv_originals == 0:
            raw = str(invoice.get("raw_text", "")).lower()
            m = _re_inv.search(r'number of original.*?\((\d+)\)', raw)
            if m:
                inv_originals = int(m.group(1))
            else:
                m2 = _re_inv.search(r'(\d+)\s*\)?\s*original', raw)
                if m2:
                    inv_originals = int(m2.group(1))
                else:
                    word_map = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6}
                    for word, num in word_map.items():
                        if _re_inv.search(word + r'.*original', raw):
                            inv_originals = num
                            break
        if inv_originals > 0 and inv_originals < inv_copies_required:
            discrepancies.append({
                "document": "商业发票",
                "field": "份数",
                "lc_requirement": f"要求 {inv_copies_required} 份正本（triplicate）",
                "doc_shows": f"仅提供 {inv_originals} 份正本",
                "description": f"发票份数不足：信用证要求 {inv_copies_required} 份正本，实际仅提供 {inv_originals} 份",
                "ucp_reference": "UCP600 Article 17(a)",
                "severity": "严重"
            })
        elif inv_originals >= inv_copies_required:
            compliant_items.append(f"商业发票 — 份数满足要求（{inv_originals}/{inv_copies_required}）")
        else:
            compliant_items.append("商业发票 — 份数：无法确定实际份数")

    # 检查提单份数（full set）
    bl_full_set_required = False
    bl_copies_required = 0
    for field_val in [required_docs_text, str(lc.get("documents_required", "")), str(lc.get("document_requirements", ""))]:
        fv_lower = field_val.lower()
        if "full set" in fv_lower or "3/3" in fv_lower:
            bl_full_set_required = True
            bl_copies_required = 3
        elif "2/3" in fv_lower:
            bl_copies_required = 2

    bl_originals = bl.get("number_of_originals", bl.get("originals", 0))
    if isinstance(bl_originals, str):
        import re as _re2
        nums2 = _re2.findall(r'\d+', str(bl_originals))
        bl_originals = int(nums2[0]) if nums2 else 0

    if bl_copies_required > 0 and bl_originals > 0 and bl_originals < bl_copies_required:
        discrepancies.append({
            "document": "提单",
            "field": "份数",
            "lc_requirement": f"要求全套 {bl_copies_required} 份正本提单（full set）" if bl_full_set_required else f"要求 {bl_copies_required} 份正本提单",
            "doc_shows": f"仅提供 {bl_originals} 份正本",
            "description": f"提单份数不足：信用证要求{'全套' if bl_full_set_required else ''} {bl_copies_required} 份正本，实际仅提供 {bl_originals} 份",
            "ucp_reference": "UCP600 Article 20(a)(iv)",
            "severity": "严重"
        })
    elif bl_copies_required > 0:
        compliant_items.append(f"提单 — 份数满足要求（{bl_originals}/{bl_copies_required}）")

    # ⑧ 贸易术语检查
    lc_trade = lc.get("trade_terms", lc.get("incoterms", "")).strip()
    inv_trade = invoice.get("trade_terms", invoice.get("incoterms", "")).strip()

    # 也从货物描述中提取贸易术语
    if not lc_trade:
        goods_desc = str(lc.get("goods_description", ""))
        import re as _re3
        trade_match = _re3.search(r'\b(FOB|CIF|CFR|CIP|FCA|EXW|DAP|DDP|FAS|CPT|DAT|DPU)\b', goods_desc, _re3.IGNORECASE)
        if trade_match:
            lc_trade = trade_match.group(0).upper()

    if not inv_trade:
        inv_desc = str(invoice.get("goods_description", invoice.get("description", "")))
        import re as _re4
        trade_match2 = _re4.search(r'\b(FOB|CIF|CFR|CIP|FCA|EXW|DAP|DDP|FAS|CPT|DAT|DPU)\b', inv_desc, _re4.IGNORECASE)
        if trade_match2:
            inv_trade = trade_match2.group(0).upper()

    if lc_trade and inv_trade:
        # 提取术语类型（如 FOB SHANGHAI 中的 FOB）
        lc_term = lc_trade.split()[0].upper() if lc_trade else ""
        inv_term = inv_trade.split()[0].upper() if inv_trade else ""
        if lc_term and inv_term and lc_term != inv_term:
            discrepancies.append({
                "document": "商业发票",
                "field": "贸易术语",
                "lc_requirement": lc_trade,
                "doc_shows": inv_trade,
                "description": f"贸易术语不一致：信用证要求 {lc_trade}，发票显示 {inv_trade}",
                "ucp_reference": "UCP600 Article 18(c)",
                "severity": "严重"
            })
        else:
            compliant_items.append(f"商业发票 — 贸易术语一致（{lc_trade}）")
    elif lc_trade and not inv_trade:
        compliant_items.append("商业发票 — 贸易术语：发票未明确标注（待AI审核）")


    # ⑨ 货物描述精确匹配检查（大小写敏感）
    import re as _re_goods
    lc_raw = str(lc.get("raw_text", ""))
    inv_raw = str(invoice.get("raw_text", ""))
    lc_goods_desc = lc.get("goods_description", "")
    
    # 从发票获取货物描述
    inv_goods_desc = ""
    inv_goods_list = invoice.get("goods", [])
    if isinstance(inv_goods_list, list) and inv_goods_list:
        inv_goods_desc = inv_goods_list[0].get("description", "")
    if not inv_goods_desc:
        inv_goods_desc = invoice.get("goods_description", "")
    
    # 检查是否要求精确匹配
    exact_required = "exactly as stated" in lc_raw.lower() or "exactly as per" in lc_raw.lower()
    
    if lc_goods_desc and inv_raw:
        # 提取型号信息
        model_match = _re_goods.search(r'MODEL[:\s]+([A-Za-z0-9\s\-\.\/]+?)(?:,|$)', lc_goods_desc)
        if model_match:
            lc_model = model_match.group(1).strip()
            # 在发票 raw_text 中查找对应的型号行
            inv_model_match = _re_goods.search(r'[Mm]odel[:\s]+([A-Za-z0-9\s\-\.\/]+?)(?:\n|,|$)', inv_raw)
            if inv_model_match:
                inv_model = inv_model_match.group(1).strip()
                # 如果语义相同但大小写不同
                if lc_model.lower() == inv_model.lower() and lc_model != inv_model:
                    discrepancies.append({
                        "document": "商业发票",
                        "field": "货物描述",
                        "lc_requirement": f"MODEL: {lc_model}" + (" (EXACTLY AS STATED)" if exact_required else ""),
                        "doc_shows": f"Model: {inv_model}",
                        "description": f"型号描述大小写不一致：信用证为 \"{lc_model}\"，发票为 \"{inv_model}\"" + ("。信用证要求 EXACTLY AS STATED" if exact_required else ""),
                        "ucp_reference": "UCP600 Article 18(c)",
                        "severity": "一般" if not exact_required else "严重"
                    })

    return discrepancies, compliant_items


# ============================================================
# 第四部分：第二层 — AI 全面审核（核心）
# ============================================================
def ai_full_review(lc, invoice, bl, insurance, presentation_date):
    """
    让大模型一次性全面审核所有单据
    使用动态 RAG 检索 + 宁多勿漏原则
    """

    # 动态检索相关条款（新策略）
    print("\n  [AI审核] 开始检索相关 UCP600 条款...")
    all_context = retrieve_comprehensive_context(lc, invoice, bl, insurance)

    # 构造完整的审核 Prompt（优化版，强调宁多勿漏）
    system_prompt = """你是一位资深的信用证审单专家，精通 UCP600。你的任务是对照信用证条款，逐项审核所有单据，找出每一个不符点。

【核心原则：宁可多查，不可漏查】
- 任何细微的不一致都应该报告
- 即使是边缘情况或轻微问题，也请列出
- 如果你认为某个判断存在疑问，请标记为"不确定，建议复核"
- 不要因为问题看起来"太小"而忽略它
- 信用证审单的原则是"严格相符"，请严格把关

你必须检查以下所有方面（包括但不限于）：
1. 货物描述：发票描述是否与信用证完全一致（Article 18(c)），提单描述是否与信用证矛盾（Article 14(d)）
2. 装卸港：提单装货港、卸货港是否与信用证一致（Article 20(a)(iii)）
3. 清洁提单：提单是否有不清洁批注（Article 27），即使是轻微的包装问题
4. 已装船批注：提单是否显示清洁已装船（Article 20(a)(ii)）
5. 受益人名称：各单据中受益人/托运人/被保险人名称是否严格一致（包括 Inc./Incorporated/Co.,Ltd./Company Limited 等缩写差异）
6. 保险险别：是否覆盖信用证要求的所有险种，有无除外条款与信用证矛盾（Article 28）
7. 保险金额：是否至少为发票金额的110%（Article 28(f)(ii)）
8. 保险起运地/目的地：是否与提单装卸港一致（Article 28(h)）
9. 贸易术语：发票贸易术语是否与信用证一致
10. 分批装运：如果信用证禁止分批装运，提单或发票是否显示分批（Article 31）
11. 转运：如果信用证禁止转运，提单是否显示转运（Article 20(c)）
12. 单据份数：发票份数、提单份数是否符合信用证要求（Article 17）
13. 租船提单：如果是租船提单，是否符合 Article 22 的特殊规定
14. 舱面货：提单是否显示货装舱面（Article 26）
15. 数量和单位：各单据之间的数量、单位表述是否一致
16. 申请人/抬头：发票抬头是否为信用证申请人
17. 交单期限：是否在信用证规定的交单期限内（Article 14(c)）
18. 正本单据：是否提交了要求的正本份数（Article 17）
19. 其他任何你发现的不一致，无论大小

回答要求：
- 只输出 JSON 数组格式
- 每个不符点一个 JSON 对象
- 如果没有发现不符点，输出空数组 []
- 即使问题轻微，也请报告，可以使用"severity": "轻微"
- 对于不确定的判断，添加 "uncertain": true 标记

JSON 格式：
[
  {
    "document": "涉及的单据名称",
    "field": "不符的字段",
    "lc_requirement": "信用证的要求",
    "doc_shows": "单据实际显示",
    "description": "不符点的详细说明",
    "ucp_reference": "UCP600 条款编号",
    "severity": "严重/一般/轻微",
    "uncertain": false
  }
]"""

    # 构造单据信息
    lc_info = json.dumps(lc, ensure_ascii=False, indent=2)
    inv_info = json.dumps(invoice, ensure_ascii=False, indent=2)
    bl_info = json.dumps(bl, ensure_ascii=False, indent=2)
    ins_info = json.dumps(insurance, ensure_ascii=False, indent=2)

    user_prompt = f"""以下是 UCP600 相关条款（请严格依据这些条款判断）：

{all_context}

===== 信用证 =====
{lc_info}

===== 商业发票 =====
{inv_info}

===== 提单 =====
{bl_info}

===== 保险单 =====
{ins_info}

交单日期：{presentation_date}

请逐项检查上述所有单据，对照信用证条款和 UCP600 规定，找出所有不符点。

【重要提醒】
- 宁可多报，不可漏报。即使是轻微的不一致也请报告。
- 请仔细检查每一个细节，包括名称拼写、日期、金额、港口、货物描述等。
- 如果单据中有任何与信用证不一致的地方，无论大小，请列出。

请直接输出 JSON 数组，不要输出其他内容。"""

    response = llm_client.chat.completions.create(
        model="qwen2.5:14b",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.1,
    )

    answer = response.choices[0].message.content.strip()

    # 解析 JSON
    try:
        if answer.startswith("```"):
            answer = answer.split("\n", 1)[1]
            answer = answer.rsplit("```", 1)[0]
        result = json.loads(answer)
        if isinstance(result, list):
            return result
        return []
    except json.JSONDecodeError:
        print(f"  ⚠️ AI 返回格式异常，尝试提取...")
        # 尝试找到 JSON 数组
        import re
        match = re.search(r'\[.*\]', answer, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except json.JSONDecodeError:
                pass
        print(f"  ❌ 无法解析 AI 返回，原文：{answer[:200]}...")
        return []


# ============================================================
# 第五部分：合并去重
# ============================================================
def merge_discrepancies(rule_discs, ai_discs):
    """合并规则引擎和 AI 的结果，去除重复"""
    merged = list(rule_discs)  # 规则引擎的结果优先（更精确）
    
    for ai_d in ai_discs:
        ai_doc = ai_d.get("document", "").lower()
        ai_field = ai_d.get("field", "").lower()
        ai_desc = ai_d.get("description", "").lower()
        
        # 检查是否与已有的规则结果重复
        is_duplicate = False
        for rule_d in rule_discs:
            rule_doc = rule_d.get("document", "").lower()
            rule_field = rule_d.get("field", "").lower()
            rule_desc = rule_d.get("description", "").lower()
            
            # 如果涉及同一单据同一字段，认为是重复
            if (ai_doc in rule_doc or rule_doc in ai_doc) and \
               (ai_field in rule_field or rule_field in ai_field):
                is_duplicate = True
                break
            
            # 如果描述内容高度相似，也认为是重复
            if ai_doc == rule_doc and len(set(ai_desc.split()) & set(rule_desc.split())) > 3:
                is_duplicate = True
                break
        
        if not is_duplicate:
            merged.append(ai_d)
    
    return merged


# ============================================================
# 第六部分：生成报告
# ============================================================
def generate_report(case, all_discrepancies, compliant_items):
    """生成标准化审核报告"""
    lc = case["letter_of_credit"]
    
    report = []
    report.append("=" * 70)
    report.append("              信用证单据审核报告（V2 — AI 驱动）")
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

    if all_discrepancies:
        for i, d in enumerate(all_discrepancies, 1):
            report.append("-" * 70)
            report.append(f"  不符点 #{i}")
            report.append("-" * 70)
            report.append(f"  涉及单据：{d.get('document', '')}")
            report.append(f"  不符字段：{d.get('field', '')}")
            if d.get('lc_requirement'):
                report.append(f"  信用证要求：{d.get('lc_requirement', '')}")
            if d.get('doc_shows'):
                report.append(f"  单据显示：{d.get('doc_shows', '')}")
            report.append(f"  差异说明：{d.get('description', '')}")
            report.append(f"  依据条款：{d.get('ucp_reference', '')}")
            severity = d.get('severity', '一般')
            stars = {"严重": "★★★", "一般": "★★", "轻微": "★"}.get(severity, "★★")
            report.append(f"  严重程度：{stars} {severity}")
            if d.get('uncertain'):
                report.append(f"  ⚠️  注意：此判断存在不确定性，建议人工复核")
            report.append("")

    if compliant_items:
        report.append("-" * 70)
        report.append("  相符项目（已通过审核）")
        report.append("-" * 70)
        for item in compliant_items:
            report.append(f"  ✓ {item}")
        report.append("")

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
# 第七部分：主程序
# ============================================================
def main():
    data_path = "/root/lc-checker/test_data/test_cases_blind.json"
    print(f"正在加载测试数据：{data_path}\n")

    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    cases = data["cases"]
    print(f"共加载 {len(cases)} 组测试案例\n")

    report_dir = "/root/lc-checker/reports_v2"
    os.makedirs(report_dir, exist_ok=True)

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

        # 第一层：规则引擎（精确计算）
        print("  [第一层] 规则引擎 — 精确计算...")
        rule_discrepancies, compliant_items = check_calculations(
            lc, invoice, bl, insurance, presentation_date
        )
        print(f"  → 发现 {len(rule_discrepancies)} 个计算类不符点\n")

        # 第二层：AI 全面审核
        print("  [第二层] AI 全面审核 — 动态检索 + 大模型分析...")
        ai_discrepancies = ai_full_review(lc, invoice, bl, insurance, presentation_date)
        print(f"  → AI 发现 {len(ai_discrepancies)} 个不符点\n")

        # 第三层：合并去重
        print("  [第三层] 合并去重...")
        all_discrepancies = merge_discrepancies(rule_discrepancies, ai_discrepancies)
        print(f"  → 合并后共 {len(all_discrepancies)} 个不符点\n")

        # 生成报告
        report = generate_report(case, all_discrepancies, compliant_items)
        print(report)

        # 保存报告
        report_path = os.path.join(report_dir, f"{case_id}_report_v2.txt")
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"\n  报告已保存：{report_path}")

        # 对比标准答案
        expected_count = len(expected.get("discrepancies", []))
        found_count = len(all_discrepancies)

        print(f"\n  标准答案：{expected_count} 个不符点")
        print(f"  系统发现：{found_count} 个不符点")
        print(f"  预期结果：{'有不符点' if expected.get('has_discrepancies') else '无不符点'}")
        print(f"  系统判断：{'有不符点' if found_count > 0 else '无不符点'}")

        if expected.get("has_discrepancies") == (found_count > 0):
            print(f"  ✅ 大方向判断正确")
            total_correct += 1
        else:
            print(f"  ❌ 大方向判断错误")

    # 总结
    print(f"\n\n{'=' * 70}")
    print(f"              审核总结（V2 — AI 驱动架构）")
    print(f"{'=' * 70}")
    print(f"  总案例数：{len(cases)}")
    print(f"  大方向正确：{total_correct}/{len(cases)}（{total_correct/len(cases)*100:.1f}%）")
    print(f"  报告保存路径：{report_dir}/")
    print(f"{'=' * 70}")


if __name__ == "__main__":
    main()
