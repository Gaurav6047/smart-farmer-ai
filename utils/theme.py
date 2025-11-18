import streamlit as st

def load_theme():
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

    /* ==================== GLOBAL IMAGE SIZE FIX ==================== */
    img {
        max-height: 350px !important;
        width: auto !important;
        object-fit: contain !important;
        border-radius: 12px !important;
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

    /* ==================== SELECTBOX FIX ==================== */
    div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        border: 2px solid #1A9E55 !important;
        border-radius: 10px !important;
        color: #000000 !important;
        font-weight: 600 !important;
    }

    div[data-baseweb="select"] span {
        color: #000000 !important;
        font-size: 16px !important;
        font-weight: 600 !important;
    }

    div[data-baseweb="select"] svg {
        fill: #000000 !important;
    }

    ul[role="listbox"] {
        background-color: white !important;
        border: 2px solid #1A9E55 !important;
        border-radius: 10px !important;
    }

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
        border: 1px solid rgba(255,255,255,0.45);
        box-shadow: 0 4px 20px rgba(0,0,0,0.06);
    }

    /* ==================== HEADER ==================== */
    .header-box {
        background: var(--header-gradient);
        padding: 18px 28px;
        border-radius: 18px;
        color: white;
    }

    /* ==================== PERFECT MOBILE OPTIMIZATION ==================== */
    @media (max-width: 480px) {

        .block-container {
            padding-top: 0.5rem !important;
            padding-left: 0.6rem !important;
            padding-right: 0.6rem !important;
        }

        [data-testid="stSidebar"] {
            width: 230px !important;
        }

        .stButton>button {
            width: 100% !important;
            height: 55px !important;
            font-size: 18px !important;
        }

        .header-box h2 {
            font-size: 24px !important;
        }

        .header-box p {
            font-size: 14px !important;
        }

        img {
            max-width: 100% !important;
            height: auto !important;
            border-radius: 12px !important;
        }

        .stTabs [data-baseweb="tab"] {
            font-size: 14px !important;
            padding: 6px !important;
        }
    }

    /* REMOVE DEFAULT STREAMLIT EFFECT */
    .block-container, .main, section {
        background: transparent !important;
        box-shadow: none !important;
        border: none !important;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    </style>
    """, unsafe_allow_html=True)
