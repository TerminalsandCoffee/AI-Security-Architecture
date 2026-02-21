# Exercise 3: Architecture Design Review

## Objective

Review a provided AI system architecture and identify security issues. This exercise simulates a real security design review — you'll receive an architecture description and diagram, then systematically find vulnerabilities and recommend fixes.

**Difficulty:** Intermediate
**Time estimate:** 30-45 minutes
**Prerequisites:** Read Chapters 3, 7, and 9

---

## Scenario: DocuSearch AI

A startup called DocuSearch has built an AI-powered document search and Q&A product for enterprise customers. Their sales team is pitching it as "Drop in your company documents, ask questions, get instant answers."

You've been brought in as a security consultant to review the architecture before they launch to their first enterprise customer (a healthcare company).

### System Description

**Product:** DocuSearch AI — enterprise document Q&A platform

**How it works:**
1. Customers upload documents (PDFs, Word docs, spreadsheets) through a web portal
2. Documents are chunked, embedded, and stored in a vector database
3. Users type questions in natural language
4. The system retrieves relevant document chunks and sends them to GPT-4o with the user's question
5. The response is displayed to the user with citations

**Technical details:**
- **Frontend:** React web app, authenticated with email/password (no MFA)
- **Backend:** Node.js API server
- **Model:** GPT-4o via OpenAI API (using a single shared API key)
- **Vector DB:** Pinecone (cloud-hosted)
- **Document storage:** AWS S3 bucket (documents stored as-is)
- **Embedding model:** OpenAI text-embedding-3-small
- **System prompt:** "You are a helpful document assistant. Answer questions based on the provided context. If the answer isn't in the context, say you don't know."
- **Deployment:** Single AWS EC2 instance, no load balancer

**Current security measures:**
- HTTPS on the frontend
- User authentication (email/password)
- S3 bucket is private (not publicly accessible)
- OpenAI API key stored in an environment variable on the EC2 instance

### Architecture Diagram

```
+--------+        +----------+        +---------+
|  User  | HTTPS  |  React   |  HTTP  | Node.js |
|(Browser|------->|  Frontend|------->|   API   |
|        |        |          |        | Server  |
+--------+        +----------+        +---------+
                                       |  |  |  |
                              +--------+  |  |  +--------+
                              |           |  |           |
                              v           v  v           v
                         +--------+  +------+  +---------+
                         |Pinecone|  |OpenAI|  |  AWS S3  |
                         |Vector  |  | API  |  | (docs)   |
                         |  DB    |  |      |  |          |
                         +--------+  +------+  +---------+

Notes:
- Single OpenAI API key used for all customers
- All users share the same Pinecone index
- Documents from all customers stored in same S3 bucket
- No rate limiting on API
- System prompt is generic (same for all customers)
- No output filtering
- Logs are minimal (errors only)
```

---

## Your Task: Find 10 Security Issues

Review the architecture above and identify at least 10 security issues. For each issue, document:

1. **What's wrong** (the vulnerability)
2. **Why it matters** (the impact)
3. **How to fix it** (the recommendation)

Use the worksheet below. The issues span multiple categories — look across authentication, data isolation, network security, AI-specific threats, and operational security.

### Security Review Worksheet

**Issue 1:**
- What's wrong: _______________________________________________
- Why it matters: _______________________________________________
- How to fix it: _______________________________________________

**Issue 2:**
- What's wrong: _______________________________________________
- Why it matters: _______________________________________________
- How to fix it: _______________________________________________

**Issue 3:**
- What's wrong: _______________________________________________
- Why it matters: _______________________________________________
- How to fix it: _______________________________________________

**Issue 4:**
- What's wrong: _______________________________________________
- Why it matters: _______________________________________________
- How to fix it: _______________________________________________

**Issue 5:**
- What's wrong: _______________________________________________
- Why it matters: _______________________________________________
- How to fix it: _______________________________________________

**Issue 6:**
- What's wrong: _______________________________________________
- Why it matters: _______________________________________________
- How to fix it: _______________________________________________

**Issue 7:**
- What's wrong: _______________________________________________
- Why it matters: _______________________________________________
- How to fix it: _______________________________________________

**Issue 8:**
- What's wrong: _______________________________________________
- Why it matters: _______________________________________________
- How to fix it: _______________________________________________

**Issue 9:**
- What's wrong: _______________________________________________
- Why it matters: _______________________________________________
- How to fix it: _______________________________________________

**Issue 10:**
- What's wrong: _______________________________________________
- Why it matters: _______________________________________________
- How to fix it: _______________________________________________

### Bonus: Severity Rating

After finding all 10, rate each by severity:

| Issue # | Category | Severity (Critical/High/Medium/Low) |
|---|---|---|
| 1 | | |
| 2 | | |
| 3 | | |
| 4 | | |
| 5 | | |
| 6 | | |
| 7 | | |
| 8 | | |
| 9 | | |
| 10 | | |

---

## Solution Guide

### Issue 1: No Tenant Data Isolation in Vector Database
- **What's wrong:** All customers share the same Pinecone index. When a user queries, they might retrieve document chunks from other customers.
- **Why it matters:** Customer A can see Customer B's confidential documents. For a healthcare customer, this could expose PHI (HIPAA violation).
- **How to fix it:** Use per-tenant namespaces in Pinecone with mandatory tenant filtering on every query. Alternatively, use separate indexes per customer.
- **Severity:** Critical

### Issue 2: No Tenant Isolation in S3
- **What's wrong:** All customer documents stored in the same S3 bucket with no per-tenant access controls.
- **Why it matters:** A path traversal or access control bug could expose one customer's documents to another. Shared bucket makes blast radius of any S3 misconfiguration affect all customers.
- **How to fix it:** Use per-tenant S3 prefixes with IAM policies that scope access, or use separate buckets per tenant. Enforce tenant context on every S3 operation.
- **Severity:** Critical

### Issue 3: No Input Validation or Injection Scanning
- **What's wrong:** User queries are passed directly to the LLM with no input validation, injection detection, or sanitization.
- **Why it matters:** Users can perform prompt injection to bypass the system prompt, extract data from other tenants' documents (if retrieval isn't scoped), or make the model generate harmful content.
- **How to fix it:** Add an input validation pipeline: length check, injection pattern detection, and PII scanning before the query reaches the model.
- **Severity:** High

### Issue 4: No Output Filtering
- **What's wrong:** Model responses are sent directly to users with no scanning for PII, sensitive data, or inappropriate content.
- **Why it matters:** The model could include PII from documents, leak system prompt details, or hallucinate harmful content. With a healthcare customer, unfiltered output could expose PHI.
- **How to fix it:** Add output filtering: PII detection/redaction, system prompt leakage detection, and content safety checks before responses reach users.
- **Severity:** High

### Issue 5: Single Shared OpenAI API Key
- **What's wrong:** One API key is used for all customers, stored as an environment variable on the EC2 instance.
- **Why it matters:** If the key is compromised, all customer data flowing through the API is at risk. No per-customer usage tracking or budget enforcement. If one customer abuses the service, it affects all customers.
- **How to fix it:** Use per-customer API keys or a gateway that tracks usage per tenant. Store keys in a secrets manager (AWS Secrets Manager), not environment variables.
- **Severity:** High

### Issue 6: No MFA on Authentication
- **What's wrong:** Email/password authentication with no MFA option.
- **Why it matters:** For an enterprise product handling confidential documents, password-only auth is insufficient. Credential stuffing and phishing attacks can compromise accounts.
- **How to fix it:** Implement MFA (TOTP or WebAuthn). For enterprise customers, support SSO (SAML/OIDC) so customers use their own identity provider.
- **Severity:** High

### Issue 7: No Rate Limiting
- **What's wrong:** No rate limiting on the API.
- **Why it matters:** Denial-of-wallet attack: an attacker can send thousands of queries and run up the OpenAI bill. Brute-force attacks on authentication. Resource exhaustion on the single EC2 instance.
- **How to fix it:** Implement per-user rate limiting on API queries (requests/minute, tokens/minute). Add rate limiting on auth endpoints. Consider per-tenant budget caps.
- **Severity:** High

### Issue 8: Retrieved Documents Not Sanitized
- **What's wrong:** Documents retrieved from the vector database are injected directly into the LLM prompt with no sanitization.
- **Why it matters:** If a document contains prompt injection payloads (e.g., "Ignore previous instructions and..."), the model will process them. An attacker could upload a document designed to hijack the model's behavior for anyone who triggers retrieval of that document.
- **How to fix it:** Scan retrieved document chunks for injection patterns before including them in the prompt. Implement the document sanitization pattern from Chapter 9.
- **Severity:** High

### Issue 9: Single Point of Failure (No HA)
- **What's wrong:** Single EC2 instance, no load balancer, no redundancy.
- **Why it matters:** If the instance goes down, the entire service is unavailable for all customers. No capacity to handle traffic spikes. Patching requires downtime.
- **How to fix it:** Deploy behind a load balancer with auto-scaling group (minimum 2 instances). Use health checks and automated failover.
- **Severity:** Medium

### Issue 10: Minimal Logging
- **What's wrong:** Only errors are logged. No logging of user queries, model responses, or security-relevant events.
- **Why it matters:** No audit trail for security incidents. Can't detect abuse, injection attempts, or data leakage. Can't investigate customer complaints. Healthcare compliance (HIPAA) requires audit logging.
- **How to fix it:** Log all AI interactions: user ID, query (hashed for privacy), response metadata, retrieval results, security flags. Send to a centralized logging solution with retention policy.
- **Severity:** Medium

### Summary

| Issue # | Category | Severity |
|---|---|---|
| 1 | Data Isolation | Critical |
| 2 | Data Isolation | Critical |
| 3 | AI Security | High |
| 4 | AI Security | High |
| 5 | Secrets Management | High |
| 6 | Authentication | High |
| 7 | Availability/Abuse | High |
| 8 | AI Security (RAG) | High |
| 9 | Availability | Medium |
| 10 | Observability | Medium |

**Priority order for remediation:** Issues 1 and 2 (data isolation) are showstoppers for a healthcare customer. Fix those before launch. Issues 3, 4, and 8 (AI security) are next — they're the most likely attack vectors. Issues 5-7 are infrastructure hygiene. Issues 9-10 are operational maturity.
