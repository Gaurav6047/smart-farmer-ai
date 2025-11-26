import streamlit as st

def render_sidebar():
    """Global sidebar with permanent language state"""

    # Disable Streamlit sidebar navigation
    st.markdown("""
        <style>
            [data-testid="stSidebarNav"] {display: none !important;}
        </style>
    """, unsafe_allow_html=True)

    # 1. Initialize State if not present
    if "lang" not in st.session_state:
        st.session_state["lang"] = "English"

    # 2. Get current state to set default index
    current_lang = st.session_state["lang"]
    lang_index = 0 if current_lang == "English" else 1

    with st.sidebar:
        st.header("Settings" if current_lang == "English" else "सेटिंग्स")

        # 3. Widget with a TEMPORARY key (NOT "lang")
        # हमने key को "lang_select_box" कर दिया है ताकि यह session_state["lang"] से टकराए नहीं
        selected = st.selectbox(
            "Language / भाषा",
            ["English", "Hindi"],
            index=lang_index,
            key="lang_select_box" 
        )

        # 4. Manual Update Logic
        # अगर यूजर ने भाषा बदली, तो हम Main Variable ("lang") को अपडेट करेंगे
        if selected != current_lang:
            st.session_state["lang"] = selected
            st.rerun()

        st.markdown("---")

        # --- MENU RENDERING BASED ON CURRENT_LANG ---
        menu = {
            "Home":              ("Home Page",                "मुख्य पेज"),
            "Router":            ("Smart Auto-Scan",          "स्मार्ट ऑटो-स्कैन"),
            "Disease":           ("Plant Disease Detection",  "पौधे की बीमारी पहचान"),
            "Pest":              ("Pest Identification",      "कीट पहचान"),
            "Fruit":             ("Fruit & Veg Classifier",   "फल-सब्ज़ी पहचान"),
            "Fertilizer":        ("Fertilizer Calculator",    "खाद गणना"),
            "Irrigation":        ("Irrigation Advisory",      "सिंचाई सलाह"),
            "CropReco":          ("Crop Recommendation",      "फसल सिफारिश"),
            "ModelInfo":         ("Model & Engine Info",      "मॉडल और इंजन जानकारी"),
        }

        # Label helper
        idx = 0 if current_lang == "English" else 1

        st.markdown("### " + ("Menu" if current_lang == "English" else "मेनू"))

        st.page_link("main.py", label=menu["Home"][idx])
        
        st.caption("AI Tools" if current_lang == "English" else "AI टूल्स")
        st.page_link("pages/Auto_Routing.py", label=menu["Router"][idx])
        st.page_link("pages/Plant_Disease.py", label=menu["Disease"][idx])
        st.page_link("pages/Pest_Detection.py", label=menu["Pest"][idx])
        st.page_link("pages/Fruit_Classification.py", label=menu["Fruit"][idx])

        st.caption("Advisory" if current_lang == "English" else "सलाह")
        st.page_link("pages/Fertilizer_Recommendation.py", label=menu["Fertilizer"][idx])
        st.page_link("pages/Irrigation.py", label=menu["Irrigation"][idx])
        st.page_link("pages/Crop_Recommendation.py", label=menu["CropReco"][idx])

        st.caption("Info" if current_lang == "English" else "जानकारी")
        st.page_link("pages/Model_Classes_Info.py", label=menu["ModelInfo"][idx])