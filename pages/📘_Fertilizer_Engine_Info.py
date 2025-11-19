import streamlit as st
from utils.language import get_text
from utils.theme import load_theme
st.set_page_config(
    page_title="Fertilizer Engine Info",
    page_icon="📘",
    layout="wide"
)
# Load global theme
load_theme()

# ---------------------------
# Language System
# ---------------------------
lang = st.sidebar.selectbox("Language / भाषा", ["English", "Hindi"])
T = get_text(lang)

def tr(key):
    return T[key]


# ---------------------------
# HEADER (MATCHED WITH THEME)
# ---------------------------
st.markdown(f"""
<div style="
    background: var(--header-gradient);
    padding: 25px; 
    border-radius: 16px; 
    color:white;
    box-shadow: 0 4px 14px rgba(0,0,0,0.1);
">
    <h1 style="margin:0;">📘 {tr('info_title')}</h1>
    <p style="margin:0;opacity:0.9;">AI + Agronomy Based Nutrient Engine</p>
</div>
""", unsafe_allow_html=True)


# ---------------------------
# CARD COMPONENT
# ---------------------------
def card(title, body, icon):
    st.markdown(f"""
    <div style="
        background: var(--card-bg);
        padding: 22px 25px;
        border-radius: 16px;
        margin-top: 22px;
        border-left: 6px solid var(--primary);
        backdrop-filter: blur(8px);
        box-shadow: 0px 4px 20px rgba(0,0,0,0.06);
    ">
        <h3 style="margin-top:0; color: var(--primary-dark);">{icon} {title}</h3>
        <div style="font-size:16px; line-height:1.65; color:#08361A;">{body}</div>
    </div>
    """, unsafe_allow_html=True)


# ---------------------------
# INTRO
# ---------------------------
card(
    tr("info_title"),
    tr("info_intro").replace("\n", "<br>"),
    "🌱"
)


# ---------------------------
# PROBLEM
# ---------------------------
card(
    tr("info_problem"),
    tr("info_problem_text").replace("\n", "<br>"),
    "🎯"
)


# ---------------------------
# ARCHITECTURE
# ---------------------------
card(
    tr("info_arch"),
    tr("info_arch_text").replace("\n", "<br>"),
    "🏗️"
)


# ---------------------------
# DATA
# ---------------------------
card(
    tr("info_data"),
    tr("info_data_text").replace("\n", "<br>"),
    "📂"
)


# ---------------------------
# WORKFLOW (FIXED WITH <br>)
# ---------------------------
workflow = """
1. Soil analysis (N, P, K, pH, EC, Zn, Fe)<br>
2. Select STCR / Standard method<br>
3. Calculate base NPK<br>
4. Deduct organic credits (IPNS)<br>
5. Apply pH/EC/rotation corrections<br>
6. Convert NPK → Urea / DAP / MOP<br>
7. Generate alerts + breakdown<br>
"""

if lang == "Hindi":
    workflow = """
1. मृदा विश्लेषण (N, P, K, pH, EC, Zn, Fe)<br>
2. STCR / Standard विधि चुनें<br>
3. आधार NPK आवश्यकता निकालें<br>
4. जैविक कटौती घटाएँ (IPNS)<br>
5. pH / EC / फसल चक्र सुधार जोड़ें<br>
6. NPK को Urea / DAP / MOP में बदलें<br>
7. चेतावनी + तकनीकी विवरण तैयार करें<br>
"""

card(
    tr("info_workflow"),
    workflow,
    "🧠"
)


# ---------------------------
# LEVEL (FIXED WITH <br>)
# ---------------------------
level = """
This is NOT:<br><br>
❌ A basic calculator<br>
❌ A college mini-project<br>
❌ A simple Streamlit app<br><br>

This IS:<br>
✅ Production-grade Agritech Engine<br>
✅ Modular, scalable architecture<br>
✅ Industry-level design<br>
"""

if lang == "Hindi":
    level = """
यह बिल्कुल भी नहीं है:<br><br>
❌ एक साधारण कैलकुलेटर<br>
❌ कॉलेज प्रोजेक्ट<br>
❌ बेसिक Streamlit ऐप<br><br>

यह वास्तव में है:<br>
✅ प्रोडक्शन-ग्रेड एग्रीटेक इंजन<br>
✅ मॉड्यूलर और स्केलेबल<br>
✅ इंडस्ट्री-स्तर की आर्किटेक्चर<br>
"""

card(
    tr("info_level"),
    level,
    "🏆"
)


# ---------------------------
# FUTURE (FIXED WITH <br>)
# ---------------------------
future = """
- AI-based yield prediction<br>
- Satellite/weather integration<br>
- Irrigation-specific formulas<br>
- Regional fertilizer models<br>
"""

if lang == "Hindi":
    future = """
- एआई आधारित उपज अनुमान<br>
- उपग्रह/मौसम API एकीकरण<br>
- सिंचाई आधारित उर्वरक सूत्र<br>
- क्षेत्रीय उर्वरक मॉडल<br>
"""

card(
    tr("info_future"),
    future,
    "🔮"
)


# ---------------------------
# FOOTER
# ---------------------------
st.markdown("""
<br>
<div style='
    text-align:center;
    opacity:0.9;
    font-size:17px;
    color:white;'>
🚜 Smart Farmer — India's First Open-Source Agritech Engine
</div>
""", unsafe_allow_html=True)
