import streamlit as st
import numpy as np
import pickle

from utils.theme import load_theme
from utils.sidebar import render_sidebar
from utils.language import get_text

# ----------------------------------------------------
# LOAD THEME + SIDEBAR (Sidebar sets lang safely)
# ----------------------------------------------------
load_theme()
render_sidebar()

# ----------------------------------------------------
# LANGUAGE (sidebar already updated st.session_state["lang"])
# ----------------------------------------------------
# AFTER render_sidebar()
lang = st.session_state.get("lang", "English")
T = get_text(lang)
tr = lambda k: T.get(k, k)


# ----------------------------------------------------
# HEADER
# ----------------------------------------------------
st.markdown(f"""
<div class="header-box">
    <h2 style='margin:0;color:white;'>{tr("crop_recommendation")}</h2>
    <p style='margin:0;color:white;'>{tr("enter_soil_data")}</p>
</div>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# LOAD MODEL + SCALER + LABEL ENCODER
# ----------------------------------------------------
with open("models/crop_rf_final.pkl", "rb") as f:
    model = pickle.load(f)

with open("models/scaler.pkl", "rb") as f:
    scaler = pickle.load(f)

with open("models/label_encoder.pkl", "rb") as f:
    le = pickle.load(f)

# ----------------------------------------------------
# INPUT SECTION
# ----------------------------------------------------
st.subheader(tr("enter_soil_data"))

col1, col2, col3 = st.columns(3)

with col1:
    N = st.number_input(tr("nitrogen"), min_value=0, max_value=140, value=50)
    temperature = st.number_input(tr("temperature"), min_value=5.0, max_value=55.0, value=25.0)

with col2:
    P = st.number_input(tr("phosphorus"), min_value=0, max_value=145, value=50)
    humidity = st.number_input(tr("humidity"), min_value=10.0, max_value=100.0, value=70.0)

with col3:
    K = st.number_input(tr("potassium"), min_value=0, max_value=200, value=50)
    ph = st.number_input(tr("ph_level"), min_value=3.5, max_value=10.0, value=6.5)
    rainfall = st.number_input(tr("rainfall"), min_value=10.0, max_value=500.0, value=100.0)

# ----------------------------------------------------
# PREDICT
# ----------------------------------------------------
if st.button(tr("recommend_btn"), use_container_width=True):

    arr = np.array([[N, P, K, temperature, humidity, ph, rainfall]])
    scaled = scaler.transform(arr)

    pred = model.predict(scaled)[0]
    crop_eng = le.inverse_transform([pred])[0].lower()

    # Hindi translation if available
    crop_final = T.get("crop_classes", {}).get(crop_eng, crop_eng)

    st.success(f"{tr('recommended_crop')}: **{crop_final.upper()}**")
