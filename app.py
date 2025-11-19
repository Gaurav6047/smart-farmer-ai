import streamlit as st
from utils.language import get_text

# ----------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------
st.set_page_config(
    page_title="Smart Farmer",
    page_icon="🌱",
    layout="wide"
)

# ----------------------------------------------------
# FULL PREMIUM THEME + SIDEBAR & LANGUAGE FIX
# ----------------------------------------------------
st.markdown("""
<style>

:root {
    --primary: #1A9E55;
    --primary-dark: #157B44;
    --sidebar-bg: #DFFFEF;
    --sidebar-bg-dark: #C8F7DF;
    --sidebar-text: #08361A;
    --card-bg: rgba(255, 255, 255, 0.55);
    --header-gradient: linear-gradient(90deg, #1A9E55, #36D17B);
}

/* GLOBAL BACKGROUND */
body {
    background: #F4FFF8 !important;
}

/* ==================== SIDEBAR ==================== */
[data-testid="stSidebar"] {
    background-color: var(--sidebar-bg-dark) !important;
    backdrop-filter: blur(6px);
    border-right: none !important;
    box-shadow: 3px 0px 14px rgba(0,0,0,0.06);
    padding: 25px 15px;
}
[data-testid="stSidebar"] * {
    color: var(--sidebar-text) !important;
    font-weight: 600 !important;
}

/* ==================== FIX LANGUAGE SELECTBOX ==================== */

/* Selectbox Main */
div[data-baseweb="select"] > div {
    background-color: #FFFFFF !important;
    border: 2px solid #1A9E55 !important;
    border-radius: 10px !important;
    color: #000000 !important;
    font-weight: 600 !important;
}

/* Selected text */
div[data-baseweb="select"] span {
    color: #000000 !important;
    font-size: 16px !important;
}

/* Arrow Icon */
div[data-baseweb="select"] svg {
    fill: #000000 !important;
}

/* Dropdown Panel */
ul[role="listbox"] {
    background-color: #FFFFFF !important;
    border-radius: 10px !important;
    border: 2px solid #1A9E55 !important;
}

/* Dropdown Options */
ul[role="listbox"] li {
    color: #0A3D1F !important;
    font-weight: 600 !important;
    padding: 10px;
}
ul[role="listbox"] li:hover {
    background-color: #E6FFF1 !important;
}

/* ==================== BUTTONS ==================== */
.stButton > button {
    background: var(--primary) !important;
    color: white !important;
    font-size: 18px !important;
    border-radius: 12px !important;
    padding: 10px 18px !important;
    border: none !important;
}
.stButton > button:hover {
    background: var(--primary-dark) !important;
}

/* ==================== CARDS ==================== */
.glass-card {
    background: var(--card-bg);
    backdrop-filter: blur(6px);
    border-radius: 16px;
    padding: 20px 25px;
    border: 1px solid rgba(255, 255, 255, 0.45);
    box-shadow: 0 4px 20px rgba(0,0,0,0.06);
}

/* ==================== HEADER ==================== */
.header-box {
    background: var(--header-gradient);
    padding: 18px 28px;
    border-radius: 18px;
    color: white;
}

/* ==================== MOBILE OPTIMIZATION ==================== */
@media (max-width: 480px) {

    .stButton>button {
        width: 100% !important;
        height: 55px !important;
        font-size: 18px !important;
    }

    img {
        max-width: 100% !important;
        height: auto !important;
    }

    h1 { font-size: 26px !important; }
}

/* Hide Streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# LANGUAGE SELECTOR (now visible 100%)
# ----------------------------------------------------
language = st.sidebar.selectbox("Language / भाषा", ["English", "Hindi"])
T = get_text(language)

# ----------------------------------------------------
# PREMIUM HEADER
# ----------------------------------------------------
st.markdown(f"""
<div class="header-box">
    <h1 style="margin:0; font-size:32px;">{T["app_title"]}</h1>
    <p style="margin:0; font-size:18px;">AI-powered Crop, Pest & Disease Assistant</p>
</div>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# HOME BANNER GIF
# ----------------------------------------------------
try:
    st.image("assets/ui/Ask The Storybots Farm GIF by StoryBots.gif", use_container_width=True)
except:
    st.warning("Home banner missing → assets/ui/farm_banner.gif")

# ----------------------------------------------------
# FEATURES CARD
# ----------------------------------------------------
st.markdown("""
<div class="glass-card">

<h2>🚀 Features</h2>

<ul style="font-size:18px; line-height:1.6;">
    <li>🌿 Plant Disease Detection</li>
    <li>🐛 Pest Detection (YOLO + Bounding Boxes)</li>
    <li>🍎 Fruit Classification</li>
    <li>🔀 Auto Routing (Image Type Detection)</li>
    <li>📘 Model Classes Information</li>
    <li>❓ Wrong Prediction Troubleshooting</li>
    <li>📊 Crop Recommendation (NPK-based)</li>
    <li>🧪 Fertilizer Recommendation Engine</li>
</ul>

<p style="font-size:17px; color:#0f3e1e;">
Use the <b>Left Sidebar</b> to navigate between Smart Farmer features.
</p>

</div>
""", unsafe_allow_html=True)
