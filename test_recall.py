import json
import os
import time

WORK_DIR = os.path.dirname(os.path.abspath(__file__))

EXPECTED_SIGNATURES = {
    "case_11": [],
    "case_12": [
        {
            "id": "case12_invoice_copies",
            "description": "发票份数不足（要求3份，仅2份）",
            "keywords_groups": [
                ["invoice", "triplicate"],
                ["invoice", "3/3", "2"],
                ["invoice", "份数"],
                ["invoice", "originals", "2"],
                ["发票", "份数"],
                ["发票", "正本", "2"],
                ["发票", "三份", "两份"],
            ]
        },
        {
            "id": "case12_bl_copies",
            "description": "提单份数不足（要求全套3份，仅2份）",
            "keywords_groups": [
                ["bill of lading", "full set"],
                ["bill of lading", "3/3", "2"],
                ["提单", "份数"],
                ["提单", "全套"],
                ["提单", "正本", "2"],
                ["bl", "originals"],
                ["提单", "三份", "两份"],
            ]
        },
    ],
    "case_13": [
        {
            "id": "case13_invoice_beneficiary_name",
            "description": "发票受益人名称 Co., Ltd. vs Company Limited",
            "keywords_groups": [
                ["invoice", "beneficiary", "name"],
                ["invoice", "co., ltd", "company limited"],
                ["发票", "受益人", "名称"],
                ["发票", "co.", "company"],
                ["invoice", "beneficiary", "co."],
            ]
        },
        {
            "id": "case13_bl_shipper_name",
            "description": "提单发货人名称 Corp. vs Company Limited",
            "keywords_groups": [
                ["bill of lading", "shipper"],
                ["提单", "发货人"],
                ["提单", "shipper", "corp"],
                ["bl", "shipper", "name"],
                ["提单", "托运人"],
                ["提单", "名称"],
            ]
        },
        {
            "id": "case13_insurance_insured_name",
            "description": "保险单被保险人 Ltd vs Limited",
            "keywords_groups": [
                ["insurance", "insured", "name"],
                ["insurance", "ltd", "limited"],
                ["保险", "被保险人"],
                ["保险", "名称"],
                ["保险单", "insured"],
            ]
        },
    ],
    "case_14": [
        {
            "id": "case14_partial_shipment",
            "description": "分批装运违规",
            "keywords_groups": [
                ["partial shipment"],
                ["分批装运"],
                ["分批"],
                ["partial", "prohibited"],
                ["两批", "装运"],
                ["lot 1", "lot 2"],
            ]
        },
        {
            "id": "case14_trade_terms",
            "description": "贸易术语 FOB vs CIF 不一致",
            "keywords_groups": [
                ["trade term"],
                ["贸易术语"],
                ["fob", "cif"],
                ["fob valencia", "cif lisbon"],
                ["incoterm"],
            ]
        },
        {
            "id": "case14_onboard_notation",
            "description": "装船批注与禁止分批矛盾",
            "keywords_groups": [
                ["on board", "partial"],
                ["装船", "分批"],
                ["lot 1", "lot 2"],
                ["批注", "分批"],
                ["两批", "装船"],
            ]
        },
    ],
    "case_15": [
        {
            "id": "case15_invoice_amount",
            "description": "发票金额超支 885,000 vs 875,000",
            "keywords_groups": [
                ["invoice", "amount", "exceed"],
                ["invoice", "amount", "超"],
                ["金额", "超"],
                ["885,000", "875,000"],
                ["885000", "875000"],
                ["发票", "金额"],
                ["amount", "overdrawn"],
            ]
        },
        {
            "id": "case15_model_reference",
            "description": "型号描述大小写差异",
            "keywords_groups": [
                ["model", "reference"],
                ["型号"],
                ["chronomaster"],
                ["goods description", "model"],
                ["货物描述", "型号"],
                ["03.2040.400"],
            ]
        },
        {
            "id": "case15_insurance_coverage",
            "description": "保险条款排除了神秘失踪",
            "keywords_groups": [
                ["mysterious disappearance"],
                ["神秘失踪"],
                ["coverage", "exclud"],
                ["coverage", "除外"],
                ["insurance", "mysterious"],
                ["承保", "排除"],
                ["保险", "失踪"],
            ]
        },
        {
            "id": "case15_insurance_amount",
            "description": "保险金额未达110%",
            "keywords_groups": [
                ["insurance", "amount", "110"],
                ["保险", "金额", "110"],
                ["保险金额", "不足"],
                ["insurance amount", "insuffi"],
                ["28(f)", "110"],
                ["保险", "加成"],
            ]
        },
    ],
}


def match_discrepancy(disc, keywords_group):
    text = json.dumps(disc, ensure_ascii=False).lower()
    return all(kw.lower() in text for kw in keywords_group)


def check_recall(discrepancies, expected_sigs):
    results = []
    for sig in expected_sigs:
        found = False
        matched_by = None
        for disc in discrepancies:
            for kg in sig["keywords_groups"]:
                if match_discrepancy(disc, kg):
                    found = True
                    matched_by = f"{disc.get('document','')}/{disc.get('field','')}"
                    break
            if found:
                break
        results.append({
            "id": sig["id"],
            "description": sig["description"],
            "recalled": found,
            "matched_by": matched_by,
        })
    return results


print("=" * 70)
print("  V2 vs V3 召回率对比（宁可误报，不可漏报）")
print("=" * 70)

data_path = os.path.join(WORK_DIR, "test_data", "test_cases_blind.json")
with open(data_path, "r", encoding="utf-8") as f:
    data = json.load(f)

cases = data["cases"]
v2_total_recall = 0
v3_total_recall = 0
v2_total_expected = 0
v3_total_expected = 0
v2_total_reported = 0
v3_total_reported = 0
all_results = []

for case in cases:
    case_id = case["case_id"]
    desc = case.get("case_description", "")
    lc = case["letter_of_credit"]
    invoice = case["commercial_invoice"]
    bl = case["bill_of_lading"]
    insurance = case["insurance_policy"]
    presentation_date = case.get("presentation_date", "")
    expected_sigs = EXPECTED_SIGNATURES.get(case_id, [])

    print(f"\n{'#' * 70}")
    print(f"# {case_id} - {desc}")
    print(f"# 标准答案：{len(expected_sigs)} 个不符点")
    print(f"{'#' * 70}")

    print(f"\n  [V2] 审核中...")
    t0 = time.time()
    try:
        from check_v2 import check_calculations, ai_full_review, merge_discrepancies
        rule_disc, compliant = check_calculations(lc, invoice, bl, insurance, presentation_date)
        ai_disc = ai_full_review(lc, invoice, bl, insurance, presentation_date)
        v2_result = merge_discrepancies(rule_disc, ai_disc)
        v2_time = time.time() - t0
    except Exception as e:
        print(f"  [V2] 出错：{e}")
        v2_result = []
        v2_time = 0

    print(f"\n  [V3] 增强审核中...")
    t0 = time.time()
    try:
        from enhanced_review import enhanced_review
        v3_obj = enhanced_review(lc, invoice, bl, insurance, presentation_date)
        if hasattr(v3_obj, 'discrepancies'):
            v3_result = v3_obj.discrepancies
        elif isinstance(v3_obj, dict):
            v3_result = v3_obj.get("discrepancies", [])
        else:
            v3_result = []
        v3_time = time.time() - t0
    except Exception as e:
        print(f"  [V3] 出错：{e}")
        v3_result = []
        v3_time = 0

    print(f"\n  V2 报告了 {len(v2_result)} 个不符点（耗时 {v2_time:.1f}s）")
    print(f"  V3 报告了 {len(v3_result)} 个不符点（耗时 {v3_time:.1f}s）")

    if expected_sigs:
        v2_recall = check_recall(v2_result, expected_sigs)
        v3_recall = check_recall(v3_result, expected_sigs)

        v2_hit = sum(1 for r in v2_recall if r["recalled"])
        v3_hit = sum(1 for r in v3_recall if r["recalled"])
        total_exp = len(expected_sigs)

        v2_total_recall += v2_hit
        v3_total_recall += v3_hit
        v2_total_expected += total_exp
        v3_total_expected += total_exp

        print(f"\n  召回率：V2 = {v2_hit}/{total_exp}  |  V3 = {v3_hit}/{total_exp}")
        print(f"\n  逐项召回详情：")
        for i, sig in enumerate(expected_sigs):
            v2_s = "✅ 召回" if v2_recall[i]["recalled"] else "❌ 漏报"
            v3_s = "✅ 召回" if v3_recall[i]["recalled"] else "❌ 漏报"
            v2_m = f" <- {v2_recall[i]['matched_by']}" if v2_recall[i]["recalled"] else ""
            v3_m = f" <- {v3_recall[i]['matched_by']}" if v3_recall[i]["recalled"] else ""
            print(f"    {sig['description']}")
            print(f"      V2: {v2_s}{v2_m}")
            print(f"      V3: {v3_s}{v3_m}")
    else:
        print(f"\n  [无不符点案例] V2 误报 {len(v2_result)} 个 | V3 误报 {len(v3_result)} 个")

    v2_total_reported += len(v2_result)
    v3_total_reported += len(v3_result)

    all_results.append({
        "case_id": case_id,
        "expected": len(expected_sigs),
        "v2_reported": len(v2_result),
        "v3_reported": len(v3_result),
        "v2_recalled": sum(1 for r in check_recall(v2_result, expected_sigs) if r["recalled"]) if expected_sigs else 0,
        "v3_recalled": sum(1 for r in check_recall(v3_result, expected_sigs) if r["recalled"]) if expected_sigs else 0,
    })

print(f"\n\n{'=' * 70}")
print(f"              召回率对比总结")
print(f"{'=' * 70}")

v2_rr = v2_total_recall / v2_total_expected * 100 if v2_total_expected else 0
v3_rr = v3_total_recall / v3_total_expected * 100 if v3_total_expected else 0

print(f"""
  ┌──────────────────────┬───────────────────┬───────────────────┐
  │ 指标                 │ V2（现有）         │ V3（增强版）       │
  ├──────────────────────┼───────────────────┼───────────────────┤
  │ 召回率（核心）        │ {v2_total_recall}/{v2_total_expected} ({v2_rr:.0f}%)           │ {v3_total_recall}/{v3_total_expected} ({v3_rr:.0f}%)           │
  │ 总报告不符点数        │ {v2_total_reported}                  │ {v3_total_reported}                  │
  │ 误报数（总报-真召回） │ {v2_total_reported - v2_total_recall}                  │ {v3_total_reported - v3_total_recall}                  │
  └──────────────────────┴───────────────────┴───────────────────┘

  核心指标解读：
  * 召回率 = 标准答案中的不符点被找到了几个（越高越好，100%最理想）
  * 误报数 = 报告了但不在标准答案中的数量（可接受，但越少越精准）
  * 理想系统：召回率 100% + 误报数尽量少
""")

if v3_rr >= v2_rr and v3_total_reported <= v2_total_reported:
    print("  >>> 结论：V3 全面优于 V2（召回率不低 + 误报更少）")
elif v3_rr >= v2_rr:
    print("  >>> 结论：V3 召回率不低于 V2（核心指标达标）")
elif v3_rr < v2_rr:
    diff = v2_total_recall - v3_total_recall
    print(f"  >>> 结论：V3 召回率低于 V2，漏报了 {diff} 个标准不符点，需要调优")

output_path = os.path.join(WORK_DIR, "reports_v2", "v2_vs_v3_recall.json")
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(all_results, f, ensure_ascii=False, indent=2)
print(f"\n  详细结果已保存：{output_path}")
print(f"{'=' * 70}")
