"""
用 case_01 的 raw_text 生成测试用 PDF 文件
"""
import fitz  # PyMuPDF
import os
import json

# 加载测试数据
data_path = "/root/lc-checker/test_data/test_cases.json"
with open(data_path, "r", encoding="utf-8") as f:
    data = json.load(f)

case = data["cases"][0]  # case_01

# 输出目录
output_dir = "/root/lc-checker/test_pdf"
os.makedirs(output_dir, exist_ok=True)

def create_pdf(text, output_path, title="Document"):
    """将文字内容生成为 PDF"""
    doc = fitz.open()
    
    # 按行分割文字
    lines = text.split("\n")
    
    page = doc.new_page(width=595, height=842)  # A4 尺寸
    y = 50  # 起始 y 坐标
    
    for line in lines:
        if y > 790:  # 换页
            page = doc.new_page(width=595, height=842)
            y = 50
        
        # 标题行用粗体
        fontsize = 9
        if line.strip().startswith(("BILL OF LADING", "COMMERCIAL INVOICE", 
                                     "INSURANCE POLICY", "MT700")):
            fontsize = 11
        
        page.insert_text(
            fitz.Point(40, y),
            line,
            fontsize=fontsize,
            fontname="helv"
        )
        y += 14
    
    doc.save(output_path)
    doc.close()
    print(f"  ✅ 已生成：{output_path}")

# 生成 4 份 PDF
print("正在生成测试 PDF 文件...\n")

create_pdf(
    case["letter_of_credit"]["raw_text"],
    os.path.join(output_dir, "case_01_lc.pdf"),
    "Letter of Credit"
)

create_pdf(
    case["commercial_invoice"]["raw_text"],
    os.path.join(output_dir, "case_01_invoice.pdf"),
    "Commercial Invoice"
)

create_pdf(
    case["bill_of_lading"]["raw_text"],
    os.path.join(output_dir, "case_01_bl.pdf"),
    "Bill of Lading"
)

create_pdf(
    case["insurance_policy"]["raw_text"],
    os.path.join(output_dir, "case_01_insurance.pdf"),
    "Insurance Policy"
)

print(f"\n全部 PDF 已生成到：{output_dir}/")
print("文件列表：")
for f in os.listdir(output_dir):
    size = os.path.getsize(os.path.join(output_dir, f))
    print(f"  {f} ({size} bytes)")