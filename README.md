# AI Security Architecture

A practical guide to securing LLM-powered systems. Covers the AI threat landscape, attack techniques, secure design patterns, and reference architectures — written for security professionals, developers, and architects. No PhD required.

## Who This Is For

- **Security professionals** expanding into AI security (SOC analysts, pentesters, GRC)
- **Developers and architects** building LLM-powered applications
- **IT leaders** who need to understand AI risks for governance and policy
- **Career changers** targeting the AI security space

**Prerequisites:** Basic IT or security knowledge. No AI/ML experience needed.

## What You'll Learn

1. How LLMs work at the level needed to identify and mitigate security risks
2. Threat modeling AI systems using STRIDE and the OWASP Top 10 for LLM Applications
3. Identifying and defending against prompt injection, jailbreaks, and data leakage
4. Designing secure AI architectures with trust boundaries, input validation, and guardrails
5. Evaluating AI supply chain risks — model provenance, dependencies, training pipelines
6. Applying four reference architecture patterns to real-world deployments
7. Building a 30/60/90 day AI security program

## Contents

### Chapters

| # | Chapter | Topics |
|---|---|---|
| 1 | The AI Security Landscape | AI/ML/LLM definitions, attack surface overview, career opportunity |
| 2 | How LLMs Work | Tokens, context windows, temperature, inference pipeline, trust boundaries |
| 3 | Threat Modeling AI Systems | OWASP LLM Top 10 (2025), STRIDE for AI, data flow diagrams |
| 4 | Prompt Injection | Direct/indirect injection, encoding bypasses, 6 defense patterns, dual-LLM architecture |
| 5 | Jailbreaks & Guardrail Bypass | 6 jailbreak categories, 5-layer guardrail architecture, monitoring signals |
| 6 | Data Leakage & Privacy | Training data extraction, PII flows, privacy-by-design, GDPR/AI Act |
| 7 | Secure AI System Design | Input validation, output filtering, guardrails proxy, rate limiting, logging |
| 8 | AI Supply Chain Security | Model provenance, pickle risks, SBOM for AI, pipeline hardening |
| 9 | Reference Architectures | LLM Gateway, Secure RAG, Secure AI Agent, Multi-Model Orchestration |
| 10 | Building Your AI Security Program | Risk assessment, governance, red teaming, 30/60/90 day plan |

### Appendices

- **Appendix A** — AI Security Cheat Sheet (threats + mitigations table, decision checklist)
- **Appendix B** — Tools & Resources (Garak, PyRIT, ModelScan, OWASP, NIST AI RMF, MITRE ATLAS)
- **Appendix C** — Glossary (40 key terms with plain-English definitions)

### Hands-On Exercises

| # | Exercise | Difficulty |
|---|---|---|
| 1 | Threat Model a Customer Service Chatbot | Beginner |
| 2 | Prompt Injection Lab (Python, no API keys) | Beginner-Intermediate |
| 3 | Architecture Design Review — Find 10 Issues | Intermediate |
| 4 | AI Supply Chain Audit | Beginner-Intermediate |
| 5 | Architecture Challenge — Design from Scratch | Intermediate-Advanced |

## Project Structure

```
AI Security Architecture/
├── README.md
├── outline.md              # Full table of contents
├── build.py                # Markdown -> PDF build script
├── style.css               # PDF styling (security teal theme)
├── content/                # Chapters + appendices (Markdown)
│   ├── chapter-01 ... 10
│   ├── appendix-a ... c
├── exercises/              # Hands-on exercises with solutions
│   ├── exercise-01 ... 05
├── assets/                 # Diagrams (if needed)
└── export/                 # Generated PDFs
```

## Building the PDF

```bash
pip install markdown playwright
playwright install chromium
python build.py              # Build PDF
python build.py --html       # Also save intermediate HTML
```

Output: `export/AI-Security-Architecture-Guide.pdf`

## Key Frameworks Referenced

- [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)
- [MITRE ATLAS](https://atlas.mitre.org/)
- [EU AI Act](https://artificialintelligenceact.eu/)

## License

All rights reserved. This content is not licensed for redistribution.

## Author

Built by [@TerminalsandCoffee](https://github.com/TerminalsandCoffee)
