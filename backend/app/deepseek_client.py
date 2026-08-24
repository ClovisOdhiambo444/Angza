import httpx
from app.config import (
    LLM_PROVIDER,
    OPENROUTER_API_KEY, OPENROUTER_BASE_URL, OPENROUTER_MODEL,
    GROQ_API_KEY, GROQ_BASE_URL, GROQ_MODEL,
    GEMINI_API_KEY, GEMINI_BASE_URL, GEMINI_MODEL
)

async def ask_llm(prompt: str, temperature: float = 0.1) -> str:
    if LLM_PROVIDER == "openrouter":
        return await ask_openrouter(prompt, temperature)
    elif LLM_PROVIDER == "groq":
        return await ask_groq(prompt, temperature)
    elif LLM_PROVIDER == "gemini":
        return await ask_gemini(prompt, temperature)
    else:
        raise ValueError(f"Unsupported LLM provider: {LLM_PROVIDER}")

async def ask_openrouter(prompt: str, temperature: float = 0.1) -> str:
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": OPENROUTER_MODEL,
        "messages": [
            {"role": "system", "content": "You are a precise, no-hallucination contract auditor."},
            {"role": "user", "content": prompt}
        ],
        "temperature": temperature,
        "max_tokens": 4096,  # Limit response length to stay within free tier
    }
    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(f"{OPENROUTER_BASE_URL}/chat/completions", json=payload, headers=headers)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

async def ask_groq(prompt: str, temperature: float = 0.1) -> str:
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": "You are a precise, no-hallucination contract auditor."},
            {"role": "user", "content": prompt}
        ],
        "temperature": temperature,
    }
    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(f"{GROQ_BASE_URL}/chat/completions", json=payload, headers=headers)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

async def ask_gemini(prompt: str, temperature: float = 0.1) -> str:
    headers = {
        "x-goog-api-key": GEMINI_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "model": GEMINI_MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": temperature,
    }
    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(f"{GEMINI_BASE_URL}/chat/completions", json=payload, headers=headers)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
