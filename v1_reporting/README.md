# Risk Atlas AI Report Writer — Streamlit Demo

A runnable Streamlit MVP implementing a **guided reporting workflow**:

**Short goal → Live report plan → Focused confirmation → Generate → Download**

## What this version demonstrates

- Starts from a short natural-language report goal.
- Infers an initial legal entity, business division, population, audience and section set.
- Reveals the live report plan only after the short goal is reviewed.
- Moves confirmation into a focused page before generation.
- Keeps the final page scoped to confirmation and generation status/download.
- Synchronizes goal, structured scope, report sections, live preview and output filename.
- Supports dependent legal-entity/business-division selections.
- Preserves a manually customized filename until the user resets it.
- Invalidates confirmation automatically after any plan change.
- Shows generation status on the same page with `st.status`.
- Produces a real `.pptx` package using `python-pptx`.

## Run locally

```bash
cd risk_atlas_guided_reporting
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Then open the local Streamlit URL shown in the terminal, typically:

```text
http://localhost:8501
```

## Production integration points

### Goal interpretation

Replace `infer_plan_from_goal()` in `report_engine.py` with an AICE/LLM structured-output call that returns the same `ReportPlan` schema.

### Inventory retrieval

Use only the confirmed structured scope to query inventory data:

```python
filters = {
    "inventory": plan.inventory,
    "comparison": plan.comparison,
    "legal_entity": plan.legal_entity,
    "business_division": plan.business_division,
    "risk_population": plan.risk_population,
}
```

The natural-language goal should control analysis and narrative, not bypass confirmed filters.

### Report generation

Replace `_placeholder_content()` with your existing Risk Atlas skills, such as portfolio summary, top risks, QoQ comparison, quantification alignment, concentration analysis, management actions and source Risk ID appendix.

### Long-running jobs

For production, replace the synchronous demo loop with a queue or job table using statuses such as:

```text
PENDING → RUNNING → VALIDATING → COMPLETED / FAILED
```
