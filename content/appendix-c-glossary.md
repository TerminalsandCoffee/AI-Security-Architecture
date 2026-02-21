# Appendix C: Glossary

Key terms used throughout this guide, in plain English.

| Term | Definition | Chapter |
|---|---|---|
| **Adversarial Input** | Input deliberately crafted to make an AI system malfunction or behave in unintended ways. | Ch 4, 5 |
| **AI Agent** | An AI system that can take actions in the real world — calling APIs, querying databases, sending messages — not just generating text. | Ch 9 |
| **AI SBOM** | AI Software Bill of Materials — a document listing every component in an AI system: models, datasets, dependencies, and configurations. | Ch 8 |
| **Alignment** | Training an AI model to behave according to human values and intentions. RLHF and Constitutional AI are alignment techniques. | Ch 2 |
| **API-Based Model** | An LLM accessed via an API hosted by a provider (OpenAI, Anthropic, Google). Your data travels to their infrastructure. | Ch 2 |
| **Backdoor (Model)** | Hidden behavior inserted during training that activates when a specific trigger input is provided. Normal inputs produce normal outputs. | Ch 8 |
| **Constitutional AI** | An alignment technique where the model is trained to follow a set of principles (a "constitution") that guide its behavior. | Ch 2, 5 |
| **Context Window** | The maximum amount of text (measured in tokens) an LLM can process in a single request. Everything in the window — system prompt, user input, history — competes for space. | Ch 2 |
| **Crescendo Attack** | A multi-turn jailbreak technique where the attacker gradually escalates requests across multiple messages, starting innocuously and building toward restricted content. | Ch 5 |
| **Data Poisoning** | An attack where malicious data is injected into a training or fine-tuning dataset to alter the model's behavior. | Ch 3, 8 |
| **Defense in Depth** | A security strategy that uses multiple layers of controls so that if one layer fails, others still provide protection. | Ch 4, 5, 7 |
| **Denial of Wallet** | An attack that causes excessive API costs by sending expensive prompts or triggering many model calls. The AI equivalent of a denial-of-service attack on your budget. | Ch 3, 7 |
| **Dual-LLM Pattern** | An architecture where two separate LLMs handle different privilege levels — a low-privilege "planner" interprets user intent, and a high-privilege "executor" performs actions. | Ch 4, 9 |
| **Embedding** | A numerical representation (vector) of text that captures its meaning. Used in RAG systems to find relevant documents by semantic similarity. | Ch 3 |
| **Excessive Agency** | An AI system that has more permissions, broader scope, or more autonomy than it needs to perform its intended function. OWASP LLM06. | Ch 3 |
| **Fine-Tuning** | Additional training of a pre-trained model on a specific dataset to specialize it for a particular task. Can introduce new vulnerabilities. | Ch 2, 8 |
| **Guardrails** | Security controls that constrain an AI system's behavior — input validation, output filtering, content safety classifiers, and behavioral rules. | Ch 5, 7 |
| **Guardrails Proxy** | An architecture pattern where all AI interactions pass through a centralized proxy that enforces security policies. | Ch 7, 9 |
| **Hallucination** | When an LLM generates false or fabricated information that sounds plausible. The model is not "lying" — it's generating the most probable text, which may not be factual. | Ch 3 |
| **Human-in-the-Loop** | A pattern where high-risk AI actions require human approval before execution. The strongest control against unintended AI actions. | Ch 7 |
| **Indirect Prompt Injection** | A prompt injection attack where malicious instructions are hidden in external data (web pages, documents, emails) that the AI system processes, rather than in direct user input. | Ch 4 |
| **Inference** | The process of running input through a trained model to get output. When you send a prompt to an LLM and get a response, that's inference. | Ch 2 |
| **Jailbreak** | A technique for bypassing an LLM's built-in safety training to make it generate restricted content. Different from prompt injection, which overrides application instructions. | Ch 5 |
| **Least Privilege** | A security principle: give the AI system only the minimum permissions it needs to perform its function. No more access, no more tools, no more data than necessary. | Ch 4, 7 |
| **LLM (Large Language Model)** | A neural network trained on massive text datasets that predicts the next token in a sequence. GPT-4, Claude, Gemini, and Llama are LLMs. | Ch 1, 2 |
| **Model Card** | Documentation published with a model describing who created it, how it was trained, its capabilities, limitations, and intended use. | Ch 8 |
| **Model Provenance** | The verifiable history of a model — who created it, what data it was trained on, how it was distributed, and whether it's been tampered with. | Ch 8 |
| **OWASP LLM Top 10** | A ranked list of the 10 most critical security risks for LLM applications, published by the OWASP Foundation. The standard reference for LLM security. | Ch 3 |
| **Parameters (Weights)** | The numbers inside a neural network that define its behavior. A model like GPT-4 has hundreds of billions of parameters, set during training. | Ch 2 |
| **Pickle** | A Python serialization format that can contain executable code. Commonly used for ML model files. Loading an untrusted pickle file can execute arbitrary code. | Ch 8 |
| **PII (Personally Identifiable Information)** | Data that can identify a specific person — names, email addresses, phone numbers, SSNs, etc. AI systems may expose PII through training data extraction or context leakage. | Ch 6 |
| **Privilege Separation** | An architecture pattern where different components run with different permission levels. In AI: the model that interprets user intent has no tools; the model that executes actions never sees raw user input. | Ch 4, 9 |
| **Prompt Injection** | An attack where crafted input causes an LLM to ignore its intended instructions and follow the attacker's instructions instead. The #1 LLM vulnerability. | Ch 4 |
| **RAG (Retrieval-Augmented Generation)** | An architecture where the LLM retrieves relevant documents from a knowledge base before generating a response. Grounds the model's output in specific data. | Ch 3, 9 |
| **Red Teaming** | Deliberately attacking a system to find vulnerabilities. AI red teaming specifically tests LLM applications for prompt injection, jailbreaks, data leakage, and other AI-specific threats. | Ch 10 |
| **RLHF (Reinforcement Learning from Human Feedback)** | A training technique that uses human preferences to align model behavior. Humans rate model outputs, and the model is trained to produce higher-rated responses. | Ch 2, 5 |
| **Safetensors** | A model file format that only stores tensor data (numbers), with no ability to contain executable code. A safer alternative to pickle for model distribution. | Ch 8 |
| **Sandwich Defense** | Placing critical security instructions after the user's input in the prompt, so they're the last thing the model sees and harder to override. | Ch 4 |
| **Self-Hosted Model** | An LLM running on your own infrastructure (on-premises or private cloud). Data stays in your environment, but you take on full operational responsibility. | Ch 2 |
| **STRIDE** | A threat modeling framework with six categories: Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege. | Ch 3 |
| **System Prompt** | Instructions sent to the LLM before the user's input that define its behavior, personality, and constraints. Not a security boundary — can be overridden or extracted. | Ch 2 |
| **Temperature** | A parameter that controls randomness in the model's output. Lower temperature = more deterministic. Higher temperature = more creative but less predictable. | Ch 2 |
| **Token** | The basic unit of text that LLMs process — typically 3-4 characters, roughly a word or word fragment. Context windows and costs are measured in tokens. | Ch 2 |
| **Training Data Extraction** | An attack that causes an LLM to output memorized data from its training set, potentially including PII, code, or other sensitive information. | Ch 6 |
| **Trust Boundary** | A point in an architecture where the level of trust changes. Data crossing a trust boundary must be validated. AI systems have trust boundaries on both sides of the model. | Ch 2, 3 |
| **Vector Database** | A database optimized for storing and searching embeddings (numerical vectors). Used in RAG systems to find documents semantically similar to a user's query. | Ch 3, 9 |
