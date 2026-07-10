import streamlit as st

from services.mock_data import apply_filters, get_risk_inventory

st.header("Risk Grouping")

inventory = apply_filters(get_risk_inventory(), st.session_state)

taxonomy, theme, watchlist = st.tabs(
    ["Taxonomy-based", "Theme Proposal", "Non-material risk watchlist"]
)

with taxonomy:
    st.subheader("Taxonomy-based grouping")
    grouping = (
        inventory.groupby(["risk_type", "division", "entity"], as_index=False)
        .size()
        .sort_values("size", ascending=False)
    )
    st.dataframe(grouping, use_container_width=True, hide_index=True)

with theme:
    st.subheader("Theme proposal")
    themes = [
        "Underwriting quality and credit discipline",
        "Capital markets distribution and spread risk",
        "Funding concentration and stress liquidity",
        "Process resilience and operational control",
    ]
    for item in themes:
        st.write(f"• {item}")
    if st.session_state.show_ai:
        st.info(
            "Theme Proposal groups similar risk records into business-friendly narratives for management reporting."
        )

with watchlist:
    st.subheader("Non-material risk watchlist")
    watch = inventory.loc[~inventory["material"], ["risk_id", "risk_name", "division", "entity", "qoq_status", "overall"]]
    st.dataframe(watch, use_container_width=True, hide_index=True)
    st.caption("Use this watchlist to monitor non-material items that may become more relevant over time.")
