---
name: mattpocock-skills
description: Matt Pocock's complete engineering skill suite - specification-driven development, grilling, tdd, bug diagnosis, and agent handoffs.
---

# Matt Pocock Agent Skills Suite for IC (Intelligent Central)

Source: [https://github.com/mattpocock/skills](https://github.com/mattpocock/skills)

Engineering skills designed for software engineering discipline, eliminating hallucinations, vibe coding, and slop.

---

## 1. Skill Catalog & Mapping to IC Development

| Command / Skill | Matt Pocock Workflow | Specific Use Case in IC (Intelligent Central) Development |
| :--- | :--- | :--- |
| **`/grill-me`** / `grilling` | Relentless interview loop to stress-test plans | Use before building new commercial vertical scrapers or outreach templates to resolve all unknowns. |
| **`/to-spec`** | Turn conversation & requirements into a typed spec | Convert raw sales ideas into concrete API contracts (`/api/leads`, `/api/scout`, `/api/workforce`). |
| **`/tdd`** | Test-Driven Development (Red-Green-Refactor) | Writing unit/integration tests for Scrapling, Google Maps parsers, and TTFB latency diagnostic functions. |
| **`/implement-spec`** | Dispatches sub-tasks to build features against a spec | Parallel execution of frontend sheet components, backend endpoints, and crawler jobs. |
| **`/diagnosing-bugs`** | 4-phase root-cause investigation | Debugging scraper DOM breakages, WebSocket/SSE telemetry dropouts, or SQLite locks without guesswork. |
| **`/improve-codebase-architecture`** | Safe structural refactoring under tests | Splitting large monolithic files (like `dashboard.html` or `server.py`) into modular components and services. |
| **`/handoff`** | Zero-loss inter-agent state transfer | Passing lead data between IC swarm agents (Lead Scout ➔ Auditor ➔ Strategy Writer ➔ Hermes Closer). |
| **`/code-review`** | Multi-lens code review against best practices | Verifying UI alignment, CSS token cleanliness, and ECC AgentShield compliance before merging. |
| **`/retro`** | Engineering retrospective to update guardrails | Analyzing outreach bounce rates or failed crawl runs and updating `AGENTS.md` rules. |

---

## 2. Deep Dive: How to Use Each Core Skill in IC

### 1. `/grill-me` — Pre-Flight Design Alignment
When the user asks for a complex feature (e.g. "Add automated WhatsApp rate bots for freight companies"):
- Trigger `/grill-me` or ask clarifying questions.
- Challenge assumptions: "What is the timeout for rate queries? How do we handle companies without WhatsApp Business API? Where is chat state stored?"
- Never begin coding until the user agrees on the edge cases.

### 2. `/to-spec` — Engineering Specification
Produces an unambiguous specification with:
- **Problem Statement** from the user's perspective.
- **Solution Architecture** (FastAPI route + SQLite schema + frontend component).
- **Test Seams**: Exactly where tests will verify inputs and outputs.
- **Numbered User Stories**: e.g., "As an SDR, I want to approve outreach drafts before WhatsApp sends them."

### 3. `/tdd` — Test-Driven Scraper & Engine Development
Scrapers and automated crawlers are brittle without TDD:
1. Write test with mock HTML/DOM fixtures in `tests/test_scrapers.py`.
2. Run test to verify it fails (`Red`).
3. Implement minimal parsing logic in Scrapling / Web Discovery (`Green`).
4. Refactor and verify clean code passes `python cli.py dev-check`.

### 4. `/handoff` — Swarm Agent State Transfer
For the 6 autonomous agents in the IC swarm:
```typescript
interface HandoffEnvelope<T> {
  fromAgent: 'LeadScout' | 'MobileAuditor' | 'StrategyWriter' | 'HermesCloser';
  toAgent: 'PaperclipGate' | 'OutreachDispatcher';
  leadId: string;
  verifiedPayload: T;
  agentShieldCheck: boolean;
  timestamp: string;
}
```
Ensures no lead data, contact numbers, or TTFB metrics are lost between agent execution stages.

---

## 3. Directory Layout in Workspace
- Deployed skills: `.agents/skills/<skill-name>/SKILL.md` (27 individual skills indexed by Antigravity).
- Full upstream repository: `.agents/skills/mattpocock-skills/upstream/` (complete reference docs, exercise scaffolds, and agent guides).
