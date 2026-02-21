# Chapter 7: Secure AI System Design

## Why This Matters

Chapters 4-6 showed you the attacks. This chapter shows you how to build systems that withstand them. Secure AI design isn't about adding security after the system is built — it's about making security a structural property of the architecture from day one.

The patterns in this chapter apply to any LLM-powered application, from a simple chatbot to a complex multi-agent system. Each pattern addresses a specific class of risk, and together they form a comprehensive security architecture.

## Input Validation and Sanitization Architecture

Every piece of data that enters an AI system must pass through validation before it reaches the model. This is your first line of defense and the one you have the most control over.

### Input Validation Pipeline

```
User Input
    |
    v
+-------------------+
| Length Validation  |  --> Reject if too long (context stuffing)
+-------------------+
    |
    v
+-------------------+
| Format Validation  |  --> Reject if unexpected format (binary, etc.)
+-------------------+
    |
    v
+-------------------+
| PII Scanner       |  --> Redact or warn about PII in input
+-------------------+
    |
    v
+-------------------+
| Injection Scanner  |  --> Score for prompt injection indicators
+-------------------+
    |
    v
+-------------------+
| Content Classifier |  --> Flag off-topic or policy-violating input
+-------------------+
    |
    v
Validated Input --> Model
```

### Implementation

```python
from dataclasses import dataclass

@dataclass
class ValidationResult:
    allowed: bool
    input_text: str        # Possibly redacted/sanitized version
    flags: list[str]       # Any warnings or flags
    risk_score: float      # 0.0 to 1.0

class InputValidator:
    """Multi-stage input validation for LLM applications."""

    MAX_INPUT_LENGTH = 4000  # Characters, not tokens
    MAX_TOKEN_ESTIMATE = 1500  # Rough char/4 estimate

    def validate(self, user_input: str) -> ValidationResult:
        flags = []
        risk_score = 0.0

        # Stage 1: Length check
        if len(user_input) > self.MAX_INPUT_LENGTH:
            return ValidationResult(
                allowed=False,
                input_text=user_input,
                flags=["input_too_long"],
                risk_score=1.0,
            )

        # Stage 2: Empty or whitespace-only
        if not user_input.strip():
            return ValidationResult(
                allowed=False,
                input_text=user_input,
                flags=["empty_input"],
                risk_score=0.0,
            )

        # Stage 3: PII detection (redact but allow)
        redacted = self._redact_pii(user_input)
        if redacted != user_input:
            flags.append("pii_detected_and_redacted")

        # Stage 4: Injection pattern scoring
        injection_score = self._score_injection(redacted)
        risk_score = max(risk_score, injection_score)
        if injection_score > 0.3:
            flags.append("injection_indicators")

        # Stage 5: Decision
        allowed = risk_score < 0.7
        if not allowed:
            flags.append("blocked_high_risk")

        return ValidationResult(
            allowed=allowed,
            input_text=redacted,
            flags=flags,
            risk_score=risk_score,
        )

    def _redact_pii(self, text: str) -> str:
        """Redact detected PII patterns."""
        import re
        patterns = {
            "SSN": r"\b\d{3}-\d{2}-\d{4}\b",
            "EMAIL": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
            "PHONE": r"\b\d{3}[-.\s]\d{3}[-.\s]\d{4}\b",
        }
        for label, pattern in patterns.items():
            text = re.sub(pattern, f"[{label}_REDACTED]", text)
        return text

    def _score_injection(self, text: str) -> float:
        """Score text for prompt injection indicators."""
        import re
        score = 0.0
        patterns = [
            (r"ignore\s+(all\s+)?previous", 0.4),
            (r"you\s+are\s+now\s+", 0.3),
            (r"new\s+(system\s+)?instructions", 0.4),
            (r"disregard\s+(the\s+)?(above|rules)", 0.4),
            (r"respond\s+in\s+base64", 0.3),
            (r"system\s*prompt", 0.2),
        ]
        for pattern, weight in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                score += weight
        return min(score, 1.0)
```

> **Architecture Tip:** The input validator runs traditional code — regex, classifiers, rules. It cannot be prompt-injected because it's not an LLM. This is a key principle: use non-LLM code for security decisions whenever possible.

## Output Filtering and Content Safety

Model output is untrusted. Before it reaches the user or any downstream system, it must pass through output filtering.

### Output Filtering Pipeline

```
Model Response
    |
    v
+---------------------+
| Format Validator     |  --> Reject if not expected format (JSON, etc.)
+---------------------+
    |
    v
+---------------------+
| PII Scanner          |  --> Redact PII in model output
+---------------------+
    |
    v
+---------------------+
| System Prompt Leak   |  --> Block if output contains system prompt
| Detector             |
+---------------------+
    |
    v
+---------------------+
| Content Safety       |  --> Flag harmful or off-topic content
| Classifier           |
+---------------------+
    |
    v
+---------------------+
| Hallucination Check  |  --> Flag unsupported claims (if grounding data available)
+---------------------+
    |
    v
Filtered Response --> User
```

### Implementation

```python
@dataclass
class OutputFilterResult:
    allowed: bool
    output_text: str       # Possibly redacted version
    violations: list[str]
    action: str            # "allow", "redact", "block"

class OutputFilter:
    """Multi-stage output filtering for LLM responses."""

    def __init__(self, system_prompt: str):
        self.system_prompt = system_prompt

    def filter(self, model_output: str) -> OutputFilterResult:
        violations = []
        filtered_text = model_output

        # Stage 1: PII redaction
        filtered_text = self._redact_pii(filtered_text)
        if filtered_text != model_output:
            violations.append("pii_in_output")

        # Stage 2: System prompt leakage detection
        if self._detect_prompt_leak(model_output):
            violations.append("system_prompt_leakage")
            return OutputFilterResult(
                allowed=False,
                output_text="[Response blocked: potential system prompt leakage]",
                violations=violations,
                action="block",
            )

        # Stage 3: Content safety (harmful content patterns)
        safety_issues = self._check_content_safety(filtered_text)
        violations.extend(safety_issues)

        # Decision
        if any(v.startswith("critical_") for v in violations):
            return OutputFilterResult(
                allowed=False,
                output_text="I'm unable to provide that information.",
                violations=violations,
                action="block",
            )

        return OutputFilterResult(
            allowed=True,
            output_text=filtered_text,
            violations=violations,
            action="redact" if violations else "allow",
        )

    def _detect_prompt_leak(self, output: str) -> bool:
        """Check if output contains the system prompt."""
        # Compare word overlap between output and system prompt
        prompt_words = set(self.system_prompt.lower().split())
        output_words = set(output.lower().split())
        # If more than 50% of system prompt words appear in output
        if len(prompt_words) > 10:
            overlap = len(prompt_words & output_words) / len(prompt_words)
            return overlap > 0.5
        return False

    def _redact_pii(self, text: str) -> str:
        import re
        patterns = {
            "SSN": r"\b\d{3}-\d{2}-\d{4}\b",
            "EMAIL": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
            "PHONE": r"\b\d{3}[-.\s]\d{3}[-.\s]\d{4}\b",
        }
        for label, pattern in patterns.items():
            text = re.sub(pattern, f"[{label}_REDACTED]", text)
        return text

    def _check_content_safety(self, text: str) -> list[str]:
        import re
        issues = []
        # Check for potentially harmful instructional content
        harmful_patterns = [
            (r"step\s+\d+.*(?:hack|exploit|attack)", "critical_harmful_instructions"),
            (r"here'?s\s+how\s+to\s+(?:bypass|break|crack)", "critical_harmful_instructions"),
        ]
        for pattern, label in harmful_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                issues.append(label)
        return issues
```

### When to Block vs Redact vs Log

| Signal | Action | Rationale |
|---|---|---|
| PII in output | Redact | Remove PII but return useful response |
| System prompt in output | Block | Complete response replacement |
| Harmful instructions | Block | Cannot partially return harmful content |
| Off-topic response | Log + return | Low risk, useful for model tuning |
| Unusual output length | Log | Possible injection indicator |
| Format deviation | Block or retry | Structured output expected but not received |

## Guardrails as a Design Pattern

Guardrails aren't a bolt-on. They're an architectural component that should be designed into the system from the start.

### The Guardrails Proxy Pattern

Instead of scattering security checks throughout your application code, centralize them in a guardrails proxy:

```
                    GUARDRAILS PROXY PATTERN

                  +---------------------------+
                  |     GUARDRAILS PROXY       |
                  |                           |
User --> [Input]  |  [Input]    [Output]      |  [Response] --> User
         -------->|  Scanner    Filter        |---------->
                  |     |          ^          |
                  |     v          |          |
                  |  [Model    [Model         |
                  |   Call] --> Response]      |
                  |                           |
                  +---------------------------+

All security logic lives in the proxy.
Application code only talks to the proxy, not the model directly.
```

**Benefits:**
- **Single point of enforcement.** Every model interaction passes through the same security checks.
- **Separation of concerns.** Application developers don't need to implement security logic — they call the proxy.
- **Centralized logging.** All interactions are logged in one place.
- **Easy to update.** New guardrail rules are deployed to the proxy, not to every application.

### Guardrails Configuration

Make guardrails configurable so different applications can have different policies:

```python
# guardrails_config.yaml
customer_service_bot:
  input:
    max_length: 2000
    pii_action: "redact"         # redact, warn, block
    injection_threshold: 0.7     # block above this score
    allowed_topics: ["products", "orders", "returns", "shipping"]
  output:
    pii_action: "redact"
    block_system_prompt_leak: true
    max_response_length: 4000
  monitoring:
    log_all_interactions: true
    alert_on_block: true
    rate_limit: 30              # requests per minute per user

internal_code_assistant:
  input:
    max_length: 8000
    pii_action: "warn"
    injection_threshold: 0.9    # Higher threshold -- devs write code-like input
    allowed_topics: null         # No topic restriction
  output:
    pii_action: "warn"
    block_system_prompt_leak: true
    max_response_length: 16000
  monitoring:
    log_all_interactions: true
    alert_on_block: true
    rate_limit: 60
```

> **Architecture Tip:** The guardrails proxy pattern is exactly what an LLM security gateway does (see Chapter 9, Pattern 1). If you're building multiple AI applications, invest in a shared guardrails proxy early — it pays dividends.

## Rate Limiting and Abuse Prevention

AI endpoints are expensive to run and easy to abuse. Rate limiting is both a security control and a cost control.

### What to Rate Limit

| Dimension | Limit | Purpose |
|---|---|---|
| Requests per minute | 10-60 per user | Prevent brute-force and abuse |
| Tokens per minute | 5K-50K per user | Prevent cost attacks (denial of wallet) |
| Tokens per day | 50K-500K per user | Budget control |
| Concurrent requests | 1-5 per user | Prevent resource exhaustion |
| Context window usage | 70-80% max | Leave room for system prompt and output |
| Conversation length | 20-50 turns | Prevent unbounded context growth |

### Rate Limiting Architecture

```python
import time
from collections import defaultdict

class RateLimiter:
    """Token bucket rate limiter for AI endpoints."""

    def __init__(self, rpm: int = 30, tpm: int = 10000):
        self.rpm = rpm
        self.tpm = tpm
        self._request_windows = defaultdict(list)  # user_id -> [timestamps]
        self._token_windows = defaultdict(list)     # user_id -> [(ts, count)]

    def check(self, user_id: str, estimated_tokens: int = 0) -> tuple[bool, str]:
        now = time.time()
        window = 60.0  # 1 minute window

        # Clean old entries
        self._request_windows[user_id] = [
            ts for ts in self._request_windows[user_id] if now - ts < window
        ]
        self._token_windows[user_id] = [
            (ts, count) for ts, count in self._token_windows[user_id]
            if now - ts < window
        ]

        # Check request rate
        if len(self._request_windows[user_id]) >= self.rpm:
            return False, f"Rate limit exceeded: {self.rpm} requests/min"

        # Check token rate
        total_tokens = sum(c for _, c in self._token_windows[user_id])
        if total_tokens + estimated_tokens > self.tpm:
            return False, f"Token limit exceeded: {self.tpm} tokens/min"

        # Allow and record
        self._request_windows[user_id].append(now)
        if estimated_tokens > 0:
            self._token_windows[user_id].append((now, estimated_tokens))

        return True, "OK"
```

### Abuse Detection Signals

Beyond simple rate limits, watch for patterns that indicate abuse:

- **Rapid-fire variations:** Same user sending many slightly different prompts (probing for injection bypasses)
- **Unusual hours:** Automated attacks often run outside business hours
- **Token asymmetry:** Very short inputs requesting very long outputs
- **Repeated blocks:** User hitting guardrail blocks and retrying with modifications
- **Session anomalies:** New accounts immediately sending complex/adversarial prompts

## Logging, Monitoring, and Observability

If you can't see what your AI system is doing, you can't secure it. AI systems need purpose-built observability.

### What to Log

```python
import hashlib
import json
from datetime import datetime, timezone

def log_ai_interaction(
    request_id: str,
    user_id: str,
    user_input: str,
    model_output: str,
    model_name: str,
    input_tokens: int,
    output_tokens: int,
    latency_ms: float,
    input_flags: list[str],
    output_flags: list[str],
    action_taken: str,
):
    """Log a complete AI interaction for security monitoring."""
    log_entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "request_id": request_id,
        "user_id": user_id,
        # Hash the input instead of logging raw text (privacy)
        "input_hash": hashlib.sha256(user_input.encode()).hexdigest(),
        "input_length": len(user_input),
        "output_length": len(model_output),
        "model": model_name,
        "tokens": {
            "input": input_tokens,
            "output": output_tokens,
            "total": input_tokens + output_tokens,
        },
        "latency_ms": latency_ms,
        "security": {
            "input_flags": input_flags,
            "output_flags": output_flags,
            "action": action_taken,  # allow, redact, block
            "risk_score": max_risk_score(input_flags),
        },
    }
    # Send to logging pipeline / SIEM
    print(json.dumps(log_entry))
```

### Monitoring Dashboard Metrics

Essential metrics for an AI security dashboard:

| Metric | What It Shows | Alert Threshold |
|---|---|---|
| Blocked requests/hour | Active attack attempts | >5% of total requests |
| Unique flagged users/day | Breadth of adversarial activity | Sudden increase |
| Average risk score | Overall threat level | Trending upward |
| Token spend/hour | Cost and potential abuse | >150% of baseline |
| Output PII detections/hour | Data leakage rate | Any increase |
| System prompt leak detections | Extraction attempts | Any occurrence |
| P95 latency | Performance impact of security controls | >2x baseline |
| Guardrail bypass rate | Effectiveness of defenses | Trending upward |

### Detection Rules for SIEM Integration

If you're shipping AI logs to a SIEM, here are detection rules to implement:

```
RULE: Prompt Injection Probing
CONDITION: Same user_id triggers injection_indicators flag > 5 times in 10 minutes
ACTION: Alert + temporary rate limit

RULE: System Prompt Extraction Attempt
CONDITION: output_flags contains "system_prompt_leakage"
ACTION: Alert + block response + review conversation

RULE: Denial of Wallet
CONDITION: Single user_id consumes > 100K tokens in 5 minutes
ACTION: Alert + hard rate limit

RULE: Jailbreak Escalation
CONDITION: User has > 3 blocked requests followed by an allowed request with risk_score > 0.5
ACTION: Alert (possible successful bypass after probing)

RULE: Unusual Data Exfiltration
CONDITION: output_length / input_length ratio > 50 AND output_flags contains "pii_in_output"
ACTION: Alert + review response
```

> **Security Note:** Log enough to investigate incidents, but be mindful of privacy. Hashing user inputs instead of logging them raw protects user privacy while still enabling pattern analysis. For investigations, maintain a secure, access-controlled archive of full prompts with a short retention period.

## The Human-in-the-Loop Pattern

For high-stakes AI actions, human approval is the strongest security control.

### When to Use Human-in-the-Loop

```
LOW RISK (no human needed):
  - Answering questions from documentation
  - Summarizing public content
  - Generating code suggestions (user reviews before running)

MEDIUM RISK (human review recommended):
  - Sending emails or messages
  - Modifying user-facing content
  - Generating reports with data access

HIGH RISK (human approval required):
  - Executing database queries
  - Making financial transactions
  - Modifying access controls or permissions
  - Deleting data
  - Sending communications to external parties
```

### Implementation Pattern

```python
class HumanApprovalGate:
    """Require human approval for high-risk AI actions."""

    HIGH_RISK_ACTIONS = {
        "delete_record", "send_email", "execute_query",
        "modify_permissions", "financial_transaction",
    }

    MEDIUM_RISK_ACTIONS = {
        "update_record", "create_report", "send_notification",
    }

    def check(self, action: str, parameters: dict, user_id: str) -> dict:
        """Check if an AI-proposed action needs human approval."""
        if action in self.HIGH_RISK_ACTIONS:
            return {
                "approved": False,
                "requires_approval": True,
                "message": f"AI wants to perform: {action}\n"
                           f"Parameters: {json.dumps(parameters, indent=2)}\n"
                           f"Approve or deny?",
                "timeout_seconds": 300,  # Auto-deny after 5 min
            }

        if action in self.MEDIUM_RISK_ACTIONS:
            return {
                "approved": False,
                "requires_approval": True,
                "message": f"AI is about to: {action}. Continue?",
                "timeout_seconds": 60,
            }

        return {"approved": True, "requires_approval": False}
```

### Design Considerations

- **Timeout to deny:** If no human responds within the timeout, default to deny. Never default to approve.
- **Clear action description:** Show the human exactly what the AI wants to do, in plain language.
- **Batch approval:** For repetitive actions (e.g., processing 100 similar records), let the human approve the pattern once rather than each individual action.
- **Audit trail:** Log every approval decision with the approver's identity and timestamp.

## Cost and Latency Considerations

Security controls add latency and cost. Here's how to balance them:

### Latency Budget

```
Typical AI request latency breakdown:

Input validation:     5-20ms   (regex, PII scan)
Model inference:      500-3000ms  (the big one)
Output filtering:     5-20ms   (regex, content check)
Logging:              1-5ms    (async)
                      -----------
Total overhead:       ~40ms added by security controls
                      (<5% of total request time)
```

Security controls are cheap compared to model inference. Don't skip them to save milliseconds.

### Cost Optimization

| Control | Cost Impact | Optimization |
|---|---|---|
| Input validation | Negligible (CPU only) | None needed |
| Input classifier (ML) | Small (fast model) | Batch requests, cache results |
| Output filtering | Negligible (CPU only) | None needed |
| Output classifier (ML) | Small (fast model) | Only run when input risk score > 0 |
| Comprehensive logging | Storage costs | Log levels: debug in dev, warn in prod |
| Human-in-the-loop | Time cost (waiting for human) | Only for high-risk actions |

> **Architecture Tip:** The most expensive security "control" is no security at all. A single prompt injection incident that leaks customer data will cost orders of magnitude more than running input/output scanners on every request.

## Key Takeaways

- **Input validation is your first line of defense.** Build a multi-stage pipeline: length check, format check, PII scan, injection scoring, content classification. Use traditional code, not the LLM.
- **Output filtering is equally important.** Scan model output for PII, system prompt leakage, and harmful content before it reaches users or downstream systems.
- **Centralize guardrails in a proxy.** The guardrails proxy pattern gives you a single point of enforcement, consistent security across applications, and centralized logging.
- **Rate limit on multiple dimensions:** Requests per minute, tokens per minute, tokens per day, and concurrent requests. This prevents abuse and controls costs.
- **Log everything, monitor actively.** Hash sensitive inputs for privacy, track security metrics, and build SIEM detection rules specific to AI threats.
- **Use human-in-the-loop for high-risk actions.** Default to deny on timeout. Show clear descriptions of proposed actions. Log all approval decisions.
- **Security controls are cheap.** Input and output filtering add ~40ms — less than 5% of typical AI request latency. The cost of not having them is much higher.
