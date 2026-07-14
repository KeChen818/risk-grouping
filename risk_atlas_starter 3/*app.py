from pathlib import Path

import streamlit as st

from components.sidebar import render_sidebar_filters


BASE_DIR = Path(__file__).parent
PAGES_DIR = BASE_DIR / "m_pages"
LOGO_PATH = BASE_DIR / "assets" / "risk_atlas_logo.png"


def configure_app() -> None:
    st.set_page_config(
        page_title="Risk Atlas",
        page_icon="🌐",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    if LOGO_PATH.exists():
        st.logo(
            LOGO_PATH,
            size="large",
            icon_image=LOGO_PATH,
        )


def build_pages() -> dict[str, st.Page]:
    return {
        "top_exposure": st.Page(
            PAGES_DIR / "01_Top_Exposure.py",
            title="Top Exposure",
            icon=":material/trending_up:",
            default=True,
        ),
        "quant_alignment": st.Page(
            PAGES_DIR / "02_Risk_Quantification_Alignment.py",
            title="Risk Quantification Alignment",
            icon=":material/compare_arrows:",
        ),
        "qoq_change": st.Page(
            PAGES_DIR / "03_QoQ_Change.py",
            title="QoQ Change",
            icon=":material/timeline:",
        ),
        "taxonomy_grouping": st.Page(
            PAGES_DIR / "04_Taxonomy_Grouping.py",
            title="Taxonomy Grouping",
            icon=":material/account_tree:",
        ),
        "theme_proposal": st.Page(
            PAGES_DIR / "05_Theme_Proposal.py",
            title="Theme Proposal",
            icon=":material/auto_awesome:",
        ),
        "watchlist": st.Page(
            PAGES_DIR / "06_Watchlist.py",
            title="Non-material Risk Watchlist",
            icon=":material/visibility:",
        ),
        "inventory_expert": st.Page(
            PAGES_DIR / "07_Inventory_Expert.py",
            title="Inventory Expert",
            icon=":material/smart_toy:",
        ),
        "reporting": st.Page(
            PAGES_DIR / "08_Reporting.py",
            title="Reporting",
            icon=":material/slideshow:",
        ),
        "admin": st.Page(
            PAGES_DIR / "09_Admin.py",
            title="Admin",
            icon=":material/monitoring:",
        ),
    }


def render_sidebar_navigation(pages: dict[str, st.Page]) -> None:
    with st.sidebar:
        st.markdown("## Risk Atlas")
        st.caption("Inventory Intelligence")

        st.divider()

        with st.expander(
            "Risk Profile Summary",
            expanded=False,
            icon=":material/assessment:",
        ):
            st.page_link(pages["top_exposure"])
            st.page_link(pages["quant_alignment"])
            st.page_link(pages["qoq_change"])

        with st.expander(
            "Risk Grouping",
            expanded=False,
            icon=":material/category:",
        ):
            st.page_link(pages["taxonomy_grouping"])
            st.page_link(pages["theme_proposal"])
            st.page_link(pages["watchlist"])

        st.divider()

        st.page_link(pages["inventory_expert"])
        st.page_link(pages["reporting"])
        st.page_link(pages["admin"])

        st.divider()

        render_sidebar_filters()


def main() -> None:
    configure_app()

    pages = build_pages()

    current_page = st.navigation(
        list(pages.values()),
        position="hidden",
    )

    render_sidebar_navigation(pages)

    current_page.run()


if __name__ == "__main__":
    main()