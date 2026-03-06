"""
V2 vs V3 对比测试脚本
"""
import json
import os
import time

WORK_DIR = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(WORK_DIR, "test_data", "test_cases_blind.json")

print("=" * 70)
print("  V2 vs V3 增强效果对比测试")
print("=" * 70)

with open(data_path, "r", encoding="utf-8") as f:
    data = json.load(f)

cases = data["cases"]
print(f"\n共加载 {len(cases)} 组测试案例\n")

results = []

for case in cases:
    case_id = case["case_id"]
    desc = case.get("case_description", "")
    lc = case["letter_of_credit"]
    invoice = case["commercial_invoice"]
    bl = case["bill_of_lading"]
    insurance = case["insurance_policy"]
    presentation_date = case.get("presentation_date", "")
    expected = case.get("expected_result", {})

    print(f"\n{'#' * 70}")
    print(f"# 案例：{case_id} — {desc}")
    print(f"{'#' * 70}")

    # V2 审核
    print(f"\n  [V2] 开始审核...")
    t0 = time.time()
    try:
        from check_v2 import check_calculations, ai_full_review, merge_discrepancies
        rule_disc, compliant = check_calculations(lc, invoice, bl, insurance, presentation_date)
        ai_disc = ai_full_review(lc, invoice, bl, insurance, presentation_date)
        v2_result = merge_discrepancies(rule_disc, ai_disc)
        v2_time = time.time() - t0
        print(f"  [V2] 完成，发现 {len(v2_result)} 个不符点，耗时 {v2_time:.1f}s")
    except Exception as e:
        print(f"  [V2] 出错：{e}")
        import traceback; traceback.print_exc()
        v2_result = []
        v2_time = 0

    # V3 增强审核
    print(f"\n  [V3] 开始增强审核...")
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
        print(f"  [V3] 完成，发现 {len(v3_result)} 个不符点，耗时 {v3_time:.1f}s")
    except Exception as e:
        print(f"  [V3] 出错：{e}")
        import traceback; traceback.print_exc()
        v3_result = []
        v3_time = 0

    # 对比
    expected_count = len(expected.get("discrepancies", []))
    has_disc = expected.get("has_discrepancies", False)

    v2_correct = (len(v2_result) > 0) == has_disc
    v3_correct = (len(v3_result) > 0) == has_disc

    print(f"\n  ─── 对比结果 ───")
    print(f"  标准答案：{'有' if has_disc else '无'}不符点，共 {expected_count} 个")
    print(f"  V2 判断：{'有' if v2_result else '无'}不符点，共 {len(v2_result)} 个 → {'✅' if v2_correct else '❌'}")
    print(f"  V3 判断：{'有' if v3_result else '无'}不符点，共 {len(v3_result)} 个 → {'✅' if v3_correct else '❌'}")
    print(f"  V2 耗时：{v2_time:.1f}s | V3 耗时：{v3_time:.1f}s")

    v2_fields = set(f"{d.get('document','')}/{d.get('field','')}" for d in v2_result)
    v3_fields = set(f"{d.get('document','')}/{d.get('field','')}" for d in v3_result)
    only_v2 = v2_fields - v3_fields
    only_v3 = v3_fields - v2_fields
    if only_v2:
        print(f"  V2 独有（V3 去掉了）：{only_v2}")
    if only_v3:
        print(f"  V3 新增（V2 没发现）：{only_v3}")

    results.append({
        "case_id": case_id, "expected_count": expected_count,
        "has_discrepancies": has_disc,
        "v2_count": len(v2_result), "v3_count": len(v3_result),
        "v2_correct": v2_correct, "v3_correct": v3_correct,
        "v2_time": v2_time, "v3_time": v3_time,
        "v2_only": list(only_v2), "v3_only": list(only_v3),
    })

# 汇总
print(f"\n\n{'=' * 70}")
print(f"              对比测试总结")
print(f"{'=' * 70}")

total = len(results)
v2_ok = sum(1 for r in results if r["v2_correct"])
v3_ok = sum(1 for r in results if r["v3_correct"])
v2_avg = sum(r["v2_time"] for r in results) / total if total else 0
v3_avg = sum(r["v3_time"] for r in results) / total if total else 0
v2_exact = sum(1 for r in results if r["v2_count"] == r["expected_count"])
v3_exact = sum(1 for r in results if r["v3_count"] == r["expected_count"])
improved = sum(1 for r in results if r["v3_correct"] and not r["v2_correct"])
degraded = sum(1 for r in results if not r["v3_correct"] and r["v2_correct"])

print(f"""
  总案例数：{total}

  ┌──────────────────┬─────────────────┬─────────────────┐
  │ 指标             │ V2（现有）       │ V3（增强版）     │
  ├──────────────────┼─────────────────┼─────────────────┤
  │ 大方向正确率     │ {v2_ok}/{total} ({v2_ok/total*100:.0f}%)          │ {v3_ok}/{total} ({v3_ok/total*100:.0f}%)          │
  │ 精确匹配数量     │ {v2_exact}/{total}                │ {v3_exact}/{total}                │
  │ 平均耗时         │ {v2_avg:.1f}s              │ {v3_avg:.1f}s              │
  └──────────────────┴─────────────────┴─────────────────┘

  V3 改善了的案例：{improved} 个
  V3 退步了的案例：{degraded} 个
""")

output_path = os.path.join(WORK_DIR, "reports_v2", "v2_vs_v3_comparison.json")
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print(f"  详细结果已保存：{output_path}")
print(f"{'=' * 70}")
