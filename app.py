from __future__ import annotations

import html
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from theme_engine import OUTPUT_COLUMNS, SUMMARY_COLUMNS, ThemeEngine


BASE_DIR = Path(__file__).resolve().parent
APP_TITLE = "AI Risk Theme Assignment Engine"


def configure_page(page_title: str | None = None) -> None:
    st.set_page_config(
        page_title=page_title or APP_TITLE,
        page_icon="RT",
        layout="wide",
        initial_sidebar_state="expanded",
    )


def inject_css() -> None:
    st.markdown(
        """
        <style>
        :root {
            --bg: #f5f2ec;
            --bg-card: #fff;
            --ink: #1a1814;
            --ink-soft: #5c5650;
            --line: #e3ddd2;
            --line-soft: #ecebe6;
            --accent: #d64545;
            --green: #2f7d6d;
        }
        .block-container {
            padding-top: 1.35rem;
            padding-bottom: 2rem;
        }
        .stApp {
            background: var(--bg);
            color: var(--ink);
        }
        header[data-testid="stHeader"],
        div[data-testid="stDecoration"] {
            background: var(--bg);
        }
        section[data-testid="stSidebar"] {
            background: #eee8de;
            border-right: 1px solid var(--line);
        }
        h1, h2, h3, p, label {
            letter-spacing: 0 !important;
            color: var(--ink);
        }
        h1 {
            font-size: 1.55rem !important;
            margin-bottom: 0.1rem !important;
        }
        h2 {
            font-size: 1.05rem !important;
            margin-top: 0.5rem !important;
        }
        div[data-testid="stMetric"] {
            border: 1px solid var(--line);
            border-radius: 8px;
            padding: 0.8rem 0.9rem;
            background: var(--bg-card);
            min-height: 98px;
            box-shadow: 0 1px 1px rgba(26, 24, 20, 0.04);
        }
        div[data-testid="stMetric"] label {
            color: var(--ink-soft);
        }
        div[data-testid="stMetricValue"] {
            color: var(--ink);
            font-size: 1.45rem;
        }
        div[data-testid="stMetricDelta"] {
            color: var(--accent);
        }
        div[data-testid="stTabs"] button {
            border-radius: 8px 8px 0 0;
        }
        div[data-testid="stTabs"] button[aria-selected="true"] {
            border-bottom-color: var(--accent);
            color: var(--accent);
        }
        .app-subtitle {
            color: var(--ink-soft);
            font-size: 0.92rem;
            margin: 0 0 0.65rem;
        }
        .status-strip {
            align-items: center;
            background: var(--bg-card);
            border: 1px solid var(--line);
            border-radius: 8px;
            display: flex;
            gap: 0.65rem;
            justify-content: space-between;
            margin: 0.35rem 0 0.85rem;
            padding: 0.7rem 0.85rem;
            box-shadow: 0 1px 1px rgba(26, 24, 20, 0.04);
        }
        .status-strip strong {
            color: var(--ink);
            font-size: 0.88rem;
        }
        .status-strip span {
            color: var(--ink-soft);
            font-size: 0.82rem;
        }
        .status-pill {
            background: #fff6f6;
            border: 1px solid #f0c6c6;
            border-radius: 999px;
            color: var(--accent);
            font-size: 0.72rem;
            font-weight: 700;
            padding: 0.28rem 0.55rem;
            text-transform: uppercase;
            white-space: nowrap;
        }
        .status-pill-ok {
            background: #edf8f5;
            border-color: #bfded5;
            color: var(--green);
        }
        .section-kicker,
        .review-controls-title {
            color: var(--ink-soft);
            font-size: 0.78rem;
            font-weight: 700;
            margin: 0.9rem 0 0.35rem;
            text-transform: uppercase;
        }
        .panel-card,
        .method-card,
        .taxonomy-card {
            border: 1px solid var(--line);
            border-radius: 8px;
            background: var(--bg-card);
            padding: 0.9rem;
            margin-bottom: 0.65rem;
            box-shadow: 0 1px 1px rgba(26, 24, 20, 0.04);
        }
        .panel-card h3,
        .method-card h3,
        .taxonomy-card h3 {
            font-size: 1rem;
            line-height: 1.25;
            margin: 0 0 0.55rem;
        }
        .taxonomy-meta,
        .method-card p,
        .panel-card p {
            color: var(--ink-soft);
            font-size: 0.82rem;
            line-height: 1.45;
            margin-bottom: 0.35rem;
        }
        .ai-card-title {
            color: var(--accent);
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0 !important;
            margin-bottom: 0.4rem;
            text-transform: uppercase;
        }
        .risk-pop-card {
            border: 1px solid var(--line-soft);
            border-radius: 8px;
            background: #fffaf2;
            padding: 0.75rem;
            margin: 0 0 0.6rem;
        }
        .risk-pop-card b {
            color: var(--ink);
            display: block;
            font-size: 0.92rem;
            line-height: 1.3;
            margin-bottom: 0.35rem;
        }
        .risk-pop-card span {
            color: var(--ink-soft);
            display: block;
            font-size: 0.78rem;
            line-height: 1.45;
        }
        .risk-table-wrap {
            border: 1px solid var(--line);
            border-radius: 8px;
            background: #fff;
            max-height: 520px;
            overflow: auto;
            width: 100%;
            box-shadow: 0 1px 1px rgba(26, 24, 20, 0.04);
        }
        .risk-table-wrap-wide {
            overflow-x: auto;
            overflow-y: auto;
        }
        .risk-html-table {
            background: #fff;
            border-collapse: separate;
            border-spacing: 0;
            color: var(--ink);
            font-size: 0.82rem;
            line-height: 1.35;
            width: 100%;
        }
        .risk-table-wrap-wide .risk-html-table {
            min-width: 1680px;
            width: max-content;
        }
        .risk-html-table thead th {
            background: var(--line-soft);
            border-bottom: 1px solid var(--line);
            color: var(--ink);
            font-weight: 700;
            padding: 0.56rem 0.68rem;
            position: sticky;
            text-align: left;
            top: 0;
            z-index: 1;
        }
        .risk-html-table tbody tr,
        .risk-html-table tbody td {
            background: #fff !important;
        }
        .risk-html-table tbody td {
            border-bottom: 1px solid var(--line-soft);
            color: var(--ink);
            padding: 0.52rem 0.68rem;
            vertical-align: top;
        }
        .risk-html-table tbody tr:hover td {
            background: #fff !important;
        }
        .risk-table-wrap-wide .risk-html-table th,
        .risk-table-wrap-wide .risk-html-table td {
            min-width: 130px;
            white-space: nowrap;
        }
        .risk-table-wrap-wide .risk-html-table th:nth-child(2),
        .risk-table-wrap-wide .risk-html-table td:nth-child(2),
        .risk-table-wrap-wide .risk-html-table th:nth-child(5),
        .risk-table-wrap-wide .risk-html-table td:nth-child(5),
        .risk-table-wrap-wide .risk-html-table th:nth-child(6),
        .risk-table-wrap-wide .risk-html-table td:nth-child(6),
        .risk-table-wrap-wide .risk-html-table th:nth-child(8),
        .risk-table-wrap-wide .risk-html-table td:nth-child(8),
        .risk-table-wrap-wide .risk-html-table th:nth-child(14),
        .risk-table-wrap-wide .risk-html-table td:nth-child(14),
        .risk-table-wrap-wide .risk-html-table th:nth-child(15),
        .risk-table-wrap-wide .risk-html-table td:nth-child(15) {
            min-width: 240px;
            white-space: normal;
        }
        .risk-table-wrap-wide .risk-html-table .col-assignment-rationale,
        .risk-table-wrap-wide .risk-html-table .col-llm-assignment-justification,
        .risk-table-wrap-wide .risk-html-table .col-llm-evidence,
        .risk-table-wrap-wide .risk-html-table .col-key-risk-titles,
        .risk-table-wrap-wide .risk-html-table .col-ai-summary,
        .risk-table-wrap-wide .risk-html-table .col-llm-summary,
        .risk-table-wrap-wide .risk-html-table .col-llm-key-drivers,
        .risk-table-wrap-wide .risk-html-table .col-llm-management-takeaway {
            min-width: 300px;
            white-space: normal;
        }
        .col-total-risks,
        .col-material-risks,
        .col-risks {
            color: var(--ink);
            font-variant-numeric: tabular-nums;
            font-weight: 700;
            text-align: right;
            white-space: nowrap;
        }
        .score-bar-cell {
            align-items: center;
            display: flex;
            gap: 0.5rem;
            min-width: 116px;
        }
        .score-bar-track {
            background: var(--line-soft);
            border: 1px solid var(--line);
            border-radius: 999px;
            height: 7px;
            min-width: 72px;
            overflow: hidden;
        }
        .score-bar-fill {
            background: var(--accent);
            display: block;
            height: 100%;
        }
        .score-bar-fill-secondary {
            background: var(--green);
        }
        .score-bar-label {
            color: var(--ink-soft);
            font-size: 0.74rem;
            font-variant-numeric: tabular-nums;
            min-width: 2rem;
        }
        .bool-badge {
            border-radius: 999px;
            display: inline-block;
            font-size: 0.68rem;
            font-weight: 700;
            line-height: 1;
            min-width: 42px;
            padding: 0.28rem 0.45rem;
            text-align: center;
            text-transform: uppercase;
        }
        .bool-badge-true {
            background: #f8d7d7;
            color: #9f2f2f;
        }
        .bool-badge-false {
            background: var(--line-soft);
            color: var(--ink-soft);
        }
        div[data-testid="stDataFrame"],
        div[data-testid="stDataEditor"] {
            border: 1px solid var(--line);
            border-radius: 8px;
            background: #fff !important;
            overflow: hidden;
        }
        div[data-testid="stDataFrame"] > div,
        div[data-testid="stDataEditor"] > div {
            background: var(--bg-card) !important;
        }
        div[data-testid="stDataFrame"] [role="columnheader"],
        div[data-testid="stDataEditor"] [role="columnheader"],
        div[data-testid="stDataFrame"] thead th,
        div[data-testid="stDataEditor"] thead th {
            background: var(--line-soft) !important;
            color: var(--ink) !important;
        }
        div[data-testid="stExpander"] {
            background: var(--bg-card);
            border-color: var(--line) !important;
            border-radius: 8px;
        }
        div[data-testid="stExpander"] summary,
        details[data-testid="stExpander"] summary {
            background: var(--line-soft) !important;
            border-radius: 8px;
        }
        .stButton button, .stDownloadButton button {
            border-radius: 8px;
            border-color: var(--line);
            color: var(--ink);
            background: var(--bg-card);
        }
        .stButton button:hover, .stDownloadButton button:hover {
            border-color: var(--accent);
            color: var(--accent);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


configure_page()
inject_css()


@st.cache_resource(show_spinner=False)
def get_engine() -> ThemeEngine:
    engine = ThemeEngine(BASE_DIR)
    engine.initialize()
    return engine


def reset_results() -> None:
    st.session_state.assigned_df = pd.DataFrame()
    st.session_state.candidates_df = pd.DataFrame()
    st.session_state.theme_summary_df = pd.DataFrame(columns=SUMMARY_COLUMNS)
    st.session_state.llm_log_df = pd.DataFrame()


def material_count(df: pd.DataFrame) -> int:
    if "materiality" not in df.columns:
        return 0
    values = df["materiality"].fillna("").astype(str).str.lower().str.strip()
    return int(values.isin(["material", "yes", "true", "high"]).sum())


def section_label(text: str) -> None:
    st.markdown(f"<div class='section-kicker'>{html.escape(text)}</div>", unsafe_allow_html=True)


def safe_value(value: object) -> str:
    if value is None:
        return ""
    try:
        if pd.isna(value):
            return ""
    except TypeError:
        pass
    return str(value)


def score_bar(value: object, secondary: bool = False) -> str:
    text = safe_value(value)
    if not text:
        return ""
    try:
        score = float(text)
    except ValueError:
        return html.escape(text)
    width = max(0.0, min(score, 1.0)) * 100
    fill_class = "score-bar-fill score-bar-fill-secondary" if secondary else "score-bar-fill"
    return (
        "<div class='score-bar-cell'>"
        "<div class='score-bar-track'>"
        f"<span class='{fill_class}' style='width:{width:.0f}%'></span>"
        "</div>"
        f"<span class='score-bar-label'>{score:.2f}</span>"
        "</div>"
    )


def review_badge(value: object) -> str:
    text = safe_value(value) or "No"
    is_review = text.lower() == "yes"
    badge_class = "bool-badge-true" if is_review else "bool-badge-false"
    return f"<span class='bool-badge {badge_class}'>{html.escape(text)}</span>"


def column_class(column: str) -> str:
    clean = "".join(char if char.isalnum() else "-" for char in column.lower())
    while "--" in clean:
        clean = clean.replace("--", "-")
    return f"col-{clean.strip('-')}"


def render_html_table(
    df: pd.DataFrame,
    columns: list[str] | None = None,
    *,
    wide: bool = False,
    max_rows: int = 200,
) -> None:
    if columns is None:
        columns = list(df.columns)
    visible = df.loc[:, [column for column in columns if column in df.columns]].head(max_rows).copy()

    if visible.empty:
        st.info("No records to display.")
        return

    score_columns = {
        "primary_theme_score",
        "secondary_theme_score",
        "score_gap",
        "semantic_similarity",
        "business_match_score",
        "risk_type_match_score",
        "root_cause_match_score",
        "keyword_match_score",
        "final_score",
    }
    header = "".join(
        f"<th class='{column_class(column)}'>{html.escape(column.replace('_', ' ').title())}</th>"
        for column in visible.columns
    )
    rows = []
    for _, row in visible.iterrows():
        cells = []
        for column in visible.columns:
            value = row[column]
            if column in score_columns:
                rendered = score_bar(value, secondary=column == "secondary_theme_score")
            elif column == "review_flag":
                rendered = review_badge(value)
            else:
                rendered = html.escape(safe_value(value))
            cells.append(f"<td class='{column_class(column)}'>{rendered}</td>")
        rows.append("<tr>" + "".join(cells) + "</tr>")

    wrap_class = "risk-table-wrap risk-table-wrap-wide" if wide else "risk-table-wrap"
    st.markdown(
        f"""
        <div class="{wrap_class}">
            <table class="risk-html-table">
                <thead><tr>{header}</tr></thead>
                <tbody>{''.join(rows)}</tbody>
            </table>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_status_strip(status_text: str, status_message: str, ok: bool) -> None:
    pill_class = "status-pill status-pill-ok" if ok else "status-pill"
    pill_text = "Vector Store Ready" if ok else "Fallback Mode"
    st.markdown(
        f"""
        <div class="status-strip">
            <div>
                <strong>{html.escape(status_text)}</strong><br>
                <span>{html.escape(status_message)}</span>
            </div>
            <div class="{pill_class}">{pill_text}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_theme_cards(summary_df: pd.DataFrame, limit: int = 3) -> None:
    if summary_df.empty:
        return
    for _, row in summary_df.head(limit).iterrows():
        st.markdown(
            f"""
            <div class="taxonomy-card">
                <div class="ai-card-title">{html.escape(safe_value(row['domain']))}</div>
                <h3>{html.escape(safe_value(row['theme_name']))}</h3>
                <div class="taxonomy-meta">
                    {int(row['total_risks'])} risks | {int(row['material_risks'])} material |
                    {html.escape(safe_value(row['risk_types']))}
                </div>
                <div class="taxonomy-meta">{html.escape(safe_value(row['top_root_causes']))}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_method_card(title: str, body: str, kicker: str = "Methodology") -> None:
    st.markdown(
        f"""
        <div class="method-card">
            <div class="ai-card-title">{html.escape(kicker)}</div>
            <h3>{html.escape(title)}</h3>
            <p>{html.escape(body)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def filter_assigned_inventory(df: pd.DataFrame) -> pd.DataFrame:
    filtered = df.copy()
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        business_units = st.multiselect(
            "Business unit",
            sorted(filtered["business_unit"].dropna().unique()),
        )
    with col2:
        risk_types = st.multiselect("Risk type", sorted(filtered["risk_type"].dropna().unique()))
    with col3:
        themes = st.multiselect("Theme", sorted(filtered["primary_theme"].dropna().unique()))
    with col4:
        review_flags = st.multiselect(
            "Review flag",
            sorted(filtered["review_flag"].dropna().unique()),
        )
    with col5:
        materialities = st.multiselect(
            "Materiality",
            sorted(filtered.get("materiality", pd.Series(dtype=str)).dropna().unique()),
        )

    if business_units:
        filtered = filtered[filtered["business_unit"].isin(business_units)]
    if risk_types:
        filtered = filtered[filtered["risk_type"].isin(risk_types)]
    if themes:
        filtered = filtered[filtered["primary_theme"].isin(themes)]
    if review_flags:
        filtered = filtered[filtered["review_flag"].isin(review_flags)]
    if materialities and "materiality" in filtered.columns:
        filtered = filtered[filtered["materiality"].isin(materialities)]
    return filtered


def apply_review_edits(engine: ThemeEngine, edited_review: pd.DataFrame) -> None:
    assigned = st.session_state.assigned_df.copy()
    for _, row in edited_review.iterrows():
        risk_id = row["risk_id"]
        override = str(row.get("human_override_theme", "") or "").strip()
        mask = assigned["risk_id"] == risk_id
        assigned.loc[mask, "human_override_theme"] = override
        assigned.loc[mask, "final_theme"] = override if override else assigned.loc[mask, "primary_theme"]

    st.session_state.assigned_df = assigned
    st.session_state.theme_summary_df = engine.generate_theme_summary(assigned)


engine = get_engine()

if "inventory_df" not in st.session_state:
    st.session_state.inventory_df = engine.load_demo_inventory()
    st.session_state.data_source = "Demo inventory"

if "assigned_df" not in st.session_state:
    reset_results()

st.title(APP_TITLE)
st.markdown(
    "<div class='app-subtitle'>Executive risk theme assignment using vector retrieval plus structured metadata scoring.</div>",
    unsafe_allow_html=True,
)

status = engine.vector_store_status()
status_text = (
    f"Vector backend: {status.backend} | Themes: {status.theme_count} | "
    f"Index: {Path(status.index_path).name}"
)
render_status_strip(status_text, status.message, ok=not status.backend.startswith("TF-IDF"))

with st.sidebar:
    st.header("Controls")

    uploaded_file = st.file_uploader("Upload risk inventory", type=["csv", "xlsx", "xls"])
    if uploaded_file is not None:
        try:
            st.session_state.inventory_df = engine.load_inventory(uploaded_file)
            st.session_state.data_source = uploaded_file.name
            reset_results()
        except Exception as exc:
            st.error(str(exc))

    if st.button("Load Demo Data", width="stretch"):
        st.session_state.inventory_df = engine.load_demo_inventory()
        st.session_state.data_source = "Demo inventory"
        reset_results()

    if st.button("Rebuild Theme Vector Store", width="stretch"):
        with st.spinner("Rebuilding theme vector store..."):
            rebuild_status = engine.rebuild_vector_store()
        if rebuild_status.backend.startswith("TF-IDF"):
            st.warning(rebuild_status.message)
        else:
            st.success(rebuild_status.message)

    st.divider()
    auto_threshold = st.slider(
        "Auto-assignment threshold",
        min_value=0.50,
        max_value=0.95,
        value=0.80,
        step=0.01,
    )
    review_threshold = st.slider(
        "Low-confidence threshold",
        min_value=0.40,
        max_value=0.90,
        value=0.70,
        step=0.01,
    )
    ambiguity_gap = st.slider(
        "Minimum score gap",
        min_value=0.00,
        max_value=0.30,
        value=0.10,
        step=0.01,
    )

    if st.button("Run Theme Assignment", type="primary", width="stretch"):
        with st.spinner("Assigning executive risk themes..."):
            assigned, candidates = engine.assign_inventory(
                st.session_state.inventory_df,
                auto_threshold=auto_threshold,
                review_threshold=review_threshold,
                ambiguity_gap=ambiguity_gap,
            )
            st.session_state.assigned_df = assigned
            st.session_state.candidates_df = candidates
            st.session_state.theme_summary_df = engine.generate_theme_summary(assigned)

    st.divider()
    if st.session_state.assigned_df.empty:
        st.caption("Run assignment, then use the Exports tab for Excel and slide downloads.")
    else:
        st.caption("Excel and slide downloads are available in the Exports tab.")

inventory_df = st.session_state.inventory_df
assigned_df = st.session_state.assigned_df

st.markdown(
    f"<div class='small-caption'>Current inventory: {st.session_state.data_source} | "
    f"{len(inventory_df):,} risks | {len(engine.themes_df):,} themes in library</div>",
    unsafe_allow_html=True,
)

tabs = st.tabs(
    [
        "Overview",
        "Assigned Inventory",
        "Human Review Queue",
        "Theme Summary",
        "Theme Library",
        "AI Narratives",
        "Exports",
        "Methodology",
    ]
)

with tabs[0]:
    if assigned_df.empty:
        section_label("Demo Inventory Preview")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total risks", f"{len(inventory_df):,}")
        col2.metric("Library themes", f"{len(engine.themes_df):,}")
        col3.metric("Vector backend", status.backend.split(" ")[0])
        col4.metric("Review items", "Run assignment")
        st.markdown(
            """
            <div class="panel-card">
                <div class="ai-card-title">Ready To Classify</div>
                <h3>Load a file or use the demo inventory</h3>
                <p>The engine will retrieve candidate themes from the local vector store and then apply business unit, risk type, root cause, and keyword evidence before assigning the final theme.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        render_html_table(
            inventory_df,
            columns=[
                "risk_id",
                "risk_title",
                "business_unit",
                "risk_type",
                "taxonomy",
                "root_cause",
                "materiality",
            ],
            wide=True,
            max_rows=15,
        )
    else:
        review_items = int((assigned_df["review_flag"] == "Yes").sum())
        auto_items = int((assigned_df["review_flag"] == "No").sum())
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total risks", f"{len(assigned_df):,}")
        col2.metric("Themes used", f"{assigned_df['primary_theme'].nunique():,}")
        col3.metric("Review items", f"{review_items:,}", delta=f"{auto_items:,} auto assigned")
        col4.metric("Material risks", f"{material_count(assigned_df):,}")

        section_label("Portfolio View")
        chart_left, chart_right = st.columns([1.35, 1])
        with chart_left:
            theme_counts = (
                assigned_df["primary_theme"]
                .value_counts()
                .rename_axis("theme")
                .reset_index(name="risks")
                .head(15)
            )
            fig = px.bar(
                theme_counts,
                x="risks",
                y="theme",
                orientation="h",
                color="risks",
                color_continuous_scale=["#4b5563", "#2f9e8f", "#7c3aed"],
                title="Risks by theme",
            )
            fig.update_layout(
                yaxis={"categoryorder": "total ascending"},
                height=500,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="#fff",
                font={"color": "#1a1814"},
                margin={"l": 10, "r": 10, "t": 45, "b": 10},
            )
            st.plotly_chart(fig, width="stretch")

        with chart_right:
            reasons = (
                assigned_df.assign(
                    reason=assigned_df["review_reason"].replace("", "Auto assigned")
                )["reason"]
                .value_counts()
                .rename_axis("review_reason")
                .reset_index(name="risks")
            )
            fig = px.bar(reasons, x="review_reason", y="risks", color="review_reason", title="Review reasons")
            fig.update_layout(
                showlegend=False,
                height=500,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="#fff",
                font={"color": "#1a1814"},
                margin={"l": 10, "r": 10, "t": 45, "b": 90},
            )
            st.plotly_chart(fig, width="stretch")

        section_label("Top Executive Themes")
        card_cols = st.columns(3)
        summary_for_cards = st.session_state.theme_summary_df.head(3).reset_index(drop=True)
        for idx, column in enumerate(card_cols):
            with column:
                if idx < len(summary_for_cards):
                    render_theme_cards(summary_for_cards.iloc[[idx]], limit=1)

with tabs[1]:
    if assigned_df.empty:
        section_label("Inventory Loaded")
        render_html_table(
            inventory_df,
            columns=[
                "risk_id",
                "risk_title",
                "business_unit",
                "risk_type",
                "taxonomy",
                "root_cause",
                "materiality",
            ],
            wide=True,
        )
    else:
        section_label("Assignment Filters")
        filtered = filter_assigned_inventory(assigned_df)
        col1, col2, col3 = st.columns(3)
        col1.metric("Visible risks", f"{len(filtered):,}")
        col2.metric("Visible review items", f"{int((filtered['review_flag'] == 'Yes').sum()):,}")
        col3.metric("Average score", f"{filtered['primary_theme_score'].mean():.2f}" if not filtered.empty else "-")
        section_label("Assigned Inventory")
        render_html_table(filtered, columns=OUTPUT_COLUMNS, wide=True)

        with st.expander("Top candidate diagnostics"):
            candidate_cols = [
                "risk_id",
                "candidate_rank",
                "theme_name",
                "semantic_similarity",
                "business_match_score",
                "risk_type_match_score",
                "root_cause_match_score",
                "keyword_match_score",
                "final_score",
            ]
            render_html_table(
                st.session_state.candidates_df,
                columns=candidate_cols,
                wide=True,
                max_rows=250,
            )

with tabs[2]:
    if assigned_df.empty:
        section_label("Human Review Queue")
        st.markdown(
            """
            <div class="panel-card">
                <div class="ai-card-title">Awaiting Assignment</div>
                <h3>No review queue yet</h3>
                <p>Run theme assignment to populate low-confidence and multi-theme cases for reviewer action.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        review_queue = assigned_df[assigned_df["review_flag"] == "Yes"].copy()
        if review_queue.empty:
            st.success("No items are currently flagged for review.")
        else:
            section_label("Review Workbench")
            col1, col2, col3 = st.columns(3)
            col1.metric("Review items", f"{len(review_queue):,}")
            col2.metric(
                "Multi-theme cases",
                f"{int(review_queue['review_reason'].str.contains('Multiple', case=False, na=False).sum()):,}",
            )
            col3.metric(
                "Low-confidence cases",
                f"{int(review_queue['review_reason'].str.contains('Low confidence', case=False, na=False).sum()):,}",
            )

            reason_cols = st.columns(3)
            reason_counts = review_queue["review_reason"].value_counts().head(3)
            for idx, (reason, count) in enumerate(reason_counts.items()):
                with reason_cols[idx]:
                    st.markdown(
                        f"""
                        <div class="risk-pop-card">
                            <b>{html.escape(reason)}</b>
                            <span>{count} risks require reviewer confirmation or override.</span>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

            section_label("Review Queue Preview")
            render_html_table(review_queue, columns=OUTPUT_COLUMNS, wide=True, max_rows=25)

            section_label("Override Editor")
            theme_options = [""] + sorted(engine.themes_df["theme_name"].dropna().unique())
            edited_review = st.data_editor(
                review_queue[OUTPUT_COLUMNS],
                width="stretch",
                hide_index=True,
                height=540,
                disabled=[
                    column for column in OUTPUT_COLUMNS if column != "human_override_theme"
                ],
                column_config={
                    "human_override_theme": st.column_config.SelectboxColumn(
                        "human_override_theme",
                        options=theme_options,
                    )
                },
                key="review_editor",
            )
            apply_review_edits(engine, edited_review)

with tabs[3]:
    summary_df = st.session_state.theme_summary_df
    if summary_df.empty:
        section_label("Theme Summary")
        st.markdown(
            """
            <div class="panel-card">
                <div class="ai-card-title">No Summary Yet</div>
                <h3>Run assignment to generate executive summaries</h3>
                <p>Theme-level narratives will aggregate business units, risk types, root causes, materiality, and key risk titles.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        section_label("Executive Theme Summary")
        card_cols = st.columns(3)
        for idx, column in enumerate(card_cols):
            with column:
                if idx < len(summary_df):
                    render_theme_cards(summary_df.iloc[[idx]], limit=1)

        section_label("Theme Summary Table")
        render_html_table(summary_df, columns=SUMMARY_COLUMNS, wide=True)

with tabs[4]:
    library_df = engine.theme_library_for_display()
    section_label("Theme Library Coverage")
    domain_counts = library_df["domain"].value_counts().rename_axis("domain").reset_index(name="themes")
    domain_cols = st.columns(3)
    for idx, row in domain_counts.head(6).iterrows():
        with domain_cols[idx % 3]:
            st.markdown(
                f"""
                <div class="taxonomy-card">
                    <div class="ai-card-title">Domain</div>
                    <h3>{html.escape(safe_value(row['domain']))}</h3>
                    <div class="taxonomy-meta">{int(row['themes'])} executive themes available for matching.</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    section_label("Theme Cards")
    render_html_table(
        library_df,
        columns=[
            "theme_id",
            "theme_name",
            "domain",
            "description",
            "typical_business_units",
            "typical_risk_types",
            "root_causes",
            "keywords",
        ],
        wide=True,
        max_rows=100,
    )

with tabs[5]:
    section_label("AI Narrative Enrichment")
    if assigned_df.empty:
        st.markdown(
            """
            <div class="panel-card">
                <div class="ai-card-title">Narratives Locked</div>
                <h3>Run theme assignment first</h3>
                <p>The LLM step uses the completed assignments and candidate evidence to draft executive summaries and risk-level justifications.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        summary_df = st.session_state.theme_summary_df
        llm_theme_count = int(
            summary_df.get("llm_summary", pd.Series(dtype=str))
            .fillna("")
            .astype(str)
            .str.strip()
            .ne("")
            .sum()
        )
        llm_risk_count = int(
            assigned_df.get("llm_assignment_justification", pd.Series(dtype=str))
            .fillna("")
            .astype(str)
            .str.strip()
            .ne("")
            .sum()
        )

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Themes ready", f"{len(summary_df):,}")
        col2.metric("Risks available", f"{len(assigned_df):,}")
        col3.metric("LLM themes drafted", f"{llm_theme_count:,}")
        col4.metric("Risk justifications", f"{llm_risk_count:,}")

        left, right = st.columns([1, 1.25])
        with left:
            st.markdown(
                """
                <div class="panel-card">
                    <div class="ai-card-title">Optional GPT Step</div>
                    <h3>Narrative polish, not assignment logic</h3>
                    <p>The deterministic engine still performs retrieval, scoring, assignment, and review flagging. GPT is only used here to draft richer summaries and explain the evidence supporting each assigned theme.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            llm_model = st.text_input("OpenAI model", value="gpt-5.2")
            llm_scope = st.radio(
                "Narrative scope",
                ["Top 5 assigned themes", "All assigned themes"],
                horizontal=True,
            )
            api_key = st.text_input(
                "OpenAI API key",
                type="password",
                help="Leave blank to use OPENAI_API_KEY from the local environment.",
            )

            if st.button("Generate LLM Narratives", type="primary", width="stretch"):
                try:
                    with st.spinner("Generating executive narratives and justifications..."):
                        enriched_assigned, enriched_summary, llm_log = engine.enrich_with_llm(
                            st.session_state.assigned_df,
                            st.session_state.theme_summary_df,
                            api_key=api_key.strip() or None,
                            model=llm_model.strip() or "gpt-5.2",
                            scope=llm_scope,
                        )
                    st.session_state.assigned_df = enriched_assigned
                    st.session_state.theme_summary_df = enriched_summary
                    st.session_state.llm_log_df = llm_log
                    assigned_df = st.session_state.assigned_df
                    summary_df = st.session_state.theme_summary_df
                    st.success(f"Generated narratives for {len(llm_log):,} theme groups.")
                except Exception as exc:
                    st.error(str(exc))

        with right:
            st.markdown(
                """
                <div class="panel-card">
                    <div class="ai-card-title">Governance Guardrails</div>
                    <h3>Prompted to use only supplied evidence</h3>
                    <p>The payload includes theme metadata, risk titles, descriptions, business units, risk types, taxonomy, root cause, score, review status, and deterministic rationale. The response is requested as structured JSON and stored in dedicated LLM narrative columns.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            log_df = st.session_state.get("llm_log_df", pd.DataFrame())
            if not log_df.empty:
                section_label("LLM Run Log")
                render_html_table(log_df, wide=False)

        section_label("Theme Narrative Preview")
        theme_narrative_cols = [
            "theme_name",
            "domain",
            "total_risks",
            "material_risks",
            "llm_summary",
            "llm_key_drivers",
            "llm_management_takeaway",
            "ai_summary",
        ]
        render_html_table(summary_df, columns=theme_narrative_cols, wide=True, max_rows=20)

        section_label("Risk Justification Preview")
        risk_narrative_cols = [
            "risk_id",
            "risk_title",
            "primary_theme",
            "primary_theme_score",
            "review_flag",
            "assignment_rationale",
            "llm_assignment_justification",
            "llm_evidence",
        ]
        render_html_table(assigned_df, columns=risk_narrative_cols, wide=True, max_rows=50)

with tabs[6]:
    section_label("Export Center")
    if assigned_df.empty:
        st.markdown(
            """
            <div class="panel-card">
                <div class="ai-card-title">Exports Locked</div>
                <h3>Run theme assignment first</h3>
                <p>Excel and slide exports are generated from the assigned inventory and theme summary outputs.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        summary_df = st.session_state.theme_summary_df
        review_queue = assigned_df[assigned_df["review_flag"] == "Yes"]

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Assigned risks", f"{len(assigned_df):,}")
        col2.metric("Theme summaries", f"{len(summary_df):,}")
        col3.metric("Review queue", f"{len(review_queue):,}")
        col4.metric("Material risks", f"{material_count(assigned_df):,}")

        excel_col, slide_col = st.columns([1, 1.35])
        with excel_col:
            section_label("Excel Outputs")
            st.markdown(
                """
                <div class="panel-card">
                    <div class="ai-card-title">Workbook</div>
                    <h3>Assignment workbook</h3>
                    <p>Includes assigned inventory, review queue, theme summary, and the theme library.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.download_button(
                "Download Full Excel Workbook",
                data=engine.build_excel_export(assigned_df, review_queue, summary_df),
                file_name="risk_theme_assignment_results.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                width="stretch",
            )

            st.markdown(
                """
                <div class="panel-card">
                    <div class="ai-card-title">Summary</div>
                    <h3>Theme summary only</h3>
                    <p>Exports the executive theme summary table for reporting or downstream analysis.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.download_button(
                "Download Theme Summary Excel",
                data=engine.build_summary_excel_export(summary_df),
                file_name="risk_theme_summary.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                width="stretch",
            )

        with slide_col:
            section_label("Slide Output")
            slide_scope = st.radio(
                "Slide export scope",
                ["Top 5 assigned themes", "All assigned themes"],
                horizontal=True,
            )
            style_preset = st.selectbox(
                "Slide style preset",
                ["Executive Warm", "Board Minimal", "Slate Contrast"],
            )
            deck_title = st.text_input(
                "Deck title",
                value="AI Risk Theme Assignment Summary",
            )
            deck_subtitle = st.text_input(
                "Deck subtitle",
                value=f"{slide_scope} | Vector retrieval plus metadata scoring",
            )

            selected_theme_count = min(5, len(summary_df)) if slide_scope.startswith("Top 5") else len(summary_df)
            st.markdown(
                f"""
                <div class="panel-card">
                    <div class="ai-card-title">PowerPoint</div>
                    <h3>{selected_theme_count + 1} editable slides</h3>
                    <p>Includes 1 overall summary slide plus {selected_theme_count} theme detail slide{'s' if selected_theme_count != 1 else ''}. Each theme slide lists all underlying assigned risks for that theme.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            try:
                with st.spinner("Preparing slide deck..."):
                    slide_bytes = engine.build_slide_export(
                        assigned_df,
                        summary_df,
                        scope=slide_scope,
                        deck_title=deck_title,
                        deck_subtitle=deck_subtitle,
                        style_preset=style_preset,
                    )
                st.download_button(
                    "Download PowerPoint Slides",
                    data=slide_bytes,
                    file_name=(
                        "risk_theme_top_5_slides.pptx"
                        if slide_scope.startswith("Top 5")
                        else "risk_theme_all_theme_slides.pptx"
                    ),
                    mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                    width="stretch",
                )
            except Exception as exc:
                st.error(str(exc))

        section_label("Export Preview")
        preview_cols = [
            "theme_name",
            "domain",
            "total_risks",
            "material_risks",
            "business_units",
            "risk_types",
            "top_root_causes",
            "llm_summary",
            "llm_management_takeaway",
        ]
        render_html_table(summary_df, columns=preview_cols, wide=True)

with tabs[7]:
    section_label("Methodology")
    col1, col2 = st.columns(2)
    with col1:
        render_method_card(
            "Root Cause, Theme, Risk Type",
            "Root cause explains why a risk is happening. Executive Risk Theme explains the business vulnerability or reporting topic. Risk Type explains how the risk manifests in the existing taxonomy.",
            "Hierarchy",
        )
        render_method_card(
            "Vector Store",
            "The theme library is converted into searchable theme documents and indexed locally in vector_store/theme_index.faiss with metadata in vector_store/theme_metadata.json. The vector store retrieves candidates only.",
            "Retrieval",
        )
    with col2:
        render_method_card(
            "Hybrid Final Assignment",
            "The final theme assignment combines semantic similarity, business unit, risk type, taxonomy/root cause, and keyword evidence. Vector similarity alone never determines the final assignment.",
            "Scoring",
        )
        render_method_card(
            "Human Review",
            "Each risk receives one primary theme to avoid double counting. Reviewers can select an override theme while preserving the original model assignment and rationale for traceability.",
            "Governance",
        )
        render_method_card(
            "Optional LLM Narratives",
            "GPT enrichment can draft theme-level summaries, key drivers, management takeaways, and risk-level justifications after assignment. It does not replace the hybrid scoring model or change the assigned theme.",
            "Narratives",
        )

    scoring_df = pd.DataFrame(
        [
            {"Signal": "Semantic similarity", "Weight": "50%", "Purpose": "Meaning-based candidate fit from vector retrieval."},
            {"Signal": "Business unit match", "Weight": "20%", "Purpose": "Business or function alignment with the theme card."},
            {"Signal": "Risk type match", "Weight": "15%", "Purpose": "Compatibility with the existing risk type taxonomy."},
            {"Signal": "Root cause/taxonomy match", "Weight": "10%", "Purpose": "Driver and taxonomy evidence for the business vulnerability."},
            {"Signal": "Keyword match", "Weight": "5%", "Purpose": "Specific words or phrases associated with the executive theme."},
        ]
    )
    section_label("Scoring Formula")
    st.markdown(
        """
        <div class="panel-card">
            <div class="ai-card-title">Formula</div>
            <h3>final_score = 0.50 semantic + 0.20 business + 0.15 risk type + 0.10 root cause + 0.05 keyword</h3>
            <p>The weighted score is applied only to the top semantic candidates returned by the local vector store.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    render_html_table(scoring_df, wide=False)

    rules_df = pd.DataFrame(
        [
            {"Condition": "top_score >= 0.80 and score_gap >= 0.10", "Outcome": "Auto assign", "Review Flag": "No"},
            {"Condition": "top_score >= 0.70 and score_gap < 0.10", "Outcome": "Multiple plausible themes", "Review Flag": "Yes"},
            {"Condition": "top_score < 0.70", "Outcome": "Low confidence", "Review Flag": "Yes"},
        ]
    )
    section_label("Assignment Rules")
    render_html_table(rules_df, wide=False)
