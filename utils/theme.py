import streamlit as st

COLOR_PRIMARY = "#1A1A1A"
COLOR_SURFACE = "#FFFFFF"
COLOR_NEUTRAL = "#808080"
COLOR_ACCENT = "#B38B6D"
COLOR_BORDER = "#E5E5E0"
COLOR_ALERT = "#C0392B"
COLOR_OK = "#2E7D5B"

BASE_CSS = f"""
<style>
    html, body, [class*="css"] {{
        font-family: -apple-system, "Segoe UI", Inter, sans-serif;
    }}
    .swiss-header {{
        font-size: clamp(1.75rem, 3.2vw, 2.25rem);
        font-weight: 700;
        color: {COLOR_PRIMARY};
        letter-spacing: -0.01em;
        margin-bottom: 0.25rem;
    }}
    .swiss-subheader {{
        color: {COLOR_NEUTRAL};
        font-size: 0.95rem;
        margin-bottom: 2rem;
    }}
    .swiss-label {{
        font-size: 0.75rem;
        font-weight: 500;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        color: {COLOR_NEUTRAL};
    }}
    .icon {{
        display: inline-flex;
        align-items: center;
        vertical-align: middle;
        color: {COLOR_PRIMARY};
    }}
    .icon.accent {{ color: {COLOR_ACCENT}; }}
    .icon.alert {{ color: {COLOR_ALERT}; }}
    .icon.ok {{ color: {COLOR_OK}; }}

    /* --- Building card (home page) --- */
    .building-card {{
        background-color: {COLOR_SURFACE};
        border: 1px solid {COLOR_BORDER};
        border-radius: 0px;
        padding: 24px 20px;
        text-align: center;
        transition: box-shadow 0.2s ease-out, border-color 0.2s ease-out, transform 0.2s ease-out;
        height: 100%;
    }}
    .building-card:hover {{
        border-color: {COLOR_ACCENT};
        box-shadow: 0 4px 16px rgba(0,0,0,0.08);
        transform: translateY(-2px);
    }}
    .building-card .icon {{
        margin-bottom: 10px;
    }}
    .building-card .building-name {{
        font-size: 1.05rem;
        font-weight: 600;
        color: {COLOR_PRIMARY};
    }}
    .building-card .building-caption {{
        font-size: 0.8rem;
        color: {COLOR_NEUTRAL};
        margin-top: 4px;
    }}

    div[data-testid="column"] {{
        background-color: transparent;
        border: none;
        padding: 6px;
    }}

    /* --- Metric cards (dashboard) --- */
    .metric-card {{
        background-color: {COLOR_SURFACE};
        border: 1px solid {COLOR_BORDER};
        border-left: 4px solid {COLOR_OK};
        border-radius: 0px;
        padding: 20px;
        margin-bottom: 16px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.05);
    }}
    .metric-card.alert {{ border-left-color: {COLOR_ALERT}; }}
    .metric-title-row {{
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 10px;
    }}
    .metric-title {{
        font-size: 0.8rem;
        font-weight: 500;
        letter-spacing: 0.03em;
        text-transform: uppercase;
        color: {COLOR_NEUTRAL};
    }}
    .metric-value {{
        font-size: 1.75rem;
        font-weight: 700;
        color: {COLOR_PRIMARY};
    }}
    .metric-value.alert {{ color: {COLOR_ALERT}; }}
    .metric-value.ok {{ color: {COLOR_OK}; }}
    .metric-footnote {{
        margin-top: 10px;
        color: {COLOR_NEUTRAL};
        font-size: 0.85rem;
    }}
    .sidebar-brand {{
        display: flex;
        align-items: center;
        gap: 8px;
        font-weight: 600;
        margin-bottom: 4px;
    }}

        /* --- Status badges (home + overview) --- */
    .badge-row {{
        display: flex;
        justify-content: center;
        gap: 8px;
        margin-top: 8px;
        flex-wrap: wrap;
    }}
    .status-badge {{
        display: inline-flex;
        align-items: center;
        gap: 4px;
        padding: 3px 8px;
        font-size: 0.72rem;
        font-weight: 600;
        border: 1px solid;
    }}
    .status-badge.alert {{
        color: {COLOR_ALERT};
        border-color: {COLOR_ALERT};
        background: #FBEAE8;
    }}
    .status-badge.ok {{
        color: {COLOR_OK};
        border-color: {COLOR_OK};
        background: #EAF3EE;
    }}

.overview-cta {{
        display: flex;
        align-items: center;
        gap: 18px;
        background-color: {COLOR_SURFACE};
        border: 1px solid {COLOR_BORDER};
        border-left: 4px solid {COLOR_ACCENT};
        padding: 22px 24px;
        transition: box-shadow 0.2s ease-out, border-color 0.2s ease-out, transform 0.2s ease-out;
    }}
    .overview-cta:hover {{
        border-color: {COLOR_ACCENT};
        box-shadow: 0 4px 16px rgba(0,0,0,0.08);
        transform: translateY(-2px);
    }}
    .overview-cta .icon {{
        color: {COLOR_ACCENT};
        flex-shrink: 0;
    }}
    .overview-cta .overview-cta-title {{
        font-size: 1.05rem;
        font-weight: 600;
        color: {COLOR_PRIMARY};
    }}
    .overview-cta .overview-cta-caption {{
        font-size: 0.85rem;
        color: {COLOR_NEUTRAL};
        margin-top: 2px;
    }}
    .overview-cta .overview-cta-arrow {{
        margin-left: auto;
        color: {COLOR_ACCENT};
        font-size: 1.3rem;
    }}
    /* --- Overview table --- */
    .overview-building {{
        font-weight: 600;
        font-size: 0.8rem;
        color: {COLOR_NEUTRAL};
        text-transform: uppercase;
        letter-spacing: 0.03em;
        margin: 18px 0 4px;
    }}
    .overview-row {{
        display: grid;
        grid-template-columns: 1.2fr 1fr 1fr 1fr;
        align-items: center;
        padding: 10px 14px;
        border-bottom: 1px solid {COLOR_BORDER};
        font-size: 0.9rem;
    }}
    .overview-row.header {{
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.03em;
        text-transform: uppercase;
        color: {COLOR_NEUTRAL};
        border-bottom: 2px solid {COLOR_PRIMARY};
    }}

    .campus-banner {{
        display: flex;
        justify-content: center;
    }}
    .campus-banner img {{
        max-width: 100%;
        width: 700px;
        border-radius: 0px;
    }}   

</style>
"""


def inject_base_css() -> None:
    st.markdown(BASE_CSS, unsafe_allow_html=True)