# Governance Mapping

## OWASP Top 10 for LLM Applications (2025) -> risks, attacks, controls

| OWASP ID | Risk | Attack in this project | Control implemented | File |
|---|---|---|---|---|
| LLM01 | Prompt Injection | A01, A03, A09 | Input pattern filter; untrusted-data prompt design | security.py, assistant.py |
| LLM01 | Indirect Prompt Injection | A06 (poisoned upload) | Retrieved-text sanitiser strips instruction-like sentences; documents wrapped as untrusted data | security.py |
| LLM02 | Sensitive Information Disclosure | A02, A10 | Role-based retrieval access control; output redaction of secrets | rag.py, security.py |
| LLM06 | Excessive Agency | A04, A05, A07, A08 | Per-role tool authorisation, recipient domain allow-list, human approval for email | security.py, tools.py |
| LLM07 | System Prompt Leakage | A01 | Input filter + output redaction of internal marker | security.py |
| LLM08 | Vector and Embedding Weaknesses | A02, A06 | Access levels on every chunk, filtered before the model sees them | rag.py |
| LLM10 | Unbounded Consumption | (not attacked) | Per-user rate limit | monitor.py |

## NIST AI RMF functions

| Function | How this project addresses it |
|---|---|
| GOVERN | Roles and access levels defined (security.py); human approval policy for high-impact actions; risk register owner and review cadence |
| MAP | System context, users, data classes and threat model documented; attack catalogue A01-A10 |
| MEASURE | Repeatable attack suite with success-rate metrics before/after controls (reports/before_after.md); detection rules and dashboard |
| MANAGE | Layered controls, residual-risk tracking, monitoring alerts, retest after each change |

## Honest limitations
- Regex input filters are easy to bypass with paraphrasing; they are a cheap first layer only.
- The real protection is deterministic: retrieval access control, tool authorisation and human approval.
- Results depend on the LLM used and on only 10 attack types; this is not a full security assessment.
- Data and email are simulated; nothing real is sent.
