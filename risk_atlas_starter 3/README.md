# Risk Atlas Starter

A lightweight Streamlit starter app for Risk Atlas.

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

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Recommended next steps
1. Replace `services/mock_data.py` with real inventory and mapping data.
2. Connect the chatbot to your internal model service.
3. Add export logic for PowerPoint and Excel.
4. Add role-based visibility if needed.
5. Upgrade styling for a more polished internal app.
