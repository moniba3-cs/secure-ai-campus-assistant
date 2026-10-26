# Text to add to your CV (replace X and Y with the numbers from reports/before_after.md)

## Heading: Projects  (or: AI Security Projects)

**Secure AI Campus Assistant - RAG Chatbot with Tool-Using Agent** | Python, Flask, Gemini API, OWASP LLM Top 10, NIST AI RMF | GitHub: github.com/<your-username>/secure-ai-campus-assistant
- Built a retrieval-augmented campus assistant with a tool-using agent (grade lookup, email) and a role-based user model.
- Red-teamed it with 10 attack types (prompt injection, indirect injection via poisoned documents, secret leakage, cross-user access, excessive agency); baseline attack success was X%.
- Implemented layered controls: role-based retrieval access control, input filtering, retrieved-text sanitisation, per-role tool authorisation with human approval, and output redaction; reduced attack success to Y% on retest.
- Added security monitoring (event logging, detection rules, dashboard) and mapped risks and controls to OWASP Top 10 for LLM Applications and NIST AI RMF with a risk register.

## One-line version (for tight CVs)
Built and red-teamed a RAG + agent campus assistant; cut attack success from X% to Y% using access control, tool authorisation, guardrails and monitoring; mapped to OWASP LLM Top 10 and NIST AI RMF.

## Email sentence for professors
I recently built and security-tested an AI campus assistant (RAG + agent), measuring prompt-injection and data-leakage attack success before and after adding controls; the project is on my GitHub: <link>.
