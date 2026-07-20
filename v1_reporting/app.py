from __future__ import annotations

import time
from copy import deepcopy

import streamlit as st

from report_engine import (
    ReportPlan,
    build_default_filename,
    build_refined_goal,
    generate_powerpoint,
    infer_plan_from_goal,
    sanitize_filename,
)

st.set_page_config(
    page_title="Risk Atlas | AI Report Writer",
    page_icon="🧭",
    layout="wide",
)

st.markdown(
    """
    <style>
      :root {
        --ra-navy: #001f3f;
        --ra-red: #e60000;
        --ra-gray-50: #f7f8fa;
        --ra-gray-100: #eef0f3;
        --ra-gray-300: #d5d9df;
        --ra-gray-600: #667085;
        --ra-gray-900: #1d2939;
      }
      .block-container {padding-top: 1rem; padding-bottom: 3rem; max-width: 1450px;}
      h1, h2, h3 {color: var(--ra-navy);}
      .ra-header {display:flex; justify-content:space-between; align-items:flex-start; gap:1rem; margin-bottom:.75rem;}
      .ra-title {font-size:1.65rem; font-weight:750; color:var(--ra-navy);}
      .ra-subtitle {font-size:.92rem; color:var(--ra-gray-600); margin-top:.2rem;}
      .ra-chip {display:inline-flex; border-radius:999px; padding:.3rem .7rem; background:#eef4ff; color:#1d4ed8; font-size:.78rem; font-weight:650;}
      .ra-card {border:1px solid var(--ra-gray-300); border-radius:8px; padding:1rem 1.05rem; background:#fff; margin-bottom:1rem;}
      .ra-card-title {font-size:1rem; font-weight:700; color:var(--ra-gray-900);}
      .ra-muted {font-size:.86rem; color:var(--ra-gray-600); margin-top:.15rem;}
      .ra-status-pill {display:inline-flex; align-items:center; gap:.35rem; border-radius:999px; padding:.3rem .65rem; font-size:.78rem; font-weight:650;}
      .ra-draft {background:#f2f4f7; color:#475467;}
      .ra-review {background:#fff7e6; color:#9a6700;}
      .ra-ready {background:#ecfdf3; color:#027a48;}
      .ra-running {background:#eff6ff; color:#1d4ed8;}
      .ra-complete {background:#ecfdf3; color:#027a48;}
      .ra-row {display:flex; justify-content:space-between; gap:1rem; padding:.48rem 0; border-bottom:1px solid var(--ra-gray-100); font-size:.9rem;}
      .ra-row:last-child {border-bottom:none;}
      .ra-label {color:var(--ra-gray-600);}
      .ra-value {font-weight:650; text-align:right; color:var(--ra-gray-900);}
      .ra-outline-item {padding:.45rem .55rem; border:1px solid var(--ra-gray-100); border-radius:8px; margin-bottom:.4rem; font-size:.88rem; background:#fafafa;}
      div.stButton > button[kind="primary"] {background:var(--ra-red); border-color:var(--ra-red);}
      div.stButton > button[kind="primary"]:hover {background:#c90000; border-color:#c90000;}
      [data-testid="stMetricValue"] {font-size:1.35rem;}
    </style>
    """,
    unsafe_allow_html=True,
)

BUSINESSES_BY_ENTITY = {
    "CUSO": ["Investment Bank", "Wealth Management", "Asset Management", "All Businesses"],
    "US Branches": ["Corporate Lending", "Global Markets", "Treasury", "All Businesses"],
    "AH LLC": ["Investment Bank", "Corporate Center", "All Businesses"],
    "Group": ["Investment Bank", "Wealth Management", "Asset Management", "Corporate Center", "All Businesses"],
}

SECTION_OPTIONS = [
    "Executive Summary",
    "Portfolio Overview",
    "Top Risks",
    "QoQ Changes",
    "Risk Quantification",
    "Risk Concentrations",
    "Management Actions",
    "Risk ID Appendix",
]

DEFAULT_GOAL = "Create a WM quarterly risk update focusing on material changes"
WORKFLOW_GOAL = "goal"
WORKFLOW_PLAN = "plan"
WORKFLOW_CONFIRM = "confirm"
WORKFLOW_GENERATE = "generate"
VALID_WORKFLOW_STEPS = {WORKFLOW_GOAL, WORKFLOW_PLAN, WORKFLOW_CONFIRM, WORKFLOW_GENERATE}


def initial_plan() -> ReportPlan:
    plan = infer_plan_from_goal(DEFAULT_GOAL)
    return plan


def initialize_state() -> None:
    defaults = {
        "short_goal": DEFAULT_GOAL,
        "plan": initial_plan(),
        "refined_goal": "",
        "selected_sections": [],
        "filename": "",
        "filename_customized": False,
        "plan_confirmed": False,
        "status": "Draft",
        "generated_bytes": None,
        "last_error": None,
        "goal_reviewed": False,
        "workflow_step": WORKFLOW_GOAL,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = deepcopy(value)

    plan: ReportPlan = st.session_state.plan
    if not st.session_state.refined_goal:
        st.session_state.refined_goal = build_refined_goal(plan)
    if not st.session_state.selected_sections:
        st.session_state.selected_sections = list(plan.sections)
    if not st.session_state.filename:
        st.session_state.filename = build_default_filename(plan)


def mark_plan_changed(status: str = "Draft") -> None:
    st.session_state.plan_confirmed = False
    st.session_state.status = status
    st.session_state.generated_bytes = None
    st.session_state.last_error = None


def refresh_auto_fields(*, update_goal: bool = True) -> None:
    plan: ReportPlan = st.session_state.plan
    if update_goal:
        st.session_state.refined_goal = build_refined_goal(plan)
        if "refined_goal_editor" in st.session_state:
            st.session_state.refined_goal_editor = st.session_state.refined_goal
    if not st.session_state.filename_customized:
        st.session_state.filename = build_default_filename(plan)
        if "filename_input" in st.session_state:
            st.session_state.filename_input = st.session_state.filename


def review_short_goal() -> None:
    goal = st.session_state.short_goal.strip()
    if len(goal) < 6:
        st.session_state.last_error = "Please enter a slightly more specific report goal."
        return

    inferred = infer_plan_from_goal(goal)
    st.session_state.plan = inferred
    st.session_state.selected_sections = list(inferred.sections)
    st.session_state.refined_goal = build_refined_goal(inferred)
    st.session_state.filename_customized = False
    st.session_state.filename = build_default_filename(inferred)
    st.session_state.goal_reviewed = True
    st.session_state.workflow_step = WORKFLOW_PLAN
    st.session_state.status = "Reviewing"
    st.session_state.plan_confirmed = False
    st.session_state.generated_bytes = None
    st.session_state.last_error = None

    # Synchronize widget keys with the newly inferred plan.
    st.session_state.scope_inventory = inferred.inventory
    st.session_state.scope_comparison = inferred.comparison
    st.session_state.scope_entity = inferred.legal_entity
    st.session_state.scope_business = inferred.business_division
    st.session_state.scope_population = inferred.risk_population
    st.session_state.scope_audience = inferred.audience
    st.session_state.refined_goal_editor = st.session_state.refined_goal
    st.session_state.section_editor = list(st.session_state.selected_sections)
    st.session_state.filename_input = st.session_state.filename


def use_example_goal(goal: str) -> None:
    st.session_state.short_goal = goal
    st.session_state.last_error = None


def sync_plan_from_scope() -> None:
    plan: ReportPlan = st.session_state.plan
    plan.inventory = st.session_state.scope_inventory
    plan.comparison = st.session_state.scope_comparison
    plan.legal_entity = st.session_state.scope_entity

    valid_businesses = BUSINESSES_BY_ENTITY[plan.legal_entity]
    business = st.session_state.scope_business
    if business not in valid_businesses:
        business = valid_businesses[0]
        st.session_state.scope_business = business
    plan.business_division = business
    plan.risk_population = st.session_state.scope_population
    plan.audience = st.session_state.scope_audience

    st.session_state.plan = plan
    refresh_auto_fields(update_goal=True)
    mark_plan_changed("Reviewing")


def on_entity_change() -> None:
    entity = st.session_state.scope_entity
    valid_businesses = BUSINESSES_BY_ENTITY[entity]
    if st.session_state.scope_business not in valid_businesses:
        st.session_state.scope_business = valid_businesses[0]
    sync_plan_from_scope()


def on_filename_change() -> None:
    current = st.session_state.filename_input.strip()
    st.session_state.filename = current
    st.session_state.filename_customized = current != build_default_filename(st.session_state.plan)
    mark_plan_changed("Reviewing")


def reset_filename() -> None:
    st.session_state.filename_customized = False
    st.session_state.filename = build_default_filename(st.session_state.plan)
    st.session_state.filename_input = st.session_state.filename
    mark_plan_changed("Reviewing")


def add_focus(sentence: str, required_sections: list[str] | None = None) -> None:
    if sentence not in st.session_state.refined_goal:
        st.session_state.refined_goal = f"{st.session_state.refined_goal.rstrip()} {sentence}".strip()
    for section in required_sections or []:
        if section not in st.session_state.selected_sections:
            st.session_state.selected_sections.append(section)
    st.session_state.refined_goal_editor = st.session_state.refined_goal
    st.session_state.section_editor = list(st.session_state.selected_sections)
    mark_plan_changed("Reviewing")


def continue_to_confirmation() -> None:
    if not st.session_state.selected_sections:
        st.session_state.last_error = "Select at least one report section before continuing."
        return
    st.session_state.workflow_step = WORKFLOW_CONFIRM
    st.session_state.last_error = None


def edit_report_plan() -> None:
    st.session_state.workflow_step = WORKFLOW_PLAN
    mark_plan_changed("Reviewing")


def confirm_plan() -> bool:
    if not st.session_state.selected_sections:
        st.session_state.last_error = "Select at least one report section before confirming."
        return False
    st.session_state.plan_confirmed = True
    st.session_state.workflow_step = WORKFLOW_GENERATE
    st.session_state.status = "Ready"
    st.session_state.last_error = None
    return True


def start_generation() -> None:
    st.session_state.status = "Generating"
    st.session_state.generated_bytes = None


initialize_state()
plan: ReportPlan = st.session_state.plan

# Ensure widget state exists and remains valid.
widget_defaults = {
    "scope_inventory": plan.inventory,
    "scope_comparison": plan.comparison,
    "scope_entity": plan.legal_entity,
    "scope_business": plan.business_division,
    "scope_population": plan.risk_population,
    "scope_audience": plan.audience,
    "refined_goal_editor": st.session_state.refined_goal,
    "section_editor": list(st.session_state.selected_sections),
    "filename_input": st.session_state.filename,
}
for key, value in widget_defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

if st.session_state.scope_business not in BUSINESSES_BY_ENTITY[st.session_state.scope_entity]:
    st.session_state.scope_business = BUSINESSES_BY_ENTITY[st.session_state.scope_entity][0]

if st.session_state.workflow_step not in VALID_WORKFLOW_STEPS:
    st.session_state.workflow_step = WORKFLOW_PLAN if st.session_state.goal_reviewed else WORKFLOW_GOAL

if st.session_state.status in {"Generating", "Completed"}:
    st.session_state.workflow_step = WORKFLOW_GENERATE
elif st.session_state.workflow_step == WORKFLOW_GENERATE and not st.session_state.plan_confirmed:
    st.session_state.workflow_step = WORKFLOW_CONFIRM if st.session_state.goal_reviewed else WORKFLOW_GOAL
elif st.session_state.workflow_step == WORKFLOW_CONFIRM and not st.session_state.goal_reviewed:
    st.session_state.workflow_step = WORKFLOW_GOAL

st.markdown(
    """
    <div class="ra-header">
      <div>
        <div class="ra-title">Risk Atlas AI Report Writer</div>
        <div class="ra-subtitle">Short goal → live report plan → focused confirmation → generate → download</div>
      </div>
      <span class="ra-chip">Guided step flow</span>
    </div>
    """,
    unsafe_allow_html=True,
)

status_class = {
    "Draft": "ra-draft",
    "Reviewing": "ra-review",
    "Ready": "ra-ready",
    "Generating": "ra-running",
    "Completed": "ra-complete",
}.get(st.session_state.status, "ra-draft")

m1, m2, m3, m4 = st.columns(4)
m1.metric("Inventory", plan.inventory)
m2.metric("Legal entity", plan.legal_entity)
m3.metric("Business", plan.business_division)
m4.markdown(
    f'<div class="ra-card"><div class="ra-muted">Workflow status</div><div style="margin-top:.45rem"><span class="ra-status-pill {status_class}">{st.session_state.status}</span></div></div>',
    unsafe_allow_html=True,
)


def render_plan_summary_card(title: str = "Live report plan") -> None:
    current_plan: ReportPlan = st.session_state.plan
    st.markdown(
        f'<div class="ra-card"><div class="ra-card-title">{title}</div>',
        unsafe_allow_html=True,
    )
    rows = {
        "Legal entity": current_plan.legal_entity,
        "Business": current_plan.business_division,
        "Inventory": current_plan.inventory,
        "Comparison": current_plan.comparison,
        "Population": current_plan.risk_population,
        "Audience": current_plan.audience,
        "Estimated slides": str(max(4, len(st.session_state.selected_sections) + 3)),
    }
    for label, value in rows.items():
        st.markdown(
            f'<div class="ra-row"><span class="ra-label">{label}</span><span class="ra-value">{value}</span></div>',
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)


def render_planned_output_card() -> None:
    st.markdown(
        '<div class="ra-card"><div class="ra-card-title">Planned output</div>',
        unsafe_allow_html=True,
    )
    if st.session_state.selected_sections:
        for idx, section in enumerate(st.session_state.selected_sections, start=1):
            st.markdown(
                f'<div class="ra-outline-item"><strong>{idx}.</strong> {section}</div>',
                unsafe_allow_html=True,
            )
    else:
        st.caption("No report sections selected.")
    st.markdown("</div>", unsafe_allow_html=True)


def render_output_file_card() -> None:
    st.markdown(
        f'<div class="ra-card"><div class="ra-card-title">Output file</div>'
        f'<div class="ra-muted" style="word-break:break-word;margin-top:.45rem">{sanitize_filename(st.session_state.filename)}</div></div>',
        unsafe_allow_html=True,
    )


def render_short_goal_step() -> None:
    st.markdown(
        '<div class="ra-card"><div class="ra-card-title">1. Start with a short report goal</div>'
        '<div class="ra-muted">Risk Atlas proposes the structured scope, report sections and output settings.</div></div>',
        unsafe_allow_html=True,
    )

    st.text_input(
        "What do you want to generate?",
        key="short_goal",
        placeholder="Example: Create a WM quarterly risk update focusing on material changes",
    )

    examples = st.columns(3)
    example_goals = [
        ("IB executive report", "Create an IB executive risk report"),
        ("WM quarterly update", "Create a WM quarterly risk update focusing on material changes"),
        ("CUSO regulatory package", "Generate a CUSO regulatory package with detailed Risk IDs"),
    ]
    for col, (label, goal) in zip(examples, example_goals):
        col.button(label, use_container_width=True, on_click=use_example_goal, args=(goal,))

    st.button(
        "Review and refine plan",
        type="primary",
        use_container_width=True,
        on_click=review_short_goal,
    )

    if st.session_state.last_error and st.session_state.workflow_step == WORKFLOW_GOAL:
        st.warning(st.session_state.last_error)


def render_plan_review_step() -> None:
    st.markdown(
        '<div class="ra-card"><div class="ra-card-title">2. Review and refine the live report plan</div>'
        '<div class="ra-muted">Scope determines the records. The refined goal determines emphasis and presentation.</div></div>',
        unsafe_allow_html=True,
    )

    left, right = st.columns([1.45, 0.75], gap="large")

    with left:
        st.markdown("### Scope")
        c1, c2 = st.columns(2)
        with c1:
            st.selectbox(
                "Inventory",
                ["Q2 2026", "Q1 2026", "Q4 2025"],
                key="scope_inventory",
                on_change=sync_plan_from_scope,
            )
            st.selectbox(
                "Legal entity",
                list(BUSINESSES_BY_ENTITY),
                key="scope_entity",
                on_change=on_entity_change,
            )
            st.selectbox(
                "Business division",
                BUSINESSES_BY_ENTITY[st.session_state.scope_entity],
                key="scope_business",
                on_change=sync_plan_from_scope,
            )
        with c2:
            st.selectbox(
                "Compare with",
                ["Q1 2026", "Q4 2025", "No comparison"],
                key="scope_comparison",
                on_change=sync_plan_from_scope,
            )
            st.selectbox(
                "Risk population",
                ["Material risks only", "New and changed risks", "All active risks", "Non-material risks only"],
                key="scope_population",
                on_change=sync_plan_from_scope,
            )
            st.selectbox(
                "Audience",
                ["Executive Leadership", "CRO", "Risk Manager", "Regulator"],
                key="scope_audience",
                on_change=sync_plan_from_scope,
            )

        st.markdown("### Refined report goal")
        edited_goal = st.text_area(
            "Detailed instruction",
            height=135,
            key="refined_goal_editor",
        )
        if edited_goal != st.session_state.refined_goal:
            st.session_state.refined_goal = edited_goal
            mark_plan_changed("Reviewing")

        focus_cols = st.columns(3)
        focus_cols[0].button(
            "Top deterioration",
            use_container_width=True,
            on_click=add_focus,
            args=("Focus on the top five deteriorating risks and management attention items.",),
        )
        focus_cols[1].button(
            "Concentrations",
            use_container_width=True,
            on_click=add_focus,
            args=(
                "Emphasize exposure concentrations and risk quantification alignment.",
                ["Risk Quantification", "Risk Concentrations"],
            ),
        )
        focus_cols[2].button(
            "Audit appendix",
            use_container_width=True,
            on_click=add_focus,
            args=(
                "Include a detailed appendix with source Risk IDs for audit review.",
                ["Risk ID Appendix"],
            ),
        )

        st.markdown("### Report sections")
        selected = st.multiselect(
            "Included sections",
            SECTION_OPTIONS,
            key="section_editor",
        )
        if selected != st.session_state.selected_sections:
            st.session_state.selected_sections = selected
            mark_plan_changed("Reviewing")

        st.markdown("### Output")
        st.text_input(
            "PowerPoint filename",
            key="filename_input",
            on_change=on_filename_change,
        )
        f1, f2 = st.columns([1, 2])
        f1.button("Reset from scope", use_container_width=True, on_click=reset_filename)
        clean_filename = sanitize_filename(st.session_state.filename)
        f2.caption(
            "Custom filename" if st.session_state.filename_customized else "Automatically generated from scope"
        )
        if clean_filename != st.session_state.filename:
            st.caption(f"Final output filename: `{clean_filename}`")

    with right:
        render_plan_summary_card()
        render_planned_output_card()
        render_output_file_card()

    if st.session_state.last_error and st.session_state.workflow_step == WORKFLOW_PLAN:
        st.warning(st.session_state.last_error)

    continue_col, spacer_col = st.columns([1, 1])
    continue_col.button(
        "Continue to confirmation",
        type="primary",
        use_container_width=True,
        on_click=continue_to_confirmation,
    )
    spacer_col.empty()


def render_confirmation_step() -> None:
    st.markdown(
        '<div class="ra-card"><div class="ra-card-title">3. Confirm the report plan</div>'
        '<div class="ra-muted">Confirm the scope, sections and filename before generation.</div></div>',
        unsafe_allow_html=True,
    )

    summary_col, output_col = st.columns([1.15, 0.85], gap="large")
    with summary_col:
        render_plan_summary_card("Scope to confirm")
        render_output_file_card()
    with output_col:
        render_planned_output_card()

    if st.session_state.last_error and st.session_state.workflow_step == WORKFLOW_CONFIRM:
        st.warning(st.session_state.last_error)

    action_col, edit_col = st.columns([1, 1])
    if st.session_state.plan_confirmed:
        st.success("Plan confirmed. The generation scope is locked for this run.")
    else:
        action_col.button(
            "Confirm report plan",
            type="primary",
            use_container_width=True,
            on_click=confirm_plan,
        )

    edit_col.button("Edit report plan", use_container_width=True, on_click=edit_report_plan)


def render_generation_step() -> None:
    st.markdown(
        '<div class="ra-card"><div class="ra-card-title">4. Generation status</div>'
        '<div class="ra-muted">Generate, monitor status and download the PowerPoint package.</div></div>',
        unsafe_allow_html=True,
    )

    if not st.session_state.plan_confirmed:
        st.info("Confirm the report plan before generation.")
        return

    if st.session_state.status == "Ready":
        st.button(
            "Generate PowerPoint",
            type="primary",
            use_container_width=True,
            on_click=start_generation,
        )

    if st.session_state.status == "Generating":
        stages = [
            "Validate confirmed scope",
            "Load current inventory",
            "Load comparison inventory",
            "Apply population filters",
            "Rank risks and material changes",
            "Generate report narrative",
            "Create charts and tables",
            "Assemble and validate PowerPoint",
        ]

        try:
            with st.status("Generating report package...", expanded=True) as status:
                for stage in stages:
                    status.write(stage)
                    time.sleep(0.18)

                st.session_state.generated_bytes = generate_powerpoint(
                    plan=st.session_state.plan,
                    refined_goal=st.session_state.refined_goal,
                    sections=st.session_state.selected_sections,
                )
                st.session_state.status = "Completed"
                status.update(label="Report package completed", state="complete", expanded=False)
        except Exception as exc:  # pragma: no cover - defensive UI path
            st.session_state.status = "Draft"
            st.session_state.plan_confirmed = False
            st.session_state.workflow_step = WORKFLOW_CONFIRM
            st.session_state.last_error = str(exc)
            st.error(f"Generation failed: {exc}")

    if st.session_state.status == "Completed" and st.session_state.generated_bytes:
        final_filename = sanitize_filename(st.session_state.filename)
        st.success(f"Report package completed: {final_filename}")
        st.download_button(
            "Download PowerPoint package",
            data=st.session_state.generated_bytes,
            file_name=final_filename,
            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
            type="primary",
            use_container_width=True,
        )
    elif st.session_state.status != "Generating":
        stage_labels = [
            ("Draft", "Define or revise the report goal and scope"),
            ("Reviewing", "Review the synchronized plan"),
            ("Ready", "Confirmed and ready to generate"),
            ("Generating", "Building the PowerPoint package"),
            ("Completed", "Ready for download"),
        ]
        for stage, description in stage_labels:
            marker = "●" if stage == st.session_state.status else "○"
            st.write(f"{marker} **{stage}** — {description}")


if st.session_state.workflow_step in {WORKFLOW_GOAL, WORKFLOW_PLAN}:
    render_short_goal_step()
    if st.session_state.workflow_step == WORKFLOW_PLAN:
        st.divider()
        render_plan_review_step()
elif st.session_state.workflow_step == WORKFLOW_CONFIRM:
    render_confirmation_step()
else:
    render_confirmation_step()
    st.divider()
    render_generation_step()
