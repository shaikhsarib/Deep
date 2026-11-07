# DEEP — EXISTING FEATURE & CAPABILITY INVENTORY (MILESTONE 0)

**Date**: November 5, 2026  
**Auditor**: Senior Software Architect & Autonomous Systems Engineer  
**Coverage**: Complete code audit across Presentation, Routing, Services, Governance, and Persistence layers.

---

## 1. Summary Ledger of Capabilities

| Category | Count | Status | Primary File |
| :--- | :---: | :---: | :--- |
| **REST API Routes** | 32 | Active | `src/api/server.py` |
| **Pydantic Domain Schemas** | 18 | Validated | `src/models/lead.py`, `src/core/contracts.py` |
| **Autonomous Workforce Agents** | 12 | Active | `src/services/workforce.py`, `src/services/agency_swarm.py` |
| **Core Services** | 9 | Operational | `src/services/*.py` |
| **Frontend UI Modules** | 6 | Integrated | `src/api/templates/dashboard.html` |
| **Automated Test Suites** | 8 | 48/48 Passing | `tests/*.py` |

---

## 2. Detailed Feature Breakdown

### 2.1 Presentation & User Interface (`src/api/templates/dashboard.html`)
1. **Twenty CRM Virtualized Data Grid**:
   - Table view with column sorting, keyword search, status filtering, and bulk selection.
   - Inline status badge rendering (`DISCOVERED`, `AUDITED`, `SYNTHESIZED`, `PENDING_APPROVAL`, `CONTACTED`, `WON`, `REJECTED`).
   - Quick action triggers: "Audit Site", "Synthesize Pitch", "Approve & Dispatch", "Delete Lead".
2. **Deals Pipeline (Kanban Board)**:
   - Visual multi-column stage view: *Discovered* ➔ *Site Audited* ➔ *Outbox (Pending)* ➔ *Dispatched* ➔ *Won*.
   - Lead cards showing business name, detected revenue leak, verified speed flaws, and assigned SDR agent.
3. **Rakazo 3-Column Living Agent OS**:
   - **Column 1 (Agent Directory)**: Interactive fleet roster with live status badges (`ACTIVE`, `BUSY`, `IDLE`).
   - **Column 2 (Session Chat & Stream)**: Direct real-time bidirectional messaging with selected agent. Optimistic message rendering, agent thoughts, action chips, and terminal commands.
   - **Column 3 (Computer Sandbox & Telemetry)**: Live simulated terminal feed (`$ exec-agent ...`), viewport capture display, routine triggers, and token budget meters.
4. **Paperclip Approvals Gate (Outbox)**:
   - Human-in-the-Loop circuit breaker queue.
   - Displays side-by-side view: raw audit evidence on the left, synthesized pitch on the right.
   - 1-click "Approve & Dispatch", "Edit Message", or "Reject" buttons.
5. **Procedural 3D Canvas Avatars**:
   - Canvas-based rendering (`<canvas id="avatar-canvas">`, `<canvas id="org-avatar-${a.id}">`).
   - Smooth procedural floating animations, dynamic pupil tracking, status ring halos, and role-specific geometry.
6. **Cross-View Seamless Navigation (`openAgentInOS`)**:
   - Clicking an agent in the Fleet Org Chart, Swarm Flow, or Approvals Gate automatically switches to the Living Agent OS, selects that agent, and focuses the input prompt.

---

### 2.2 Routing & REST API Layer (`src/api/server.py`)

#### A. CRM & Lead Management
- `GET /api/leads`: Retrieves all leads with optional status, channel, and query filtering.
- `POST /api/leads`: Creates a new business lead with validation.
- `GET /api/leads/{id}`: Fetches complete lead record including audit report, outreach draft, and conversation history.
- `DELETE /api/leads/{id}`: Deletes lead record from repository.
- `POST /api/leads/inline-edit`: Updates lead fields inline from the data grid.
- `POST /api/leads/bulk-action`: Performs batch operations (audit all, approve all, delete selected).

#### B. Autonomous Workforce Pipeline
- `POST /api/scout`: Triggers Google Places & Overpass crawler for targeted business sourcing.
- `POST /api/audit`: Initiates website technical inspection and speed audit.
- `POST /api/leads/{id}/approve`: Approves staged pitch and dispatches via configured channel.
- `POST /api/leads/{id}/reject`: Rejects draft pitch with audit log note.
- `POST /api/leads/{id}/reply`: Simulates or processes inbound prospect message through Hermes Closer SDR.
- `POST /api/workforce/process-all`: Triggers batch processing across all discovered leads.

#### C. Paperclip Control Plane
- `GET /api/paperclip/overview`: Returns combined workforce metrics, swarm topology, and telemetry logs.
- `GET /api/paperclip/health`: Liveness probe and circuit breaker status.
- `GET /api/paperclip/agents`: Official Paperclip agent schema for all 12 workforce bots.
- `GET /api/paperclip/approvals`: Retrieves all pending items in the Approvals Outbox.
- `POST /api/paperclip/approvals/{id}/approve`: Action handler for human sign-off.
- `POST /api/paperclip/approvals/{id}/reject`: Action handler for human rejection.
- `POST /api/paperclip/heartbeat`: Triggers autonomous fleet pulse across up to 5 pending leads.
- `POST /api/paperclip/agents/pulse`: Emits heartbeat and updates activity counters for a specific agent.

#### D. Living Agent OS Endpoints
- `POST /api/agent-workspace/interact`: Core execution endpoint routing prompts to Scout, Auditor, Closer, or Growth Director with structured thoughts and terminal logs.
- `GET /api/agent-workspace/routines`: Returns predefined automation routines (e.g., "Full Corridor Sweep", "Audit High-Leak Targets").
- `POST /api/copilot/execute`: Unified copilot instruction router.
- `GET /api/workspace/hierarchy`: Formal enterprise hierarchy (Workspace ➔ Teams ➔ Workflows ➔ Computers).

#### E. Governance & Security
- `POST /api/ecc/audit-pitch`: Evaluates outbound copy against AgentShield rules (PII leak, prompt leak, ungrounded claims).
- `POST /api/ecc/verify-code`: Static analysis scan for dangerous `eval()`, hardcoded credentials, and unsafe subprocesses.

---

### 2.3 Services & Workforce Intelligence

1. **`WorkforceManager` (`src/services/workforce.py`)**:
   - Orchestrates the 10-step SDR journey across all 12 agency divisions.
   - Manages token budget tracking ($0.15/1M tokens) and telemetry logging.
2. **`SiteInspector` (`src/services/site_inspector.py`)**:
   - Performs website technical inspection (TTFB, SSL validity, viewport tags, heuristic score).
3. **`EvidenceVerifier` (`src/services/evidence_verifier.py`)**:
   - Pstack-inspired evidence grounding. Calculates deterministic SHA-256 evidence hashes and generates terminal reproduction commands.
4. **`DeepResearchEngine` (`src/services/deep_research.py`)**:
   - Live citation gathering via DuckDuckGo search (`ddgs`), market overview synthesis, and competitor insights.
5. **`ECCShield` (`src/services/ecc_shield.py`)**:
   - Runtime compliance and pre-commit security verification. Enforces zero-hallucination and anti-slop gates.
6. **`InboundCloserSDR` (`src/services/inbound_closer.py`)**:
   - Classifies prospect inbound replies (Price Objection, Agency Objection, Interested, Unsubscribe) and generates consultative rebuttals with booking links.
7. **`ScheduledCadenceEngine` (`src/services/scheduled_cadence.py`)**:
   - Manages background scheduled follow-ups and routine triggers.
8. **`AgencySwarm` (`src/services/agency_swarm.py`)**:
   - Ruflo-inspired swarm topology manager (Hierarchical Core, Consensus Gating, Mesh Communication).
9. **`DeliveryDispatcher` (`src/delivery/dispatcher.py`)**:
   - Multi-channel delivery routing for WhatsApp (Twilio), Email (SMTP/SendGrid), and Telegram.

---

### 2.4 Domain Contracts & Models (`src/models/lead.py`, `src/core/contracts.py`)

- `Lead`: Comprehensive business entity tracking contact info, business profile, audit report, outreach draft, conversation history, and status transitions.
- `BusinessProfile`: Firmographic details (company name, business type, location, phone, email, website).
- `AuditReport`: Empirical and heuristic technical site metrics (TTFB, SSL, mobile responsiveness, performance score, critical flaws).
- `OutreachDraft`: Multi-channel copy (WhatsApp message, email subject, email body, target pain points).
- `HandoffEnvelope`: Matt Pocock typed contract handoff with schema validation and compliance tokens.
- `AgentRole`: Strict enum of all 12 specialized workforce roles.

