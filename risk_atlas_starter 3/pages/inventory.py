import streamlit as st

from services.mock_data import apply_filters, get_risk_inventory

st.header("Inventory")

inventory = apply_filters(get_risk_inventory(), st.session_state)

tab1, tab2, tab3, tab4 = st.tabs(["Profile Summary", "Alignment", "QoQ Change", "Grouping"])

with tab1:
    left, right = st.columns([1, 1])
    with left:
        st.subheader("Top Risks by Overall Score")
        st.dataframe(
            inventory[["risk_id", "risk_name", "division", "entity", "risk_type", "overall"]]
            .sort_values(["overall", "risk_id"], ascending=[False, True])
            .head(5),
            use_container_width=True,
            hide_index=True,
        )
    with right:
        st.subheader("Material Risk Split")
        material_counts = inventory["material"].map({True: "Material", False: "Non-material"}).value_counts()
        st.bar_chart(material_counts)

with tab2:
    st.subheader("Assessment Alignment")
    alignment = (
        inventory.groupby(["division", "risk_type"], as_index=False)[["likelihood", "impact", "overall"]]
        .mean()
        .sort_values("overall", ascending=False)
    )
    st.dataframe(alignment, use_container_width=True, hide_index=True)

with tab3:
    st.subheader("Quarter-over-Quarter Change")
    top_movers = inventory.sort_values("qoq_delta", ascending=False)[
        ["risk_id", "risk_name", "qoq_status", "qoq_delta", "overall", "material"]
    ]
    st.dataframe(top_movers, use_container_width=True, hide_index=True)
    if st.session_state.show_ai:
        st.info(
            "QoQ highlights: new operational risk items appeared in AH LLC, while underwriting and capital markets distribution risks moved higher."
        )

with tab4:
    st.subheader("Risk Grouping")
    st.markdown("**Taxonomy-based view**")
    grouping = inventory.groupby(["risk_type", "material"], as_index=False).size()
    st.dataframe(grouping, use_container_width=True, hide_index=True)
    st.markdown("**AI Theme Proposal**")
    st.write("• underwriting quality  • capital markets distribution  • concentration and spillover  • process/control resilience")
