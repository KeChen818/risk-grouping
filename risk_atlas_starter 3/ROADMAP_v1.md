# Risk Atlas — Roadmap v1

## Objective
Build Risk Atlas as a focused inventory intelligence application first, with a strong foundation for future connected risk workflows.

## Product scope agreed so far
### In scope for v1
- Risk Profile Summary
  - Top Exposure
  - Risk Quantification Alignment
  - QoQ Change
- Risk Grouping
  - Taxonomy-based
  - Theme Proposal
  - Non-material risk watchlist
- AI Chatbot - Inventory Expert
- Report Export (Slides/Excel)
- Admin

### Future scope
- Connected Intelligence
  - CUSO-Group Risk ID SGE Materiality Coverage
  - CUSO Risk ID - RCA & Scenario Design
  - CUSO Risk ID - Risk Limit/Appetite
- Skills layer for advanced AI workflows
- Redis-backed shared cache and jobs

---

## Roadmap phases

## Phase 0 — Foundation and design lock
### Goal
Finalize the product structure and implementation direction.

### Key outcomes
- final page-based navigation agreed
- reusable UI pattern agreed
- architecture direction agreed
- v1 scope separated from future scope

### Deliverables
- page list and grouping
- README v1
- Roadmap v1
- manager summary slides

---

## Phase 1 — App shell and reusable UI
### Goal
Create a clean, consistent Streamlit application shell.

### Features
- grouped sidebar navigation
- one page per module
- shared theme / CSS
- KPI metric row component
- ECharts wrapper
- section intro component
- module summary card

### Deliverables
- app shell
- reusable components package
- polished first-pass page templates

### Success criteria
- all main pages render with consistent layout
- no page-specific styling drift
- page structure is ready for real data

---

## Phase 2 — Deterministic analytics modules
### Goal
Implement non-LLM business logic first.

### Risk Profile Summary pages
#### Top Exposure
- exposure ranking
- key KPI strip
- exposure charts and detail table

#### Risk Quantification Alignment
- comparison views across scope
- alignment summary
- mismatch table / highlight logic

#### QoQ Change
- new / retired / changed items
- top movers
- quarter-over-quarter trend logic

### Risk Grouping pages
#### Taxonomy-based
- taxonomy distribution
- grouped risk views
- detail table

#### Theme Proposal
- initial AI-assisted grouping output surface
- theme buckets
- review-friendly display

#### Non-material risk watchlist
- flagged non-material items
- trend / pattern support
- monitoring list view

### Success criteria
- pages work without AI dependency
- analytics output is stable and testable
- loading remains fast for common cases

---

## Phase 3 — AI layer v1
### Goal
Add controlled AI support with clear boundaries.

### Agent decisions
- 1 Inventory Expert Agent
- 1 Report Writer Agent

### Inventory Expert Agent
#### Responsibilities
- answer inventory questions
- explain exposure and QoQ change
- support grouping interpretation
- call app-owned tools/functions

### Report Writer Agent
#### Responsibilities
- produce manager-ready text
- create slide-ready wording
- support export language generation

### Shared AI services
#### Shared tool registry
- central tool definitions
- argument schemas
- handler routing
- agent permission control

#### Shared telemetry/logger
- token usage logging
- page/module tracking
- tool-call logging
- latency and error capture

### Success criteria
- AI is only triggered intentionally
- tool-calling is stable
- token usage becomes observable
- reporting output is reusable

---

## Phase 4 — Data persistence and admin controls
### Goal
Make the app operationally usable.

### Storage direction
- Postgres as system of record
- Redis held for future use only

### Postgres scope
- inventory snapshots
- historical assessments
- theme outputs
- prompt versions
- usage logs
- export history
- admin settings

### Admin page
#### Sections
- Cache & State
- Token Usage
- Prompt Config
- AI Health

#### Functions
- cache clear actions
- session control where appropriate
- token usage review
- prompt/model visibility
- recent error tracking

### Success criteria
- durable logs exist
- admin can monitor AI usage
- cached summaries can be reused

---

## Phase 5 — Performance and token optimization
### Goal
Keep the app responsive and token-efficient.

### Agreed design principles
- shell first, compute later
- no automatic LLM call on page load
- forms for filter submission
- run only selected module when user submits
- cache deterministic results
- reuse cached AI outputs whenever possible

### Technical approach
- `st.cache_data` for deterministic analytics outputs
- `st.cache_resource` for clients and connections
- `st.session_state` for user-specific transient state
- Postgres for durable AI summary cache and logs

### Future optimization path
- Redis for shared hot cache
- Redis for job queue / export background tasks
- broader cross-user reuse once scaling requires it

### Success criteria
- low unnecessary token use
- reduced repeated computations
- acceptable multi-user performance

---

## Future roadmap after v1
### Connected Intelligence
Potential future modules:
- CUSO-Group Risk ID SGE Materiality Coverage
- CUSO Risk ID - RCA & Scenario Design
- CUSO Risk ID - Risk Limit/Appetite

### Skills layer
Potential future skills:
- QoQ management summary workflow
- report writing workflow
- theme review workflow
- standardized export narrative workflow

### Redis expansion
Future Redis use cases:
- shared cache across workers
- background export jobs
- cross-instance session support
- fast transient coordination

---

## Final takeaway
### What v1 should be
A focused, page-based, inventory intelligence application with:
- strong reusable UI
- deterministic analytics first
- controlled AI support
- operational telemetry
- Postgres-backed persistence

### What v1 should not try to be
- a large multi-agent autonomous platform
- a fully connected end-to-end risk operating model
- a heavy infrastructure build before product value is proven

### Guiding principle
Build a clean, useful inventory intelligence product first, then expand into connected intelligence and more advanced AI workflow capabilities.
