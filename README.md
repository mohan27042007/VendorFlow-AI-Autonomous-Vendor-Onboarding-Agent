# VendorFlow AI

**Autonomous Vendor Onboarding Agent**

Live App: https://vendorflow-ai0.streamlit.app  
GitHub: https://github.com/mohan27042007/VendorFlow-AI-Autonomous-Vendor-Onboarding-Agent  
Hackathon: TinyFish $2M Pre-Accelerator Hackathon 2026

An agentic infrastructure layer that autonomously onboards B2B companies to vendor portals -- navigating forms, uploading documents, and tracking approvals without any human involvement.

[![Live App](https://img.shields.io/badge/Live%20App-Streamlit-green)](https://vendorflow-ai0.streamlit.app)
[![Built with TinyFish](https://img.shields.io/badge/Powered%20by-TinyFish-blue)](https://tinyfish.ai)

---

## The Problem

Every B2B company onboards 50-200 vendors per year. Each portal takes **2-4 hours of manual work** -- filling multi-page forms, uploading GST/PAN certificates, managing logins, tracking approvals. That's **100-800 hours of wasted labor per year**, per company.

Vendor portals have **no public API**. The only way to automate this is with a real browser agent navigating live websites.

---

## The Solution

VendorFlow AI uses the **TinyFish Web Agent API** to:
1. Navigate to each vendor portal in a real browser
2. Fill every form field from the company profile
3. Upload compliance documents (GST cert, PAN card, etc.)
4. Submit and track approval status
5. Learn from each portal run to get faster next time

---

## Features

| Feature | Status |
|---|---|
| Preflight Compliance Scanner | Live |
| Autonomous Portal Navigation (TinyFish) | Live |
| Multi-Portal Parallel Execution | Live |
| Portal Blueprint Learning | Live |
| Layout-Change Resilience Mode | Live |
| Time-Lapse Run Replay | Live |
| ROI and Throughput Dashboard | Live |
| "What If Manual?" Simulator | Live |
| Scoped Data Vaults per Portal | Live |
| PDF Report Generator | Live |

---

## Tech Stack

| Component | Technology |
|---|---|
| Language | Python 3.11+ |
| Agent Runtime | TinyFish Web Agent API (SSE streaming) |
| Frontend | Streamlit (4 pages) |
| Database | SQLite (stdlib sqlite3) |
| HTTP Client | httpx (async) |
| Parallelism | asyncio + asyncio.gather() |
| Validation | pydantic v2 |
| PDF Handling | PyMuPDF (fitz) |
| PDF Reports | FPDF2 |
| Config | python-dotenv + PyYAML |
| Testing | pytest |

---

## How to Run Locally

### 1. Clone the repo
```bash
git clone https://github.com/mohan27042007/VendorFlow-AI-Autonomous-Vendor-Onboarding-Agent
cd VendorFlow-AI-Autonomous-Vendor-Onboarding-Agent/vendorflow
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up environment
```bash
cp .env.example .env
# Open .env and add your TINYFISH_API_KEY
```

### 4. Run the app
```bash
streamlit run ui/app.py
```

### 5. Use the app
1. Go to **Setup** and fill in the company profile, then upload documents
2. Click **Run Preflight** and confirm all checks pass
3. Go to **Run**, enter portal URLs, and click Start Onboarding
4. Watch the TinyFish agent navigate real portals live
5. Go to **Dashboard** to see hours saved and ROI metrics
6. Go to **Replay** to watch a time-lapse of each agent run

---

## Project Structure

```
vendorflow/
  config/               Configuration and policy rules
  core/                 All backend logic
    tinyfish_client.py  TinyFish API wrapper
    profile.py          Company profile schema
    document_vault.py   Document upload and retrieval
    preflight.py        Compliance scanner
    blueprint.py        Portal blueprint save/load
    orchestrator.py     Main async run coordinator
    report_generator.py PDF report output
  db/                   SQLite database layer
  ui/                   Streamlit pages and components
    pages/
      1_Setup.py        Profile input and document upload
      2_Run.py          Portal run configuration and live progress
      3_Dashboard.py    ROI metrics and run history
      4_Replay.py       Screenshot replay viewer
  tests/                pytest test suite (23 tests)
  data/                 Runtime data (gitignored)
```

---

## Demo Portals Tested

- IndiaMART Seller Registration
- TradeIndia Supplier Registration
- GeM Government e-Marketplace
- Flipkart Seller Hub
- Amazon Seller Central India

---

## Testing

```bash
cd vendorflow
python -m pytest tests/ -v
```

23 tests covering profile validation, TinyFish client mocking, orchestrator retry logic, preflight compliance checks, batch execution, and scoped data vaults.

---

## License

MIT License -- see [LICENSE](LICENSE) for details.

Built for the TinyFish $2M Pre-Accelerator Hackathon 2026  
Powered by [TinyFish Web Agent API](https://tinyfish.ai)
