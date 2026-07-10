import streamlit as st

from services.mock_data import apply_filters, get_risk_inventory

st.header("Risk Profile Summary")

inventory = apply_filters(get_risk_inventory(), st.session_state)

top_exposure, quant_alignment, qoq_change = st.tabs(
    ["Top Exposure", "Risk Quantification Alignment", "QoQ Change"]
)

with top_exposure:
    col1, col2 = st.columns([1.2, 1])
    with col1:
        st.subheader("Top Exposure by selected scope")
        exposure = (
            inventory[["risk_id", "risk_name", "division", "entity", "risk_type", "overall", "material"]]
            .sort_values(["overall", "risk_id"], ascending=[False, True])
        )
        st.dataframe(exposure, use_container_width=True, hide_index=True)
    with col2:
        st.subheader("Exposure mix")
        risk_mix = inventory.groupby("risk_type").size().sort_values(ascending=False)
        st.bar_chart(risk_mix)
        st.subheader("Material vs non-material")
        material_counts = inventory["material"].map({True: "Material", False: "Non-material"}).value_counts()
        st.bar_chart(material_counts)

with quant_alignment:
    st.subheader("Risk Quantification Alignment")
    alignment = (
        inventory.groupby(["division", "risk_type"], as_index=False)[["likelihood", "impact", "overall"]]
        .mean()
        .sort_values("overall", ascending=False)
    )
    st.dataframe(alignment, use_container_width=True, hide_index=True)
    if st.session_state.show_ai:
        st.info(
            "Quantification is most elevated in Credit for IB and NCL. Use this view to compare how risk scoring aligns across divisions and risk types."
        )

with qoq_change:
    left, right = st.columns([1.2, 1])
    with left:
        st.subheader("Quarter-over-quarter change")
        movers = inventory.sort_values(["qoq_delta", "overall"], ascending=[False, False])[
            ["risk_id", "risk_name", "qoq_status", "qoq_delta", "overall", "material"]
        ]
        st.dataframe(movers, use_container_width=True, hide_index=True)
    with right:
        st.subheader("QoQ distribution")
        st.bar_chart(inventory["qoq_status"].value_counts())
        if st.session_state.show_ai:
            st.info(
                "Use this section to explain which risks are new, retired, stable, or moved in severity since the prior quarter."
            )
