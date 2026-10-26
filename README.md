# Secure AI Campus Assistant

A security-focused campus assistant that combines retrieval-augmented generation (RAG), controlled agent tools, and security monitoring. Built with Flask and Gemini, the project demonstrates practical safeguards for AI applications that work with sensitive information.

> All campus records are fictional. Email actions are simulated and written to a local log; no email is sent.

## Project Overview

The assistant answers questions using campus documents and provides a small set of agent actions. The application includes secure and vulnerable-baseline modes to support security testing and comparison.

Key capabilities:
- Document retrieval with role-based access for student, staff, and administrator roles.
- Prompt-injection screening and sanitisation of retrieved document content.
- Authorised tool calls for sample grade lookup and simulated email.
- Human approval workflow for email actions, plus output redaction.
- Security event logging, alerts, rate limiting, and a monitoring dashboard.
- A red-team suite covering ten prompt-injection, data-access, and agent-abuse scenarios.

## Security Design

```text
User request -> input screening -> access-controlled retrieval -> content sanitisation
             -> Gemini -> tool authorisation / approval -> output redaction
             -> security event logging and dashboard
```

The secure mode applies the controls above. The vulnerable mode is an intentionally less-protected baseline for controlled comparison, not a recommended deployment configuration.

## Run Locally

Requirements: Python 3.10+ and a Gemini API key.

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
Copy-Item .env.example .env
```

Add your Gemini API key to `.env`, then start the application:

```powershell
python app.py
```

Open http://127.0.0.1:5000. Keep `.env` private; it is excluded from Git.

## Testing

The application has been manually tested locally with Gemini, and the core workflows were confirmed to run successfully. The included red-team suite exercises ten attack scenarios against both the vulnerable baseline and secure mode. To run it with your configured Gemini key:

```powershell
python attacks/run_attacks.py --runs 3
```

The suite writes detailed results to `reports/attack_results.json` and `reports/before_after.md`. Results depend on the Gemini model and configuration; do not interpret one run as a general security guarantee.

## Project Structure

| File | Purpose |
|---|---|
| `app.py` | Flask chat interface, API, dashboard, and approval route |
| `assistant.py` | Chat and tool-use pipeline |
| `rag.py` | TF-IDF document retrieval |
| `security.py` | Roles, access policy, input checks, sanitisation, and redaction |
| `tools.py` | Fictional grade records and simulated email tool |
| `monitor.py` | Event logging, alerts, rate limiting, and dashboard summary |
| `llm.py` | Gemini API integration |
| `attacks/run_attacks.py` | Red-team test runner |
| `reports/` | Governance mapping, risk register, and test reports |

## Screenshots

![Campus assistant chat interface](docs/screenshots/chat-demo.png)

![Security monitoring dashboard](docs/screenshots/security-dashboard.png)

## Governance and Scope

See [the governance mapping](reports/governance_mapping.md) for OWASP LLM risk and NIST AI RMF references, and [the risk register](reports/risk_register.md) for identified project risks and mitigations.

This is an educational prototype, not a production campus service or a formal security assessment. Its pattern-based input filter can be bypassed, and the test suite covers a limited set of scenarios. Access control, tool authorisation, and human approval provide important additional safeguards but do not eliminate all risk.
