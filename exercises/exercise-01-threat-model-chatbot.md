# Exercise 1: Threat Model a Customer Service Chatbot

## Objective

Apply STRIDE threat modeling to a realistic AI chatbot scenario. By the end of this exercise, you'll have identified trust boundaries, mapped data flows, and documented the top threats — the same process you'd use for any AI system in your organization.

**Difficulty:** Beginner
**Time estimate:** 30-45 minutes
**Prerequisites:** Read Chapters 1-3

---

## Scenario: MegaMart Customer Service Bot

MegaMart is a mid-size e-commerce company that has deployed an AI-powered customer service chatbot on their website. Here's what the engineering team has built:

### System Description

- **Model:** GPT-4o via OpenAI API
- **Interface:** Web chat widget embedded on megamart.com
- **Users:** Any website visitor (no login required to start chatting, but order lookups require account verification)
- **Capabilities:**
  - Answer questions about products, shipping, and return policies
  - Look up order status (after email verification)
  - Process return requests (creates a return label)
  - Escalate to human agent when it can't help
- **Data access:**
  - RAG-based knowledge base with product catalog and FAQ documents
  - Order database (read-only access via API)
  - Returns system (can create return labels via API)
  - Customer email addresses (for verification)
- **System prompt:** Contains brand guidelines, allowed topics, escalation rules, and return policy details
- **Logging:** All conversations are logged for quality assurance
- **Rate limiting:** 20 messages per session, 3 sessions per IP per hour

### Architecture Diagram

```
+--------+       +-----------+       +----------+       +---------+
| Website|       |   Chat    |       |  App     |       | OpenAI  |
| Visitor| ----->|  Widget   | ----->| Server   | ----->|   API   |
|        |       | (Browser) |       |          |       |         |
+--------+       +-----------+       +----------+       +---------+
                                          |
                                    +-----+-----+
                                    |     |     |
                                    v     v     v
                              +------+ +----+ +-------+
                              | RAG  | |Order| |Returns|
                              | KB   | | DB  | |System |
                              +------+ +----+ +-------+
                                                   |
                                              +--------+
                                              |  QA    |
                                              |  Logs  |
                                              +--------+
```

---

## Your Tasks

### Task 1: Identify Trust Boundaries (10 minutes)

Look at the architecture diagram above. Identify every trust boundary — every point where the level of trust changes and data should be validated.

**Worksheet:**

| Trust Boundary | From | To | What crosses this boundary? |
|---|---|---|---|
| TB1 | | | |
| TB2 | | | |
| TB3 | | | |
| TB4 | | | |
| TB5 | | | |
| TB6 | | | |

### Task 2: Map Data Flows (10 minutes)

For each trust boundary you identified, document what sensitive data flows across it and in which direction.

**Worksheet:**

| Trust Boundary | Sensitive Data | Direction | Currently Protected? |
|---|---|---|---|
| TB1 | | | Yes / No / Unknown |
| TB2 | | | Yes / No / Unknown |
| TB3 | | | Yes / No / Unknown |
| TB4 | | | Yes / No / Unknown |
| TB5 | | | Yes / No / Unknown |
| TB6 | | | Yes / No / Unknown |

### Task 3: Apply STRIDE (15 minutes)

For each STRIDE category, identify at least one specific threat to this system. Be specific — don't just say "data leakage," describe the specific attack scenario.

**Worksheet:**

| STRIDE Category | Specific Threat | Affected Component | Severity (H/M/L) |
|---|---|---|---|
| **S**poofing | | | |
| **T**ampering | | | |
| **R**epudiation | | | |
| **I**nfo Disclosure | | | |
| **D**enial of Service | | | |
| **E**levation of Privilege | | | |

### Task 4: Identify Your Top 5 Threats (10 minutes)

From your STRIDE analysis, rank the top 5 threats by risk (likelihood x impact). For each, propose a specific mitigation.

**Worksheet:**

| Rank | Threat | Likelihood (H/M/L) | Impact (H/M/L) | Proposed Mitigation |
|---|---|---|---|---|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |
| 4 | | | | |
| 5 | | | | |

### Task 5: Check Against OWASP LLM Top 10 (5 minutes)

Quick scan: which OWASP LLM Top 10 categories apply to this system?

| OWASP LLM Category | Applies? | Notes |
|---|---|---|
| LLM01: Prompt Injection | | |
| LLM02: Sensitive Information Disclosure | | |
| LLM03: Supply Chain | | |
| LLM04: Data and Model Poisoning | | |
| LLM05: Improper Output Handling | | |
| LLM06: Excessive Agency | | |
| LLM07: System Prompt Leakage | | |
| LLM08: Vector/Embedding Weaknesses | | |
| LLM09: Misinformation | | |
| LLM10: Unbounded Consumption | | |

---

## Solution Guide

> **Note:** Review this only after completing the exercise yourself. Threat modeling is partly subjective — your answers may differ and still be correct.

### Task 1 Solution: Trust Boundaries

| Trust Boundary | From | To | What crosses this boundary? |
|---|---|---|---|
| TB1 | Website Visitor | Chat Widget | User messages (free-form text) |
| TB2 | Chat Widget | App Server | User messages via HTTPS |
| TB3 | App Server | OpenAI API | System prompt + user message + RAG context |
| TB4 | App Server | RAG Knowledge Base | Search queries; retrieved documents |
| TB5 | App Server | Order DB / Returns System | Order lookups, return creation requests |
| TB6 | OpenAI API | App Server | Model responses (untrusted) |

### Task 2 Solution: Data Flows

| Trust Boundary | Sensitive Data | Direction | Currently Protected? |
|---|---|---|---|
| TB1 | User PII (names, order #s, emails) | User -> Widget | No — no input sanitization mentioned |
| TB2 | User messages with potential PII | Widget -> Server | Yes — HTTPS |
| TB3 | System prompt, user PII, customer data from RAG | Server -> OpenAI | Partial — TLS in transit, but data leaves org |
| TB4 | Product data (non-sensitive), FAQ content | KB -> Server | Unknown — are RAG docs sanitized? |
| TB5 | Customer emails, order details, return info | Server -> DBs | Unknown — are queries parameterized? |
| TB6 | Model responses (may contain PII, injection results) | OpenAI -> Server | No — no output filtering mentioned |

### Task 3 Solution: STRIDE

| STRIDE Category | Specific Threat | Affected Component | Severity |
|---|---|---|---|
| **S**poofing | Attacker enters someone else's email during "verification" to access their order history | Order lookup flow | H |
| **T**ampering | Attacker poisons RAG knowledge base documents with prompt injection payloads | RAG KB | H |
| **R**epudiation | Customer claims chatbot approved a return the bot didn't actually process; QA logs are incomplete | Logging | M |
| **I**nfo Disclosure | Attacker uses prompt injection to extract system prompt containing return policy business logic | System prompt | M |
| **D**enial of Service | Attacker sends max-length messages at rate limit ceiling to run up API costs (denial of wallet) | OpenAI API billing | M |
| **E**levation of Privilege | Attacker uses prompt injection to make the bot create return labels for orders that don't qualify | Returns system | H |

### Task 4 Solution: Top 5 Threats

| Rank | Threat | Likelihood | Impact | Proposed Mitigation |
|---|---|---|---|---|
| 1 | Prompt injection -> unauthorized returns | H | H | Output validation: verify return eligibility in app code before calling returns API, don't rely on model decision alone |
| 2 | Email spoofing for order access | H | H | Implement proper auth: email + OTP verification, not just email address |
| 3 | RAG knowledge base poisoning | M | H | Access controls on KB uploads, scan documents for injection patterns before indexing |
| 4 | PII leakage in model responses | M | H | Output PII scanning, redact before returning to user |
| 5 | System prompt extraction | H | M | Treat system prompt as public, remove sensitive business logic from it |

### Task 5 Solution: OWASP LLM Top 10

| OWASP LLM Category | Applies? | Notes |
|---|---|---|
| LLM01: Prompt Injection | **Yes** | No input validation or injection scanning mentioned |
| LLM02: Sensitive Information Disclosure | **Yes** | PII in conversations, order data accessible |
| LLM03: Supply Chain | **Partially** | Using OpenAI API — provider risk |
| LLM04: Data and Model Poisoning | **Yes** | RAG KB could be poisoned |
| LLM05: Improper Output Handling | **Yes** | Returns API called based on model output without validation |
| LLM06: Excessive Agency | **Yes** | Bot can create return labels — write access |
| LLM07: System Prompt Leakage | **Yes** | No extraction defenses mentioned |
| LLM08: Vector/Embedding Weaknesses | **Yes** | RAG system with no access controls mentioned |
| LLM09: Misinformation | **Partially** | Could give wrong product info, but low impact |
| LLM10: Unbounded Consumption | **Partially** | Rate limits exist but may not prevent cost attacks |
