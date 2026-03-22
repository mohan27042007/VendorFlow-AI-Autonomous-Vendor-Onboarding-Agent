"""Streamlit entry point for VendorFlow AI."""

import os
import sys

_vendorflow_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _vendorflow_dir not in sys.path:
    sys.path.insert(0, _vendorflow_dir)
# Robust path for Streamlit Cloud
_path = os.path.abspath(__file__)
for _ in range(5):
    _path = os.path.dirname(_path)
    if os.path.exists(os.path.join(_path, "config", "settings.py")):
        if _path not in sys.path:
            sys.path.insert(0, _path)
        break

import streamlit as st

from config.settings import TINYFISH_API_KEY
from ui.styles import inject_css

st.set_page_config(
    page_title="VendorFlow AI",
    page_icon="🐟",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_css()

st.html("""
<script>
function animateCounter(element, target, duration) {
    let start = 0;
    const increment = target / (duration / 16);
    const timer = setInterval(() => {
        start += increment;
        if (start >= target) {
            element.textContent = target;
            clearInterval(timer);
        } else {
            element.textContent = Math.floor(start);
        }
    }, 16);
}

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.counter').forEach(el => {
        const target = parseInt(el.dataset.target);
        if (!isNaN(target)) {
            animateCounter(el, target, 1500);
        }
    });
});
</script>
""")
with st.sidebar:
    st.html("""
    <div style="padding:0.5rem 0 1.5rem;">
        <div style="font-size:1.1rem;font-weight:700;
             color:#F0F6FC;letter-spacing:-0.01em;">
             VendorFlow AI
        </div>
        <div style="font-size:0.75rem;color:#8B949E;
             margin-top:2px;">
             Vendor Onboarding Agent
        </div>
    </div>
    <div style="height:1px;background:#21262D;
         margin-bottom:1.5rem;"></div>
    """)
    st.page_link("pages/1_Setup.py", label="Setup")
    st.page_link("pages/2_Run.py", label="Run")
    st.page_link("pages/3_Dashboard.py", label="Dashboard")
    st.page_link("pages/4_Replay.py", label="Replay")
    st.html('<div style="height:1px;background:#21262D;margin:1.5rem 0;"></div>')

    if TINYFISH_API_KEY and TINYFISH_API_KEY != "your_api_key_here":
        st.html("""
        <div style="display:inline-flex;align-items:center;
             gap:6px;background:rgba(63,185,80,0.1);
             border:1px solid rgba(63,185,80,0.2);
             border-radius:6px;padding:6px 12px;">
            <div style="width:6px;height:6px;
                 background:#3FB950;border-radius:50%;"></div>
            <span style="color:#3FB950;font-size:0.75rem;
                  font-weight:500;">API Connected</span>
        </div>
        """)
    else:
        st.html("""
        <div style="display:inline-flex;align-items:center;
             gap:6px;background:rgba(248,81,73,0.1);
             border:1px solid rgba(248,81,73,0.2);
             border-radius:6px;padding:6px 12px;">
            <div style="width:6px;height:6px;
                 background:#F85149;border-radius:50%;"></div>
            <span style="color:#F85149;font-size:0.75rem;
                  font-weight:500;">API Not Connected</span>
        </div>
        """)

# ── Hero Section ──
st.html("""
<div style="padding:3rem 0 2rem;">

    <!-- Eyebrow label -->
    <div style="display:inline-flex;align-items:center;
         gap:8px;margin-bottom:1.5rem;">
        <div style="width:6px;height:6px;
             background:#00B4A6;border-radius:50%;"></div>
        <span style="color:#8B949E;font-size:0.8rem;
              font-weight:500;text-transform:uppercase;
              letter-spacing:0.1em;">
              Powered by TinyFish Web Agent API
        </span>
    </div>
    
    <!-- Headline -->
    <h1 style="font-size:3rem;font-weight:700;
         color:#F0F6FC;margin:0 0 0.75rem;
         line-height:1.15;letter-spacing:-0.02em;">
        VendorFlow AI
    </h1>
    
    <!-- Subheadline -->
    <p style="font-size:1.1rem;color:#8B949E;
         margin:0 0 0.5rem;font-weight:400;
         max-width:520px;line-height:1.6;">
        Autonomous vendor portal onboarding.
        Forms filled. Documents uploaded. 
        Submissions confirmed.
    </p>
    
    <p style="font-size:0.875rem;color:#6E7681;
         margin:0 0 3rem;">
        No human involvement required.
    </p>

</div>
""")

# ── 4 Stat Cards ──
cols = st.columns(4)
stats = [
    ("5", "+", "Portals Supported"),
    ("4", " hrs saved", "Saved Per Portal"),
    ("100", "%", "Autonomous"),
    ("∞", "", "Scales Infinitely"),
]
for col, (value, suffix, label) in zip(cols, stats):
    with col:
        counter_attrs = f'class="counter" data-target="{value}"' if value.isdigit() else ""
        st.html(f"""
        <div style="background:rgba(22, 27, 34, 0.95);
             border:1px solid #30363D;
             border-radius:8px;
             padding:1.5rem;">
            <div style="color:#8B949E;font-size:0.75rem;
                 font-weight:500;text-transform:uppercase;
                 letter-spacing:0.1em;margin-bottom:0.75rem;">
                 {label}
            </div>
            <div style="color:#F0F6FC;
                 font-family:'DM Mono',monospace;
                 font-size:2.25rem;font-weight:500;
                 line-height:1;">
                 <span {counter_attrs}>{value}</span><span style="font-family:'DM Sans',sans-serif;font-size:1.25rem;margin-left:2px;color:#8B949E;">{suffix}</span>
            </div>
        </div>
        """)

# ── How It Works ──
st.html("""
<div style="margin-top:3rem;">
    <div style="display:flex;align-items:center;
         gap:10px;margin:2rem 0 1.25rem;
         padding-bottom:0.75rem;
         border-bottom:1px solid #21262D;">
        <span style="color:#F0F6FC;font-size:1rem;
              font-weight:600;letter-spacing:0.01em;">
              How It Works
        </span>
    </div>
</div>
""")

cols = st.columns(3)
steps = [
    ("Step 01", "Setup", "Add your company profile and compliance documents once."),
    ("Step 02", "Run", "Agent navigates real portals automatically."),
    ("Step 03", "Done", "Track submissions and approvals live."),
]
for col, (eyebrow, title, desc) in zip(cols, steps):
    with col:
        st.html(f"""
        <div style="background:rgba(22, 27, 34, 0.95);
             border:1px solid #30363D;
             border-radius:8px;padding:1.5rem;">
            <div style="color:#00B4A6;font-size:0.75rem;
                 font-weight:600;text-transform:uppercase;
                 letter-spacing:0.1em;margin-bottom:0.75rem;">
                 {eyebrow}
            </div>
            <div style="color:#F0F6FC;font-weight:600;
                 font-size:1rem;margin-bottom:0.5rem;">
                 {title}
            </div>
            <div style="color:#8B949E;font-size:0.875rem;
                 line-height:1.5;">
                 {desc}
            </div>
        </div>
        """)

# ── Get Started Banner ──
st.html("""
<div style="background:rgba(22, 27, 34, 0.95);border:1px solid #30363D;
     border-radius:8px;padding:1.5rem 2rem;margin-top:2rem;">
    <span style="color:#8B949E;font-weight:500;">
        → Go to <strong>Setup</strong> to configure your company profile,
        then <strong>Run</strong> to start onboarding.
    </span>
</div>
""")
