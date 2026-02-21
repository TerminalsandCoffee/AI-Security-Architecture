# Exercise 5: Architecture Challenge

## Objective

Design a secure architecture from scratch for a given business scenario. This is an open-ended exercise where you apply everything from the guide — threat modeling, security controls, reference architecture patterns, and operational considerations.

**Difficulty:** Intermediate-Advanced
**Time estimate:** 45-60 minutes
**Prerequisites:** Read all chapters (especially 7 and 9)

---

## Scenario: InsureCo Internal Document Q&A

InsureCo is a mid-size insurance company with 2,000 employees. They want to build an internal AI-powered Q&A system that lets employees ask questions about company policies, procedures, and guidelines. Today, employees spend significant time searching through SharePoint, Confluence, and shared drives to find answers.

### Business Requirements

1. **Users:** All 2,000 employees, authenticated through the company's existing Azure AD (SSO)
2. **Data sources:**
   - HR policies and procedures (~500 documents)
   - IT security policies (~200 documents)
   - Insurance underwriting guidelines (~1,000 documents)
   - Compliance and regulatory documents (~300 documents)
   - Employee handbook
3. **Access control:**
   - HR documents: accessible to all employees
   - IT security policies: accessible to all employees
   - Underwriting guidelines: accessible only to underwriters and managers
   - Compliance documents: accessible only to compliance team and leadership
   - Employee handbook: accessible to all
4. **Capabilities:**
   - Answer natural language questions with citations to source documents
   - Summarize documents on request
   - NO ability to modify, delete, or create documents
   - NO ability to send emails, messages, or communicate externally
5. **Compliance requirements:**
   - SOC 2 Type II (in progress)
   - Insurance industry regulations require audit trails
   - PII must be protected (employee records are in some HR documents)
   - Data must stay within the US

### Constraints

- Budget: Moderate (can afford cloud services but not a dedicated ML team)
- Timeline: 3 months to MVP
- Internal expertise: One senior developer, one cloud engineer, no ML engineers
- Existing infrastructure: Azure cloud, Azure AD, Microsoft 365

---

## Your Task

### Part 1: Architecture Design (20 minutes)

Design the complete system architecture. Include:

**1. Architecture Diagram**

Draw (ASCII is fine) the full architecture showing all components and data flows. Include:
- User interface
- Authentication
- Application server(s)
- AI model (which one and why)
- Vector database
- Document ingestion pipeline
- Security controls (input validation, output filtering, etc.)
- Logging and monitoring

```
YOUR ARCHITECTURE DIAGRAM HERE:




```

**2. Component Choices**

Fill in your choices and justification:

| Component | Your Choice | Why? |
|---|---|---|
| LLM Model | | |
| Vector Database | | |
| Application Framework | | |
| Hosting | | |
| Authentication | | |
| Document Processing | | |
| Logging/Monitoring | | |

### Part 2: Trust Boundaries and Security Controls (15 minutes)

**1. Trust Boundary Map**

Identify every trust boundary in your architecture:

| Trust Boundary | From | To | Security Control |
|---|---|---|---|
| TB1 | | | |
| TB2 | | | |
| TB3 | | | |
| TB4 | | | |
| TB5 | | | |

**2. Security Controls Specification**

For each control, specify what it does and how it works:

| Control | What It Does | Implementation Detail |
|---|---|---|
| Input Validation | | |
| Output Filtering | | |
| Access Control (RAG) | | |
| Rate Limiting | | |
| Logging | | |
| PII Protection | | |

### Part 3: Threat Model (10 minutes)

Identify the top 5 threats specific to this system:

| # | Threat | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |
| 4 | | | | |
| 5 | | | | |

### Part 4: Operational Considerations (5 minutes)

Answer these questions:

1. **How will new documents be added to the system?**

2. **How will you detect and respond to security incidents?**

3. **How will you handle model updates or changes?**

4. **What's your plan for the first 30 days after launch?**

---

## Solution Guide

> **Note:** There is no single "correct" architecture. The solution below represents one well-designed approach. Your design may differ and still be secure.

### Part 1: Architecture Design

**Architecture Diagram:**

```
+-----------------------------------------------------------------------+
|                    INSURECO DOCUMENT Q&A                               |
|                                                                       |
|  +--------+     +----------+     +------------------+                 |
|  |Employee| SSO | Azure AD | --> | Web App          |                 |
|  |Browser | --> |  (Auth)  |     | (Azure App Svc)  |                 |
|  +--------+     +----------+     +------------------+                 |
|                                         |                             |
|                                   +-----+------+                      |
|                                   |            |                      |
|                                   v            v                      |
|                            +----------+  +-----------+                |
|                            |  INPUT   |  |  OUTPUT   |                |
|                            |VALIDATOR |  |  FILTER   |                |
|                            +----------+  +-----------+                |
|                                   |            ^                      |
|                                   v            |                      |
|                            +------------------+                       |
|                            | GUARDRAILS PROXY |                       |
|                            +------------------+                       |
|                              |       |       |                        |
|                              v       v       v                        |
|                        +------+ +------+ +-------+                    |
|                        |Azure | |Azure | |Azure  |                    |
|                        |OpenAI| |AI    | |Monitor|                    |
|                        |GPT-4o| |Search | |+ Log |                    |
|                        +------+ |(Vec) | |Analyt.|                    |
|                                 +------+ +-------+                    |
|                                    ^                                  |
|                                    |                                  |
|                            +------------------+                       |
|                            | DOCUMENT         |                       |
|                            | INGESTION        |                       |
|                            | PIPELINE         |                       |
|                            +------------------+                       |
|                                    ^                                  |
|                                    |                                  |
|                            +------------------+                       |
|                            | SharePoint /     |                       |
|                            | Confluence /     |                       |
|                            | File Shares      |                       |
|                            +------------------+                       |
+-----------------------------------------------------------------------+
```

**Component Choices:**

| Component | Choice | Why? |
|---|---|---|
| LLM Model | Azure OpenAI GPT-4o | Data stays in Azure (US regions), enterprise agreement, no data used for training, SOC 2 compliant |
| Vector Database | Azure AI Search | Native Azure integration, supports metadata filtering (for access control), managed service |
| Application Framework | Python FastAPI on Azure App Service | Lightweight, async, team knows Python |
| Hosting | Azure App Service (PaaS) | Managed, scales, integrates with Azure AD, SOC 2 scope |
| Authentication | Azure AD SSO (OIDC) | Already in place, supports group-based access, MFA enabled |
| Document Processing | Azure Document Intelligence + custom chunking | Handles PDFs, Word, Excel; Azure-native |
| Logging/Monitoring | Azure Monitor + Log Analytics | Centralized logging, alerting, compliance retention |

### Part 2: Trust Boundaries

| Trust Boundary | From | To | Security Control |
|---|---|---|---|
| TB1 | Employee browser | Web app | Azure AD SSO + MFA, HTTPS |
| TB2 | Web app | Guardrails proxy | Input validation, rate limiting |
| TB3 | Guardrails proxy | Azure OpenAI | Managed identity auth, data stays in Azure |
| TB4 | Guardrails proxy | Azure AI Search | Metadata filter by user's access groups |
| TB5 | Azure OpenAI | Guardrails proxy | Output filtering (PII, prompt leak) |

**Security Controls:**

| Control | What It Does | Implementation |
|---|---|---|
| Input Validation | Length check, injection scan, PII warning | Regex + lightweight classifier, max 2000 chars |
| Output Filtering | PII redaction, prompt leak detection | Regex PII scanner, word-overlap prompt leak check |
| Access Control (RAG) | Scoped document retrieval | Azure AD groups mapped to document access tags; metadata filter on every query |
| Rate Limiting | Prevent abuse and cost overruns | 20 queries/user/hour, 200 tokens/query avg |
| Logging | Audit trail for all interactions | Log: user ID, query hash, response metadata, security flags. 1-year retention. |
| PII Protection | Prevent PII exposure in responses | Scan output for PII patterns, redact before returning. Flag PII in input with warning. |

### Part 3: Threat Model

| # | Threat | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| 1 | Access control bypass — user retrieves underwriting docs they shouldn't see | Medium | High | Double-check access: filter in vector query + validate in app layer |
| 2 | Prompt injection to extract data from restricted documents | Medium | High | Input validation, doc sanitization, output filtering |
| 3 | PII leakage — HR documents contain employee PII that appears in responses | High | High | PII scanning on output, redact before returning. Consider PII-free summaries in RAG index. |
| 4 | System prompt extraction revealing business logic | High | Low | Treat system prompt as public. No secrets in prompt. Output leak detection. |
| 5 | Document poisoning — malicious content in uploaded documents causes indirect injection | Low | High | Document sanitization during ingestion. Review pipeline for new/modified docs. |

### Part 4: Operational Considerations

**1. Document updates:** Scheduled sync from SharePoint/Confluence nightly. Documents go through ingestion pipeline (chunk, embed, tag with access groups, scan for injection patterns). Manual trigger available for urgent updates.

**2. Incident detection/response:** Azure Monitor alerts on: guardrail block rate spike, PII detection in output, unusual query volume. Incident response follows company IR plan with AI-specific additions from Chapter 10.

**3. Model updates:** Azure OpenAI model versions are pinned. Before updating: test with red team prompt suite in staging, compare output quality, verify guardrails still work. Roll out during maintenance window.

**4. First 30 days:** Soft launch to IT team (50 users) for 2 weeks. Monitor logs daily. Adjust guardrail thresholds based on false positive rate. Expand to all employees after tuning. Run basic red team tests weekly for the first month.
