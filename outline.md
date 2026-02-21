# AI Security Architecture — Full Outline

## Part I: Foundations (Chapters 1-3)

### Chapter 1: The AI Security Landscape
- What AI, ML, and LLM actually mean (plain English, no hype)
- Why AI security is a distinct discipline — not just "regular appsec"
- The AI attack surface at a glance (inputs, model, outputs, data, supply chain)
- Who needs to care: developers, architects, security teams, leadership
- Career opportunity in AI security: roles, skills, and demand
- **Key Takeaways**

### Chapter 2: How LLMs Work (Just Enough to Secure Them)
- Tokens, context windows, and temperature — the 5 concepts that matter
- API-based vs self-hosted models: security trade-offs
- The inference pipeline: prompt -> model -> response
- What the model "knows" vs what it "does" (the stochastic parrot problem)
- Why architects care: trust boundaries change when a model is in the loop
- **Key Takeaways**

### Chapter 3: Threat Modeling AI Systems
- OWASP Top 10 for LLM Applications (2025 edition) — full walkthrough
- STRIDE applied to AI systems (with examples for each category)
- Trust boundaries in AI architectures: user -> app -> model -> data
- Data flow diagrams for common AI patterns (chatbot, RAG, agent)
- Mapping threats to architecture layers
- **Exercise tie-in:** Exercise 1 — Threat Model a Customer Service Chatbot
- **Key Takeaways**

---

## Part II: Attack Techniques (Chapters 4-6)

### Chapter 4: Prompt Injection
- Direct prompt injection: overriding system instructions
- Indirect prompt injection: poisoning external data sources
- Real-world examples (sanitized reproductions)
- Why "just filter bad input" doesn't work (and what does)
- Defense patterns: input validation, privilege separation, output filtering
- Architecture-level mitigations: dual-LLM pattern, least privilege, sandboxing
- **Exercise tie-in:** Exercise 2 — Prompt Injection Lab
- **Key Takeaways**

### Chapter 5: Jailbreaks & Guardrail Bypass
- System prompt extraction techniques and why it matters
- Common jailbreak categories: role-play, encoding, multi-turn, crescendo
- Defense in depth: layered guardrails architecture
- Monitoring and detection patterns for jailbreak attempts
- The arms race reality: why 100% prevention is impossible
- Practical budget: how much guardrail is enough?
- **Key Takeaways**

### Chapter 6: Data Leakage & Privacy
- Training data extraction: memorization and regurgitation risks
- PII in prompts and completions: the invisible data flow problem
- Data flow architecture: where sensitive data actually travels
- Privacy-by-design patterns for AI systems
- Regulatory landscape: GDPR, EU AI Act, CCPA (high-level implications)
- Data classification for AI workloads
- **Key Takeaways**

---

## Part III: Secure Design (Chapters 7-8)

### Chapter 7: Secure AI System Design
- Input validation and sanitization architecture
- Output filtering and content safety layers
- Guardrails as a design pattern (not an afterthought)
- Rate limiting and abuse prevention for AI endpoints
- Logging, monitoring, and observability: what to capture and why
- The "human in the loop" pattern: when and how to use it
- Cost and latency considerations for security controls
- **Key Takeaways**

### Chapter 8: AI Supply Chain Security
- Model provenance: where did this model come from?
- Model marketplaces and trust: Hugging Face, model registries, model cards
- Dependency risks in AI pipelines: libraries, frameworks, datasets
- SBOM for AI: what it looks like and why it matters
- Securing the training and fine-tuning pipeline
- Model signing and verification
- **Key Takeaways**

---

## Part IV: Putting It Together (Chapters 9-10)

### Chapter 9: Reference Architectures
- **Pattern 1: Secure LLM API Gateway** — Input scan -> model -> output scan
  - Components, trust boundaries, failure modes
  - ASCII architecture diagram
- **Pattern 2: Secure RAG Pipeline** — Retrieval-Augmented Generation with access controls
  - Components, trust boundaries, failure modes
  - ASCII architecture diagram
- **Pattern 3: Secure AI Agent** — Agent with tool/API access and safety guardrails
  - Components, trust boundaries, failure modes
  - ASCII architecture diagram
- **Pattern 4: Multi-Model Orchestration** — Multiple models with trust boundary isolation
  - Components, trust boundaries, failure modes
  - ASCII architecture diagram
- **Key Takeaways**

### Chapter 10: Building Your AI Security Program
- Risk assessment frameworks for AI (lightweight and enterprise approaches)
- Governance: policies, acceptable use, model inventory
- Evaluation and testing: red teaming basics, automated scanning
- Continuous monitoring and incident response for AI-specific events
- The 30/60/90 day plan: getting started from zero
- Maturity model: crawl, walk, run
- **Key Takeaways**

---

## Appendices

### Appendix A: AI Security Cheat Sheet
- One-page reference: top 10 threats + recommended mitigations (table format)
- Architecture decision checklist (10 questions to ask before deploying AI)
- Quick-reference: which chapter covers what

### Appendix B: Tools & Resources
- Open source tools for AI security testing (Garak, PyRIT, Rebuff, etc.)
- Frameworks and standards: OWASP LLM Top 10, NIST AI RMF, MITRE ATLAS
- Communities, conferences, and further learning
- Recommended reading list

### Appendix C: Glossary
- 30-40 key terms with plain-English definitions
- Cross-references to chapters where each term is covered

---

## Exercises

### Exercise 1: Threat Model a Customer Service Chatbot
- **Objective:** Apply STRIDE to identify threats in a realistic AI chatbot scenario
- **Given:** Architecture description, data flow diagram, user personas
- **Task:** Identify trust boundaries, data flows, and top 5 threats
- **Deliverable:** Completed threat model worksheet
- **Difficulty:** Beginner

### Exercise 2: Prompt Injection Lab
- **Objective:** Understand prompt injection by attempting attacks and building defenses
- **Given:** A simple Python LLM wrapper (runs locally, no API keys — uses mock responses)
- **Task:** Try 5 prompt injection techniques, then implement 3 defense layers
- **Deliverable:** Working defense code + attack/defense report
- **Difficulty:** Beginner-Intermediate
- **Prerequisites:** Python 3, no external dependencies

### Exercise 3: Architecture Design Review
- **Objective:** Review an AI system architecture and identify security gaps
- **Given:** Architecture diagram + system description for a document Q&A product
- **Task:** Find 10 security issues and recommend fixes for each
- **Deliverable:** Security review report
- **Difficulty:** Intermediate

### Exercise 4: AI Supply Chain Audit
- **Objective:** Audit an AI project's dependencies, model sources, and pipeline
- **Given:** Sample project with requirements.txt, model config, and pipeline scripts
- **Task:** Identify supply chain risks and create a risk register
- **Deliverable:** Completed supply chain risk assessment
- **Difficulty:** Beginner-Intermediate

### Exercise 5: Architecture Challenge
- **Objective:** Design a secure architecture from scratch
- **Given:** Business requirements for a RAG-based internal document Q&A system
- **Task:** Design the architecture, define trust boundaries, specify security controls
- **Deliverable:** Architecture diagram + security controls specification
- **Difficulty:** Intermediate-Advanced
