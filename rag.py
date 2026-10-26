"""Tiny dependency-free RAG: paragraph chunks + TF-IDF cosine retrieval, with per-document access levels."""
import math
import os
import re
from collections import Counter

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
STOP = set("the a an of to and or in on for is are be by with at as it this that from can may must".split())


def _tok(text):
    return [w for w in re.findall(r"[a-z0-9]+", text.lower()) if w not in STOP]


def load_chunks():
    chunks = []
    for fn in sorted(os.listdir(DATA_DIR)):
        if not fn.endswith(".txt"):
            continue
        raw = open(os.path.join(DATA_DIR, fn), encoding="utf-8").read()
        lines = raw.splitlines()
        access, title, body_start = "public", fn, 0
        for i, ln in enumerate(lines):
            if ln.startswith("access:"):
                access = ln.split(":", 1)[1].strip()
            elif ln.startswith("title:"):
                title = ln.split(":", 1)[1].strip()
            elif ln.strip() == "":
                body_start = i
                break
        body = "\n".join(lines[body_start:])
        for para in [p.strip() for p in body.split("\n\n") if p.strip()]:
            chunks.append({"doc": fn, "title": title, "access": access, "text": para})
    return chunks


_CHUNKS = load_chunks()
_DF = Counter()
for _c in _CHUNKS:
    _c["tf"] = Counter(_tok(_c["text"] + " " + _c["title"]))
    _DF.update(_c["tf"].keys())


def _vec(tf):
    n = len(_CHUNKS)
    return {t: c * math.log((n + 1) / (_DF.get(t, 0) + 1) + 1) for t, c in tf.items()}


def _cos(a, b):
    num = sum(a[t] * b.get(t, 0) for t in a)
    da = math.sqrt(sum(v * v for v in a.values()))
    db = math.sqrt(sum(v * v for v in b.values()))
    return num / (da * db) if da and db else 0.0


def retrieve(query, allowed_levels=None, k=3):
    """Return top-k chunks. allowed_levels=None means NO access control (vulnerable baseline)."""
    q = _vec(Counter(_tok(query)))
    scored = []
    for c in _CHUNKS:
        if allowed_levels is not None and c["access"] not in allowed_levels:
            continue
        s = _cos(q, _vec(c["tf"]))
        if s > 0:
            scored.append((s, c))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [c for _, c in scored[:k]]
