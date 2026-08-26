from fastapi import APIRouter, File, UploadFile, HTTPException, Request
from fastapi.responses import Response
from app.parsers import parse_document
from app.audit_engine import audit_document
from app.models import AuditReport
from app.config import MAX_FILE_SIZE, ALLOWED_EXTENSIONS
from app.report_generator import generate_pdf_report, generate_excel_report, generate_json_report
from slowapi import Limiter
from slowapi.util import get_remote_address

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

latest_report = {}

def allowed_file(filename: str) -> bool:
    ext = filename.split(".")[-1].lower()
    return ext in ALLOWED_EXTENSIONS

@router.post("/upload", response_model=AuditReport)
@limiter.limit("10/minute")
async def upload_file(request: Request, file: UploadFile = File(...)):
    if not allowed_file(file.filename):
        raise HTTPException(
            status_code=400,
            detail="File type not allowed. Supported: PDF, Word, Excel, TXT"
        )

    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Max size: {MAX_FILE_SIZE // 1024 // 1024}MB"
        )

    try:
        text = parse_document(file.filename, content)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Parsing error: {str(e)}")

    try:
        result = await audit_document(text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Audit failed: {str(e)}")

    global latest_report
    latest_report = {
        "filename": file.filename,
        "risk_score": result.get("risk_score", 0),
        "findings": result.get("findings", []),
        "key_terms": result.get("key_terms", {}),
        "red_flags": result.get("red_flags", [])
    }

    return AuditReport(**latest_report)

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
