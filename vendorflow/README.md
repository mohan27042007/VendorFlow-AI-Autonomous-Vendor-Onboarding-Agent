# VendorFlow AI

**Autonomous Vendor Onboarding Agent**

Live App: https://vendorflow-ai0.streamlit.app  
GitHub: https://github.com/mohan27042007/VendorFlow-AI-Autonomous-Vendor-Onboarding-Agent  
Hackathon: TinyFish $2M Pre-Accelerator Hackathon 2026

---

## What It Does

VendorFlow AI automates the entire vendor registration process across multiple B2B portals. Feed it a company profile and a list of portal URLs. It fills forms, uploads compliance documents, navigates multi-page wizards, and submits registrations -- no human touches a single form field.

Powered by the TinyFish Web Agent API, which provides a real browser agent capable of navigating live websites, managing authenticated sessions, handling file uploads, and executing multi-step workflows.

## The Problem

Every B2B company in India must register on dozens of vendor portals (IndiaMART, TradeIndia, GeM, Flipkart Seller Hub, Amazon Seller Central, etc.) before doing business. Each portal has a completely different UI, login system, and form structure. This takes 2-4 hours of skilled manual work per portal -- 100 to 800 hours of wasted labor per year per company.

VendorFlow AI eliminates this entirely.

## Features

**Core (V1)**
- Company Profile Manager with validation (GSTIN, PAN, TAN, IFSC)
- Document Vault -- upload once, use everywhere
- Autonomous Portal Navigation via TinyFish Web Agent API
- Multi-Portal Parallel Execution with concurrency control
- Live Status Dashboard with per-portal progress tracking
- Intelligent Field Mapping with Fallback
- Retry and Recovery Engine with exponential backoff
- Approval Status Monitor
- PDF Submission Report Generator

**Intelligence (V2)**
- Portal Blueprint Learning -- saves and reloads DOM selectors per portal
- Layout-Change Resilience Mode with exploratory fallback
- Preflight Compliance Scanner (GSTIN/PAN/TAN validation)
- Risk and Policy Guardrails via YAML configuration
- Adaptive Portal Prioritization
- Time-Lapse Run Replay with screenshot per action
- Scoped Data Vaults per Portal (minimum necessary data)
- Red-Flag Anomaly Alerts
- ROI and Throughput Dashboard
- "What If Manual?" Simulator

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

## Project Structure

```
vendorflow/
  config/               Configuration and settings
    settings.py         Environment variable loader
    portal_policies.yaml  Risk and policy rules
  core/                 Backend logic
    profile.py          Company profile schema
    document_vault.py   Document upload and retrieval
    preflight.py        Compliance scanner
    tinyfish_client.py  TinyFish API wrapper
    blueprint.py        Portal blueprint save/load
    resilience.py       Layout-change detection
    scoped_vault.py     Data scoping per portal
    orchestrator.py     Main async run coordinator
    report_generator.py PDF report output
  db/                   Database layer
    database.py         SQLite init, queries, migrations
    models.py           Dataclasses for results and summaries
  ui/                   Streamlit frontend
    app.py              Entry point
    pages/              1_Setup, 2_Run, 3_Dashboard, 4_Replay
    components/         Reusable UI components
  data/                 Runtime data (gitignored)
  tests/                pytest test suite
  deploy/               Streamlit deployment config
```

## Quick Start

### Prerequisites

- Python 3.11+
- TinyFish API key (from TinyFish $2M Pre-Accelerator Hackathon)

### Local Setup

```bash
git clone https://github.com/mohan27042007/VendorFlow-AI-Autonomous-Vendor-Onboarding-Agent
cd VendorFlow-AI-Autonomous-Vendor-Onboarding-Agent/vendorflow
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add your TINYFISH_API_KEY
streamlit run ui/app.py
```

### Streamlit Cloud Deployment

The app is deployed at: https://vendorflow-ai0.streamlit.app

To deploy your own instance:
1. Fork the repository
2. Connect to Streamlit Cloud
3. Set main file to `streamlit_app.py`
4. Add `TINYFISH_API_KEY` in Streamlit Cloud secrets

## How It Works

1. **Setup** -- Enter your company profile (legal name, GSTIN, PAN, TAN, bank details, contact info). Upload compliance documents (GST certificate, PAN card, etc.). Run the preflight check to validate everything.

2. **Run** -- Select target portals (IndiaMART, TradeIndia, GeM, etc.) and start onboarding. The TinyFish agent navigates each portal in parallel, fills forms, uploads documents, and submits registrations. Watch live progress with status cards and activity logs.

3. **Dashboard** -- View ROI metrics, run history, portal blueprints, and the "What If Manual?" simulator showing time and cost savings.

4. **Replay** -- Review screenshot replays of past agent runs to audit what was submitted on each portal.

## Testing

```bash
cd vendorflow
python -m pytest tests/ -v
```

23 tests covering profile validation, TinyFish client mocking, orchestrator retry logic, preflight compliance checks, batch execution, and scoped data vaults.

## License

MIT License -- see [LICENSE](LICENSE) for details.
