import streamlit as st

from services.mock_data import apply_filters, get_risk_inventory, summarize

st.header("Overview")

inventory = apply_filters(get_risk_inventory(), st.session_state)
summary = summarize(inventory)

a, b, c, d = st.columns(4)
a.metric("Total risks", summary["total"])
b.metric("Material risks", summary["material"])
c.metric("QoQ movers", summary["changed"])
d.metric("Non-material watchlist", summary["non_material"])

st.subheader("Risk Atlas structure")
left, right = st.columns(2)

with left:
    with st.container(border=True):
        st.markdown("### Risk Profile Summary")
        st.write("Top Exposure, Risk Quantification Alignment, and QoQ Change.")
        st.page_link("pages/risk_profile_summary.py", label="Open Risk Profile Summary", use_container_width=True)

    with st.container(border=True):
        st.markdown("### Risk Grouping")
        st.write("Taxonomy-based grouping, theme proposal, and non-material risk watchlist.")
        st.page_link("pages/risk_grouping.py", label="Open Risk Grouping", use_container_width=True)

with right:
    with st.container(border=True):
        st.markdown("### AI Chatbot - Inventory Expert")
        st.write("Natural-language inventory Q&A focused on risk records and profile analysis.")
        st.page_link("pages/copilot.py", label="Open AI Chatbot - Inventory Expert", use_container_width=True)

    with st.container(border=True):
        st.markdown("### Report Export")
        st.write("Slides and Excel export for Risk Profile and Risk Grouping views.")
        st.page_link("pages/reporting.py", label="Open Report Export", use_container_width=True)

st.subheader("Connected Intelligence")
st.info(
    "Extends the inventory into CUSO-Group Risk ID SGE Materiality Coverage, "
    "CUSO Risk ID - RCA & Scenario Design, and CUSO Risk ID - Risk Limit/Appetite."
)
st.page_link(
    "pages/connected_intelligence.py",
    label="Open Connected Intelligence",
    use_container_width=True,
)

if st.session_state.show_ai:
    st.subheader("AI positioning")
    st.info(
        "Risk Atlas uses the inventory as the foundation for profile analysis, grouping, chatbot workflows, reporting, and connected intelligence use cases."
    )
