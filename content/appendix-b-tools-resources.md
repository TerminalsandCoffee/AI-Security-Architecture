# Appendix B: Tools & Resources

## Open Source Tools for AI Security Testing

### Prompt Injection and Red Teaming

| Tool | What It Does | Link |
|---|---|---|
| **Garak** | LLM vulnerability scanner — automated probing for injection, jailbreaks, data leakage, hallucination | github.com/NVIDIA/garak |
| **PyRIT** | Microsoft's Python Risk Identification Toolkit for generative AI — automated red teaming framework | github.com/Azure/PyRIT |
| **Rebuff** | Prompt injection detection API — self-hosted or cloud, uses multiple detection strategies | github.com/protectai/rebuff |
| **Prompt Injection Detector** | Lightweight classifier for detecting prompt injection attempts in user input | Various implementations |
| **ART (Adversarial Robustness Toolbox)** | IBM's toolkit for adversarial ML attacks and defenses — broader than LLMs | github.com/Trusted-AI/adversarial-robustness-toolbox |

### Model Security and Supply Chain

| Tool | What It Does | Link |
|---|---|---|
| **ModelScan** | Scan ML model files for malicious code (pickle exploits, etc.) | github.com/protectai/modelscan |
| **safetensors** | Safe model serialization format — stores only tensor data, no code execution | github.com/huggingface/safetensors |
| **pip-audit** | Audit Python dependencies for known vulnerabilities | github.com/pypa/pip-audit |
| **Trivy** | Container and dependency vulnerability scanner — supports Python, npm, etc. | github.com/aquasecurity/trivy |
| **Sigstore** | Keyless signing for software supply chain integrity | sigstore.dev |

### Content Safety and PII Detection

| Tool | What It Does | Link |
|---|---|---|
| **Presidio** | Microsoft's PII detection and anonymization SDK — supports text and images | github.com/microsoft/presidio |
| **NeMo Guardrails** | NVIDIA's framework for adding guardrails to LLM applications | github.com/NVIDIA/NeMo-Guardrails |
| **Guardrails AI** | Define and enforce guardrails on LLM outputs with validation specs | github.com/guardrails-ai/guardrails |
| **LLM Guard** | Input/output scanning for LLM applications — injection, PII, toxicity | github.com/protectai/llm-guard |

## Frameworks and Standards

### OWASP

| Resource | Description |
|---|---|
| **OWASP Top 10 for LLM Applications** | The standard reference for LLM security risks. Updated regularly. Essential reading. |
| **OWASP AI Security and Privacy Guide** | Broader AI security guidance beyond just LLMs |
| **OWASP Machine Learning Security Top 10** | Security risks specific to ML systems (training, inference, model theft) |

### NIST

| Resource | Description |
|---|---|
| **NIST AI Risk Management Framework (AI RMF)** | Voluntary framework for managing AI risks. Four functions: Govern, Map, Measure, Manage. |
| **NIST AI 100-2: Adversarial Machine Learning** | Taxonomy of attacks on ML systems — data poisoning, evasion, privacy attacks |
| **NIST SP 800-218A: Secure Software Development (AI)** | Extending secure development practices to AI/ML systems |

### MITRE

| Resource | Description |
|---|---|
| **MITRE ATLAS** | Adversarial Threat Landscape for AI Systems — a knowledge base of attacks on ML, modeled after ATT&CK |
| **MITRE ATT&CK** | The foundational framework — useful for mapping AI attacks to broader threat intelligence |

### Other Standards

| Resource | Description |
|---|---|
| **EU AI Act** | European regulation classifying AI systems by risk level with compliance requirements |
| **ISO/IEC 42001** | AI management system standard — requirements for establishing, implementing, and improving AI |
| **CISA AI Security Guidelines** | US cybersecurity agency guidance on securing AI systems |

## Communities and Learning

### Communities

| Community | Description |
|---|---|
| **OWASP AI Exchange** | Working group focused on AI security — regular meetings, collaborative projects |
| **AI Village (DEF CON)** | Security research community focused on AI/ML — annual events, CTFs, talks |
| **MLSecOps Community** | Community focused on security of ML operations and pipelines |
| **r/AIsecurity (Reddit)** | Subreddit for AI security discussions and news |
| **AI Security Alliance** | Industry group working on AI security standards and best practices |

### Conferences and Events

| Event | Focus |
|---|---|
| **DEF CON AI Village** | AI security research, CTFs, red teaming exercises |
| **RSA Conference (AI track)** | Enterprise AI security talks and vendor showcases |
| **Black Hat (AI sessions)** | Technical AI security research presentations |
| **NeurIPS (ML Safety Workshop)** | Academic ML safety and security research |
| **USENIX Security** | Academic security research including AI/ML topics |

### Certifications and Training

| Resource | Description |
|---|---|
| **SANS SEC595: Applied Data Science and AI/ML for Cybersecurity** | Hands-on training for using AI in security operations |
| **Certified AI Security Professional (CAISP)** | Emerging certification focused on AI security |
| **Cloud provider AI security courses** | AWS, Azure, and GCP all offer AI security training |
| **OWASP LLM Top 10 training** | Free training materials based on the OWASP LLM Top 10 |

## Recommended Reading

### Books

| Title | Author(s) | Focus |
|---|---|---|
| *Not with a Bug, But with a Sticker* | Comiter | Adversarial ML attacks in the real world |
| *AI Security* | Various | Comprehensive AI security coverage |
| *Practical Deep Learning for Cloud, Mobile, and Edge* | Koul et al. | Understanding deep learning for security practitioners |

### Papers and Reports

| Title | Why It Matters |
|---|---|
| "Ignore This Title and HackAPrompt" (Schulhoff et al.) | Taxonomy of prompt injection techniques from a competition |
| "Not What You've Signed Up For" (Greshake et al.) | Seminal paper on indirect prompt injection |
| "Universal and Transferable Adversarial Attacks on Aligned Language Models" (Zou et al.) | Automated methods for generating adversarial prompts |
| "Extracting Training Data from Large Language Models" (Carlini et al.) | Demonstrated training data memorization and extraction |
| MITRE ATLAS Case Studies | Real-world examples of attacks on AI systems |

### Blogs and Newsletters

| Resource | Description |
|---|---|
| **Simon Willison's blog** | Prolific coverage of LLM security issues, especially prompt injection |
| **Trail of Bits AI blog** | Technical AI security research from a leading security firm |
| **Anthropic Research blog** | Research on AI safety and alignment from model provider perspective |
| **NVIDIA AI Red Team blog** | Practical AI red teaming insights |
