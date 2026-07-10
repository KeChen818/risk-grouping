import streamlit as st

st.header("Report Export")

export_format = st.selectbox("Export format", ["Slides", "Excel"])
content = st.multiselect(
    "Include output sections",
    ["Risk Profile", "Risk Grouping"],
    default=["Risk Profile"],
)

left, right = st.columns(2)
with left:
    st.subheader("Risk Profile")
    st.write("Export profile summary outputs including Top Exposure, Risk Quantification Alignment, and QoQ Change.")
with right:
    st.subheader("Risk Grouping")
    st.write("Export taxonomy grouping, theme proposal, and non-material watchlist outputs.")

st.write(f"Selected format: **{export_format}**")
st.write(f"Selected content: **{', '.join(content)}**")
st.button("Generate export", type="primary")
