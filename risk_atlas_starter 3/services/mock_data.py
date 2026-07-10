from __future__ import annotations

import pandas as pd


_DATA = [
    {
        "risk_id": "R-001",
        "risk_name": "Distribution risk in capital markets pipeline",
        "division": "IB",
        "entity": "CUSO",
        "risk_type": "Credit",
        "material": True,
        "likelihood": 4,
        "impact": 4,
        "overall": 16,
        "qoq_status": "Increased",
        "qoq_delta": 2,
        "rca_status": "Mapped",
        "sge_status": "Matched",
        "appetite_status": "Mapped",
        "scenario_status": "Primary driver",
    },
    {
        "risk_id": "R-002",
        "risk_name": "Underwriting standards deterioration",
        "division": "NCL",
        "entity": "CUSO",
        "risk_type": "Credit",
        "material": True,
        "likelihood": 3,
        "impact": 5,
        "overall": 15,
        "qoq_status": "Increased",
        "qoq_delta": 1,
        "rca_status": "Partially mapped",
        "sge_status": "Partial",
        "appetite_status": "Mapped",
        "scenario_status": "Primary driver",
    },
    {
        "risk_id": "R-003",
        "risk_name": "Market share loss to direct lenders",
        "division": "IB",
        "entity": "CUSO",
        "risk_type": "Strategic",
        "material": True,
        "likelihood": 4,
        "impact": 3,
        "overall": 12,
        "qoq_status": "Stable",
        "qoq_delta": 0,
        "rca_status": "Not mapped",
        "sge_status": "Local only",
        "appetite_status": "Not mapped",
        "scenario_status": "Secondary driver",
    },
    {
        "risk_id": "R-004",
        "risk_name": "Funding concentration under stress",
        "division": "GM",
        "entity": "US Branches",
        "risk_type": "Liquidity",
        "material": True,
        "likelihood": 3,
        "impact": 4,
        "overall": 12,
        "qoq_status": "Decreased",
        "qoq_delta": -1,
        "rca_status": "Mapped",
        "sge_status": "Matched",
        "appetite_status": "Partially mapped",
        "scenario_status": "Primary driver",
    },
    {
        "risk_id": "R-005",
        "risk_name": "Trade processing control breakdown",
        "division": "GM",
        "entity": "AH LLC",
        "risk_type": "Operational",
        "material": False,
        "likelihood": 3,
        "impact": 3,
        "overall": 9,
        "qoq_status": "New",
        "qoq_delta": 9,
        "rca_status": "Partially mapped",
        "sge_status": "Unmatched",
        "appetite_status": "Not mapped",
        "scenario_status": "Contextual",
    },
    {
        "risk_id": "R-006",
        "risk_name": "Mortgage servicing operational disruption",
        "division": "WM",
        "entity": "US Branches",
        "risk_type": "Operational",
        "material": False,
        "likelihood": 2,
        "impact": 3,
        "overall": 6,
        "qoq_status": "Retired",
        "qoq_delta": -6,
        "rca_status": "Mapped",
        "sge_status": "Matched",
        "appetite_status": "Mapped",
        "scenario_status": "Contextual",
    },
    {
        "risk_id": "R-007",
        "risk_name": "Spread widening on residual positions",
        "division": "IB",
        "entity": "CUSO",
        "risk_type": "Market",
        "material": True,
        "likelihood": 4,
        "impact": 4,
        "overall": 16,
        "qoq_status": "Stable",
        "qoq_delta": 0,
        "rca_status": "Mapped",
        "sge_status": "Matched",
        "appetite_status": "Mapped",
        "scenario_status": "Primary driver",
    },
    {
        "risk_id": "R-008",
        "risk_name": "Counterparty downgrade spillover",
        "division": "GM",
        "entity": "AH LLC",
        "risk_type": "Credit",
        "material": False,
        "likelihood": 2,
        "impact": 4,
        "overall": 8,
        "qoq_status": "Increased",
        "qoq_delta": 2,
        "rca_status": "Not mapped",
        "sge_status": "Partial",
        "appetite_status": "Partially mapped",
        "scenario_status": "Secondary driver",
    },
]


def get_risk_inventory() -> pd.DataFrame:
    return pd.DataFrame(_DATA)


def apply_filters(df: pd.DataFrame, session_state) -> pd.DataFrame:
    out = df.copy()
    if session_state.entity != "All":
        out = out[out["entity"] == session_state.entity]
    if session_state.division != "All":
        out = out[out["division"] == session_state.division]
    if session_state.risk_type != "All":
        out = out[out["risk_type"] == session_state.risk_type]
    if session_state.material_only:
        out = out[out["material"]]
    return out.reset_index(drop=True)


def summarize(df: pd.DataFrame) -> dict[str, int]:
    return {
        "total": int(len(df)),
        "material": int(df["material"].sum()),
        "changed": int((df["qoq_status"] != "Stable").sum()),
        "non_material": int((~df["material"]).sum()),
    }
