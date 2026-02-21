# Appendix A: AI Security Cheat Sheet

## Top 10 Threats and Mitigations

| # | Threat | What It Is | Primary Mitigation | Chapter |
|---|---|---|---|---|
| 1 | Prompt Injection (Direct) | Attacker overrides system instructions via user input | Input validation + sandwich defense + structured output | Ch 4 |
| 2 | Prompt Injection (Indirect) | Malicious instructions hidden in external data (RAG, web, email) | Document sanitization + privilege separation | Ch 4 |
| 3 | Jailbreak / Guardrail Bypass | Attacker bypasses model safety training | Layered guardrails (input classifier + output classifier + monitoring) | Ch 5 |
| 4 | System Prompt Extraction | Attacker reveals hidden instructions | Treat prompts as public, output leak detection, no secrets in prompts | Ch 5 |
| 5 | Data Leakage (Training Data) | Model outputs memorized PII or sensitive data | Output PII scanning + redaction | Ch 6 |
| 6 | Data Leakage (Context) | PII from RAG documents or user input exposed | PII scanning on input + output, access-controlled RAG | Ch 6 |
| 7 | Excessive Agency | AI takes unauthorized actions via tools/APIs | Least privilege, human-in-the-loop, plan validation | Ch 7 |
| 8 | Supply Chain (Models) | Backdoored or malicious model files | Verified sources, safetensors format, hash verification | Ch 8 |
| 9 | Supply Chain (Dependencies) | Vulnerable or compromised ML libraries | Pin versions, vulnerability scanning, private package index | Ch 8 |
| 10 | Denial of Wallet | Attacker causes excessive API costs | Per-user rate limiting, budget caps, token limits | Ch 7 |

## Architecture Decision Checklist

Before deploying any AI system, answer these 10 questions:

| # | Question | Your Answer |
|---|---|---|
| 1 | What data does the AI process, and what's its classification? | |
| 2 | Is the model API-based or self-hosted? If API, what's the data agreement? | |
| 3 | Are there input validation controls before the model? | |
| 4 | Are there output filtering controls after the model? | |
| 5 | Can the AI take actions (tools, APIs, databases)? If yes, what's the authorization model? | |
| 6 | Is there tenant/user data isolation in RAG and storage? | |
| 7 | Are all model sources verified and model files integrity-checked? | |
| 8 | Is there rate limiting (requests, tokens, cost) per user? | |
| 9 | Are all AI interactions logged with security-relevant metadata? | |
| 10 | Is there a plan for incident response specific to AI threats? | |

**Scoring:** If you answered "no" or "don't know" to 3+ questions, your AI system needs a security review before production.

## Defense Layers Quick Reference

```
LAYER 1: INPUT VALIDATION        Regex, length limits, PII scan
         |                        Catches: ~20% of basic attacks
         v
LAYER 2: INPUT CLASSIFIER        ML model for injection detection
         |                        Catches: ~60% of injection attempts
         v
LAYER 3: SYSTEM PROMPT           Hardened, specific, sandwich defense
         |                        Reduces: instruction override success
         v
LAYER 4: MODEL SAFETY            Provider's built-in RLHF alignment
         |                        Varies by model and version
         v
LAYER 5: STRUCTURED OUTPUT       JSON schema, enum validation
         |                        Constrains: what the model can produce
         v
LAYER 6: OUTPUT FILTER           PII redaction, content safety, leak detection
         |                        Catches: leakage the model missed
         v
LAYER 7: AUTHORIZATION           Least privilege, plan validation, tool sandbox
         |                        Prevents: unauthorized actions
         v
LAYER 8: HUMAN-IN-THE-LOOP      Approval gate for high-risk actions
         |                        Prevents: catastrophic outcomes
         v
LAYER 9: MONITORING              Logging, alerting, anomaly detection
                                  Detects: everything that slipped through
```

## Reference Architecture Selection

| Your Scenario | Use Pattern | Chapter |
|---|---|---|
| Multiple apps calling LLM APIs | Pattern 1: LLM API Gateway | Ch 9 |
| Knowledge base / document Q&A | Pattern 2: Secure RAG Pipeline | Ch 9 |
| AI that calls tools, APIs, or databases | Pattern 3: Secure AI Agent | Ch 9 |
| Multiple models, specialist routing | Pattern 4: Multi-Model Orchestration | Ch 9 |

## Risk Assessment Quick Scoring

For any AI system, score these factors:

| Factor | Low Risk (1 pt) | Medium Risk (2 pts) | High Risk (3 pts) |
|---|---|---|---|
| Data sensitivity | Public data | Internal data | PII / confidential |
| Action capability | Read-only responses | Read data access | Write / execute actions |
| User base | Internal, small | Internal, large | External / public |
| Regulatory scope | None | General (SOC 2) | Industry-specific (HIPAA, etc.) |
| Model hosting | Self-hosted | API with data agreement | API, unknown data handling |

**Total 5-8:** Low risk — baseline controls.
**Total 9-12:** Medium risk — enhanced controls + monitoring.
**Total 13-15:** High risk — full architecture + red teaming + human oversight.
