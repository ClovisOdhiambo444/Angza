import json
import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import pandas as pd

def generate_pdf_report(data: dict) -> bytes:
    """Generate a PDF audit report."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=24,
        alignment=TA_CENTER,
        spaceAfter=20,
        textColor=colors.HexColor('#1E1B4B')
    )
    
    heading_style = ParagraphStyle(
        'HeadingStyle',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=10,
        textColor=colors.HexColor('#2563EB')
    )
    
    normal_style = ParagraphStyle(
        'NormalStyle',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=6,
        alignment=TA_LEFT
    )
    
    story = []
    
    # Title
    story.append(Paragraph("Angza Audit Report", title_style))
    story.append(Spacer(1, 0.2 * inch))
    
    # Filename
    story.append(Paragraph(f"<b>Filename:</b> {data.get('filename', 'N/A')}", normal_style))
    story.append(Spacer(1, 0.1 * inch))
    
    # Risk Score
    risk = data.get('risk_score', 0)
    risk_color = 'green'
    if risk > 70:
        risk_color = 'red'
    elif risk > 40:
        risk_color = 'orange'
    story.append(Paragraph(f"<b>Risk Score:</b> <font color='{risk_color}'>{risk}/100</font>", normal_style))
    story.append(Spacer(1, 0.2 * inch))
    
    # Key Terms
    story.append(Paragraph("Key Terms", heading_style))
    key_terms = data.get('key_terms', {})
    for key, value in key_terms.items():
        if value:
            story.append(Paragraph(f"<b>{key.replace('_', ' ').title()}:</b> {value}", normal_style))
    story.append(Spacer(1, 0.2 * inch))
    
    # Findings
    story.append(Paragraph("Findings", heading_style))
    findings = data.get('findings', [])
    if findings:
        for i, f in enumerate(findings, 1):
            severity_color = 'red' if f.get('severity', 0) > 70 else 'orange' if f.get('severity', 0) > 40 else 'green'
            story.append(Paragraph(f"<b>{i}. {f.get('clause', 'Clause')}</b>", normal_style))
            story.append(Paragraph(f"Issue: {f.get('issue', 'N/A')}", normal_style))
            story.append(Paragraph(f"Recommendation: {f.get('recommendation', 'N/A')}", normal_style))
            story.append(Paragraph(f"<font color='{severity_color}'><b>Severity: {f.get('severity', 0)}/100</b></font>", normal_style))
            story.append(Spacer(1, 0.1 * inch))
    else:
        story.append(Paragraph("No specific findings identified.", normal_style))
    story.append(Spacer(1, 0.2 * inch))
    
    # Red Flags
    story.append(Paragraph("Red Flags", heading_style))
    red_flags = data.get('red_flags', [])
    if red_flags:
        for flag in red_flags:
            story.append(Paragraph(f"• {flag}", normal_style))
    else:
        story.append(Paragraph("No critical red flags detected.", normal_style))
    
    # Build PDF
    doc.build(story)
    return buffer.getvalue()

def generate_excel_report(data: dict) -> bytes:
    """Generate an Excel audit report."""
    buffer = io.BytesIO()
    
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        # Summary sheet
        summary_data = {
            'Metric': ['Filename', 'Risk Score', 'Document Type'],
            'Value': [
                data.get('filename', 'N/A'),
                f"{data.get('risk_score', 0)}/100",
                data.get('doc_type', 'N/A')
            ]
        }
        summary_df = pd.DataFrame(summary_data)
        summary_df.to_excel(writer, sheet_name='Summary', index=False)
        
        # Key Terms sheet
        key_terms = data.get('key_terms', {})
        if key_terms:
            terms_df = pd.DataFrame(list(key_terms.items()), columns=['Term', 'Value'])
            terms_df.to_excel(writer, sheet_name='Key Terms', index=False)
        
        # Findings sheet
        findings = data.get('findings', [])
        if findings:
            findings_df = pd.DataFrame(findings)
            findings_df.to_excel(writer, sheet_name='Findings', index=False)
        
        # Red Flags sheet
        red_flags = data.get('red_flags', [])
        if red_flags:
            flags_df = pd.DataFrame({'Red Flags': red_flags})
            flags_df.to_excel(writer, sheet_name='Red Flags', index=False)
    
    return buffer.getvalue()

def generate_json_report(data: dict) -> bytes:
    """Generate a JSON audit report."""
    return json.dumps(data, indent=2).encode('utf-8')
