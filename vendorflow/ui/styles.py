"""Shared design system CSS for VendorFlow AI."""

GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400&family=DM+Mono:wght@400;500&display=swap');

/* ── RESET & BASE ── */
.stApp {
    background-color: #0D1117 !important;
    font-family: 'DM Sans', sans-serif !important;
    background-image: url('https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=1920&q=80') !important;
    background-size: cover !important;
    background-position: center center !important;
    background-attachment: fixed !important;
    background-repeat: no-repeat !important;
}

.stApp::before {
    content: '' !important;
    position: fixed !important;
    top: 0 !important;
    left: 0 !important;
    width: 100% !important;
    height: 100% !important;
    background: rgba(13, 17, 23, __OVERLAY_OPACITY__) !important;
    z-index: -1 !important;
    pointer-events: none !important;
}

/* Hide the Streamlit Top Header (Deploy/Menu) for a true clean SaaS look */
[data-testid="stHeader"] {
    display: none !important;
    visibility: hidden !important;
    height: 0 !important;
}

/* Safely apply DM Sans to standard text elements without breaking internal icons */
p, span, div, h1, h2, h3, h4, h5, h6, label, input, button, textarea {
    font-family: 'DM Sans', sans-serif;
}

.main .block-container {
    padding: 2.5rem 3rem 4rem !important;
    max-width: 1200px !important;
    animation: fadeUp 0.25s ease-out !important;
}

/* Page fade-in */
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(6px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: #0D1117 !important;
    border-right: 1px solid #30363D !important;
}
[data-testid="stSidebar"] > div {
    padding: 1.5rem 1rem !important;
}

/* Hide Sidebar Toggle Controls on Desktop (Make it permanent) */
@media (min-width: 900px) {
    /* ONLY hide the close chevron (inside the open sidebar). 
       This makes the sidebar impenetrable and permanently open.
       We specifically DO NOT hide the expand button, so users trapped 
       in localstorage-collapsed states can still rescue themselves. */
    [data-testid="stSidebar"] button[kind="header"] {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        pointer-events: none !important;
    }
}

/* Hide Streamlit auto-generated page nav */
[data-testid="stSidebarNav"] { display: none !important; }

/* ── BUTTONS ── */
.stButton > button {
    background: #00B4A6 !important;
    color: #0D1117 !important;
    border: none !important;
    border-radius: 6px !important;
    padding: 0.55rem 1.4rem !important;
    font-weight: 600 !important;
    font-size: 0.875rem !important;
    font-family: 'DM Sans', sans-serif !important;
    transition: all 0.15s ease !important;
    letter-spacing: 0.01em !important;
}
.stButton > button:hover {
    background: #00C9B8 !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}

.stButton > button[kind="secondary"] {
    background: transparent !important;
    color: #C9D1D9 !important;
    border: 1px solid #30363D !important;
}
.stButton > button[kind="secondary"]:hover {
    border-color: #8B949E !important;
    color: #F0F6FC !important;
}

/* ── INPUTS ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div {
    background: rgba(22, 27, 34, 0.95) !important;
    border: 1px solid #30363D !important;
    border-radius: 6px !important;
    color: #F0F6FC !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.875rem !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #00B4A6 !important;
    box-shadow: 0 0 0 3px rgba(0,180,166,0.1) !important;
    outline: none !important;
}

/* ── FILE UPLOADER ── */
[data-testid="stFileUploader"] {
    background: rgba(22, 27, 34, 0.95) !important;
    border: 1px dashed #30363D !important;
    border-radius: 8px !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: #00B4A6 !important;
}

/* ── METRICS ── */
[data-testid="stMetric"] {
    background: rgba(22, 27, 34, 0.95) !important;
    border: 1px solid #30363D !important;
    border-radius: 8px !important;
    padding: 1.25rem !important;
}
[data-testid="stMetricValue"] {
    color: #F0F6FC !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 1.8rem !important;
    font-weight: 500 !important;
}
[data-testid="stMetricLabel"] {
    color: #8B949E !important;
    font-size: 0.8rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
}

/* ── DATAFRAME ── */
[data-testid="stDataFrame"] {
    border: 1px solid #30363D !important;
    border-radius: 8px !important;
}

/* ── ALERTS ── */
.stAlert {
    border-radius: 6px !important;
    border-left-width: 3px !important;
}

/* ── SLIDERS ── */
[data-testid="stSlider"] > div > div > div > div {
    background: #00B4A6 !important;
}

/* ── DIVIDER ── */
hr { border-color: #21262D !important; }

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #0D1117; }
::-webkit-scrollbar-thumb { 
    background: #30363D; 
    border-radius: 3px; 
}
::-webkit-scrollbar-thumb:hover { 
    background: #00B4A6; 
}
/* ── FORMS AND ALERTS FIX ── */
.stTextInput > div > div > input {
    background: rgba(22, 27, 34, 0.98) !important;
    border: 1px solid #30363D !important;
}

[data-testid="stForm"] {
    background: rgba(13, 17, 23, 0.95) !important;
    border: 1px solid #21262D !important;
    border-radius: 12px !important;
    padding: 1.5rem !important;
}

[data-testid="stAlert"] {
    background: rgba(22, 27, 34, 0.95) !important;
    border: 1px solid #30363D !important;
    border-left: 3px solid #00B4A6 !important;
    color: #F0F6FC !important;
}

.stTextInput label,
.stSelectbox label,
.stTextArea label {
    color: #E6EDF3 !important;
    font-weight: 600 !important;
}

</style>
"""


def inject_css(overlay_opacity="0.88"):
    """Inject global design CSS into the page."""
    import streamlit as st
    css_to_inject = GLOBAL_CSS.replace("__OVERLAY_OPACITY__", str(overlay_opacity))
    st.html(css_to_inject)


def section_header(title: str, badge: str = "") -> str:
    """Return a styled section header HTML string."""
    badge_html = f"""<span style="background:#21262D;color:#8B949E;font-size:0.7rem;font-weight:500;padding:2px 8px;border-radius:50px;text-transform:uppercase;letter-spacing:0.08em;">{badge}</span>""" if badge else ""
    return f"""
    <div style="display:flex;align-items:center;
         gap:10px;margin:2rem 0 1.25rem;
         padding-bottom:0.75rem;
         border-bottom:1px solid #21262D;">
        <span style="color:#F0F6FC;font-size:1rem;
              font-weight:600;letter-spacing:0.01em;">
              {title}
        </span>
        {badge_html}
    </div>
    """


def page_header(title: str, subtitle: str) -> str:
    """Return a styled page header HTML string."""
    return f"""
    <div style="margin-bottom:2.5rem;">
        <h1 style="font-size:1.75rem;font-weight:700;
             color:#F0F6FC;margin:0 0 0.4rem;
             letter-spacing:-0.01em;">
             {title}
        </h1>
        <p style="color:#8B949E;font-size:0.875rem;
             margin:0;">
             {subtitle}
        </p>
    </div>
    """


def render_sidebar_nav():
    """Render sidebar navigation for all pages using native Streamlit routing."""
    import streamlit as st
    import os
    
    st.html("""
    <div style="padding:0.5rem 0 1.5rem;">
        <h1 style="color:#E6EDF3;font-size:1.25rem;
            font-weight:700;margin:0 0 0.25rem;
            letter-spacing:-0.02em;">
            VendorFlow <span style="color:#00B4A6;">AI</span>
        </h1>
        <p style="color:#8B949E;font-size:0.75rem;
           margin:0;font-weight:500;">
           Vendor Onboarding Agent
        </p>
    </div>
    <div style="height:1px;background:#21262D;
         margin-bottom:1.5rem;"></div>
    """)
    
    # Resolve correct paths dynamically regardless of deployment working directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    app_path = os.path.join(base_dir, "app.py")
    pages_dir = os.path.join(base_dir, "pages")
    
    st.page_link(app_path, label="Home")
    st.page_link(os.path.join(pages_dir, "1_Setup.py"), label="Setup")
    st.page_link(os.path.join(pages_dir, "2_Run.py"), label="Run")
    st.page_link(os.path.join(pages_dir, "3_Dashboard.py"), label="Dashboard")
    st.page_link(os.path.join(pages_dir, "4_Replay.py"), label="Replay")
