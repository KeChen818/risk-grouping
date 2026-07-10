# Risk Atlas — README v1

## Overview
Risk Atlas is a Streamlit-based internal risk intelligence application that transforms a static risk inventory into an interactive, AI-enabled workspace for analysis, grouping, and reporting.

The initial product focus is the risk inventory itself. The app helps users understand top exposures, compare quantification views, review quarter-over-quarter change, group risks in a more structured way, and generate management-ready outputs.

## Product Position
Risk Atlas turns the risk inventory from a static quarterly record into an AI-powered intelligence layer for:
- risk visibility
- analysis
- grouping
- management reporting

## v1 Scope
### Navigation structure
- **Risk Profile Summary**
  - Top Exposure
  - Risk Quantification Alignment
  - QoQ Change
- **Risk Grouping**
  - Taxonomy-based
  - Theme Proposal
  - Non-material risk watchlist
- **AI Chatbot - Inventory Expert**
- **Report Export (Slides/Excel)**
- **Admin**

### Current product boundary
Connected Intelligence remains future scope and is not part of the first active build.
Potential future extensions:
- CUSO-Group Risk ID SGE Materiality Coverage
- CUSO Risk ID - RCA & Scenario Design
- CUSO Risk ID - Risk Limit/Appetite

## UX and page design principles
### Page structure
Each item above should be a real page, not a tab.

### Shared page pattern
Each page should follow a consistent structure:
1. page header
2. filter form
3. KPI metric row
4. core chart/table area
5. optional AI summary or commentary
6. module summary / next action block

### Reusable UI components
The app should use a common UI layer so each page looks and behaves consistently.
Reusable components discussed:
- shared theme / CSS
- KPI metric row
- ECharts wrapper
- section intro block
- info note block
- extendable module summary card

## AI architecture
### Agent model
The agreed target architecture is:
- **1 Inventory Expert Agent**
- **1 Report Writer Agent**

### Inventory Expert Agent
Primary analytical agent for:
- Top Exposure
- Risk Quantification Alignment
- QoQ Change
- Taxonomy-based grouping
- Theme Proposal
- Non-material risk watchlist
- inventory Q&A

### Report Writer Agent
Controlled generation agent for:
- manager-ready summaries
- slide-ready wording
- export text for reports
- Excel / slide output preparation

### AI governance layers
Keep both of these as shared services:
- **Shared tool registry**
- **Shared telemetry / logger**

#### Shared tool registry
Central catalog of agent-callable functions.
Examples:
- get_top_exposure
- get_risk_quant_alignment
- get_qoq_change
- get_taxonomy_breakdown
- get_theme_proposal
- get_non_material_watchlist
- build_risk_profile_export
- build_risk_grouping_export

Purpose:
- consistent tool naming
- schema control
- handler routing
- agent permissions

#### Shared telemetry / logger
Central logging layer for:
- agent used
- page/module used
- model and prompt version
- tools called
- token usage
- latency
- success/failure
- export events

Purpose:
- admin monitoring
- token usage tracking
- debugging
- auditability

### Skills
Skills are not required for v1.
They are a future enhancement for repeatable multi-step AI workflows, especially for:
- QoQ management summary
- theme review workflow
- report writing workflows
- standardized slide narrative generation

## Data and storage architecture
### Agreed direction
- **Postgres** as the system of record
- **Redis** reserved for future shared cache / jobs / session support

### Postgres should store
- risk inventory snapshots
- historical assessments
- taxonomy mappings
- theme proposal outputs
- watchlist records
- prompt versions
- usage logs
- export history
- admin config

### Redis (future)
Use later for:
- shared hot cache
- queued jobs for exports
- shared session/chat support
- cross-instance coordination

## Streamlit execution strategy
The agreed performance and token-friendly design is:
- load the page shell first
- do not auto-run the LLM on page load
- use forms so filter changes do not rerun expensive logic immediately
- only run the selected module when the user submits
- cache deterministic results
- persist reusable AI summaries

### Recommended execution rules
- **Default load**: show header, filters, cheap cached KPIs, and optionally prior saved results
- **User submit**: run only the selected page/module
- **AI calls**: only when explicitly triggered by user action

### Streamlit caching approach
- `st.cache_data` for deterministic query results, transforms, and analytics outputs
- `st.cache_resource` for shared clients and connections
- `st.session_state` for user-specific transient state
- Postgres for durable AI summary cache and logs

## Admin page
The app should include an Admin page.

### Admin functions
- cache maintenance
- token usage monitoring
- prompt and model config visibility
- AI health / errors
- export history
- session/cache control where appropriate

### Suggested Admin sections
- Cache & State
- Token Usage
- Prompt Config
- AI Health

## Product messaging for management
### Core message
Risk Atlas transforms the risk inventory from a static quarterly record into an AI-powered intelligence layer for risk visibility, analysis, grouping, and reporting.

### What it delivers
- stronger visibility into top exposures and QoQ change
- more structured grouping through taxonomy and AI theme proposal
- inventory insights that can be turned into management-ready output

## v1 build priorities
1. establish final page structure
2. build reusable UI layer
3. implement deterministic analytics modules
4. add Inventory Expert Agent with tool support
5. add Report Writer Agent for reporting outputs
6. add Admin page and telemetry
7. connect Postgres for persistence and reusable AI outputs

## Non-goals for v1
- fully autonomous multi-agent orchestration
- Redis as day-one infrastructure
- Connected Intelligence module implementation
- advanced skills framework
- full background job system

## Summary
Risk Atlas v1 should be a focused inventory intelligence application with clean page-based navigation, strong reusable UI, controlled AI support, durable telemetry, and a scalable architecture that can expand into Connected Intelligence later.
