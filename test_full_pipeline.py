"""
完整链路测试：PDF → OCR/文字提取 → AI 提取字段 → 审核
"""
import json
import os
import sys

# 导入 OCR 模块
from ocr_extract import process_documents

# 导入 V2 审核模块的核心函数
from check_v2 import (
    check_calculations,
    ai_full_review,
    merge_discrepancies,
    generate_report
)

def main():
    print("=" * 70)
    print("  信用证智能审单系统 — 完整链路测试")
    print("  PDF → OCR → AI 提取 → 审核 → 报告")
    print("=" * 70)
    
    # 文件路径
    pdf_dir = "/root/lc-checker/test_pdf"
    lc_file = os.path.join(pdf_dir, "case_01_lc.pdf")
    invoice_file = os.path.join(pdf_dir, "case_01_invoice.pdf")
    bl_file = os.path.join(pdf_dir, "case_01_bl.pdf")
    insurance_file = os.path.join(pdf_dir, "case_01_insurance.pdf")
    presentation_date = "2024-08-28"
    
    # 检查文件是否存在
    for f in [lc_file, invoice_file, bl_file, insurance_file]:
        if not os.path.exists(f):
            print(f"  ❌ 文件不存在：{f}")
            print(f"  请先运行 python generate_test_pdf.py 生成测试文件")
            return
    
    # ============================================================
    # 阶段一：OCR + AI 提取
    # ============================================================
    print("\n\n" + "#" * 70)
    print("# 阶段一：文件解析（OCR + AI 提取结构化字段）")
    print("#" * 70)
    
    result = process_documents(
        lc_file=lc_file,
        invoice_file=invoice_file,
        bl_file=bl_file,
        insurance_file=insurance_file,
        presentation_date=presentation_date
    )
    
    if not result:
        print("\n  ❌ 文件解析失败，无法继续审核")
        return
    
    lc = result["letter_of_credit"]
    invoice = result["commercial_invoice"]
    bl = result["bill_of_lading"]
    insurance = result["insurance_policy"]
    
    # 打印提取的关键字段
    print("\n\n" + "-" * 70)
    print("  提取的关键字段一览")
    print("-" * 70)
    print(f"  信用证号：{lc.get('lc_number', 'N/A')}")
    print(f"  信用证金额：{lc.get('currency', '')} {lc.get('amount', 0):,.2f}")
    print(f"  发票金额：{invoice.get('currency', '')} {invoice.get('total_amount', 0):,.2f}")
    print(f"  装船日期：{bl.get('onboard_date', 'N/A')}")
    print(f"  最迟装运日：{lc.get('latest_shipment_date', 'N/A')}")
    print(f"  装货港：{bl.get('port_of_loading', 'N/A')}")
    print(f"  卸货港：{bl.get('port_of_discharge', 'N/A')}")
    print(f"  保险金额：{insurance.get('currency', '')} {insurance.get('insurance_amount', 0):,.2f}")
    print(f"  保险险别：{insurance.get('coverage', 'N/A')}")
    
    # ============================================================
    # 阶段二：审核（复用 check_v2.py 的逻辑）
    # ============================================================
    print("\n\n" + "#" * 70)
    print("# 阶段��：智能审核")
    print("#" * 70)
    
    # 第一层：规则引擎
    print("\n  [第一层] 规则引擎 — 精确计算...")
    rule_discrepancies, compliant_items = check_calculations(
        lc, invoice, bl, insurance, presentation_date
    )
    print(f"  → 发现 {len(rule_discrepancies)} 个计算类不符点")
    
    # 第二层：AI 全面审核
    print("\n  [第二层] AI 全面审核 — 检索 UCP600 + 大模型分析...")
    ai_discrepancies = ai_full_review(lc, invoice, bl, insurance, presentation_date)
    print(f"  → AI 发现 {len(ai_discrepancies)} 个不符点")
    
    # 第三层：合并去重
    print("\n  [第三层] 合并去重...")
    all_discrepancies = merge_discrepancies(rule_discrepancies, ai_discrepancies)
    print(f"  → 合并后共 {len(all_discrepancies)} 个不符点")
    
    # 生成报告
    case_data = {
        "case_id": "full_pipeline_test",
        "case_description": "完整链路测试（PDF → OCR → AI 提取 → 审核）",
        "letter_of_credit": lc,
        "presentation_date": presentation_date
    }
    
    report = generate_report(case_data, all_discrepancies, compliant_items)
    
    print("\n")
    print(report)
    
    # 保存报告
    report_dir = "/root/lc-checker/reports_v2"
    os.makedirs(report_dir, exist_ok=True)
    report_path = os.path.join(report_dir, "full_pipeline_test_report.txt")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"\n  报告已保存：{report_path}")
    
    # 对比标准答案（case_01 应该是无不符点）
    print(f"\n  标准答案：0 个不符点（case_01 为无不符点案例）")
    print(f"  系统发现：{len(all_discrepancies)} 个不符点")


if __name__ == "__main__":
    main()