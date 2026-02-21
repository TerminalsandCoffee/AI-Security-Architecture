# Exercise 4: AI Supply Chain Audit

## Objective

Audit a sample AI project's dependencies, model sources, and pipeline for security risks. You'll review a project's configuration files, identify supply chain vulnerabilities, and create a risk register — the same process you'd use to evaluate any AI project before production deployment.

**Difficulty:** Beginner-Intermediate
**Time estimate:** 30-40 minutes
**Prerequisites:** Read Chapter 8

---

## Scenario: SentimentBot

Your company is evaluating an open-source project called "SentimentBot" — a sentiment analysis tool that classifies customer feedback as positive, negative, or neutral. The team wants to deploy it internally to automatically triage customer support tickets.

You've been asked to perform a supply chain security audit before deployment.

Below are the project's key configuration files. Review each one and identify the risks.

### File 1: requirements.txt

```
torch==2.1.0
transformers>=4.30.0
numpy
flask==2.3.2
gunicorn
requests
huggingface-hub
sentencepiece
protobuf
pyyaml
boto3
python-dotenv
accelerate
bitsandbytes
scikit-learn==1.3.0
```

### File 2: model_config.json

```json
{
  "model_name": "sentiment-analyzer-v2",
  "source": "https://huggingface.co/randomuser42/sentiment-bert-uncased",
  "format": "pytorch_model.bin",
  "base_model": "bert-base-uncased",
  "fine_tuned_on": "custom dataset (internal + scraped reviews)",
  "last_updated": "2024-08-15",
  "download_url": "https://huggingface.co/randomuser42/sentiment-bert-uncased/resolve/main/pytorch_model.bin",
  "checksum": "",
  "license": "unknown"
}
```

### File 3: pipeline.sh (training/deployment script)

```bash
#!/bin/bash
# Download and deploy the sentiment model

# Download model from Hugging Face
wget https://huggingface.co/randomuser42/sentiment-bert-uncased/resolve/main/pytorch_model.bin \
  -O models/sentiment_model.bin

# Download tokenizer
wget https://huggingface.co/randomuser42/sentiment-bert-uncased/resolve/main/tokenizer.json \
  -O models/tokenizer.json

# Load and test model
python -c "
import torch
model = torch.load('models/sentiment_model.bin')
print('Model loaded successfully')
print(f'Parameters: {sum(p.numel() for p in model.parameters())}')
"

# Deploy
pip install -r requirements.txt
gunicorn app:app --bind 0.0.0.0:8080
```

### File 4: app.py (relevant excerpt)

```python
import torch
from flask import Flask, request, jsonify
from transformers import AutoTokenizer

app = Flask(__name__)

# Load model at startup
MODEL = torch.load("models/sentiment_model.bin")
TOKENIZER = AutoTokenizer.from_pretrained("randomuser42/sentiment-bert-uncased")

@app.route("/analyze", methods=["POST"])
def analyze():
    text = request.json.get("text", "")
    # ... sentiment analysis logic ...
    return jsonify({"sentiment": result, "confidence": score})

@app.route("/health")
def health():
    return "OK"
```

---

## Your Task: Identify Supply Chain Risks

Review all four files and identify as many supply chain security risks as you can. For each risk, document:

1. **File:** Which file contains the risk
2. **Risk:** What the vulnerability is
3. **Impact:** What could happen if exploited
4. **Severity:** Critical / High / Medium / Low
5. **Recommendation:** How to fix it

### Risk Register Worksheet

| # | File | Risk | Impact | Severity | Recommendation |
|---|---|---|---|---|---|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |
| 6 | | | | | |
| 7 | | | | | |
| 8 | | | | | |
| 9 | | | | | |
| 10 | | | | | |

### Bonus Questions

1. What additional information would you request from the development team before approving deployment?
2. What changes would you require before this project goes to production?
3. How would you create an AI SBOM for this project?

---

## Solution Guide

### Complete Risk Register

| # | File | Risk | Impact | Severity | Recommendation |
|---|---|---|---|---|---|
| 1 | model_config.json | Model from unverified community user ("randomuser42") | Could be a backdoored or malicious model — no way to verify creator's identity or intentions | Critical | Use models only from verified organizations. If using community models, perform thorough evaluation. |
| 2 | model_config.json / pipeline.sh | Model in pickle format (pytorch_model.bin) — can execute arbitrary code on load | Remote code execution when loading the model. Attacker can get a reverse shell, steal data, install malware. | Critical | Convert to safetensors format. Use `torch.load(weights_only=True)` at minimum. |
| 3 | app.py | `torch.load()` without `weights_only=True` | Arbitrary code execution at application startup. Any code embedded in the pickle file runs automatically. | Critical | Use `torch.load("model.bin", weights_only=True)` or migrate to safetensors format. |
| 4 | model_config.json | Empty checksum field — no integrity verification | No way to detect if the model file was tampered with after download. An attacker could replace the model with a backdoored version. | High | Generate and verify SHA-256 hash of all model files. Store hashes in a signed manifest. |
| 5 | requirements.txt | Unpinned dependencies (numpy, gunicorn, requests, etc.) | Any `pip install` could pull a compromised version. Supply chain attacks on PyPI are common. | High | Pin ALL dependency versions. Use `pip-audit` to scan for known vulnerabilities. |
| 6 | requirements.txt | `transformers>=4.30.0` — minimum version, not pinned | Could install any future version, including ones with vulnerabilities or breaking changes | High | Pin to exact version: `transformers==4.47.0` |
| 7 | pipeline.sh | Direct `wget` download with no integrity check | Model file downloaded over HTTPS but no hash verification. MitM or CDN compromise could serve a malicious file. | High | Add hash verification after download: `echo "expected_hash model.bin" \| sha256sum -c` |
| 8 | pipeline.sh | Binding to `0.0.0.0:8080` | Service listens on all interfaces, accessible from any network. No authentication on the API endpoint. | Medium | Bind to `127.0.0.1` or deploy behind a reverse proxy with authentication. Add API key auth to the `/analyze` endpoint. |
| 9 | model_config.json | License listed as "unknown" | Legal risk — deploying a model without knowing its license could violate terms. Some licenses prohibit commercial use. | Medium | Determine the license before deployment. If license is restrictive or unknown, choose an alternative model. |
| 10 | model_config.json | Model last updated 2024-08-15 — over a year old | Could have known vulnerabilities in the base model or fine-tuning. Training data may be outdated. | Medium | Evaluate against current models. Check for any published vulnerabilities in the base model (BERT). |
| 11 | pipeline.sh | `pip install` in deployment script without virtual environment | Could conflict with system packages or other applications. Harder to reproduce exact environment. | Low | Use a virtual environment or container. Pin all deps in a lockfile. |
| 12 | model_config.json | "Fine-tuned on: custom dataset (internal + scraped reviews)" | Scraped reviews may contain PII, copyrighted content, or biased data. No data provenance documentation. | Medium | Document data sources, get legal review on scraped data, check for PII in training data. |

### Bonus Answers

**1. Additional information to request:**
- Full model card for the sentiment-bert-uncased model
- Hash/checksum of the model file at the time of testing
- Data processing pipeline for the "scraped reviews" training data
- Results of any security evaluation or adversarial testing
- Who is "randomuser42" — any verifiable identity?
- Have transitive dependencies been audited?

**2. Required changes before production:**
- Replace `torch.load()` with safetensors or `weights_only=True` (Critical)
- Pin all dependency versions (High)
- Add model integrity verification (High)
- Add API authentication (Medium)
- Bind to 127.0.0.1 or deploy behind authenticated reverse proxy (Medium)
- Source the model from a verified organization or self-host a known-good model (Critical)

**3. AI SBOM for this project:**

```yaml
metadata:
  application: "SentimentBot"
  audit_date: "2026-02-21"
  auditor: "Your Name"

models:
  - name: "sentiment-bert-uncased"
    source: "huggingface.co/randomuser42"
    verified_org: false
    format: "pytorch_model.bin (pickle - UNSAFE)"
    base_model: "bert-base-uncased"
    checksum: "NOT PROVIDED - RISK"
    license: "unknown - RISK"

datasets:
  - name: "training data"
    sources: ["internal data", "scraped reviews"]
    pii_review: "not performed - RISK"
    legal_review: "not performed - RISK"

dependencies:
  - name: torch
    version: "2.1.0"
    pinned: true
  - name: transformers
    version: ">=4.30.0"
    pinned: false  # RISK
  - name: numpy
    version: "unpinned"
    pinned: false  # RISK
  # ... (all deps listed with pin status)

risks_identified: 12
critical_risks: 3
recommendation: "DO NOT DEPLOY until critical risks resolved"
```
