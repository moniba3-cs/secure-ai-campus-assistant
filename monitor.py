"""Security monitoring: JSONL event log, detection rules and dashboard summary."""
import json
import os
import time
from collections import Counter

LOG_DIR = os.path.join(os.path.dirname(__file__), "logs")
os.makedirs(LOG_DIR, exist_ok=True)
EVENTS = os.path.join(LOG_DIR, "events.jsonl")

SEVERITY = {"info": 0, "medium": 1, "high": 2}
RATE_LIMIT = int(os.getenv("RATE_LIMIT", "15"))  # requests per user per 60 s


def log_event(etype, user, mode, severity="info", **details):
    ev = {"ts": time.time(), "type": etype, "user": user, "mode": mode, "severity": severity, "details": details}
    with open(EVENTS, "a", encoding="utf-8") as f:
        f.write(json.dumps(ev) + "\n")
    return ev


def read_events(limit=None):
    if not os.path.exists(EVENTS):
        return []
    evs = [json.loads(l) for l in open(EVENTS, encoding="utf-8") if l.strip()]
    return evs[-limit:] if limit else evs


def rate_exceeded(user, mode="secure"):
    now = time.time()
    recent = [e for e in read_events(200) if e["user"] == user and e["mode"] == mode and e["type"] == "chat_request" and now - e["ts"] < 60]
    return len(recent) >= RATE_LIMIT


def summary():
    evs = read_events()
    by_type = Counter(e["type"] for e in evs)
    alerts = [e for e in evs if SEVERITY.get(e["severity"], 0) >= 1]
    by_user = Counter(e["user"] for e in alerts)
    return {"total": len(evs), "by_type": dict(by_type), "alerts": len(alerts),
            "alerts_by_user": dict(by_user), "recent_alerts": alerts[-15:][::-1]}


def reset_logs():
    for fn in ("events.jsonl", "outbox.jsonl"):
        p = os.path.join(LOG_DIR, fn)
        if os.path.exists(p):
            os.remove(p)
