# DEEP — KNOWN DEFECTS & ARCHITECTURAL VULNERABILITY REGISTER (MILESTONE 0)

**Date**: November 5, 2026  
**Auditor**: Senior Software Architect & Autonomous Systems Engineer  
**Standard**: Independent QA Audit — Zero Sugarcoating, Grounded in Real Source Code

---

## 1. Executive Summary

A rigorous audit of the current Deep codebase reveals 10 substantive engineering defects and architectural compromises. These defects explain why prior development cycles experienced brittleness, slow test runs (353+ seconds), ungrounded pitch generation, and synchronization failures.

Each defect is documented below with its exact file location, technical root cause, severity, impact on business outcomes, and recommended engineering remedy.

---

## 2. Defect Ledger

| ID | Title | Severity | Location | Primary Risk |
| :---: | :--- | :---: | :--- | :--- |
| **DEF-01** | Disabled TLS Verification | **CRITICAL** | `src/services/site_inspector.py:53` | Security vulnerability, MITM exposure |
| **DEF-02** | Inaccurate TTFB Calculation | **MAJOR** | `src/services/site_inspector.py:54` | False technical claims in client outreach |
| **DEF-03** | Viewport Meta Check Equated to Mobile Responsive | **MAJOR** | `src/services/site_inspector.py:60` | False audit claims regarding client UI |
| **DEF-04** | Heuristic Score Labeled as Lighthouse Score | **MAJOR** | `src/services/site_inspector.py:82` | Reputational damage from unscientific audits |
| **DEF-05** | Synthetic Text Hashing Labeled as Evidence Proof | **MAJOR** | `src/services/evidence_verifier.py:34` | Anti-slop violation: ungrounded claims |
| **DEF-06** | Hardcoded Inbound Rebuttals & Static URLs | **MAJOR** | `src/services/inbound_closer.py:85` | Inflexible, non-agentic SDR responses |
| **DEF-07** | Pipeline Stage Conflation (`WON` on Booking) | **MINOR** | `src/services/inbound_closer.py:120` | Distorted sales funnel metrics in CRM |
| **DEF-08** | Flat-File JSON Concurrency Hazards | **CRITICAL** | `src/storage/repository.py:45` | Race conditions, silent data corruption |
| **DEF-09** | Synchronous Blocking I/O in Request Loop | **CRITICAL** | `src/services/workforce.py:100` | 6-minute test run, blocked ASGI threads |
| **DEF-10** | Simulated Sandbox vs. Real Computer Execution | **MAJOR** | `src/api/server.py:1000` | Inability to run real shell/browser tasks |

---

## 3. In-Depth Technical Defect Analysis

### DEF-01: Disabled TLS Verification
- **File**: [`src/services/site_inspector.py`](file:///c:/Users/JUBER/Downloads/main/my%20work/Standard%20autonomous/src/services/site_inspector.py#L53)
- **Code**:
  ```python
  async with httpx.AsyncClient(verify=False, timeout=12.0) as client:
      response = await client.get(url)
  ```
- **Root Cause**: `verify=False` was passed to httpx to prevent certificate validation errors on self-signed or misconfigured sites.
- **Risk**: Disables SSL/TLS verification across all outgoing inspection requests, exposing the scraper to Man-in-the-Middle (MITM) attacks and allowing fake responses to pollute the lead database.
- **Remedy**: Default to `verify=True`. If an SSL handshake fails, catch `httpx.ConnectError` or `ssl.SSLError`, record `ssl_valid=False` as a concrete empirical defect in the `AuditReport`, rather than ignoring the security warning.

---

### DEF-02: Inaccurate TTFB Calculation
- **File**: [`src/services/site_inspector.py`](file:///c:/Users/JUBER/Downloads/main/my%20work/Standard%20autonomous/src/services/site_inspector.py#L52-L55)
- **Code**:
  ```python
  start_time = time.perf_counter()
  response = await client.get(url)
  ttfb = (time.perf_counter() - start_time) * 1000
  ```
- **Root Cause**: Measuring the total wall-clock time between before `client.get()` and after the response body is completely downloaded.
- **Risk**: This measures `DNS lookup + TCP Handshake + TLS Negotiation + Request Transmission + TTFB + Body Download Time`. Labeling this total elapsed time as "TTFB" (Time-to-First-Byte) produces an inflated, technically false metric in outbound pitches. If a prospective CTO or webmaster inspects their real server TTFB, Deep’s claim will be immediately discredited.
- **Remedy**: Use low-level socket instrumentation or HTTPX response streaming hooks (`async with client.stream("GET", url) as res: first_byte = await res.aread(1)`) to measure exact Time-to-First-Byte.

---

### DEF-03: Viewport Meta Check Equated to Mobile Responsive
- **File**: [`src/services/site_inspector.py`](file:///c:/Users/JUBER/Downloads/main/my%20work/Standard%20autonomous/src/services/site_inspector.py#L60)
- **Code**:
  ```python
  mobile_responsive = "width=device-width" in response.text.lower()
  ```
- **Root Cause**: A simple string search for `<meta name="viewport" content="width=device-width">` in the HTML markup.
- **Risk**: A website can include a viewport meta tag but still be completely broken on mobile devices (e.g., fixed-width CSS containers overflowing the viewport, unclickable touch targets, or missing CSS media queries). Conversely, a site using modern responsive frameworks might configure viewports differently. Claiming a site is "not mobile responsive" solely because the exact string is absent is an ungrounded assertion.
- **Remedy**: Use Playwright headless browser at mobile viewport (`375x667`), evaluate `document.documentElement.scrollWidth > window.innerWidth`, and capture an actual visual screenshot as proof.

---

### DEF-04: Heuristic Score Mislabeled as Lighthouse Score
- **File**: [`src/services/site_inspector.py`](file:///c:/Users/JUBER/Downloads/main/my%20work/Standard%20autonomous/src/services/site_inspector.py#L75-L88)
- **Code**:
  ```python
  def calculate_heuristic_score(ttfb, ssl, mobile):
      score = 100
      if ttfb > 2000: score -= 30
      if not ssl: score -= 25
      if not mobile: score -= 25
      return max(score, 10)
  ```
- **Root Cause**: An arbitrary formula deducting points based on heuristic checks.
- **Risk**: In reports and pitches, this was presented as a "Lighthouse Performance Score". If a prospect runs official Google Lighthouse and sees a score of 88 while Deep claimed their score was 35, trust is permanently destroyed.
- **Remedy**: Clearly label heuristic scores as `Deep Technical Health Heuristic` or execute the actual Google Chrome Lighthouse CLI / PageSpeed Insights API when empirical scoring is required.

---

### DEF-05: Synthetic Text Hashing Labeled as Evidence Proof
- **File**: [`src/services/evidence_verifier.py`](file:///c:/Users/JUBER/Downloads/main/my%20work/Standard%20autonomous/src/services/evidence_verifier.py#L34)
- **Code**:
  ```python
  evidence_string = f"{lead_id}:{claim}:{expected_metric}"
  evidence_hash = hashlib.sha256(evidence_string.encode()).hexdigest()[:16]
  ```
- **Root Cause**: The SHA-256 hash was computed over the agent's own formatted text string rather than over raw captured network artifacts.
- **Risk**: A hash of synthetic text is not independent evidence; it only proves that the agent formatted that specific string. It does not prove the website actually had that flaw.
- **Remedy**: Compute the cryptographic hash over the raw HTTP response headers, socket timing log, or the PNG bytes of the Playwright viewport screenshot.

---

### DEF-06: Hardcoded Inbound Rebuttals & Static URLs
- **File**: [`src/services/inbound_closer.py`](file:///c:/Users/JUBER/Downloads/main/my%20work/Standard%20autonomous/src/services/inbound_closer.py#L85-L105)
- **Code**: Static `if-else` string templates returning predefined replies with `https://calendly.com/autonomous-agency/intro`.
- **Root Cause**: Fallback heuristic templates instead of a dynamic LLM agent loop with context retrieval.
- **Risk**: Fails to address nuanced prospect questions, specific industry terminology, or alternative meeting slots, breaking the conversational experience.
- **Remedy**: Connect `InboundCloserSDR` to the LLM agent harness, passing the lead's complete business profile, prior audit findings, and objection handling rules into the context window, while preserving deterministic guardrails via ECC AgentShield.

---

### DEF-07: Pipeline Stage Conflation (`WON` on Booking)
- **File**: [`src/services/inbound_closer.py`](file:///c:/Users/JUBER/Downloads/main/my%20work/Standard%20autonomous/src/services/inbound_closer.py#L120)
- **Root Cause**: Moving a lead to `status = LeadStatus.WON` immediately upon sending a Calendly booking link.
- **Risk**: Sending a booking link does not mean a demo was held, let alone that a contract was signed. In CRM best practices (Twenty, Salesforce), a deal progresses from `DEMO_SCHEDULED` ➔ `PROPOSAL_SENT` ➔ `CLOSED_WON`. Conflating booking with winning inflates pipeline revenue metrics.
- **Remedy**: Introduce explicit intermediate statuses: `DEMO_BOOKED`, `MEETING_COMPLETED`, and reserve `CLOSED_WON` for actual payment or contract execution.

---

### DEF-08: Flat-File JSON Concurrency Hazards
- **File**: [`src/storage/repository.py`](file:///c:/Users/JUBER/Downloads/main/my%20work/Standard%20autonomous/src/storage/repository.py#L45)
- **Code**: `json.dump()` directly into `data/leads.json` without file locking (`fcntl` / `msvcrt`) or transactional staging.
- **Root Cause**: Simple file write without concurrency protection.
- **Risk**: Simultaneous background heartbeats, API approvals, and scraper insertions can write to `leads.json` at the exact same millisecond, corrupting the JSON structure and dropping lead records.
- **Remedy**: Implement atomic file replacement (`write to temp file then os.replace()`) and wrap write operations in an asynchronous threading/process mutex lock, paving the path to SQLite/PostgreSQL storage.

---

### DEF-09: Synchronous Blocking I/O in Pipeline Loop
- **File**: [`src/services/workforce.py`](file:///c:/Users/JUBER/Downloads/main/my%20work/Standard%20autonomous/src/services/workforce.py#L100-L105)
- **Root Cause**: Inside `process_lead_through_pipeline()`, synchronous calls to `deep_research_engine.research_business()` invoke `DDGS().text()` (DuckDuckGo search) and `site_inspector.audit()` synchronously.
- **Risk**: This is the exact reason our baseline test run took **353.94 seconds (nearly 6 minutes)**. Every test that triggered a heartbeat or pipeline loop made live synchronous web requests. If DuckDuckGo rate limits the IP, the entire platform hangs.
- **Remedy**:
  1. Decouple pipeline execution into asynchronous background tasks with BullMQ/Celery or FastAPI `BackgroundTasks`.
  2. In test fixtures, strictly mock external network calls (`ddgs`, `httpx`, `Playwright`) so test suites run in under 5 seconds with deterministic assertions.

---

### DEF-10: Simulated Sandbox vs. Real Computer Execution
- **File**: [`src/api/server.py`](file:///c:/Users/JUBER/Downloads/main/my%20work/Standard%20autonomous/src/api/server.py#L1000)
- **Root Cause**: The "computer screen" returned by `/api/agent-workspace/interact` is a simulated JSON dictionary with static status strings, rather than a connection to a real sandboxed execution environment (like CUA or Docker).
- **Risk**: The agent cannot actually download files, run terminal commands, execute Python scripts, or navigate live websites on behalf of the user. It can only simulate that it did so.
- **Remedy**: Connect Deep's execution plane to TryCUA or an isolated local sandbox container, giving agents real terminal, browser, and file system capabilities within bounded security policies.

