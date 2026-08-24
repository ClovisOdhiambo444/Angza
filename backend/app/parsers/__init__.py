from .pdf_parser import parse_pdf
from .docx_parser import parse_docx
from .excel_parser import parse_excel
from .text_parser import parse_text

def parse_document(filename: str, content: bytes) -> str:
    ext = filename.split('.')[-1].lower()
    if ext == 'pdf':
        return parse_pdf(content)
    elif ext in ('doc', 'docx'):
        return parse_docx(content)
    elif ext in ('xls', 'xlsx'):
        return parse_excel(content)
    elif ext == 'txt':
        return parse_text(content)
    else:
        raise ValueError(f"Unsupported file type: {ext}")
