import streamlit as st
from utils.language import get_text
from utils.sidebar import render_sidebar

# ----------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------
st.set_page_config(
    page_title="Smart Farmer",
    page_icon="",
    layout="wide"
)

# ----------------------------------------------------
# RENDER GLOBAL SIDEBAR (handles language)
# ----------------------------------------------------
render_sidebar()

# ----------------------------------------------------
# READ LANGUAGE (NO SELECTBOX HERE)
# ----------------------------------------------------
# Language (Only read)
lang = st.session_state.get("lang", "English")
T = get_text(lang)
tr = lambda k: T.get(k, k)




# ----------------------------------------------------
# PREMIUM THEME
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

/* SIDEBAR */
[data-testid="stSidebar"] {
    background-color: var(--sidebar-bg-dark) !important;
    backdrop-filter: blur(6px);
    box-shadow: 3px 0px 14px rgba(0,0,0,0.06);
}
[data-testid="stSidebar"] * {
    color: var(--sidebar-text) !important;
    font-weight: 600 !important;
}

/* SELECTBOX FIX */
div[data-baseweb="select"] > div {
    background-color: #FFFFFF !important;
    border: 2px solid #1A9E55 !important;
    border-radius: 10px !important;
}
div[data-baseweb="select"] span {
    color: #000000 !important;
    font-size: 16px !important;
}
ul[role="listbox"] {
    background-color: #FFFFFF !important;
    border-radius: 10px !important;
    border: 2px solid #1A9E55 !important;
}
ul[role="listbox"] li:hover {
    background-color: #E6FFF1 !important;
}

/* BUTTON */
.stButton > button {
    background: var(--primary) !important;
    color: white !important;
    font-size: 18px !important;
    border-radius: 12px !important;
}
.stButton > button:hover {
    background: var(--primary-dark) !important;
}

/* CARDS */
.glass-card {
    background: var(--card-bg);
    backdrop-filter: blur(6px);
    border-radius: 16px;
    padding: 20px 25px;
    border: 1px solid rgba(255,255,255,0.45);
    box-shadow: 0 4px 20px rgba(0,0,0,0.06);
}

/* HEADER */
.header-box {
    background: var(--header-gradient);
    padding: 18px 28px;
    border-radius: 18px;
    color: white;
}

@media (max-width: 480px) {
    .stButton>button {
        width: 100% !important;
        height: 55px !important;
        font-size: 18px !important;
    }
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

</style>
""", unsafe_allow_html=True)


# ----------------------------------------------------
# HEADER
# ----------------------------------------------------
st.markdown(f"""
<div class="header-box">
    <h1 style="margin:0; font-size:32px;">{tr("app_title")}</h1>
    <p style="margin:0; font-size:18px;">{tr("home_sub")}</p>
</div>
""", unsafe_allow_html=True)


# ----------------------------------------------------
# HOME BANNER
# ----------------------------------------------------
try:
    st.image(
        "assets/ui/Ask The Storybots Farm GIF by StoryBots.gif",
        use_container_width=True
    )
except:
    st.warning(tr("banner_missing"))


# ----------------------------------------------------
# FEATURES
# ----------------------------------------------------
st.markdown(f"""
<div class="glass-card">

<h2>{tr("features")}</h2>

<ul style="font-size:18px; line-height:1.6;">
    <li>{tr("feat_disease")}</li>
    <li>{tr("feat_pest")}</li>
    <li>{tr("feat_fruit")}</li>
    <li>{tr("feat_auto")}</li>
    <li>{tr("feat_model_info")}</li>
    <li>{tr("feat_crop")}</li>
    <li>{tr("feat_fertilizer")}</li>
    <li>{tr("feat_irrigation")}</li>
</ul>

<p style="font-size:17px; color:#0f3e1e;">
{tr("navigate_sidebar")}
</p>

</div>
""", unsafe_allow_html=True)
