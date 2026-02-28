"""
OCR 模块：从 PDF/图片中提取文字，再用 AI 提取结构化字段
"""
import os
import json
import sys
from paddleocr import PaddleOCR
from PIL import Image
import fitz  # PyMuPDF

from openai import OpenAI

# 初始化 OCR
ocr = PaddleOCR(use_textline_orientation=True, lang='en')

# 连接本地大模型
llm_client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)


# ============================================================
# 第一部分：从文件中提取文字
# ============================================================
def extract_text_from_image(image_path):
    """从图片中提取文字"""
    print(f"  正在 OCR 识别图片：{image_path}")
    result = ocr.ocr(image_path, cls=True)
    
    lines = []
    if result and result[0]:
        for line in result[0]:
            text = line[1][0]
            confidence = line[1][1]
            lines.append(text)
    
    raw_text = "\n".join(lines)
    print(f"  → 识别出 {len(lines)} 行文字")
    return raw_text


def extract_text_from_pdf(pdf_path):
    """从 PDF 中提取文字"""
    print(f"  正在处理 PDF：{pdf_path}")
    
    # 先尝试直接提取文字（如果 PDF 是电子版）
    doc = fitz.open(pdf_path)
    all_text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text()
        if text.strip():
            all_text += text + "\n"
    doc.close()
    
    # 如果直接提取到了足够的文字，就不用 OCR
    if len(all_text.strip()) > 100:
        print(f"  → 电子版 PDF，直接提取文字，共 {len(all_text)} 字符")
        return all_text
    
    # 否则用 OCR（扫描版 PDF）
    print(f"  → 扫描版 PDF，使用 OCR 识别...")
    doc = fitz.open(pdf_path)
    all_text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        # 将 PDF 页面渲染为图片
        pix = page.get_pixmap(dpi=300)
        img_path = f"/tmp/ocr_page_{page_num}.png"
        pix.save(img_path)
        
        # OCR 识别
        page_text = extract_text_from_image(img_path)
        all_text += page_text + "\n"
        
        # 清理临时文件
        os.remove(img_path)
    
    doc.close()
    return all_text


def extract_text(file_path):
    """根据文件类型自动选择提取方式"""
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext in [".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".tif"]:
        return extract_text_from_image(file_path)
    else:
        raise ValueError(f"不支持的文件格式：{ext}，请上传 PDF 或图片文件")


# ============================================================
# 第二部分：用 AI 从文字中提取结构化字段
# ============================================================
def extract_lc_fields(raw_text):
    """从信用证文字中提取结构化字段"""
    prompt = """你是一位信用证专家。以下是一份信用证的文字内容（可能来自 OCR 识别，有少量错误）。
请从中提取以下字段，输出 JSON 格式。如果某个字段无法识别，填 null。

必须提取的字段：
{
  "lc_number": "信用证号",
  "issuing_bank": "开证行",
  "advising_bank": "通知行",
  "applicant": {
    "name": "申请人名称",
    "address": "申请人地址"
  },
  "beneficiary": {
    "name": "受益人名称",
    "address": "受益人地址"
  },
  "currency": "币种（如 USD、EUR）",
  "amount": 数字（如 485000.00），
  "amount_tolerance": "金额容差（如 +/- 5%）",
  "goods_description": "货物描述（完整内容）",
  "latest_shipment_date": "最迟装运日（YYYY-MM-DD格式）",
  "expiry_date": "到期日（YYYY-MM-DD格式）",
  "expiry_place": "到期地点",
  "presentation_period": "交单期限",
  "loading_port": "装货港",
  "discharge_port": "卸货港",
  "trade_terms": "贸易术语（如 CIF Shanghai）",
  "partial_shipment": "分批装运（Allowed 或 Not Allowed）",
  "transhipment": "转运（Allowed 或 Not Allowed）",
  "required_documents": ["要求的单据列表"],
  "additional_conditions": ["附加条件列表"]
}

请直接输出 JSON，不要输出其他内容。"""

    return _ai_extract(prompt, raw_text)


def extract_invoice_fields(raw_text):
    """从商业发票文字中提取结构化字段"""
    prompt = """你是一位信用证专家。以下是一份商业发票的文字内容（可能来自 OCR 识别）。
请从中提取以下字段，输出 JSON 格式。如果某个字段无法识别，填 null。

必须提取的字段：
{
  "invoice_number": "发票号",
  "invoice_date": "发票日期（YYYY-MM-DD格式）",
  "issued_by": "出票人（卖方）",
  "issued_to": "抬头（买方）",
  "currency": "币种",
  "goods": [
    {
      "description": "货物描述",
      "quantity": 数字,
      "unit": "单位",
      "unit_price": 数字,
      "amount": 数字
    }
  ],
  "total_amount": 数字,
  "trade_terms": "贸易术语"
}

请直接输出 JSON。"""

    return _ai_extract(prompt, raw_text)


def extract_bl_fields(raw_text):
    """从提单文字中提取结构化字段"""
    prompt = """你是一位信用证专家。以下是一份提单（Bill of Lading）的文字内容（可能来自 OCR 识别）。
请从中提取以下字段，输出 JSON 格式。如果某个字段无法识别，填 null。

必须提取的字段：
{
  "bl_number": "提单号",
  "shipper": "托运人",
  "consignee": "收货人",
  "notify_party": "通知方",
  "vessel": "船名",
  "voyage": "航次",
  "port_of_loading": "装货港",
  "port_of_discharge": "卸货港",
  "onboard_date": "装船日期（YYYY-MM-DD格式）",
  "issue_date": "签发日期（YYYY-MM-DD格式）",
  "goods_description": "货物描述",
  "number_of_packages": "包装数量",
  "gross_weight": "毛重",
  "freight": "运费（如 Freight Prepaid 或 Freight Collect）",
  "number_of_originals": "正本份数（如 3/3）",
  "clean_onboard": true或false（是否清洁已装船）,
  "carrier_signature": "承运人签名"
}

特别注意：
- 如果提单有任何不清洁批注（如 damaged、stained、torn 等），clean_onboard 为 false
- 如果提单显示 "CLEAN ON BOARD"，clean_onboard 为 true
- 如果提单显示有转运（TRANSHIPMENT AT...），请在 goods_description 中保留这个信息

请直接输出 JSON。"""

    return _ai_extract(prompt, raw_text)


def extract_insurance_fields(raw_text):
    """从保险单文字中提取结构化字段"""
    prompt = """你是一位信用证专家。以下是一份保险单的文字内容（可能来自 OCR 识别）。
请从中提取以下字段，输出 JSON 格式。如果某个字段无法识别，填 null。

必须提取的字段：
{
  "policy_number": "保险单号",
  "insured": "被保险人",
  "insurance_amount": 数字（保险金额）,
  "currency": "币种",
  "coverage": "承保范围（完整内容，包括除外条款）",
  "goods_description": "货物描述",
  "vessel": "船名/航班",
  "from": "起运地",
  "to": "目的地",
  "issue_date": "签发日期（YYYY-MM-DD格式）",
  "claims_payable_at": "理赔地点"
}

特别注意：
- coverage 字段必须包含所有险别和除外条款（EXCLUDING 开头的内容）
- 金额必须是纯数字，不要包含货币符号

请直接输出 JSON。"""

    return _ai_extract(prompt, raw_text)


def _ai_extract(prompt, raw_text):
    """调用 AI 提取结构化字段"""
    response = llm_client.chat.completions.create(
        model="qwen2.5:14b",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"以下是单据的文字内容：\n\n{raw_text}"}
        ],
        temperature=0.1,
    )
    
    answer = response.choices[0].message.content.strip()
    
    try:
        # 去除可能的 markdown 代码块标记
        if answer.startswith("```"):
            answer = answer.split("\n", 1)[1]
            answer = answer.rsplit("```", 1)[0]
        return json.loads(answer)
    except json.JSONDecodeError:
        import re
        match = re.search(r'\{.*\}', answer, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except json.JSONDecodeError:
                pass
        print(f"  ❌ AI 返回的 JSON 解析失败")
        print(f"  原文前 500 字符：{answer[:500]}")
        return None


# ============================================================
# 第三部分：完整提取流程
# ============================================================
def process_documents(lc_file, invoice_file, bl_file, insurance_file, presentation_date):
    """
    处理一套完整的单据文件
    
    参数：
      lc_file: 信用证文件路径（PDF/图片）
      invoice_file: 商业发票文件路径
      bl_file: 提单文件路径
      insurance_file: 保险单文件路径
      presentation_date: 交单日期（字符串，YYYY-MM-DD）
    
    返回：
      dict: 包含所有结构化字段的字典，可直接传入 check_v2.py
    """
    print("\n" + "=" * 70)
    print("  OCR 文件解析模块")
    print("=" * 70)
    
    # 提取信用证
    print("\n[1/4] 处理信用证...")
    lc_text = extract_text(lc_file)
    print(f"  提取文字完成，共 {len(lc_text)} 字符")
    print(f"  正在用 AI 提取结构化字段...")
    lc_data = extract_lc_fields(lc_text)
    if lc_data:
        lc_data["raw_text"] = lc_text
        print(f"  ✅ 信用证解析成功：{lc_data.get('lc_number', '未识别')}")
    else:
        print(f"  ❌ 信用证解析失败")
        return None
    
    # 提取商业发票
    print("\n[2/4] 处理商业发票...")
    inv_text = extract_text(invoice_file)
    print(f"  提取文字完成，共 {len(inv_text)} 字符")
    print(f"  正在用 AI 提取结构化字段...")
    inv_data = extract_invoice_fields(inv_text)
    if inv_data:
        inv_data["raw_text"] = inv_text
        print(f"  ✅ 商业发票解析成功：{inv_data.get('invoice_number', '未识别')}")
    else:
        print(f"  ❌ 商业发票解析失败")
        return None
    
    # 提取提单
    print("\n[3/4] 处理提单...")
    bl_text = extract_text(bl_file)
    print(f"  提取文字完成，共 {len(bl_text)} 字符")
    print(f"  正在用 AI 提取结构化字段...")
    bl_data = extract_bl_fields(bl_text)
    if bl_data:
        bl_data["raw_text"] = bl_text
        print(f"  ✅ 提单解析成功：{bl_data.get('bl_number', '未识别')}")
    else:
        print(f"  ❌ 提单解析失败")
        return None
    
    # 提取保险单
    print("\n[4/4] ��理保险单...")
    ins_text = extract_text(insurance_file)
    print(f"  提取文字完成，共 {len(ins_text)} 字符")
    print(f"  正在用 AI 提取结构化字段...")
    ins_data = extract_insurance_fields(ins_text)
    if ins_data:
        ins_data["raw_text"] = ins_text
        print(f"  ✅ 保险单解析成功：{ins_data.get('policy_number', '未识别')}")
    else:
        print(f"  ❌ 保险单解析失败")
        return None
    
    print("\n" + "=" * 70)
    print("  ✅ 全部单据解析完成！")
    print("=" * 70)
    
    return {
        "letter_of_credit": lc_data,
        "commercial_invoice": inv_data,
        "bill_of_lading": bl_data,
        "insurance_policy": ins_data,
        "presentation_date": presentation_date
    }


# ============================================================
# 第四部分：用 raw_text 测试（不需要真实文件）
# ============================================================
def process_from_raw_text(lc_raw, inv_raw, bl_raw, ins_raw, presentation_date):
    """
    直接从 raw_text 提取结构化字段（用于测试，跳过 OCR 步骤）
    """
    print("\n" + "=" * 70)
    print("  文本解析模块（从 raw_text 提取）")
    print("=" * 70)
    
    print("\n[1/4] 解析信用证...")
    lc_data = extract_lc_fields(lc_raw)
    if lc_data:
        lc_data["raw_text"] = lc_raw
        print(f"  ✅ 成功：{lc_data.get('lc_number', '未识别')}")
    
    print("\n[2/4] 解析商业发票...")
    inv_data = extract_invoice_fields(inv_raw)
    if inv_data:
        inv_data["raw_text"] = inv_raw
        print(f"  ✅ 成功：{inv_data.get('invoice_number', '未识别')}")
    
    print("\n[3/4] 解析提单...")
    bl_data = extract_bl_fields(bl_raw)
    if bl_data:
        bl_data["raw_text"] = bl_raw
        print(f"  ✅ 成功：{bl_data.get('bl_number', '未识别')}")
    
    print("\n[4/4] 解析保险单...")
    ins_data = extract_insurance_fields(ins_raw)
    if ins_data:
        ins_data["raw_text"] = ins_raw
        print(f"  ✅ 成功：{ins_data.get('policy_number', '未识别')}")
    
    print("\n" + "=" * 70)
    print("  ✅ 全部解析完成！")
    print("=" * 70)
    
    return {
        "letter_of_credit": lc_data,
        "commercial_invoice": inv_data,
        "bill_of_lading": bl_data,
        "insurance_policy": ins_data,
        "presentation_date": presentation_date
    }


# ============================================================
# 测试入口
# ============================================================
if __name__ == "__main__":
    # 用 case_01 的 raw_text 做测试
    import json
    
    data_path = "/root/lc-checker/test_data/test_cases.json"
    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    case = data["cases"][0]  # case_01
    print(f"\n测试案例：{case['case_id']} — {case['case_description']}")
    
    result = process_from_raw_text(
        lc_raw=case["letter_of_credit"]["raw_text"],
        inv_raw=case["commercial_invoice"]["raw_text"],
        bl_raw=case["bill_of_lading"]["raw_text"],
        ins_raw=case["insurance_policy"]["raw_text"],
        presentation_date=case["presentation_date"]
    )
    
    if result:
        # 打印提取结果
        print("\n\n提取的信用证字段：")
        lc = result["letter_of_credit"]
        for key in ["lc_number", "currency", "amount", "goods_description", 
                     "latest_shipment_date", "loading_port", "discharge_port"]:
            print(f"  {key}: {lc.get(key, 'N/A')}")
        
        print("\n提取的发票字段：")
        inv = result["commercial_invoice"]
        for key in ["invoice_number", "currency", "total_amount", "trade_terms"]:
            print(f"  {key}: {inv.get(key, 'N/A')}")
        
        print("\n提取的提单字段：")
        bl = result["bill_of_lading"]
        for key in ["bl_number", "port_of_loading", "port_of_discharge", 
                     "onboard_date", "clean_onboard"]:
            print(f"  {key}: {bl.get(key, 'N/A')}")
        
        print("\n提取的保险单字段：")
        ins = result["insurance_policy"]
        for key in ["policy_number", "insurance_amount", "currency", "coverage"]:
            print(f"  {key}: {ins.get(key, 'N/A')}")
        
        # 保存提取结果
        output_path = "/root/lc-checker/test_data/case_01_extracted.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"\n结果已保存：{output_path}")
