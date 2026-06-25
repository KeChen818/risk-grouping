# AI Risk Theme Assignment Engine

Streamlit demo prototype for assigning structured risk inventory rows to executive-level risk themes.

## Structure

```text
risk-theme-demo/
├── app.py
├── theme_engine.py
├── data/
│   ├── demo_inventory.xlsx
│   └── risk_theme_library.yaml
├── vector_store/
│   ├── theme_index.faiss
│   └── theme_metadata.json
├── output/
├── requirements.txt
└── README.md
```

`app.py` contains the Streamlit UI. `theme_engine.py` contains loading, vector-store management, candidate retrieval, hybrid scoring, assignment, summaries, optional LLM narrative enrichment, Excel export, and PowerPoint export.

## Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

The app loads `data/demo_inventory.xlsx` by default and can also accept uploaded CSV or Excel inventories.

Optional GPT narrative enrichment uses the OpenAI Python SDK. Set an environment variable before launching Streamlit, or enter an API key in the **AI Narratives** tab:

```bash
export OPENAI_API_KEY="your_api_key"
```

## Vector Store

On startup, the app attempts to load:

- `vector_store/theme_index.faiss`
- `vector_store/theme_metadata.json`

If those files are missing, it builds them from `data/risk_theme_library.yaml` using `sentence-transformers/all-MiniLM-L6-v2` and FAISS. The sidebar button **Rebuild Theme Vector Store** forces a rebuild.

If FAISS or `sentence-transformers` is unavailable, the app falls back gracefully to TF-IDF cosine similarity so the demo still runs.

## Assignment Method

The vector store is used for semantic candidate retrieval only. The final assignment combines semantic evidence with structured metadata:

```text
final_score =
    0.50 * semantic_similarity
  + 0.20 * business_match_score
  + 0.15 * risk_type_match_score
  + 0.10 * root_cause_match_score
  + 0.05 * keyword_match_score
```

Each risk receives one primary theme. Ambiguous or low-confidence items are flagged for human review and can receive an override theme.

## Optional LLM Narratives

The **AI Narratives** tab can call the OpenAI Responses API with a configurable model name, defaulting to `gpt-5.2`.

This step is intentionally separate from assignment. It enriches the existing outputs with:

- `llm_summary`
- `llm_key_drivers`
- `llm_management_takeaway`
- `llm_assignment_justification`
- `llm_evidence`

The prompt instructs the model to use only the supplied inventory, assignment scores, review flags, deterministic rationale, and theme summary data. If no API key is provided, the app still runs with the rule-based `ai_summary` fields.

## Exports

After running assignment, the **Exports** tab provides:

- **Export Excel Workbook**: assigned inventory, review queue, theme summary, and theme library.
- **Export Theme Summary Excel**: theme summary only.
- **Export Slides**: PowerPoint deck with one overall summary slide plus one detail slide per selected theme.

Slide export scope can be set to:

- **Top 5 assigned themes**
- **All assigned themes**

Each theme detail slide includes the LLM summary when generated, otherwise the rule-based AI summary, key theme signals, and all underlying assigned risks for that theme.

The Exports tab also includes deck polish controls for title, subtitle, export scope, and slide style preset.
