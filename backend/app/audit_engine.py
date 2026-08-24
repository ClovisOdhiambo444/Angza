import json
import re
from app.deepseek_client import ask_llm

# Limit document text to 50,000 characters to avoid token overflow
MAX_PROMPT_CHARS = 50000

AUDIT_PROMPT_TEMPLATE = """
You are a senior contract auditor. Analyze the following document text and return a JSON object with:

- "risk_score": integer 0-100 (higher = more risky)
- "findings": list of objects, each with:
    - "clause": brief description of the clause/area
    - "issue": what is wrong
    - "recommendation": how to fix it
    - "severity": integer 0-100
- "key_terms": dict with keys: "parties", "payment_terms", "termination", "liability_cap", "governing_law"
- "red_flags": list of critical red flags (strings)

Document text:
{text}

Return ONLY valid JSON. No extra text.
"""

async def audit_document(text: str) -> dict:
    # Truncate text to safe length
    truncated = text[:MAX_PROMPT_CHARS]
    prompt = AUDIT_PROMPT_TEMPLATE.format(text=truncated)
    raw = await ask_llm(prompt)
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        match = re.search(r'\{.*\}', raw, re.DOTALL)
        if match:
            return json.loads(match.group())
        raise ValueError("Could not parse LLM response as JSON")
