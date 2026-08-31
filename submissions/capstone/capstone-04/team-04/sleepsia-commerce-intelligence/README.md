# 🛒 Sleepsia Commerce Intelligence Platform

**AI-Powered E-commerce Analytics & Automated Reporting System**

A comprehensive enterprise platform enabling multi-marketplace sellers to gain actionable business intelligence through advanced KPI analytics, multi-agent AI analysis, and automated email reporting — delivered through an interactive dashboard and daily executive email briefings.

---

## 📋 Project Overview

**Sleepsia** helps e-commerce sellers (Amazon, Flipkart, Shopify, Quick Commerce, and 14 total channels) analyze their business performance across multiple dimensions:

- **Sales Analytics** — Revenue, orders, AOV, profit margins
- **AI Multi-Agent Pipeline** — 9 specialist agents (sales, advertising, inventory, logistics, competitor, product, marketplace, data validation, reporting) coordinated by a supervisor agent
- **Advertising Intelligence** — ROAS, ACOS/TACoS, campaign performance
- **Inventory & Darkstore Management** — Stock levels, turnover rates, stockout risk alerts
- **Shipping & Logistics** — Delivery times, costs, carrier performance
- **Competitive Analysis** — Pricing trends, market positioning
- **AI Insights** — Gemini-powered root-cause analysis and recommendations
- **Automated Reports** — Daily/weekly executive briefings sent via email (SMTP)
- **Chat BI Assistant** — Natural-language Q&A over your commerce data

**Authentication:** none required. There is no login screen and no Google Sign-in anywhere in the app — the dashboard and email system are open on load. Email delivery uses a single server-side SMTP account configured in `.env` (not per-user OAuth).

---

## 🏗️ Project Structure

```
sleepsia-commerce-intelligence/
├── backend/                          # Django Python Backend
│   ├── services/                    # Business logic services
│   │   ├── kpi_engine.py           # KPI calculations (50+ metrics)
│   │   ├── email_service.py        # SMTP email composition & sending
│   │   ├── scheduler.py            # Email schedule management
│   │   ├── dataset_service.py      # Data loading & caching
│   │   ├── gemini_service.py       # AI insights via Google Gemini
│   │   ├── multi_agent_supervisor.py # Agent orchestration & report builder
│   │   ├── report_image_generator.py # SVG dashboard generation
│   │   └── specialist_agents/      # Sales, Advertising, Inventory, etc. agents
│   ├── middleware/                  # CORS, security, error handling
│   ├── exceptions/                  # Custom error types
│   ├── monitoring/                  # Metrics & alerts
│   ├── config/                      # Configuration management
│   ├── security/                    # Token encryption utilities
│   └── settings.py                 # Django configuration (reads .env)
│
├── api/                             # Django REST API
│   ├── views.py                    # API endpoint handlers
│   ├── urls.py                     # URL routing
│   └── serializers.py              # Input validation
│
├── src/                             # React TypeScript Frontend
│   ├── components/                 # React components
│   │   ├── Header.tsx              # Top nav, filters, role badge
│   │   ├── ExecutiveOverview.tsx   # Main dashboard tab
│   │   ├── MultiAgentOrchestrator.tsx # AI pipeline visualization
│   │   ├── AgentLogicAnalysisView.tsx # Formula/logic transparency tab
│   │   ├── StockManagement.tsx     # Stocks & darkstores tab
│   │   ├── CategoryIntelligence.tsx
│   │   ├── MarketplaceAnalysis.tsx
│   │   ├── AdvertisingAnalysis.tsx
│   │   ├── ProductIntelligence.tsx
│   │   ├── CompetitorIntelligence.tsx
│   │   ├── ShippingIntelligence.tsx
│   │   ├── AiInsights.tsx          # Root cause insights tab
│   │   ├── DailyReportView.tsx     # Report preview tab
│   │   ├── ChatAssistant.tsx       # Chat BI tab
│   │   ├── SettingsView.tsx        # Settings & schedules tab
│   │   ├── EmailModal.tsx          # Send-now + scheduler modal
│   │   ├── RoleSwitcherModal.tsx   # RBAC persona switcher
│   │   ├── UploadModal.tsx         # Dataset upload
│   │   ├── AgentExecutionModal.tsx # Live agent execution telemetry
│   │   └── ErrorBoundary.tsx       # Catches render errors, avoids blank screen
│   ├── services/                   # API clients & business logic
│   │   ├── datasetService.ts
│   │   ├── kpiEngine.ts
│   │   └── multiAgentSupervisor.ts
│   ├── types/                      # TypeScript type definitions (incl. RBAC)
│   ├── specialistAgents/           # Frontend-side deterministic agent logic
│   ├── hooks/                      # Custom React hooks
│   └── data/                       # Sample/default datasets
│
├── tests/                          # Test suite
│   ├── unit/
│   ├── integration/
│   └── conftest.py
│
├── docs/                           # Additional documentation
│   └── API.md                      # Full API reference
│
├── .env                            # Environment configuration (create this — see below)
├── pyproject.toml                  # Python dependencies (uv/pip)
├── package.json                    # Node dependencies & scripts
├── vite.config.ts                  # Frontend dev server config (port 3000, proxies /api → :8000)
├── manage.py                       # Django CLI entrypoint
├── index.html                      # Frontend HTML shell
└── test_email.py                   # Standalone SMTP sanity-check script
```

---

## 💻 Technology Stack

### **Backend**
- **Framework:** Django 5.2 (Python 3.13+)
- **API:** Django REST Framework
- **Database:** SQLite (default, dev) — PostgreSQL supported for production
- **AI:** Google Generative AI (Gemini) — optional
- **Email:** Python `smtplib` over SMTP (Gmail, Outlook, or any SMTP provider)
- **Package manager:** [`uv`](https://docs.astral.sh/uv/) (or plain `pip`)

### **Frontend**
- **Framework:** React 19 with TypeScript
- **Build tool:** Vite 6
- **Styling:** Tailwind CSS v4
- **Icons:** Lucide React
- **Charts:** Recharts
- **Excel handling:** `xlsx`, `jspdf` for exports

---

## 🚀 Setup & Installation

### **Prerequisites**
- Python 3.13+
- Node.js 18+ and npm
- A Gmail account (or any SMTP provider) for sending reports

### **1. Install backend dependencies**

Using `uv` (recommended — matches the `package.json` scripts):
```bash
uv sync
```

Or with plain `pip`:
```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS/Linux
pip install django>=5.2 djangorestframework django-cors-headers google-genai openpyxl pandas python-dotenv requests
```

### **2. Install frontend dependencies**

```bash
npm install
```

### **3. Create the `.env` file**

Create a file named `.env` in the project root (same folder as `manage.py`). This is the **single source of configuration** — the backend loads it automatically via `python-dotenv`.

```bash
# ============================================
# DJANGO SETTINGS
# ============================================
ENVIRONMENT=development
DEBUG=True
DJANGO_SECRET_KEY=dev-only-change-this-string-to-anything-random
ALLOWED_HOSTS=localhost,127.0.0.1,localhost:5173,127.0.0.1:5173

# ============================================
# DATABASE (SQLite by default — no setup needed)
# ============================================
DATABASE_ENGINE=django.db.backends.sqlite3
DATABASE_NAME=db.sqlite3

# Uncomment to use PostgreSQL instead:
# DATABASE_ENGINE=django.db.backends.postgresql
# DATABASE_NAME=sleepsia_db
# DATABASE_USER=postgres
# DATABASE_PASSWORD=your_password
# DATABASE_HOST=localhost
# DATABASE_PORT=5432

# ============================================
# EMAIL / SMTP — REQUIRED for report sending
# ============================================
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-16-character-gmail-app-password
SMTP_RECIPIENTS=recipient1@example.com,recipient2@example.com

TIMEZONE=Asia/Kolkata
AUTO_SEND_ENABLED=True

# ============================================
# GOOGLE GEMINI AI (optional — enables live AI insights)
# ============================================
GOOGLE_GENAI_API_KEY=

# ============================================
# CORS
# ============================================
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173,http://127.0.0.1:3000,http://127.0.0.1:5173,http://localhost:8000

# ============================================
# LOGGING
# ============================================
LOG_LEVEL=INFO
ENABLE_STRUCTURED_LOGGING=True

# ============================================
# SESSION
# ============================================
SESSION_COOKIE_AGE=86400
SESSION_COOKIE_SECURE=False
SESSION_COOKIE_HTTPONLY=True
SESSION_COOKIE_SAMESITE=Lax

# ============================================
# FILE UPLOADS
# ============================================
MAX_UPLOAD_SIZE=104857600
ALLOWED_FILE_TYPES=xlsx,xls,csv

# ============================================
# API RATE LIMITING
# ============================================
RATE_LIMIT_ANON=100/hour
RATE_LIMIT_USER=1000/hour

# ============================================
# CACHE
# ============================================
CACHE_TIMEOUT=3600
CACHE_BACKEND=django.core.cache.backends.locmem.LocMemCache

# ============================================
# SECURITY (production hardening — leave defaults for local dev)
# ============================================
SECURE_SSL_REDIRECT=False
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
X_FRAME_OPTIONS=DENY
SECURE_CONTENT_SECURITY_POLICY_REPORT_ONLY=True

# ============================================
# TIME & DATE
# ============================================
TIME_ZONE=Asia/Kolkata
USE_TZ=True
DATE_FORMAT=Y-m-d
TIME_FORMAT=H:i:s

# ============================================
# FEATURE FLAGS
# ============================================
ENABLE_MULTI_AGENT_ANALYSIS=True
ENABLE_EMAIL_SCHEDULER=True
ENABLE_API_DOCUMENTATION=True
ENABLE_PERFORMANCE_MONITORING=True
```

#### Getting a Gmail App Password (required for `SMTP_PASSWORD`)

Gmail rejects your normal account password for SMTP — you need a 16-character **App Password**:

1. Go to <https://myaccount.google.com/apppasswords> (requires 2-Step Verification to be enabled on the account)
2. Select app **"Mail"**, device **"Windows Computer"** (or Other)
3. Google generates a 16-character password like `abcd efgh ijkl mnop`
4. Paste it as `SMTP_PASSWORD` in `.env` — spaces are fine, keep it exactly as shown

> Using a different provider (Outlook, custom SMTP, etc.)? Just change `SMTP_HOST` / `SMTP_PORT` accordingly (e.g. `smtp.office365.com`, port `587`).

### **4. Verify the .env is picked up (optional sanity check)**

```bash
python test_email.py
```
This sends a real test email using your `.env` credentials and prints success/failure — run it any time you change SMTP settings.

---

## ▶️ Running the App

Two servers run side-by-side: Django (API, port `8000`) and Vite (frontend, port `3000`).

**Terminal 1 — Backend:**
```bash
python manage.py runserver 0.0.0.0:8000 --nothreading
```
> `--nothreading` avoids a Windows-specific file-watcher startup issue. On macOS/Linux you can drop it.

**Terminal 2 — Frontend:**
```bash
npm run dev
```

Then open **http://localhost:3000**. The Vite dev server proxies all `/api/*` requests to the Django backend automatically (configured in `vite.config.ts`), so no CORS setup is needed for local development.

To stop either server, press `Ctrl+C` in its terminal.

### Production build
```bash
npm run build      # outputs to dist/
```

---

## 🗺️ Dashboard Tabs

| Tab | What it shows |
|---|---|
| **Executive Overview** | Top-level KPIs, wins/risks, AI briefing header |
| **AI Multi-Agent Pipeline** | Live visualization of the 9-agent supervisor pipeline |
| **Analysis Logic & Formulas** | Transparency view of exactly how each KPI/metric is calculated |
| **Stocks & Darkstores** | Inventory levels, stockout risk alerts per warehouse |
| **Category Intelligence** | Performance broken down by product category |
| **Marketplaces** | Per-channel (14 channels) sales & profit leaderboard |
| **Advertising & TACoS** | Ad spend, ROAS, ACOS, campaign performance |
| **Product Intelligence** | SKU-level performance |
| **Competitor Matrix** | Pricing/positioning vs competitors |
| **Shipping & Logistics** | Delivery times, carrier costs; supports logistics data upload |
| **Root Cause Insights** | AI-generated findings with thumbs up/down feedback loop |
| **Daily Briefing Report** | Full formatted report preview, with "Send Email" shortcut |
| **Chat BI Assistant** | Ask natural-language questions about the loaded dataset |
| **Settings & Schedules** | Manage recipients, send test/live emails, configure schedules |

Role personas (via the role-switcher badge in the header) filter which tabs are visible per persona — Admin sees all 14; other personas (Executive, Marketplace Manager, Advertising Manager, Inventory/Stock Manager, Product Manager) see a scoped subset. This is a UI/demo persona switch, not an authentication system.

---

## 📧 Email Reporting

Two ways to send reports, both SMTP-based (no Google Sign-in involved):

1. **Send Report** button (header, always visible) → opens the **Email Modal**:
   - **Send Now** tab — instant one-off dispatch with custom recipients/subject, plus a "Send Sandbox Test" option
   - **Automated Schedulers** tab — create/edit/pause/delete recurring jobs (Daily / Weekdays / Weekly / Hourly), with a "Run Now" trigger per job
2. **Settings & Schedules** tab — manage the default recipient list and fire a quick test/live send

Each email includes:
- AI-generated executive summary
- KPI dashboard table (revenue, profit, orders, margins)
- Key wins / operational risks
- Marketplace leaderboard
- Prioritized action directives
- An SVG dashboard attachment

---

## 📊 Key API Endpoints

```
GET  /api/health                    System status
GET  /api/settings                  Email settings & send history
POST /api/settings                  Save email settings

POST /api/email/send-test           Send a sandbox test email
POST /api/email/send-report         Send the live executive report
GET  /api/schedules                 List all email schedules
POST /api/schedules                 Create a schedule
PUT  /api/schedules/{id}            Update a schedule
DELETE /api/schedules/{id}          Delete a schedule
POST /api/schedules/{id}/toggle     Enable/disable a schedule
POST /api/schedules/{id}/run-now    Execute a schedule immediately

POST /api/dataset/upload            Upload a workbook (xlsx/xls/csv)
GET  /api/dataset/summary           Dataset metadata
POST /api/kpis                      Calculate KPIs
POST /api/agents/analyze            Run multi-agent analysis
POST /api/agents/feedback           Record thumbs up/down on a finding
POST /api/agents/chat               Chat BI Q&A
POST /api/report/generate           Generate the daily report
```

See `docs/API.md` for the complete reference.

---

## 🧪 Testing

```bash
pytest                    # All backend tests
pytest tests/unit -v
pytest tests/integration -v
pytest --cov              # Coverage report

npm run lint               # TypeScript type-check (tsc --noEmit)
```

---

## 🐛 Troubleshooting

**Blank white screen on the frontend**
- Hard refresh (`Ctrl+F5`) — stale build cache is the usual cause
- Check the backend is actually running: `curl http://localhost:8000/api/health`
- Open the browser console (F12) — an `ErrorBoundary` is wired in, so a real crash now shows an error panel with a stack trace instead of a blank page

**"Port already in use" when starting the frontend**
- Another process is holding port 3000. Vite will auto-pick the next free port (3001, 3002…) and print it in the terminal — use that URL, or free port 3000 first:
  ```bash
  # Windows
  netstat -ano | findstr :3000
  taskkill /F /PID <pid>
  ```

**Email fails with "Username and Password not accepted" (SMTP 535)**
- You're using your normal Gmail password instead of an **App Password** — see the setup steps above
- Double-check `SMTP_USER` matches the account the App Password was generated for
- Run `python test_email.py` to isolate whether it's a `.env` problem or a frontend/backend wiring problem

**Django won't start on Windows**
```bash
python manage.py runserver 0.0.0.0:8000 --nothreading
```

**Changes to `.env` don't take effect**
- Restart the Django server — `.env` is loaded once at process start via `load_dotenv()`

---

## 📝 License

Proprietary — Agile Ventures.

---

**Last Updated:** August 31, 2026
