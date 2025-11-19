import streamlit as st
import numpy as np
import pickle
from utils.theme import load_theme
from utils.language import get_text

load_theme()

# --------------------------------------------------
# Language Selector
# --------------------------------------------------
lang = st.sidebar.selectbox("Language / भाषा", ["English", "Hindi"])
T = get_text(lang)

# --------------------------------------------------
# Header
# --------------------------------------------------
st.markdown(f"""
<div class="header-box">
    <h2 style='margin:0;color:white;'>{T["crop_recommendation"]}</h2>
    <p style='margin:0;color:white;'>AI-based smart crop suggestion using soil & climate data</p>
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Load Model, Scaler, Label Encoder
# --------------------------------------------------
with open("models/crop_rf_final.pkl", "rb") as f:
    model = pickle.load(f)

with open("models/scaler.pkl", "rb") as f:
    scaler = pickle.load(f)

with open("models/label_encoder.pkl", "rb") as f:
    le = pickle.load(f)


# --------------------------------------------------
# Input Sliders + Ranges
# --------------------------------------------------

st.subheader("🧪 Enter soil & climate values")

col1, col2, col3 = st.columns(3)

with col1:
    N = st.number_input("Nitrogen (0–140)", min_value=0, max_value=140, value=50)
    temperature = st.number_input("Temperature °C (10–45)", min_value=10.0, max_value=45.0, value=25.0)

with col2:
    P = st.number_input("Phosphorus (0–145)", min_value=0, max_value=145, value=50)
    humidity = st.number_input("Humidity % (10–100)", min_value=10.0, max_value=100.0, value=70.0)

with col3:
    K = st.number_input("Potassium (0–200)", min_value=0, max_value=200, value=50)
    ph = st.number_input("Soil pH (3.5–10)", min_value=3.5, max_value=10.0, value=6.5)
    rainfall = st.number_input("Rainfall (20–300 mm)", min_value=20.0, max_value=300.0, value=100.0)


# --------------------------------------------------
# Validate Inputs
# --------------------------------------------------
def validate_inputs():
    if not (0 <= N <= 140): return False
    if not (0 <= P <= 145): return False
    if not (0 <= K <= 200): return False
    if not (10 <= temperature <= 45): return False
    if not (10 <= humidity <= 100): return False
    if not (3.5 <= ph <= 10): return False
    if not (20 <= rainfall <= 300): return False
    return True


# --------------------------------------------------
# Predict
# --------------------------------------------------
if st.button("🌾 Recommend Crop", use_container_width=True):

    if not validate_inputs():
        st.error("⚠️ Invalid input values. Please verify soil ranges and try again.")
        st.stop()

    input_data = np.array([[N, P, K, temperature, humidity, ph, rainfall]])
    input_scaled = scaler.transform(input_data)
    pred = model.predict(input_scaled)[0]

    crop = le.inverse_transform([pred])[0]

    st.success(f"🌾 Recommended Crop: **{crop.upper()}**")
