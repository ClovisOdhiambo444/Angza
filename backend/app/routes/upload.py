from fastapi import APIRouter, File, UploadFile, HTTPException, Response
from app.parsers import parse_document
from app.audit_engine import audit_document
from app.models import AuditReport
from app.config import MAX_FILE_SIZE
from app.report_generator import generate_pdf_report, generate_excel_report, generate_json_report
import json

router = APIRouter()

# Store the latest report in memory (for download)
latest_report = {}

@router.post("/upload", response_model=AuditReport)
async def upload_file(file: UploadFile = File(...)):
    global latest_report
    
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File too large")

    try:
        text = parse_document(file.filename, content)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Parsing error: {str(e)}")

    try:
        result = await audit_document(text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Audit failed: {str(e)}")

    # Store the report for download
    latest_report = {
        "filename": file.filename,
        "risk_score": result.get("risk_score", 0),
        "findings": result.get("findings", []),
        "key_terms": result.get("key_terms", {}),
        "red_flags": result.get("red_flags", [])
    }

    report = AuditReport(**latest_report)
    return report

@router.get("/report/pdf")
async def download_pdf():
    if not latest_report:
        raise HTTPException(status_code=404, detail="No report available. Please upload a document first.")
    
    pdf_bytes = generate_pdf_report(latest_report)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=angza_report_{latest_report.get('filename', 'document')}.pdf"}
    )

@router.get("/report/excel")
async def download_excel():
    if not latest_report:
        raise HTTPException(status_code=404, detail="No report available. Please upload a document first.")
    
    excel_bytes = generate_excel_report(latest_report)
    return Response(
        content=excel_bytes,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename=angza_report_{latest_report.get('filename', 'document')}.xlsx"}
    )

@router.get("/report/json")
async def download_json():
    if not latest_report:
        raise HTTPException(status_code=404, detail="No report available. Please upload a document first.")
    
    json_bytes = generate_json_report(latest_report)
    return Response(
        content=json_bytes,
        media_type="application/json",
        headers={"Content-Disposition": f"attachment; filename=angza_report_{latest_report.get('filename', 'document')}.json"}
    )
