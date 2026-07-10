import streamlit as st

QUARTERS = ["2026 Q2", "2026 Q1", "2025 Q4"]
ENTITIES = ["All", "CUSO", "US Branches", "AH LLC"]
DIVISIONS = ["All", "IB", "NCL", "WM", "GM"]
RISK_TYPES = ["All", "Credit", "Market", "Liquidity", "Operational", "Strategic"]


def _bootstrap_state() -> None:
    defaults = {
        "quarter": QUARTERS[0],
        "entity": ENTITIES[0],
        "division": DIVISIONS[0],
        "risk_type": RISK_TYPES[0],
        "material_only": False,
        "show_ai": True,
    }
    for key, value in defaults.items():
        st.session_state.setdefault(key, value)


def render_sidebar_filters() -> None:
    _bootstrap_state()
    with st.sidebar:
        st.markdown("### Global Filters")
        st.session_state.quarter = st.selectbox("Quarter", QUARTERS, index=QUARTERS.index(st.session_state.quarter))
        st.session_state.entity = st.selectbox("Legal Entity", ENTITIES, index=ENTITIES.index(st.session_state.entity))
        st.session_state.division = st.selectbox("Business Division", DIVISIONS, index=DIVISIONS.index(st.session_state.division))
        st.session_state.risk_type = st.selectbox("Risk Type", RISK_TYPES, index=RISK_TYPES.index(st.session_state.risk_type))
        st.session_state.material_only = st.checkbox("Show only material risks", value=st.session_state.material_only)
        st.session_state.show_ai = st.checkbox("Show AI summary blocks", value=st.session_state.show_ai)
        if st.button("Reset filters", use_container_width=True):
            for key in ["quarter", "entity", "division", "risk_type", "material_only", "show_ai"]:
                del st.session_state[key]
            st.rerun()
