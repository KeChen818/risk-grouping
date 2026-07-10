import streamlit as st

from components.sidebar import render_sidebar_filters

st.set_page_config(page_title="Risk Atlas", page_icon="🧭", layout="wide")

st.title("Risk Atlas")
st.caption("Inventory intelligence for profile summary, grouping, and connected downstream use cases")
render_sidebar_filters()

overview = st.Page("pages/overview.py", title="Overview", icon=":material/home:")
profile_summary = st.Page(
    "pages/risk_profile_summary.py",
    title="Risk Profile Summary",
    icon=":material/insights:",
)
risk_grouping = st.Page(
    "pages/risk_grouping.py",
    title="Risk Grouping",
    icon=":material/account_tree:",
)
ai_chatbot = st.Page(
    "pages/copilot.py",
    title="AI Chatbot - Inventory Expert",
    icon=":material/smart_toy:",
)
report_export = st.Page(
    "pages/reporting.py",
    title="Report Export",
    icon=":material/slideshow:",
)
connected = st.Page(
    "pages/connected_intelligence.py",
    title="Connected Intelligence",
    icon=":material/hub:",
)

nav = st.navigation(
    [overview, profile_summary, risk_grouping, ai_chatbot, report_export, connected],
    position="sidebar",
)

nav.run()
