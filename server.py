"""
信用证智能审单系统 — 后端 API 服务，信用证智能审单系统的后端 API 服务入口
"""
import os

# ============================================================
# 关键：在导入任何 HuggingFace 相关库之前，设置离线模式
# 必须在文件最开头设置！
# ============================================================
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"
os.environ["HF_DATASETS_OFFLINE"] = "1"
import json
import shutil
from datetime import datetime
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# 导入我们已有的模块
from ocr_extract import extract_text, extract_lc_fields, extract_invoice_fields, extract_bl_fields, extract_insurance_fields
from check_v2 import check_calculations, ai_full_review, merge_discrepancies

app = FastAPI(title="信用证智能审单系统 API")

# 允许跨域（开发阶段前端可能在不同端口）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 上传文件临时目录（支持环境变量，默认当前目录）
WORK_DIR = os.environ.get("WORK_DIR", os.path.dirname(os.path.abspath(__file__)))
UPLOAD_DIR = os.path.join(WORK_DIR, "uploads")
REPORT_DIR = os.path.join(WORK_DIR, "reports_v2")
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)


def save_upload_file(upload_file: UploadFile, prefix: str) -> str:
    """保存上传的文件到临时目录"""
    ext = os.path.splitext(upload_file.filename)[1]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{prefix}_{timestamp}{ext}"
    filepath = os.path.join(UPLOAD_DIR, filename)
    
    with open(filepath, "wb") as f:
        shutil.copyfileobj(upload_file.file, f)
    
    return filepath


# ============================================================
# API 接口 1：健康检查
# ============================================================
@app.get("/api/health")
async def health_check():
    """系统健康检查"""
    return {
        "status": "ok",
        "timestamp": datetime.now().isoformat(),
        "upload_dir": UPLOAD_DIR,
        "report_dir": REPORT_DIR
    }


# ============================================================
# API 接口 2：完整审核（支持 V2/V3 模式选择）
# ============================================================
@app.post("/api/review")
async def review_documents(
    lc_file: UploadFile = File(...),
    invoice_file: UploadFile = File(...),
    bl_file: UploadFile = File(...),
    insurance_file: UploadFile = File(...),
    presentation_date: str = Form(...),
    review_mode: str = Form("v2")  # v2: 快速审核, v3: 深度审核
):
    """
    接收 4 份单据文件 + 交单日期 + 审核模式，返回审核结果
    review_mode: v2 (快速审核) | v3 (深度审核，多智能体)
    """
    print(f"\n{'='*70}")
    print(f"  收到审核请求 - 模式: {review_mode.upper()}")
    print(f"{'='*70}\n")
    try:
        # ============================================================
        # 阶段一：保存上传文件
        # ============================================================
        lc_path = save_upload_file(lc_file, "lc")
        inv_path = save_upload_file(invoice_file, "invoice")
        bl_path = save_upload_file(bl_file, "bl")
        ins_path = save_upload_file(insurance_file, "insurance")

        # ============================================================
        # 阶段二：OCR + AI 提取
        # ============================================================
        steps = []

        # 解析信用证
        steps.append({"step": "解析信用证", "status": "processing"})
        lc_text = extract_text(lc_path)
        lc_data = extract_lc_fields(lc_text)
        if lc_data:
            lc_data["raw_text"] = lc_text
        steps[-1]["status"] = "done"

        # 解析商业发票
        steps.append({"step": "解析商业发票", "status": "processing"})
        inv_text = extract_text(inv_path)
        inv_data = extract_invoice_fields(inv_text)
        if inv_data:
            inv_data["raw_text"] = inv_text
        steps[-1]["status"] = "done"

        # 解析提单
        steps.append({"step": "解析提单", "status": "processing"})
        bl_text = extract_text(bl_path)
        bl_data = extract_bl_fields(bl_text)
        if bl_data:
            bl_data["raw_text"] = bl_text
        steps[-1]["status"] = "done"

        # 解析保险单
        steps.append({"step": "解析保险单", "status": "processing"})
        ins_text = extract_text(ins_path)
        ins_data = extract_insurance_fields(ins_text)
        if ins_data:
            ins_data["raw_text"] = ins_text
        steps[-1]["status"] = "done"

        # 检查是否全部解析成功
        if not all([lc_data, inv_data, bl_data, ins_data]):
            failed = []
            if not lc_data: failed.append("信用证")
            if not inv_data: failed.append("商业发票")
            if not bl_data: failed.append("提单")
            if not ins_data: failed.append("保险单")
            return JSONResponse(
                status_code=400,
                content={
                    "error": f"以下单据解析失败：{', '.join(failed)}",
                    "steps": steps
                }
            )

        # ============================================================
        # 阶段三：审核（根据 review_mode 选择 V2 或 V3）
        # ============================================================
        
        if review_mode == "v3":
            # V3 深度审核：多智能体 + 对比学习
            print("🚀 使用 V3 深度审核（多智能体）...")
            from v3agent import review_documents
            
            steps.append({"step": "多智能体预理解", "status": "processing"})
            v3_result = review_documents(
                lc_data, inv_data, bl_data, ins_data, presentation_date
            )
            steps[-1]["status"] = "done"
            
            all_discrepancies = v3_result.discrepancies
            compliant_items = v3_result.compliant_items
            review_version = "v3_kdr_agent"
            
        else:
            # V2 快速审核：规则引擎 + AI
            print("⚡ 使用 V2 快速审核...")
            
            # 第一层：规则引擎
            steps.append({"step": "规则引擎审核", "status": "processing"})
            rule_discrepancies, compliant_items = check_calculations(
                lc_data, inv_data, bl_data, ins_data, presentation_date
            )
            steps[-1]["status"] = "done"

            # 第二层：AI 全面审核
            steps.append({"step": "AI 全面审核", "status": "processing"})
            ai_discrepancies = ai_full_review(
                lc_data, inv_data, bl_data, ins_data, presentation_date
            )
            steps[-1]["status"] = "done"

            # 第三层：合并去重
            steps.append({"step": "合并去重", "status": "processing"})
            all_discrepancies = merge_discrepancies(rule_discrepancies, ai_discrepancies)
            steps[-1]["status"] = "done"
            
            review_version = "v2_standard"

        # ============================================================
        # 阶段四：整理返回结果
        # ============================================================

        # 统计严重程度
        severity_count = {"严重": 0, "一般": 0, "轻微": 0}
        for d in all_discrepancies:
            sev = d.get("severity", "一般")
            if sev in severity_count:
                severity_count[sev] += 1

        # 生成审核建议
        if not all_discrepancies:
            conclusion = "所有单据与信用证条款完全相符，建议承付。"
        elif severity_count["严重"] > 0:
            conclusion = "单据存在严重不符点，建议拒绝承付或联系申请人。"
        else:
            conclusion = "单据存在轻微不符点，建议联系申请人确认是否接受。"

        # 生成报告文本
        report_lines = []
        report_lines.append("=" * 70)
        report_lines.append("          信用证单据审核报告")
        report_lines.append("=" * 70)
        report_lines.append(f"  信用证号：{lc_data.get('lc_number', 'N/A')}")
        report_lines.append(f"  信用证金额：{lc_data.get('currency', '')} {lc_data.get('amount', 0):,.2f}")
        report_lines.append(f"  审核日期：{datetime.now().strftime('%Y-%m-%d %H:%M')}")
        report_lines.append(f"  交单日期：{presentation_date}")
        report_lines.append("")

        if all_discrepancies:
            report_lines.append(f"  ⚠️ 发现 {len(all_discrepancies)} 处不符点")
            for i, d in enumerate(all_discrepancies, 1):
                report_lines.append("-" * 70)
                report_lines.append(f"  不符点 #{i}")
                report_lines.append(f"  涉及单据：{d.get('document', '')}")
                report_lines.append(f"  不符字段：{d.get('field', '')}")
                if d.get('lc_requirement'):
                    report_lines.append(f"  信用证要求：{d.get('lc_requirement', '')}")
                if d.get('doc_shows'):
                    report_lines.append(f"  单据显示：{d.get('doc_shows', '')}")
                report_lines.append(f"  差异说明：{d.get('description', '')}")
                report_lines.append(f"  依据条款：{d.get('ucp_reference', '')}")
                report_lines.append(f"  严重程度：{d.get('severity', '')}")
                report_lines.append("")
        else:
            report_lines.append("  ✅ 所有单据相符")

        report_lines.append("-" * 70)
        report_lines.append(f"  审核结论：{conclusion}")
        report_lines.append("=" * 70)
        report_text = "\n".join(report_lines)

        # 保存报告
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"report_{timestamp}.txt"
        report_path = os.path.join(REPORT_DIR, report_filename)
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report_text)

        # 返回 JSON
        return {
            "success": True,
            "review_mode": review_mode,
            "review_version": review_version,
            "summary": {
                "lc_number": lc_data.get("lc_number", "N/A"),
                "lc_amount": f"{lc_data.get('currency', '')} {lc_data.get('amount', 0):,.2f}",
                "total_discrepancies": len(all_discrepancies),
                "severity_count": severity_count,
                "conclusion": conclusion,
                "review_time": datetime.now().isoformat()
            },
            "discrepancies": all_discrepancies,
            "compliant_items": compliant_items,
            "extracted_fields": {
                "letter_of_credit": {k: v for k, v in lc_data.items() if k != "raw_text"},
                "commercial_invoice": {k: v for k, v in inv_data.items() if k != "raw_text"},
                "bill_of_lading": {k: v for k, v in bl_data.items() if k != "raw_text"},
                "insurance_policy": {k: v for k, v in ins_data.items() if k != "raw_text"}
            },
            "report_text": report_text,
            "report_download": f"/api/download/{report_filename}",
            "steps": steps
        }

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"审核过程中出错：{str(e)}"}
        )
    finally:
        # 清理上传的临时文件
        for path in [lc_path, inv_path, bl_path, ins_path]:
            if os.path.exists(path):
                os.remove(path)


# ============================================================
# API 接口 3：下载报告
# ============================================================
@app.get("/api/download/{filename}")
async def download_report(filename: str):
    """下载审核报告"""
    filepath = os.path.join(REPORT_DIR, filename)
    if os.path.exists(filepath):
        return FileResponse(
            filepath,
            media_type="text/plain",
            filename=filename
        )
    return JSONResponse(status_code=404, content={"error": "报告不存在"})


# ============================================================
# 托管前端静态文件
# ============================================================
FRONTEND_DIR = os.path.join(WORK_DIR, "app", "dist")
if os.path.exists(FRONTEND_DIR):
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")


# ============================================================
# 启动
# ============================================================
if __name__ == "__main__":
    import uvicorn
    print("=" * 70)
    print("  信用证智能审单系统 — 后端服务启动")
    print("=" * 70)
    print(f"  工作目录：{WORK_DIR}")
    print(f"  前端目录：{FRONTEND_DIR}")
    print(f"  API 文档：http://0.0.0.0:7860/docs")
    print(f"  系统地址：http://0.0.0.0:7860")
    print("=" * 70)
    uvicorn.run(app, host="0.0.0.0", port=7860)