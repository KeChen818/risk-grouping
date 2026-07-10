import streamlit as st

from services.mock_data import apply_filters, get_risk_inventory

st.header("Connected Intelligence")

inventory = apply_filters(get_risk_inventory(), st.session_state)

sge, rca_scenario, appetite = st.tabs(
    [
        "CUSO-Group Risk ID SGE Materiality Coverage",
        "CUSO Risk ID - RCA & Scenario Design",
        "CUSO Risk ID - Risk Limit/Appetite",
    ]
)

with sge:
    st.subheader("CUSO-Group Risk ID SGE Materiality Coverage")
    st.caption("Compare local inventory against group and SGE perspectives.")
    st.dataframe(
        inventory[["risk_id", "risk_name", "sge_status", "entity", "material"]],
        use_container_width=True,
        hide_index=True,
    )

with rca_scenario:
    st.subheader("CUSO Risk ID - RCA & Scenario Design")
    st.caption("Link current inventory into coverage and scenario design workflows.")
    st.dataframe(
        inventory[["risk_id", "risk_name", "rca_status", "scenario_status", "overall"]],
        use_container_width=True,
        hide_index=True,
    )

with appetite:
    st.subheader("CUSO Risk ID - Risk Limit/Appetite")
    st.caption("Connect identified risks into appetite and limit views.")
    st.dataframe(
        inventory[["risk_id", "risk_name", "appetite_status", "risk_type", "material"]],
        use_container_width=True,
        hide_index=True,
    )

st.info(
    "Connected Intelligence uses the current inventory as the foundation for coverage, scenario, and governance linkage."
)
