from pydantic import BaseModel
from typing import List, Optional

class Finding(BaseModel):
    clause: str
    issue: str
    recommendation: str
    severity: int

class AuditReport(BaseModel):
    filename: str
    risk_score: int
    findings: List[Finding]
    key_terms: dict
    red_flags: List[str]
