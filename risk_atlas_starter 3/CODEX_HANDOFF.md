# Codex handoff: Risk Atlas Streamlit app

## Objective
Turn this starter into a polished internal app aligned to the current product structure.

## Information architecture
- Overview
- Risk Profile Summary
  - Top Exposure
  - Risk Quantification Alignment
  - QoQ Change
- Risk Grouping
  - Taxonomy-based
  - Theme Proposal
  - Non-material risk watchlist
- AI Chatbot - Inventory Expert
- Report Export
  - Slides / Excel
  - Risk Profile
  - Risk Grouping
- Connected Intelligence
  - CUSO-Group Risk ID SGE Materiality Coverage
  - CUSO Risk ID - RCA & Scenario Design
  - CUSO Risk ID - Risk Limit/Appetite

## UX rules
- Keep sidebar navigation flat.
- Use tabs inside each page for sub-functions.
- Keep global filters only in the sidebar.
- QoQ Change belongs under Risk Profile Summary.
- AI should be positioned as an inventory expert, not a generic chatbot.
- Use the page titles above directly in the UI.

## Build tasks
1. Improve styling for a cleaner enterprise look.
2. Add better KPI cards and visual hierarchy on Risk Profile Summary.
3. Add stronger grouping visuals on Risk Grouping.
4. Keep Report Export focused on Risk Profile and Risk Grouping outputs.
5. Add empty-state messaging when filters return no rows.
6. Prepare hooks for future PowerPoint and Excel generation.
7. Keep code modular and easy to extend.

## Nice-to-have
- Search within Risk Profile Summary
- Saved prompt buttons in AI Chatbot
- Simple badges for mapped / partial / not mapped statuses
- Cleaner Overview launch cards

## Acceptance criteria
- App runs with `streamlit run app.py`
- Navigation matches the information architecture above
- Risk Profile Summary reads as the main workflow
- Risk Grouping is clearly separate from profile summary
- Connected Intelligence uses the exact title above
- Overview works as a clean launcher
