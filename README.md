# VendorFlow AI 🐟
### Autonomous Vendor Onboarding Agent — TinyFish $2M Pre-Accelerator Hackathon 2026

> An agentic infrastructure layer that autonomously onboards B2B companies 
> to vendor portals — navigating forms, uploading documents, and tracking 
> approvals without any human involvement.

[![Demo Video](https://img.shields.io/badge/Demo-Watch%20Now-red)](YOUR_VIDEO_URL)
[![Live App](https://img.shields.io/badge/Live%20App-Streamlit-green)](YOUR_STREAMLIT_URL)
[![Built with TinyFish](https://img.shields.io/badge/Powered%20by-TinyFish-blue)](https://tinyfish.ai)

---

## 🎯 The Problem

Every B2B company onboards 50–200 vendors per year.  
Each portal takes **2–4 hours of manual work** — filling multi-page forms,  
uploading GST/PAN certificates, managing logins, tracking approvals.  
That's **100–800 hours of wasted labor per year**, per company.

Vendor portals have **no public API**. The only way to automate this  
is with a real browser agent navigating live websites.

---

## ✅ The Solution

VendorFlow AI uses the **TinyFish Web Agent API** to:
1. Navigate to each vendor portal in a real browser
2. Fill every form field from the company profile
3. Upload compliance documents (GST cert, PAN card, etc.)
4. Submit and track approval status
5. Learn from each portal run to get faster next time

---

## 🚀 Demo

**Watch the agent onboard to 3 real portals in under 5 minutes:**  
👉 [Demo Video](YOUR_VIDEO_URL)  
👉 [Live App](YOUR_STREAMLIT_URL)

---

## ⚡ Features

| Feature | Status |
|---|---|
| Preflight Compliance Scanner | ✅ Live |
| Autonomous Portal Navigation (TinyFish) | ✅ Live |
| Multi-Portal Parallel Execution | ✅ Live |
| Portal Blueprint Learning | ✅ Live |
| Layout-Change Resilience Mode | ✅ Live |
| Time-Lapse Run Replay | ✅ Live |
| ROI & Throughput Dashboard | ✅ Live |
| "What If Manual?" Simulator | ✅ Live |
| Scoped Data Vaults per Portal | ✅ Live |
| PDF Report Generator | ✅ Live |

---

## 🛠 Tech Stack

- **Agent Runtime:** TinyFish Web Agent API
- **Backend:** Python 3.11, httpx (async), asyncio, pydantic
- **Document Handling:** PyMuPDF
- **Frontend:** Streamlit
- **Storage:** SQLite
- **Reports:** FPDF2

---

## 🏃 How to Run Locally

### 1. Clone the repo
```bash
git clone https://github.com/yourusername/vendorflow-ai
cd vendorflow-ai
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
1. Go to **Setup** → fill company profile → upload documents
2. Click **Run Preflight** → confirm all green
3. Go to **Run** → enter portal URLs → click Start Onboarding
4. Watch the TinyFish agent navigate real portals live
5. Go to **Dashboard** → see hours saved and ROI metrics
6. Go to **Replay** → watch time-lapse of each agent run

---

## 📁 Project Structure
```
vendorflow/
├── config/          # Settings and policy config
├── core/            # All backend logic
│   ├── tinyfish_client.py
│   ├── profile.py
│   ├── document_vault.py
│   ├── preflight.py
│   ├── blueprint.py
│   ├── orchestrator.py
│   └── report_generator.py
├── db/              # SQLite database layer
├── ui/              # Streamlit pages
│   └── pages/
│       ├── 1_Setup.py
│       ├── 2_Run.py
│       ├── 3_Dashboard.py
│       └── 4_Replay.py
├── tests/           # Unit tests
└── data/            # Runtime data (gitignored)
```

---

## 🌐 Demo Portals Tested

- IndiaMART Seller Registration
- TradeIndia Supplier Registration  
- GeM Government e-Marketplace
- Flipkart Seller Hub
- Amazon Seller Central India

---

## 📄 License

MIT License — see LICENSE file

---

*Built for the TinyFish $2M Pre-Accelerator Hackathon 2026*  
*Powered by [TinyFish Web Agent API](https://tinyfish.ai)*
```

---

## .gitignore — Full File
```
# Environment
.env
*.env

# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
*.egg-info/
dist/
build/
.eggs/

# Runtime data — never commit these
data/uploads/
data/screenshots/
data/reports/
data/blueprints/
data/*.db

# Virtual environment
venv/
env/
.venv/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Streamlit
.streamlit/secrets.toml

# Test artifacts
.pytest_cache/
.coverage
htmlcov/
```

---

## LICENSE — Use MIT (Simplest)

Create a file called `LICENSE` with this content:
```
MIT License

Copyright (c) 2026 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining 
a copy of this software and associated documentation files (the 
"Software"), to deal in the Software without restriction, including 
without limitation the rights to use, copy, modify, merge, publish, 
distribute, sublicense, and/or sell copies of the Software, and to 
permit persons to whom the Software is furnished to do so, subject to 
the following conditions:

The above copyright notice and this permission notice shall be 
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, 
EXPRESS OR IMPLIED.
```

---

## Final Repo Structure at Submission
```
vendorflow-ai/          ← GitHub repo root
├── README.md           ← judges read this first
├── LICENSE             ← MIT
├── .gitignore          
├── .env.example        ← template, no real keys
├── requirements.txt    
├── config/
├── core/
├── db/
├── ui/
├── tests/
└── data/               ← empty folder, gitignored contents
    └── .gitkeep        ← keeps the folder in git
