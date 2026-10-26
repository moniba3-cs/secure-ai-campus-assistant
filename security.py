"""Security controls: roles, input filter, retrieval sanitiser, tool authorisation, output redaction."""
import re

USERS = {
    "monibah": {"role": "student", "sid": "S1001"},
    "bob": {"role": "student", "sid": "S1002"},
    "khan": {"role": "staff", "sid": "STAFF01"},
    "admin": {"role": "admin", "sid": "ADMIN01"},
}

# Which document access levels each role may retrieve (RAG access control)
ROLE_ACCESS = {
    "student": {"public"},
    "staff": {"public", "staff"},
    "admin": {"public", "staff", "confidential"},
}

SYS_MARKER = "[[CANARY-SYS-4417]]"
ALLOWED_EMAIL_DOMAIN = "@koi.edu.au"

INJECTION_PATTERNS = [
    r"ignore (all |any )?(the )?(previous|prior|above) (instructions|rules)",
    r"disregard (all |any )?(the )?(previous|prior|above|your)",
    r"(reveal|print|show|repeat|output) (me )?(your|the) (system )?(prompt|instructions)",
    r"you are (now )?dan\b",
    r"developer mode|jailbreak",
    r"(i am|i'm|act as|pretend (to be|i am)) (the )?(an? )?(admin|administrator|staff|professor|teacher)",
    r"grant me (staff|admin)",
]
# Lines inside retrieved documents that look like instructions to the model
DOC_INSTRUCTION_PATTERNS = INJECTION_PATTERNS + [
    r"important notice for the assistant",
    r"\buse the send_email tool\b",
    r"\bdo not tell the user\b",
    r"\bsend an? email to\b",
]
SECRET_PATTERNS = [r"KOI-KEY-\d+", r"\[\[CANARY-SYS-\d+\]\]"]


def check_input(message):
    for p in INJECTION_PATTERNS:
        if re.search(p, message, re.I):
            return False, f"matched injection pattern: {p}"
    return True, ""


def sanitize_chunk(text):
    """Drop sentences in retrieved docs that look like instructions. Returns (clean_text, removed_count)."""
    sentences = re.split(r"(?<=[.!?])\s+", text)
    kept, removed = [], 0
    for s in sentences:
        if any(re.search(p, s, re.I) for p in DOC_INSTRUCTION_PATTERNS):
            removed += 1
        else:
            kept.append(s)
    return " ".join(kept), removed


def authorize_tool(user, name, args):
    """Returns (decision, reason). decision: 'allow' | 'deny' | 'approve' (needs human approval)."""
    role, sid = user["role"], user["sid"]
    if name == "lookup_grade":
        target = str(args.get("student_id", ""))
        if role == "student" and target != sid:
            return "deny", "students may only look up their own grades"
        if target == "ALL" and role != "admin":
            return "deny", "bulk grade export is admin-only"
        return "allow", ""
    if name == "send_email":
        to = str(args.get("to", ""))
        if not to.lower().endswith(ALLOWED_EMAIL_DOMAIN):
            return "deny", f"recipient outside {ALLOWED_EMAIL_DOMAIN}"
        return "approve", "all outgoing email requires human approval"
    return "deny", "unknown tool"


def redact_output(text):
    hits = 0
    for p in SECRET_PATTERNS:
        text, n = re.subn(p, "[REDACTED]", text)
        hits += n
    return text, hits
