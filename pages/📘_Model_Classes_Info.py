import streamlit as st
import pandas as pd
import json
from utils.language import get_text
from utils.theme import load_theme

# ----------------------------------------------------
# Load Global Theme (same as main.py)
# ----------------------------------------------------
load_theme()

# -------------------------------
# Language
# -------------------------------
lang = st.sidebar.selectbox("Language / भाषा", ["English", "Hindi"])
T = get_text(lang)

# -------------------------------
# Page Title
# -------------------------------
st.markdown(f"""
<div class="header-box">
    <h2 style='margin:0;color:white;'>📘 Model Classes Information</h2>
</div>
""", unsafe_allow_html=True)

# -------------------------------
# Description (language wise)
# -------------------------------
if lang == "English":
    st.markdown("""
This page displays all the **classes used by your AI models**:

- 🌿 Plant Disease Model (38 classes)
- 🐛 Pest Detection Model (20 classes)
- 🍎 Fruit & Vegetable Classification (36 classes)
""")
else:
    st.markdown("""
यह पेज आपके AI मॉडल की **सभी क्लासों की सूची** दिखाता है:

- 🌿 पौधा रोग मॉडल (38 क्लास)
- 🐛 कीट पहचान मॉडल (20 क्लास)
- 🍎 फल और सब्ज़ी वर्गीकरण (36 क्लास)
""")

# -------------------------------
# Safe Loaders
# -------------------------------
def safe_load_csv(path):
    try:
        return pd.read_csv(path)
    except:
        return None

def safe_load_json(path):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except:
        return None

# -------------------------------
# Load Files
# -------------------------------
plant_df = safe_load_csv("models/Plant Village Disease-class_dict.csv")
pest_df = safe_load_csv("models/pest_classes.csv")
fruit_classes = safe_load_json("models/fruit_class_names.json")

# -------------------------------
# Tabs
# -------------------------------
tab1, tab2, tab3 = st.tabs([
    "🌿 Plant Diseases" if lang=="English" else "🌿 पौधा रोग",
    "🐛 Pests" if lang=="English" else "🐛 कीट",
    "🍎 Fruits & Vegetables" if lang=="English" else "🍎 फल / सब्ज़ियाँ"
])

# ======================================================
# TAB 1 — PLANT
# ======================================================
with tab1:
    st.subheader("🌿 Plant Disease Classes")

    if plant_df is None:
        st.error("❌ plant disease CSV missing in models/")
    else:
        st.success(f"✔ Total Classes: {len(plant_df)}")

        st.dataframe(
            plant_df[["class_index", "class"]],
            width="stretch",
            hide_index=True
        )

    st.info(
        "Upload a clear leaf image with good lighting"
        if lang=="English"
        else "स्पष्ट और रोशनी वाली पत्ती की इमेज अपलोड करें"
    )

# ======================================================
# TAB 2 — PEST
# ======================================================
with tab2:
    st.subheader("🐛 Pest Classes")

    if pest_df is None:
        st.error("❌ pest_classes.csv missing in models/")
    else:
        st.success(f"✔ Total Classes: {len(pest_df)}")

        st.dataframe(
            pest_df[["new_id", "class_name"]],
            width="stretch",
            hide_index=True
        )

    st.warning(
        "Bring camera close to pest!" 
        if lang=="English" 
        else "कीट की फोटो पास से लें!"
    )

# ======================================================
# TAB 3 — FRUIT
# ======================================================
with tab3:
    st.subheader("🍎 Fruit & Vegetable Classes")

    if fruit_classes is None:
        st.error("❌ fruit_class_names.json missing in models/")
    else:
        df = pd.DataFrame({"Classes": fruit_classes})
        st.success(f"✔ Total Classes: {len(df)}")

        st.dataframe(
            df,
            width="stretch",
            hide_index=True
        )

    st.info(
        "Use good lighting and keep fruit centered."
        if lang=="English"
        else "फल को बीच में रखें और अच्छी रोशनी का उपयोग करें।"
    )
