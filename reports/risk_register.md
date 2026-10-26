# Risk Register

| ID | Risk | Likelihood | Impact | Control | Residual risk | Owner |
|---|---|---|---|---|---|---|
| R1 | Prompt injection overrides assistant behaviour | High | Medium | Input filter, hardened system prompt, tool authorisation | Medium (filter bypass possible) | Developer |
| R2 | Poisoned uploaded document hijacks the agent | Medium | High | Chunk sanitiser, untrusted-data wrapping, human approval on email | Low-Medium | Developer |
| R3 | Staff/confidential data leaks to students | Medium | High | Role-based retrieval access control, output redaction | Low | Developer |
| R4 | Agent sends data to external address | Medium | High | Domain allow-list, human approval | Low | Developer |
| R5 | Student reads another student's grades | High | High | Own-record-only tool policy | Low | Developer |
| R6 | Abuse / denial of wallet via request flooding | Medium | Medium | Per-user rate limit, monitoring | Medium | Operations |
| R7 | Attacks go unnoticed | Medium | Medium | Event logging, detection rules, dashboard | Low-Medium | Security |

Review: after every model or prompt change, re-run `python attacks/run_attacks.py`.
