# Ocilar Python SDK

Official Python client for the [Ocilar API](https://ocilar.com) — CAPTCHA solving and document extraction.

## Install

```bash
pip install ocilar
```

## Quick Start

```python
from ocilar import OcilarClient

client = OcilarClient(api_key="sk-YOUR_KEY")

# Test connectivity
print(client.hello())

# Solve SAT CAPTCHA
import base64
with open("captcha.png", "rb") as f:
    img = base64.b64encode(f.read()).decode()

result = client.solve_sat(img)
print(result.text)       # "2VBF39"
print(result.latency_ms) # 67
print(result.task_id)    # "tsk_abc123"

# Extract data from CSF document
with open("csf.pdf", "rb") as f:
    doc = base64.b64encode(f.read()).decode()

result = client.extract_csf(doc)
print(result.data)  # {"rfc": "XAXX010101000", "nombre": "...", ...}
```

## Available Methods

### CAPTCHA Solving
- `solve_sat(image_base64)` — SAT Mexico
- `solve_imss(image_base64)` — IMSS Mexico
- `solve_image(image_base64)` — Generic image
- `solve_recaptcha_v2(site_key, site_url)` — reCAPTCHA v2
- `solve_recaptcha_v3(site_key, site_url, action)` — reCAPTCHA v3
- `solve_hcaptcha(site_key, site_url)` — hCaptcha
- `solve_cloudflare(site_url)` — Cloudflare Turnstile
- `solve_audio(audio_base64)` — Audio CAPTCHA

### Document AI
- `extract_csf(document_base64)` — Constancia de Situacion Fiscal
- `extract_ine(document_base64)` — INE / Voter ID
- `extract_cfdi(document_base64)` — CFDI Invoice
- `extract_curp(document_base64)` — CURP
- `extract_domicilio(document_base64)` — Proof of Address
- `extract_nomina(document_base64)` — Payroll Receipt
- `extract_generic(document_base64)` — Generic OCR

### Utilities
- `hello()` — Test API key
- `get_balance()` — Account balance and usage

## Free Tier

Every account gets **1,000 free solves** per CAPTCHA type and **50 free document extractions** per type. No credit card required.

## Links

- [Dashboard](https://console.ocilar.com)
- [API Docs](https://api.ocilar.com/api/v1/docs)
- [Pricing](https://ocilar.com/#pricing)
