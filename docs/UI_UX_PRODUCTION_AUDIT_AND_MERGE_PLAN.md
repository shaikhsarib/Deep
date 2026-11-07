# Deep — UI/UX & Production Audit + "Proper Merge" Plan

**Date:** 6 November 2026
**Scope:** `src/api/templates/dashboard.html` (8,447 lines / 358 KB), `src/api/server.py` (1,437 lines / 47 routes: 22 GET, 24 POST, 1 proxy), the two orphaned prototypes (`demo_deep_agent_os.html`, `demo_deep_avatar_lab.html`), and the vendored `tools/paperclip` UI.
**Method:** static read of every line cited, structural metrics computed from the files, cross-check of docs vs code, runtime contract check of UI→API calls. No file was modified during the audit.

---

## 0. Verdict in one paragraph

You do not have "one UI with a merge problem". You have **five different UIs at four different levels of completion**, glued together inside a single 358 KB HTML file, each carrying its own palette, its own data source and its own truth model — plus two orphaned prototype files and a 160 MB vendored React app that the dashboard embeds through an `<iframe>` pointing at a port nothing in this repo starts. The visual craft is genuinely high (the token layer, motion vocabulary and table density in the light shell are better than most funded SaaS). The engineering underneath it is a prototype: **the UI fabricates data when the API is empty, it never actually sends an approved message, it interpolates scraped and LLM-generated strings straight into `innerHTML`, and it has no router, no store, no component layer, no auth.** That combination is fatal for a product whose entire sales pitch is *"no fabricated evidence, human-approved outreach."* The fix is not a redesign. It is **a merge with a spine**: one shell, one router, one store, one token system, one component layer, one honest data path — and the OS/avatar surfaces kept as a deliberate second mode instead of an accidental second design system.

### Scorecard

| Area | Grade | Blockers | One-line reason |
|---|---|---|---|
| Visual craft / brand | **A−** | 0 | Token layer, typography and density are strong |
| UI architecture | **D** | 5 | One file, one global scope, view switching by `display:none` |
| Information architecture | **C−** | 3 | 8 sidebar items → 5 destinations; 3 names for one table |
| Data truth (trust) | **F** | 6 | Mock companies, fake phones, hardcoded "PASS"/"Verified" |
| Functional integrity | **F** | 1 | Approve button sends `dry_run: true` — can never dispatch |
| Accessibility | **D** | 5 | No skip link, no focus trap, 22 clickable divs, 0 `th[scope]` |
| Responsiveness | **C−** | 2 | 12 conflicting breakpoints; fixed 3-column grid |
| Performance | **C** | 2 | Full `innerHTML` rebuild, 358 KB no-cache HTML, CDN fonts |
| Security | **F** | 4 | No auth, stored XSS, open proxy, path traversal |
| Production readiness | **D** | 6 | No build, no auth, no CSP, no logging, unpinned deps |
| Docs vs reality | **D** | 4 | Docs describe a design and an app that no longer exist |

---

## 1. What you actually have — the five UIs

| # | Surface | Where | State | What it is |
|---|---|---|---|---|
| **1** | **CRM shell** (table + kanban + record drawer + copilot) | `dashboard.html` 4163–5530 markup, 6050–6300 JS | **Live** — served at `GET /` | The real product shell. Twenty/Linear-inspired, light "warm paper" theme, 8-column table, drag-and-drop kanban, slide-over record drawer |
| **2** | **Paperclip approvals gate** | `dashboard.html` 4856–4947, 6302–6760 | **Live but non-functional** | Human-in-the-loop review cards. Approve button sends `dry_run: true` (line 6673) so nothing is ever sent |
| **3** | **Living Agent OS** (3-column: roster / stream / routines) | `dashboard.html` 3572–4160 CSS, 4977–5212 markup, 7990–8440 JS | **Live, visually foreign** | Ported from `demo_deep_agent_os.html`. Hard-coded dark slab inside a light app |
| **4** | **Avatar lab** (procedural canvas agents) | `dashboard.html` 7400–7990 JS | Live, embedded | Ported from `demo_deep_avatar_lab.html`. 60 fps `requestAnimationFrame` characters. Best-preserved part of the merge |
| **5** | **Paperclip React app** (upstream) | `tools/paperclip/ui` (160 MB vendored clone) | **Cannot build here** | `package.json` v0.3.1, React 19 + Vite 8 + Tailwind 4, ~40 deps on `workspace:*` packages, no `node_modules`. Embedded via `<iframe src="http://localhost:5173">` (line 5229) |
| **6** | **Two orphaned prototypes** | repo root `demo_deep_agent_os.html` (858 lines), `demo_deep_avatar_lab.html` (713 lines) | **Dead** | Referenced by nothing. Not served, not linked, not imported. Pure reference material |

**That is the whole "merge" problem in one sentence:** surfaces 1–4 were concatenated into one file by copy-paste (three separate `<style>` blocks and two `<script>` blocks, each with its own conventions), surface 5 is an external product pretending to be a tab, and surface 6 is the design archaeology.

### Proof of concatenation (not opinion)

```
style block 1: lines   31–3571   → light design system, 258 CSS classes, 63 distinct tokens (110 declarations, redefined per theme)
style block 2: lines 3572–4160   → "RAKAZO 3-COLUMN AGENT OS" — 30 hard-coded hex colors, only 4 var() references
style block 3: lines 5491–5530   → agent-OS responsive fixes, 3 classes
script block 1: lines  18–30     → theme boot
script block 2: lines 5532–8444  → 102 functions, one flat global scope
```

Class-name overlap between block 1 and block 2 is **one selector** (`.active`). The Agent OS was namespaced with an `os-` prefix, so it *compiles* — and that is exactly why nobody noticed it never got merged: **it is a parallel universe, not a component.** Its container `#studio-subview-workspace` is `height: calc(100vh - 130px); min-height: 680px` (lines 3582–3583) and its grid is `280px 1fr 340px` with `background: #090b0f` (lines 3607, 3620) — on a phone it cannot fit, and in light mode it looks like a black hole punched through the page.

---

## 2. The merge is broken in four concrete ways

### 2.1 Four design systems, one file

| Layer | Truth |
|---|---|
| App shell | Light "warm paper", `--bg-app: #f6f6f4`, Inter + JetBrains Mono, ring-only elevation (`dashboard.html:37–115`) |
| Agent OS pane | Hard-coded obsidian `#090b0f`, white-alpha borders, `box-shadow: 0 24px 60px rgba(0,0,0,.5)` (3595–3626) — ignores `body.dark-mode` entirely |
| Docs (`UI_UX_AND_FLOW_ARCHITECTURE.md:14`) | "Obsidian Black `#07080a`… Cobalt `#1f5fff`… Emerald `#00d68f`… Plus Jakarta Sans" — **none of these appear in the code** |
| `demo_*.html` prototypes | A third palette and a fourth type ramp |

110 token declarations exist across two palettes (63 distinct properties), but no rule says *which* are allowed to be used where. The OS pane proves it: it uses 4 tokens and 30 raw hex values. **Merge rule #1: a colour may only enter a component through a token.**

### 2.2 View switching is `display:none`, not routing

```
VIEWS = { table, kanban, paperclip_inbox, paperclip_workforce, paperclip_orchestration }   // 5893–5899
showView()  → loops all five, sets display:none, shows one, restarts an animation             // 5901–5913
```

On top of that sits a **second, partial router**: `persistNavigationState()` + `restoreNavigationState()` (5996–6025) writing `location.hash` and `localStorage['ic_nav_hash']`. And a **third** mapping: `studio-subview-{topology|workspace|iframe}` panes (4979, 5024, 5214) toggled by `setStudioSubview`. So a single screen's position is encoded in **three** places (`currentViewMode` + `activeStudioSubview` + `hash`), reconciled by imperative calls in 14 different `onclick` handlers. Bugs fall out of this immediately:

- `persistNavigationState()` line 5998 is **dead code** — line 5999 immediately overwrites `hash` for the same condition. Someone patched a routing bug by adding a line under it.
- `#iframe` is a route with no nav entry, no toolbar button, no palette entry, and no server behind it.
- `restoreNavigationState()` is called from `fetchLeads()` (5831) *and* from boot (8442), so deep-linking re-renders twice.

### 2.3 Navigation lies about what exists

| Sidebar entry | What it actually does | Problem |
|---|---|---|
| **Overview** (4471) | `setViewMode('table'); switchStage('targets')` | **Identical** to the next item |
| **Targets & Leads** (4482) | same | Two items, one destination |
| **Site Audits** (4492) | `switchStage('audits')` → same table, `filter(r => r.icp)` (6031) | A *filter* is promoted to a destination |
| **Approvals Gate** (4502) | `paperclip_inbox` | OK |
| **Opportunities & Deals** (4512) | `switchStage('deals')` → same table, filtered by status | Another filter promoted to a destination |
| **Agent Workspace (OS)** (4524) | `paperclip_orchestration` + `workspace` | OK |
| **Swarm Flow** (4533) | `paperclip_orchestration` + `topology` | Same view, different pane |
| **Fleet Org Chart** (4543) | `paperclip_workforce` | OK |

So **8 rows → 5 destinations**, and two of them are filters wearing a destination's clothes. Meanwhile the toolbar duplicates all of it again with 6 segmented buttons (4710–4738), and the "saved views" dropdown duplicates it a third time (4682–4700), and the command palette a fourth (7145–7150), and single-letter shortcuts a fifth (`g t/p/r/w/f`, 7386–7390). **Five parallel navigations that must be kept in sync by hand.** They already aren't: the palette's "AI Agent Team" goes to `paperclip_workforce` while the sidebar's "Fleet Org Chart" is the same thing under a different name.

### 2.4 Two data sources, and the fake one wins

`masterCorridors` is initialised to **8 invented companies** (5602–5691) with invented phone numbers, invented TTFB, invented TLS versions and invented revenue losses. Then `fetchLeads()` runs (5759) and — **only if the API returns a non-empty array** — replaces them (5825). The fallback is not an error path, it is the default path on a fresh install, on an empty pipeline, on a network hiccup, and in `catch (err) { /* fallback */ }` (5828).

Worse, the *mapping* invents data even when the API works:

```js
phone: lead.profile.phone || '+91 22 2788 1234',                       // 5805  fake phone
url:   … : 'unlisted.in',                                              // 5795  fake domain
ttfb:  rawAudit.load_time_seconds ? `${…}s` : '1.2s',                   // 5813  fake speed
icp:   rawAudit.is_mobile_responsive !== false,                         // 5815  missing audit ⇒ "ICP match: true"
```

And the approvals view does it too: `shield: 'PASS'` hard-coded (6330, 6343), `phone: … || '+91 98200 00000'` (6322), then `await new Promise(r => setTimeout(r, 260))` — **a deliberate artificial delay so the skeleton "breathes"** (6347).

The record drawer then renders, unconditionally, at line 6897:

```html
<span class="k">Fact check</span> <span class="v" style="color:var(--emerald)">Verified accurate</span>
```

**This is the single most damaging thing in the codebase.** A product whose pitch is "we only tell buyers things we can prove" ships a UI that prints "Verified accurate" on a record that may have no evidence object at all, next to a fabricated phone number, a fabricated 1.2 s TTFB, and a compliance badge that always reads PASS.

---

## 3. UI/UX defects, by severity

### Blockers

| ID | Finding | Evidence | Why it hurts | Fix |
|---|---|---|---|---|
| **B-01** | Approve button **never dispatches**. It POSTs `dry_run: true`, and on success locally sets `rec.status = 'contacted'` then toasts *"Pitch approved & dispatched"* | 6673, 6684–6687 | The core workflow of the product is a lie. Operators believe outreach was sent; it never was. If `dry_run` were ever removed, the UI still wouldn't confirm real delivery | Server returns `{sent: bool, provider_id, channel}`; UI renders the real receipt; add an explicit "dry run" toggle with a visible banner |
| **B-02** | Fabricated data shown as real (mock rows, fake phones, hard-coded `PASS`, `Verified accurate`, `12 LIVE`, `ACTIVE`, `HUMAN REVIEW`) | 5602–5691, 5805/5813/5815, 6330, 6897, 4541, 4555–4561 | Destroys the only differentiator the product has | See §6 — demo mode must be an explicit, labelled state |
| **B-03** | Stored XSS: scraped/LLM strings interpolated into `innerHTML`, including inside `onclick` attributes. No escaping helper exists anywhere (`escapeHtml` count = 0) | 6069, 6076, 6321–6328, 6368, 6892–6917 | A malicious or compromised target website can execute JS in the operator console, read the lead DB through the API, and send mail as you | Escape at the boundary; replace inline handlers with `data-*` + event delegation |
| **B-04** | No authentication on any route; CORS `*` **with** `allow_credentials=True` | `server.py:30–36`, all 47 routes | Any page you visit while the server runs can call `/api/leads`, approve pitches, delete leads | Single-user session token + strict origin allowlist (see §7) |
| **B-05** | Two visual languages, one of which cannot be themed or resized | 3572–4160 | Agent OS is unusable in light mode, on mobile, or on short screens | Re-platform onto `--studio-*` tokens; make it a declared mode (§5.3) |
| **B-06** | **The Copilot cannot be opened.** `.copilot { display:none }` (2663) with `.copilot.show` (2668) as the only escape, but every call is `toggleCopilot(false)` (5252, 7380) — there is no launcher. `sendCopilotPrompt` also reads `#copilot-input` / `.copilot-composer input` (7108), neither of which exists (the real prompt is `contenteditable` at 5260), and `activeCopilotTab` is read at 7117 but never assigned. Result: **`POST /api/copilot/execute` is unreachable and would throw if reached** | 2650–2672, 5252, 7117, 7380 | A whole backend capability is invisible; the "AI copilot" story in the docs has no UI |
| **B-07** | **No navigation below 860 px.** `.sidebar` becomes `translateX(-100%)` (3541) and needs `.sidebar.mobile-open` (3551) — a class that appears **exactly once in the file and is never applied** by any JS or markup. There is no hamburger button in the header (4580–4665) | 3541–3553 | On a phone or narrow window the app is a content pane with no way to reach any other view |
| **B-08** | **Drag-and-drop bypasses the human gate.** `kDrop()` mutates `rec.status = newStatus` locally (6291), toasts success, and makes **no API call and no ECC check** — so dragging a card into "Dispatched" marks a lead contacted without approval | 6284–6297 | The one guardrail the product sells can be defeated with a mouse drag |
| **B-09** | **Drawer edits are silently discarded.** The drawer's pitch textarea is `#edit-pitch-text` (6932), but approving from the drawer calls `paperclipApprove('appr_'+id, …)` (6721) which looks up `#inbox-pitch-appr_<id>` — an id that only exists on inbox cards (6396) — so `customPitch` is always `null` and the stored pitch is sent instead of the operator's edit | 6721, 6666, 6932 | The human's most important action — correcting the message before it goes out — does nothing |

### Major

| ID | Finding | Evidence | Fix |
|---|---|---|---|
| M-01 | Two logos rendered simultaneously in the sidebar (SVG mark **and** `<img src="/static/deep_logo.svg">`), plus a leftover `IC` identity in `static/` | 4437–4447 | Pick one mark component; delete the duplicate `<img>` node (asset stays in `static/`) |
| M-02 | "Overview" and "Targets & Leads" are the same action | 4471 vs 4482 | Collapse to one "Leads" destination (§5.2) |
| M-03 | Three names for one table state: `Prospects & Leads` / `All Prospects` / `Companies` / `Targets` | 4592, 4676, 5931, 4488 | One noun per entity, everywhere (§5.4 lexicon) |
| M-04 | Dead code: 3 never-called functions (`fetchOrchestrationTelemetryLogs`, `minimizeCopilot`, `openFilterInput`), 1 overwritten routing line (5998), `.dark-boot` class with **no CSS rule** (line 23), `switchStage('outbox')` unreachable (6032), `sortCompanies()` alias (7397) | — | Delete the lines, not the features; keep git history |
| M-05 | Fake live-ness: no `setInterval`/`EventSource`/WebSocket exists. The telemetry stream (6514), topology map (6568), agent cards (6451), playbooks (6967) are all static arrays rendered once | grep `setInterval` → 0 | Either poll `/api/workforce/telemetry` every 5 s with a pause when tab hidden, or stop calling it LIVE |
| M-06 | `async` render functions are called without `await` from a sync dispatcher (`renderCurrentView`, 5915–5922) → overlapping renders, stale DOM, unhandled rejections | 5919, 6302 | Views return promises; router awaits and cancels in flight |
| M-07 | Sidebar collapse state, theme, nav and audio each persist under their own ad-hoc key with no schema (`ic_theme`, `ic_audio_enabled`, `ic_nav_hash`, shell state) | 22, 5536, 6007, `restoreShellState` | One namespaced settings object with a version field |
| M-08 | Emoji avatars in a system whose own comment says "monogram avatars, no emoji" — 13 emoji in `AGENTS` (5705–5716) plus `⏰` injected into routines (8433) | — | Use the existing monogram + canvas avatar system |
| M-09 | **Three agent rosters, three datasets, three spellings.** `AGENTS` (5704), `OS_AGENTS_DATA` (7405) and `TOPO_NODES` (6552) are separate arrays; names drift ("HyperResearch" vs "HyperResearch Specialist", "ECC AgentShield" vs "ECC AgentShield Guard"); only 10 of 12 agents appear in the topology — so "12 LIVE" (4541) sits above a 10-stage pipeline (4985) and is simply false | 5704, 7405, 6552 | Derive org chart, OS roster and topology from **one** agent registry |
| M-10 | **Four independent title maps** (`5930`, `5960`, `5970`, `6619`) and five nav surfaces | See §2.3 | One registry (§10.1) |
| M-11 | **Dead DOM hooks:** the backend "computer screen" update writes to `#os-screen-metric`, `#os-active-url`, `.os-screen-header` (8372–8378) but the DOM uses `#os-computer-title` / `#os-sandbox-url` (5163, 5176) → **every server-driven screen update silently no-ops**. Also dead: `.header-crumb` (837/846/3555), `.topo-flow-wrap` (5514), sprite symbols `i-chev`/`i-command`/`i-external`/`i-link` | — | Rename one side; add an id-usage assertion to CI |
| M-12 | **`catch → success` in six places**: a failed request still toasts success — `6656` "Heartbeat sent (offline demo mode)", `6683–6688` approve, `6736`, `7004`, `7059`, `7133` | — | One API client that throws; every view renders an error state |
| M-13 | **Layout collision:** `.batch-bar` (fixed, `bottom:22px`, z 1100) and `.toast-stack` (fixed, `bottom:20px`, z 2000) occupy the same strip — every batch action fires a toast directly over the buttons the user just pressed. The mobile sidebar (z 40) also sits under the batch bar | 1523, 3326 | Named z-ladder + reserved safe areas |
| M-14 | **Pointer-rate layout thrash:** a global `pointermove` listener calls `getBoundingClientRect()` on every `.decision-card` and `.agent-card` on every mouse move, then writes CSS variables | 7335–7341 | Gate behind `(hover:hover)` + `requestAnimationFrame` |

### Minor

`·` separators used as both decoration and data (6370) · tooltip-only affordances (`title=`) with no keyboard equivalent · 6 different toast durations set inline · `prompt()`/`alert()` used as real UI (`openNewRoutinePrompt` 8428–8430, `takeControlOfComputer` 8419) · no `<noscript>` · `Powered by` nothing, no version string, no session identity.

---

## 4. Accessibility (WCAG 2.2 AA)

Measured, not felt:

| Metric | Value | Requirement |
|---|---|---|
| Clickable `<div>/<span>/<tr>` with `onclick` | **22** | Must be `<button>` or carry `role`+`tabindex`+key handler |
| `role=` attributes | 12 | — |
| `aria-label`/`aria-*` | 33 | — |
| `aria-live` regions | **1** | Toasts + telemetry status need one each |
| `<th scope>` | **0** of 1 table | Mandatory for data tables |
| `<label>` vs `<input>` | 7 vs 12 | Every input needs a programmatic label |
| Skip-to-content link | **0** | Required for an 8-item sidebar |
| Focus trap / focus restore | **0** | Every modal and drawer needs both |
| `prefers-reduced-motion` coverage | 1 block (3529), covering block 1 only | The OS pane's 17 keyframes and the avatar rAF loop ignore it |

Specific breakages:

- **Theme flash on reload.** `dashboard.html:22–27` adds `.dark-boot` to `<html>` and only adds `dark-mode` to `<body>` on `DOMContentLoaded`. There is no `.dark-boot` CSS rule, so a dark-mode user sees a full white paint before the theme lands. Fix: put the class on `<html>` and write `html.dark-mode` selectors (or set `data-theme` on `<html>` and scope all tokens to it).
- **Drawer/modal focus.** `#record-peek-drawer` has `role="dialog" aria-modal="true"` (5287) but focus stays on the row behind it, Tab walks into the page, and `Esc` closes it (7379) without returning focus. Same for `#scout-modal`, `#mission-modal`, `#pain-matrix-modal` (7375–7378), which are closed by direct `classList.remove` in the key handler — bypassing their own close functions.
- **Contrast failures** in the light palette, measured: `--text-muted #8a9099` on `--bg-app #f6f6f4` = **2.97:1**, `--text-faint #b3b8bf` = **1.84:1**, and both are used for real data (column metadata 6086, mono values 6892). In dark mode `--text-muted #6b727b` on `#0b0c0f` = **4.02:1** — still below 4.5:1. Body copy is `13px` (line 176) — small for a data-dense enterprise tool, and it is the *base* size, not a deliberate exception.
- **Audio.** `Sound.play()` is attached to nearly every interaction and defaults **on** (5536). For a keyboard/screen-reader user this is a per-action WebAudio burst with no way to silence it except the tiny footer toggle. Default it off.

---

## 5. Responsiveness & layout

**12 media queries at 8 different breakpoints** (1400, 1251, 1100, 1080, 900, 860, 768, 640) spread across three style blocks, so nobody can say what the app looks like at 1000 px. Concretely:

- `#studio-subview-workspace` is `height: calc(100vh - 130px); min-height: 680px;` with a `280px 1fr 340px` grid (3582–3607). Below ~1080 px the middle column collapses to zero width before any breakpoint fires; below 768 px the 280 px roster alone is wider than the viewport.
- `body { overflow: hidden }` (182) means any overflow is clipped rather than scrollable — on mobile the table's horizontal scroll works only because `.table-scroll` is separately scrollable (4799), but the drawer (5286) and copilot (5235) are `position: fixed` and will clip their own footers on short screens.
- `--sidebar-width: 272px` is a hard token; collapse is a JS class, not a media query. Below 860 px the sidebar goes off-canvas (`translateX(-100%)`, 3547) and depends on `.sidebar.mobile-open` (3551) — **which nothing ever adds** — and there is no hamburger in the header. So the narrow layout has no navigation at all (B-07), rather than a sidebar that covers the content.
- **9 distinct z-index values** (1, 10, 40, 900, 1000, 1100, 1200, 1500, 2000). Dropdown menus sit at 10, the record drawer at 2000 — so a dropdown opened *inside* the record drawer is invisible. `.batch-bar` (1100) and `.toast-stack` (2000) are both fixed at `bottom: ~20px`, so every batch action fires a toast over the buttons just clicked. These are real bugs, not style notes.

**Fix:** one breakpoint set (`--bp-sm 640`, `--bp-md 900`, `--bp-lg 1200`) enforced by lint; named z-index ladder (`--z-dropdown 100`, `--z-sticky 200`, `--z-drawer 300`, `--z-modal 400`, `--z-toast 500`, `--z-tooltip 600`); sidebar becomes an off-canvas drawer under `md`; Agent OS becomes stacked columns under `lg` rather than a grid that can't fit.

---

## 6. Performance

| Issue | Evidence | Impact | Fix |
|---|---|---|---|
| 358 KB of HTML parsed on every navigation, served `Cache-Control: no-cache, no-store` (`server.py:1431`) and re-read from disk per request (`server.py:1425–1429`) | — | ≈0.5–0.8 MB per hard reload, zero browser caching, disk I/O per request | Split into partials + cacheable `/static` assets with hashed filenames + `ETag` |
| Every render rebuilds the entire `<tbody>`/board/card list from a template string | 6058–6064, 6244, 6362, 6451 | Loses focus, scroll and selection; O(n) DOM churn on every filter keystroke (debounced 200 ms at 6154) | Keyed diff or targeted node updates; keep `tbody` and patch rows |
| Two Google Fonts families loaded render-blocking, 2 preconnects, no `font-display` control | 13–17 | Offline/air-gapped demo = wrong type; also a third-party request from an internal tool | Self-host `Inter` + `JetBrains Mono` (woff2) under `/static/fonts` |
| 17 `@keyframes`, 3 blocks, no batching | — | Layout thrash during view transitions (`showView` forces `offsetWidth` 5910) | `will-change` discipline + `transform/opacity` only |
| `/api/leads` returns the entire DB with no pagination | `server.py:116–128` | ~740 KB JSON per load once you have a few hundred leads | Cursor pagination + field projection |
| Artificial 260 ms delay before rendering approvals | 6347 | Waste | Remove |
| Avatar rAF loop runs even when the OS pane is hidden | 7400–7990 | Wasted CPU/battery on every other view | Start/stop on mount/unmount |

---

## 7. Production blockers beyond the frontend

These are not cosmetic and they gate "production" more than any pixel does.

| ID | Problem | Evidence | Fix |
|---|---|---|---|
| P-01 | **No auth, no sessions, no CSRF.** 47 routes (24 mutating POSTs + 1 catch-all proxy), all open. The only protection is binding to `127.0.0.1` | `main.py:42`, `run_server.py`, `src/api/server.py` (all routes) | Single-user token in an `HttpOnly` cookie, `SameSite=Strict`, CSRF token on mutations, and refuse to start on a non-loopback bind without a token |
| P-02 | **CORS `*` + credentials** | `server.py:30–36` | Explicit origin list; never `*` with credentials |
| P-03 | **Open proxy**: `/api/paperclip-proxy/{path:path}` forwards any method and **all caller headers** to `127.0.0.1:3100` | `server.py:172–196` | Allowlist paths/methods, strip `cookie`/`authorization`, require auth |
| P-04 | **Path traversal**: `GET /api/screenshots/{filename}` joins raw user input onto `data/screenshots` | `server.py:353–358` | Resolve + `is_relative_to()` containment check, extension allowlist |
| P-05 | **SSRF**: `/api/inspect-url` fetches any URL, follows redirects, `verify=False` | `server.py:198–206`, `site_inspector.py` | Block private ranges/link-local, no redirects to private nets, `verify=True` |
| P-06 | **`dry_run` marks the lead CONTACTED** without sending | `workforce.py:253` per API audit | Status transition must be a consequence of a provider receipt, not of a flag |
| P-07 | **Fabricated API payloads**: `/api/paperclip/approvals` returns 3 invented companies when the DB is empty; `/api/paperclip/agents` invents task/token counts; approve returns `{success:true}` for unknown ids | `server.py:441–530`, `632–790`, `538–541` | Return `[]` / 404 and let the UI render an honest empty state |
| P-08 | **Dispatchers report success while doing nothing** when Twilio/SMTP creds are absent | `dispatcher.py:43–46, 69–71` | Fail loudly, surface "channel not configured" in the UI |
| P-09 | **Long jobs run inside the HTTP request** — scout, stage-all, batch-approve, interact invoke Selenium/Playwright/HTTP inline; `BackgroundTasks` is imported but never used | `server.py:5` + audit | Move to a task runner, return `202` + job id, poll |
| P-10 | **Unpinned dependencies and missing ones**: `requirements.txt` uses `>=` for everything and **omits `httpx`** (imported in 4 modules) and **`playwright`** (used in 9 places) | `requirements.txt` | Pin exact versions, add `httpx`, `playwright`, generate a lockfile |
| P-11 | **No security headers** (CSP, `X-Content-Type-Options`, `Referrer-Policy`, `X-Frame-Options`), no gzip, no structured logs, no request ids, no rate limit | — | Middleware stack + JSON logs |
| P-12 | **`start_ic.bat` hardcodes paths outside the repo** (`C:\Users\JUBER\Downloads\paperclip\...`) and launches `npx tsx` / `pnpm dev` | `start_ic.bat:8,11` | Repo-relative paths, fail with a clear message, never auto-install at startup |
| P-13 | **Business data is committed**: dozens of `data/leads/*.json` show as modified, lead files contain real company names/phones | `git status` | Untrack `data/`, keep a seed fixture; if already pushed, treat PII as leaked |
| P-14 | **Vendored repos dominate the tree**: `tools/ecc` 60 MB, `tools/paperclip` 160 MB, `tools/rea` 55 MB vs `src/` 1.8 MB | — | Convert to submodules or move to `vendor/` (no deletion needed) |
| **P-15** | **The app cannot be started in this checkout.** No `.venv`/`venv`/`env` folder exists; the only interpreter on PATH is a bare Windows-Store Python 3.13 with `pip` and nothing else — `fastapi`, `uvicorn`, `pydantic`, `httpx`, `pytest` and 10 others all fail to import. `pytest` therefore cannot even collect. There is no lockfile, and `requirements.txt` is missing `httpx` (imported by 4 modules) and `playwright` (used in 9 places), so following the README on a clean machine fails at import | verified by import probe + `py -0p` | Commit a `setup.ps1`/`make setup` that creates a venv from a **pinned** lockfile; add a `doctor` command that prints missing deps and provider config |

---

## 8. Docs vs reality

`docs/UI_UX_AND_FLOW_ARCHITECTURE.md` describes an app that does not exist:

| Doc claim | Reality |
|---|---|
| "dark luxury glassmorphism… Obsidian `#07080a`, Cobalt `#1f5fff`, Emerald `#00d68f`" (line 14) | Light warm-paper UI, `#f6f6f4`, `#1d68bd`, `#17803d` |
| "Plus Jakarta Sans" (line 19) | Inter |
| "React Swarm Studio:5173 / Paperclip API:3100" as part of the product (281–287) | Separate vendored app, unbuildable in this repo; iframe is dead |
| `docs/DEEP_CURRENT_STATE.md:50` "dashboard.html — Unified UI (Twenty CRM Grid + Rakazo 3-Col OS + 3D Avatars)" | "Unified" is the aspiration; the file proves it is a concatenation |
| `DEEP_CURRENT_STATE.md:98` "32+ endpoints" | 47 |
| `DEEP_CURRENT_STATE.md:74` "8 test suites, 48 tests" | 9 test files present |
| `FOLDER_STRUCTURE.md:64` lists `src/core/engine.py`, `src/scrapers/places_scraper.py`, `src/delivery/delivery_module.py` | Do not exist |

Keep the docs — but they must be regenerated *from* the merged code, not maintained as a parallel fiction. A short `docs/UI_CONTRACT.md` (route table + token table + component list) is worth more than three aspirational architecture documents.

---

## 9. "Don't delete anything" — the keep / merge / retire ledger

You asked me not to delete what's required. Here is the honest classification. **Nothing in this table needs deleting to ship**; six items are genuinely dead weight and can be retired *because they are already doing nothing*.

### KEEP as-is (good work, protect it)
| Asset | Why |
|---|---|
| The light token layer (`dashboard.html:37–161`) | Well-built; becomes the single source of truth |
| The icon sprite (`<symbol id="i-*">`) | Already the best merge mechanism in the file — reuse it |
| Motion vocabulary (`--ease-*`, `--t-*`, `--stagger`) | Rare quality; keep and extend |
| Table + kanban + record drawer | The product's core surface |
| Canvas avatar engine (7400–7990) | Genuinely distinctive; keep behind a mount/unmount API |
| Command palette (⌘K) | Good, needs to become the *only* navigation index |

### MERGE (keep the feature, re-home it)
| Current thing | New home |
|---|---|
| `paperclip_orchestration` + `studio-subview-topology` | `#/agents/flow` (a tab in the Agents destination) |
| `studio-subview-workspace` (3-column OS) | `#/agents/workspace` — **declared dark "Studio mode"**, tokenised |
| `studio-subview-iframe` (localhost:5173) | `#/agents/lab` — *optional* external surface; iframe gets a health check + graceful "not running" state. Never a silent black rectangle |
| `paperclip_workforce` (org chart) | `#/agents/team` |
| `paperclip_inbox` | `#/approvals` |
| `stage: audits` / `stage: deals` | Saved views on `#/leads` (`?view=audited`, `?view=active`), not destinations |
| `demo_deep_agent_os.html` | `design/prototypes/agent-os.html` (reference only, kept) |
| `demo_deep_avatar_lab.html` | `design/prototypes/avatar-lab.html` |
| `AGENCY_MASTER_CORRIDORS`, `AGENTS`, `VERTICAL_PLAYBOOKS` | `src/api/static/js/data/demo-seed.js`, loaded **only** under `?demo=1` with a persistent amber banner |
| `tools/paperclip` | Stays; becomes a git submodule or moves under `vendor/` (it is 160 MB and unbuildable in-tree) |

### RETIRE (already dead — zero feature loss)
1. The duplicate `<img src="/static/deep_logo.svg">` inside `.org-switcher` (4445–4447) — one mark, not two.
2. The "Overview" nav item (4471–4479) — byte-identical behaviour to "Targets & Leads".
3. Line 5998 (`persistNavigationState` first assignment, overwritten by 5999).
4. `.dark-boot` class (line 23) — **no CSS rule exists**, it does nothing.
5. Three never-called functions: `fetchOrchestrationTelemetryLogs`, `minimizeCopilot`, `openFilterInput`.
6. `switchStage('outbox')` branch (6032) — unreachable.

That is the complete list. Everything else has a home.

### Brand assets — measured, not guessed
Referenced by the UI: `deep_logo.svg`, `favicon.png`, `ic_logo_badge.png`, `standard_autonomous_logo.svg` (all exist — **no 404s**). Unreferenced in `src/api/static/`: `deep_lockup.svg`, `deep_wordmark.svg`, `favicon.svg`, `ic_logo_blocks.svg`, `ic_logo_blocks_512.png`, `ic_logo_blocks_transparent.svg`, `ic_logo_original.png` (748 KB), `ic_monogram_dark.png`, `ic_monogram_transparent.png`. Three brand generations (`ic_*` → `standard_autonomous_*` → `deep_*`) coexist, and the sidebar renders two of them at once (4437–4447). **Keep every file** — move the unused ones to `static/brand/archive/` and declare `deep_logo.svg` + `favicon.*` as canonical. A 748 KB PNG should not sit in a served directory either way.

---

## 10. The proper merge — target architecture

The goal is not "make everything look the same." The Agent OS should stay dark — it is a control room. The goal is **one spine**: one shell, one router, one store, one token contract, one component layer, one honest data path. Two *modes* on top of one *system*.

```
┌───────────────────────────────────────────────────────────────────────────┐
│  SHELL  (base.html)                                                        │
│  ├── <head> tokens.css · components.css · view css · theme boot           │
│  ├── icon sprite (single, shared)                                          │
│  ├── Sidebar  ← rendered from ROUTES, never hand-written                  │
│  ├── Header   ← title + primary action + global search                    │
│  ├── <main id="view-root">  ← views mount/unmount here                    │
│  └── Overlay host: drawers · modals · toasts · palette                    │
└───────────────────────────────────────────────────────────────────────────┘
             │                        │                        │
      ┌──────▼──────┐          ┌──────▼──────┐          ┌──────▼──────┐
      │  ROUTER     │          │   STORE     │          │   API       │
      │  hash→state │◄────────►│  leads      │◄────────►│  fetch      │
      │  1 source   │          │  approvals  │          │  typed      │
      │  of truth   │          │  workforce  │          │  errors     │
      └──────┬──────┘          │  ui         │          └─────────────┘
             │                 └──────┬──────┘
      ┌──────▼────────────────────────▼──────┐
      │  VIEW MODULES   mount(el, ctx) / unmount()   │
      │  leads · pipeline · approvals · team ·       │
      │  workspace · flow · lab                      │
      └──────────────────────────────────────────────┘
```

### 10.1 One router (replaces `currentViewMode` + `activeStudioSubview` + hash + 5 nav mechanisms)

```js
// js/core/routes.js  — the ONLY place that knows what exists
export const ROUTES = {
  '#/leads':            { view: 'leads',      nav: 'leads',     title: 'Leads',        mode: 'app' },
  '#/leads?view=audited': { view: 'leads',    nav: 'leads',     title: 'Audited sites', mode: 'app', params: { filter: 'audited' } },
  '#/pipeline':         { view: 'pipeline',   nav: 'pipeline',  title: 'Pipeline',      mode: 'app' },
  '#/conversations':    { view: 'leads',      nav: 'convs',     title: 'Conversations', mode: 'app', params: { filter: 'active' } },
  '#/approvals':        { view: 'approvals',  nav: 'approvals', title: 'Approvals',     mode: 'app' },
  '#/agents/team':      { view: 'team',       nav: 'agents',    title: 'Agent team',    mode: 'studio' },
  '#/agents/workspace': { view: 'workspace',  nav: 'agents',    title: 'Agent workspace', mode: 'studio' },
  '#/agents/flow':      { view: 'flow',       nav: 'agents',    title: 'Swarm flow',    mode: 'studio' },
  '#/agents/lab':       { view: 'lab',        nav: 'agents',    title: 'External lab',  mode: 'studio' },
};
```

Sidebar, toolbar segmented control, palette and keyboard shortcuts are **generated from this table**. One edit → four surfaces stay in sync, forever. The five hand-maintained navigations become one.

### 10.2 One view contract

```js
// js/views/approvals.js
export default {
  async mount(el, { store, api, router }) {
    const { items } = await api.approvals.list();       // honest empty array, never mock
    el.replaceChildren(renderCards(items));             // no innerHTML on user data
    this._off = store.subscribe('approvals', () => this.rerender());
  },
  unmount() { this._off?.(); },                        // timers, listeners, rAF, observers
};
```

Rules: no view touches `document` outside its own root; no view calls `fetch` directly; no view sets `display:none` on another view; every async render is awaited or cancelled via `AbortController`.

### 10.3 One store

```js
// js/core/store.js — ~60 lines, no framework
const state = { leads: [], approvals: [], workforce: null, ui: { theme, sidebar, demo } };
const subs = new Map();
export const store = {
  get: k => state[k],
  set(k, v) { state[k] = v; (subs.get(k) || []).forEach(fn => fn(v)); },
  subscribe(k, fn) { ... return () => ... }
};
```

The point is not sophistication — it is that **`masterCorridors` stops being a global that both the mock and the API write to**. Today `fetchLeads` silently overwrites it (5825), the drawer mutates rows in place (6685), and every view re-derives its own list (6030–6035). One store, one truth.

### 10.4 One token contract — two modes

```css
/* css/tokens.css */
:root {
  /* app mode: surfaces, text, borders, brand, semantics, shape, motion  (keep as-is) */
}
html[data-theme="dark"] { /* keep as-is, but scoped to html, not body */ }

/* studio mode: the Agent OS gets its OWN declared palette that still derives
   from the same primitives — it is dark ON PURPOSE, in both themes */
[data-mode="studio"] {
  --surface-0: #090b0f;   --surface-1: #0e1116;   --surface-2: #141922;
  --border-hair: rgba(255,255,255,.07);
  --text-primary: #e8eaef; --text-secondary: #9aa3b2; --text-muted: #66707e;
  --accent: var(--ic-blue);            /* same brand accent, lifted for dark */
  --elev-window: 0 24px 60px rgba(0,0,0,.5);
}
```

Then every `#090b0f` in the OS block (30 occurrences) becomes a token. Result: the OS stops fighting the light app, becomes theme-consistent *by declaration*, and can be re-skinned in one place. **This is the difference between a merged UI and a concatenated one.**

### 10.5 One component layer

Extract, once, the things currently re-implemented per view:

`Button` (4 variants × 3 sizes) · `IconButton` · `Pill/Status` (already exists — `statusPill`, 5744) · `Card` · `Panel` · `DataTable` (header, sort, selection, bulk bar, empty, skeleton) · `Drawer` · `Modal` (focus trap, Esc, restore) · `Dropdown` (`toggleDD`/`closeDDs` exist — formalise) · `Toast` (single `aria-live` host) · `Skeleton` · `EmptyState` · `ErrorState` · `CommandPalette` · `Tabs` · `Avatar` (monogram + canvas) · `Toast` · `ConfirmDialog` (replaces `confirm()`/`prompt()`).

Every component ships with: keyboard behaviour, focus ring, disabled/loading state, dark + studio tokens, and a one-line usage note.

### 10.6 One honest data path (the trust layer)

This is the part that makes the product match its promise, and it is non-negotiable:

```js
// 1. Never substitute fake rows for an empty result.
const leads = await api.leads.list();        // [] is a valid, honest answer

// 2. Three explicit UI states, never a silent blend:
if (state.ui.demo)     renderDemoBanner();   // amber: "DEMO DATA — not real leads"
else if (!leads.length) renderEmptyState();  // "No leads yet — run a scout cycle"
else                    renderTable(leads);

// 3. Evidence is a component, not a sentence.
renderEvidence(record.evidence)  // real artifact or "No evidence captured — not verified"
```

Concretely: replace `Fact check: Verified accurate` (6897) with a component that renders **the artifact** (screenshot hash + capture timestamp + measured TTFB + HTTP status) or an explicit "not captured". Replace `shield: 'PASS'` with `appr.compliance.shield ?? 'NOT CHECKED'`. Replace `phone || '+91 22 2788 1234'` with `phone ?? null` and render "no phone on record". Replace `icp: … !== false` with `icp: rawAudit.is_mobile_responsive === true`.

An operator should be able to tell, at a glance, **what the machine knows and what it is guessing**. Today the UI cannot express that distinction at all.

### 10.7 Target file tree (no framework, no bundler required — Jinja2 is already a FastAPI transitive dep)

```
src/api/
├── templates/
│   ├── base.html                      # shell, sprite, overlay host, boot
│   └── partials/
│       ├── sidebar.html               # generated from ROUTES
│       ├── header.html  toolbar.html  copilot.html
│       ├── views/{leads,pipeline,approvals,team,workspace,flow,lab}.html
│       ├── drawers/record.html
│       └── modals/{scout,mission,playbooks,palette,confirm}.html
├── static/
│   ├── css/
│   │   ├── tokens.css  base.css  components.css  utilities.css
│   │   └── views/{leads,pipeline,approvals,team,workspace,flow}.css
│   ├── js/
│   │   ├── core/{boot,router,store,api,dom,format,a11y,theme,sound,icons}.js
│   │   ├── components/{button,drawer,modal,toast,palette,dropdown,table,avatar,evidence}.js
│   │   ├── views/{leads,pipeline,approvals,team,workspace,flow,lab}.js
│   │   └── data/demo-seed.js          # only loaded with ?demo=1
│   └── fonts/{Inter,JetBrainsMono}.woff2
└── server.py                          # + Jinja2Templates, gzip, security headers, auth
```

ES modules (`<script type="module">`) need **no build step** and give you real file boundaries, circular-import detection and browser caching. That is the cheapest path from one 358 KB file to a maintainable app — and it keeps the door open to adding Vite later without a rewrite.

---

## 11. The "first UI" decision — which surface is primary

You asked how to merge "in UI and first UI". My recommendation, in order:

### 11.1 Which UI is the base?
**`dashboard.html` is the base.** Not because it is the prettiest, but because it is the only surface that: is served at `/`; owns the data wiring; owns the brand; owns the approvals workflow; and is already the most complete. The Agent OS and avatar lab are **feature contributions to it**, not competitors. Do not try to merge into the demo files, and do not adopt `tools/paperclip/ui` as the base — it is a separate product with ~40 `workspace:*` deps that cannot resolve inside this repo.

### 11.2 What is the first screen?
**`#/leads` (table view) — the operator's home.** Rationale: the platform's job is to produce qualified, evidence-backed prospects; the table is where that value is visible; and it is already the default (`currentViewMode = 'table'`, 5724).

But the landing screen must answer **"what needs me right now?"**, so the shell adds one persistent element the current UI lacks: a **primary action in the header** that is *stateful* —

```
[ ⌘K ]   [ Run cycle ]   [ ⚡ 3 approvals waiting → ]   [ Scout leads ]
```

If pending approvals > 0, that button is the primary (amber, count, deep-links to `#/approvals`); if 0, "Scout leads" is primary. That single rule converts the app from a dashboard-you-browse into a queue-you-clear, which is what an HITL product actually is.

### 11.3 Information architecture — 5 destinations, no duplicates

```
LEADS            #/leads          table ⇄ board · filters: audited / active / all
PIPELINE         #/pipeline       kanban
APPROVALS  (3)   #/approvals      human gate
CONVERSATIONS    #/conversations  inbound replies / closer
AGENTS           #/agents/{team|workspace|flow|lab}   tabs inside ONE destination
```

Two filters (audits, deals) stop being destinations. The Agent OS stops being three sidebar rows and becomes one destination with tabs. Sidebar goes from **8 ambiguous rows to 5 unambiguous ones**, and the toolbar's 6-button segmented control collapses into the leads view's own table/board toggle.

### 11.4 One lexicon (enforce in code review)

| Concept | The only allowed word | Banned synonyms found today |
|---|---|---|
| A business being sold to | **Lead** | Prospect, Target, Company, Record, Corridor |
| Its website check | **Audit** | Inspection, Site review, Diagnostic |
| A drafted message | **Pitch** | Draft, Copy, Message (for the human-review artifact) |
| The human gate | **Approval** | Paperclip Gate, Outbox, Decision, Review |
| An autonomous worker | **Agent** | Persona, Worker, Swarm member, Bot |
| The dark control room | **Studio** | Agent OS, Workspace, Living OS, Rakazo |

"Corridor" appears **85 times** in the file (identifiers and labels) and means "city"; "Paperclip" — a vendor name — appears 35 times inside your own product's vocabulary. This matters more than it sounds: **the UI currently has four different words for the same object, which is why the nav duplicates itself.**

---

## 12. Migration plan — phases, each one shippable

| Phase | Work | Owner-visible outcome | Est. | Acceptance |
|---|---|---|---|---|
| **0. Freeze** | First make the app runnable (venv + pinned lock, `httpx`/`playwright` added — see P-15), then snapshot every route/state as a Playwright smoke test (7 routes × light/dark) and generate a feature inventory from this audit | A reproducible build, plus a safety net so "merge" can't silently lose a view | 1–2 d | `python -m pip install -r requirements.lock` succeeds from clean; `pytest` + 14 browser assertions green before any refactor |
| **1. Split** | Extract Jinja2 `base.html` + partials; move CSS to 8 files; move JS to ES modules (mechanical, no behaviour change); self-host fonts | Same UI, 8,447-line file → 40 files ≤ 250 lines | 2–3 d | Visual diff at 3 viewports: pixel-identical; no console errors |
| **2. Spine** | Router + store + API client; sidebar/toolbar/palette/shortcuts generated from `ROUTES`; kill the 5 parallel navs | Navigation can no longer desync | 2–3 d | Every route reachable by URL, by sidebar, by palette, by shortcut — asserted in a test |
| **3. Honesty** | Remove all mock fallbacks; add explicit `?demo=1` mode + banner; evidence component; real approve receipt; remove fake delay | The UI stops lying | 2 d | An empty DB renders an empty state, never 8 fake companies; approve shows a provider receipt or an error |
| **4. Unify** | Token contract + studio mode; one component layer; one MD/one LG breakpoint set; z-index ladder; mobile off-canvas sidebar | One system, two modes, works on a phone | 3–4 d | Lighthouse a11y ≥ 95; no horizontal scroll at 375 px; all 4 routes usable at 768 px |
| **5. Harden** | Escaping/`textContent` everywhere, event delegation, CSP (report-only → enforce); focus traps; skip link; `aria-live`; reduced-motion for OS + avatars | WCAG 2.2 AA reachable; XSS closed | 3 d | `axe` zero criticals; CSP has no `unsafe-inline` |
| **6. Produce** | Auth token + CSRF; security headers; gzip; ETag/hashed assets; structured logs + request ids; `/health` depth; pinned deps + lockfile; `data/` untracked | Deployable and operable | 3 d | Runs behind a reverse proxy with auth, survives restart, logs correlate |

**Total: ~16–19 working days** for the full path, and **~8 days** to reach the point where the UI is merged, honest and demo-safe (phases 0–3) — which is the smallest set that removes the business risk.

### Non-negotiables during migration
1. **Never delete a feature to make a merge easier.** Re-home it; if a view is unreachable today, it must be *reachable* after, not removed.
2. **One route table.** Any new destination gets added there first.
3. **No new `innerHTML` on user/LLM/scraped data** — the diff must not add any.
4. **Every phase ships.** If phase 4 slips, phases 1–3 are already live and better.
5. **Feature parity is proven by test, not by opinion.** Phase 0's smoke suite is the contract.

---

## 13. Definition of done — production checklist

**UI**
- [ ] One served HTML shell, ≤ 200 lines; every view a module with `mount/unmount`
- [ ] Sidebar, toolbar, palette and shortcuts generated from one route table
- [ ] One token file; no raw hex in any component CSS (`grep -c '#'` in components = 0)
- [ ] Zero inline `onclick`; zero `innerHTML` on untrusted data; CSP with no `unsafe-inline`
- [ ] Every list has empty / loading / error / offline states
- [ ] Every async render cancellable; no unhandled promise rejections
- [ ] Light, dark and studio modes all pass at 375 / 768 / 1440
- [ ] No fabricated data without a visible demo banner

**A11y**
- [ ] Skip link; landmarks; one `h1` per view; `th[scope]` on all tables
- [ ] Focus trap + restore on every modal/drawer; `Esc` closes; background `inert`
- [ ] Contrast ≥ 4.5:1 for text, ≥ 3:1 for UI; body ≥ 14 px
- [ ] `prefers-reduced-motion` honoured by OS and avatar animations
- [ ] Full keyboard path: navigate → open record → approve → confirm, no mouse
- [ ] `axe` zero critical/serious

**Trust**
- [ ] Empty DB shows an empty state
- [ ] "Approved & dispatched" only after a provider receipt
- [ ] Evidence panel shows artifact or explicitly "not verified"
- [ ] No invented phone / URL / TTFB / TLS / compliance badge

**Ops**
- [ ] Auth on every route; strict CORS; no open proxy; path containment; SSRF guards
- [ ] Gzip; hashed static assets; `ETag`; immutable cache for `/static`
- [ ] Structured JSON logs with request id; `/health` checks storage + provider config
- [ ] Pinned deps + lockfile; `httpx` + `playwright` declared
- [ ] `data/` untracked; `tools/` as submodules
- [ ] One-command start with repo-relative paths and clear failure messages

---

## 14. Risks, and what I would *not* do

| Risk | Mitigation |
|---|---|
| Big-bang refactor breaks the demo you show clients | Phases are individually shippable; phase 0 smoke suite gates every merge |
| Splitting into files hides a regression | Visual diff at 3 viewports + route smoke test per phase |
| Re-platforming the OS pane loses the dark aesthetic | It keeps it — via `[data-mode="studio"]` tokens, declared not accidental |
| Adopting React to "fix" this | Do **not** do this now. The vendored `paperclip/ui` is proof of the cost (React 19 + Vite 8 + 40 workspace deps + 160 MB). ES modules + Jinja partials get 90 % of the benefit at 10 % of the risk. Revisit only after phase 6 |
| Deleting the demo prototypes | Don't. Move to `design/prototypes/` — they are your visual history and the best reference for the avatar engine |
| Retiring the iframe to `:5173` | Don't delete it — turn it into `#/agents/lab` with a health probe and an explicit "lab not running" state |

**Things I would not spend a day on:** a component framework, a state library, a CSS preprocessor, a design-token pipeline, or a Storybook. The file's problems are structural, not tooling-level. One router, one store, one token file and one component folder solve more than any dependency would.

---

## 15. If you only do five things this week

1. **Stop the lie.** Delete the `dry_run: true` at `dashboard.html:6673`, make approve return a real receipt, and remove `Fact check: Verified accurate` (6897) + `shield: 'PASS'` (6330). *One day. Removes the existential brand risk.*
2. **Kill the mock fallback.** Make `fetchLeads` render an empty state instead of 8 invented companies; gate the seed behind `?demo=1` with a banner. *Half a day.*
3. **Escape or die.** Add one `esc()` helper, route every `${record.*}` through it, replace inline `onclick` with `data-id` + delegation. *One day. Closes a stored-XSS hole in an operator console.*
4. **One route table.** Introduce `ROUTES` and generate sidebar + palette + shortcuts from it. *Two days. Ends the four parallel navigations.*
5. **Split the file.** `base.html` + partials + `tokens.css` + ES modules, mechanically, with a visual diff. *Three days. Makes everything else cheap.*

Then the rest is sequence, not risk.

---

*Audit performed against commit `08ca9d0` (working tree with modified `data/leads/*.json`). All line references are to the files as they exist on disk at the time of writing.*

