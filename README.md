# Secure AI Campus Assistant

A RAG chatbot with a tool-using agent that is **attacked, hardened, monitored and governed** - one project covering AI red teaming, secure RAG, secure agents, AI security monitoring and AI governance.

> Data is fictional and emails are simulated (written to `logs/outbox.jsonl`). Nothing real is sent.

## What it does
- Answers questions from campus documents (handbook, fees, internships, staff policy, confidential cases).
- Agent tools: `lookup_grade`, `send_email`.
- Two modes: **vulnerable** (naive baseline) and **secure** (all controls on), switchable in the UI and API.

## Architecture
```
user -> [input filter] -> [role-based retrieval] -> [chunk sanitiser] -> LLM (Gemini)
     -> [tool authorisation + human approval] -> [output redaction] -> answer
        every step -> monitor.py (JSONL events, detection rules, dashboard)
```
| File | Purpose |
|---|---|
| `app.py` | Flask UI, `/api/chat`, `/dashboard`, email approval |
| `assistant.py` | Chat pipeline (vulnerable vs secure) |
| `rag.py` | TF-IDF retrieval with per-document access levels |
| `tools.py` | Agent tools (simulated email, fake grades) |
| `security.py` | Roles, input filter, sanitiser, tool policy, redaction |
| `monitor.py` | Logging, detection rules, rate limit, summary |
| `llm.py` | Gemini API client (plus offline mock for tests) |
| `attacks/run_attacks.py` | 10-attack red-team suite, before/after report |
| `reports/` | Results, OWASP/NIST mapping, risk register |

## Setup
```bash
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
copy .env.example .env         # then put your Gemini API key in .env
python app.py                  # http://127.0.0.1:5000
```

## Run the red-team suite
```bash
python attacks/run_attacks.py --runs 3
```
Creates `reports/attack_results.json` and `reports/before_after.md`.

## Attacks (A01-A10)
Direct prompt injection, secret leakage via RAG, role-play jailbreak, cross-user data access, bulk data dump, poisoned document (indirect injection), unauthorised external email, excessive agency, privilege impersonation, obfuscated extraction.

## Controls
1. **Role-based retrieval access control** - students never see staff/confidential chunks.
2. **Input filter** - blocks common injection phrasing (weak alone, cheap first layer).
3. **Retrieved-text sanitiser** - removes instruction-like sentences from documents; documents treated as untrusted data.
4. **Tool authorisation** - students can only read their own grades; email only to `@koi.edu.au` and only after human approval.
5. **Output redaction** - secrets and internal markers removed.
6. **Monitoring** - events, alerts, rate limit and dashboard.

## Results
<!-- Paste the table from reports/before_after.md here -->
Baseline attack success: **X%** -> hardened: **Y%** (Gemini, N runs per attack).

## Screenshots
<!-- Add: chat UI, dashboard with alerts, before_after.md table -->

## Governance
See `reports/governance_mapping.md` (OWASP LLM Top 10 2025, NIST AI RMF) and `reports/risk_register.md`.

## Limitations
Regex filters can be bypassed; the strong controls are access control, tool policy and human approval. Only 10 attack types were tested, and results depend on the model. Not a full security assessment.
