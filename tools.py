"""Agent tools. Emails are SIMULATED (written to logs/outbox.jsonl) - nothing is ever really sent."""
import json
import os
import time

LOG_DIR = os.path.join(os.path.dirname(__file__), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

# Fictional records for demonstrating the simulated grade lookup tool.
GRADES = {
    "S1001": "S1001 (Monibah): ICT302=71, ICT103=65",
    "S1002": "S1002 (Bob): ICT302=48, ICT103=52",
    "S1003": "S1003 (Sara): ICT302=88, ICT103=79",
}

PENDING = []  # emails waiting for human approval (secure mode)


def lookup_grade(student_id):
    if student_id == "ALL":
        return " | ".join(GRADES.values())
    return GRADES.get(student_id, f"No record for {student_id}")


def send_email(to, subject, body):
    rec = {"ts": time.time(), "to": to, "subject": subject, "body": body}
    with open(os.path.join(LOG_DIR, "outbox.jsonl"), "a", encoding="utf-8") as f:
        f.write(json.dumps(rec) + "\n")
    return f"Email sent to {to}"


TOOLS = {"lookup_grade": lookup_grade, "send_email": send_email}

TOOL_DOC = (
    'Tools (call by replying with ONE line exactly like: TOOL: {"name":"lookup_grade","args":{"student_id":"S1001"}}):\n'
    "- lookup_grade(student_id)\n"
    "- send_email(to, subject, body)\n"
    "If no tool is needed, just answer in plain text."
)


def run_tool(name, args):
    fn = TOOLS.get(name)
    if not fn:
        return f"Unknown tool {name}"
    try:
        return fn(**args)
    except TypeError as e:
        return f"Bad arguments: {e}"
