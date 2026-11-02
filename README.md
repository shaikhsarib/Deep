# Deep (v2.5)

A production-grade, multi-agent Intelligence Center, Technical Audit, and Autonomous Sales Development Representative (SDR) platform inspired by **Paperclip** (multi-agent workforce management) and **REA** (Reverse-Engineering Anything / Chrome DevTools).

---

## ⚡ Key Capabilities & Autonomous Workforce

### 🤖 1. Specialized Agent Org Chart (Paperclip-Style)
- **`ScoutAgent`**: Autonomous lead discovery across Google Maps and Web search. Extracts verified phone numbers (+91 / E.164), sanitizes business names, and filters duplicates.
- **`AuditorAgent` (REA-Inspired)**: Deep technical & mobile site audits. Inspects TTFB response time, SSL certificates, smartphone viewport responsiveness (iPhone 14 390x844), missing WhatsApp direct ordering widgets (`wa.me`), and missing 1-click booking systems. Captures headless mobile snapshots via Playwright.
- **`CopywriterAgent`**: Synthesizes real audited flaws and quantified revenue loss into persuasive, conversion-focused WhatsApp (Hinglish/English) and consultative cold emails.
- **`ApprovalGate` (Human-in-the-Loop)**: Staging queue in the dashboard. Prevents cold-call spamming: managers can review, edit pitch copy, or 1-click approve for WhatsApp/Email dispatch.
- **`CloserAgent` (Inbound SDR)**: Evaluates incoming prospect replies, classifies intent (pricing objections, competitor agency objections, demo requests, unsubscribe), counters with audit proof, and drives prospects to book a meeting (Calendly).

### 🎯 2. Specialized Vertical Playbooks
- **Freight & Logistics**: Spotlights missing track-and-trace widgets, load booking friction, and slow RFQ turnaround.
- **Event Venues & Planners**: Audits mobile date availability checkers, virtual tours, and 1-click WhatsApp quote requests.
- **Local High-Ticket SMBs**: Focuses on mobile loading speed, click-to-call buttons, and local search visibility.

---

## 🏗️ Repository Architecture

The project adheres to a clean, senior-developer modular layout:

```text
Standard-autonomous/
├── config/              # Centralized environment settings & pitch claims
├── data/                # Local data storage (leads, sessions, screenshots)
├── docs/                # Architecture docs, flow charts & PDF audit reports
│   └── reports/         # Executive & technical research reports
├── legacy/              # Preserved V1 archive (engine, early scrapers)
├── logo/                # Official brand identity vectors (light & dark mode)
├── src/                 # Production Source Code
│   ├── agents/          # Multi-agent coordination & safety shields (ECC)
│   ├── api/             # FastAPI REST endpoints & Command Center Web UI
│   ├── core/            # System contracts & protocol definitions
│   ├── delivery/        # Multi-channel notification engine (WhatsApp, Email)
│   ├── models/          # Pydantic v2 domain schemas (Lead, Conversation)
│   ├── pipelines/       # End-to-end workflow orchestration
│   ├── scrapers/        # Resilient discovery scrapers (Maps, Web, Scrapling)
│   ├── services/        # Workforce, LLM gateway & technical auditing
│   └── storage/         # High-performance local JSON repository layer
├── tests/               # Pytest automated test suite
├── cli.py               # Unified Rich terminal CLI
├── main.py              # Primary production launcher (Server / CLI)
├── pyproject.toml       # Modern Python build & tool configuration
├── pytest.ini           # Pytest suite configuration
└── run_server.py        # Standalone FastAPI server launcher
```

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
playwright install chromium
```

### 2. Configure Environment
Copy `.env.example` to `.env` and set your credentials:
```bash
cp .env.example .env
```
Key configuration:
- `GEMINI_API_KEY`: Google Gemini API key (for AI value synthesis and SDR chats)
- `LLM_MODEL`: `gemini-2.5-flash`
- `TELEGRAM_BOT_TOKEN` & `TELEGRAM_CHAT_ID`: For instant lead capture alerts
- `TWILIO_ACCOUNT_SID` & `TWILIO_AUTH_TOKEN`: For WhatsApp message delivery
- `EMAIL_SENDER` & `EMAIL_PASSWORD`: For cold email delivery

---

## 🖥️ Running the Command Center

### Option A: Web Command Center (Recommended)
Launch the modern FastAPI web dashboard:
```bash
python main.py
# or
python run_server.py
```
Open **`http://127.0.0.1:8000`** in your browser to access:
1. **Live Discovery & Scouting**: Discover leads by category and location.
2. **REA Mobile Viewport Auditor**: Live iPhone 14 bezel displaying authentic mobile snapshots and proof verification.
3. **Outbox Human Sign-off**: Side-by-side WhatsApp & Cold Email preview with 1-click dispatch.
4. **Hermes Live Deals Desk**: Multi-turn inbound objection handling with instant objection pills and Calendly booking.
5. **Paperclip Live Studio Drawer**: Direct embedded connection to your standalone Paperclip instance running on `http://localhost:3100`.

### Option B: Unified Terminal CLI
```bash
# 1. Discover Leads via Google Maps & Web
python cli.py discover --category "logistics company" --location "Navi Mumbai" --limit 5

# 2. View All Stored Leads & Technical Audits
python cli.py list-leads

# 3. Generate AI Outreach & Preview Pitch Copy (Dry-Run)
python cli.py outreach --channel whatsapp --dry-run

# 4. Interactive Consultative Sales Chat
python cli.py chat --company "TransNational Freight" --category "logistics company"
```

---

## 🧪 Running Automated Tests

Run the full pytest suite:
```bash
pytest
```
Or run specific domain test suites:
```bash
pytest tests/test_v2_architecture.py
pytest tests/test_ecc_shield.py
pytest tests/test_paperclip_integration.py
```

---

## 📄 License & Attribution

Standard Autonomous is built for enterprise SDR automation and technical lead intelligence. Detailed architectural blueprints and audit reports are available in the [`docs/`](docs/) directory.
