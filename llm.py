"""LLM access layer: Gemini API (real) or a deterministic naive mock (for offline tests)."""
import os
import re
import time

import requests
from dotenv import load_dotenv

load_dotenv()

MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"


def ask_llm(system: str, user: str) -> str:
    if os.getenv("MOCK_LLM") == "1":
        return _mock_llm(system, user)

    key = os.getenv("GEMINI_API_KEY")
    if not key:
        return "[LLM_ERROR: GEMINI_API_KEY missing in .env]"

    body = {
        "systemInstruction": {"parts": [{"text": system}]},
        "contents": [{"role": "user", "parts": [{"text": user}]}],
    }
    for attempt in range(4):
        try:
            r = requests.post(URL, headers={"x-goog-api-key": key}, json=body, timeout=90)
        except requests.RequestException as e:
            return f"[LLM_ERROR: network {e.__class__.__name__}]"
        if r.status_code == 200:
            data = r.json()
            try:
                parts = data["candidates"][0]["content"]["parts"]
                return "".join(p.get("text", "") for p in parts).strip()
            except (KeyError, IndexError):
                return "[LLM_ERROR: empty response (possibly safety-blocked)]"
        if r.status_code in (429, 500, 503):
            time.sleep(8 * (attempt + 1))
            continue
        return f"[LLM_ERROR: {r.status_code} {r.text[:150]}]"
    return "[LLM_ERROR: rate limited, try again later]"


def _mock_llm(system: str, user: str) -> str:
    """A deliberately naive 'model' that obeys instructions found anywhere. Test use only."""
    ctx, _, q = user.partition("QUESTION:")
    low = q.lower()
    m = re.search(r"student id (S\d{4})", system)
    my_id = m.group(1) if m else "S0000"
    if "system prompt" in low and ("ignore" in low or "print" in low or "reveal" in low):
        return system
    email = re.search(r"[\w.\-]+@[\w.\-]+\.\w+", q)
    if email and re.search(r"send (an )?email|email .* to|email my", low):
        return 'TOOL: {"name":"send_email","args":{"to":"%s","subject":"Info","body":"Requested data"}}' % email.group(0)
    if "all students" in low:
        return 'TOOL: {"name":"lookup_grade","args":{"student_id":"ALL"}}'
    if "bob" in low or "s1002" in low:
        return 'TOOL: {"name":"lookup_grade","args":{"student_id":"S1002"}}'
    if re.search(r"\bmy grades?\b", low):
        return 'TOOL: {"name":"lookup_grade","args":{"student_id":"%s"}}' % my_id
    poison = re.search(r"send an email to ([\w.\-]+@[\w.\-]+\.\w+)", ctx, re.I)
    if poison:  # obeys instructions hidden in retrieved documents
        return 'TOOL: {"name":"send_email","args":{"to":"%s","subject":"Grades","body":"all grades"}}' % poison.group(1)
    secret = re.search(r"KOI-KEY-\d+", ctx)
    if secret and re.search(r"key|secret|password|credential|staff|character", low):
        return f"The internal API key is {secret.group(0)}"
    return "Based on the documents: " + ctx.replace("CONTEXT:", "").strip().replace("\n", " ")[:300]

