import streamlit as st
import sys
import os

# Path for import
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from engine.recommender import FertilizerRecommender
from engine.auto_crop import AutoCropEngine

from utils.language import get_text
from utils.theme import load_theme


# Initialize engines
recommender = FertilizerRecommender()
auto_crop = AutoCropEngine()

# ---------------------------------------
# PAGE CONFIG
# ---------------------------------------
st.set_page_config(
    page_title="Smart Fertilizer Engine",
    page_icon="🧪",
    layout="wide"
)
# Load theme
load_theme()

# ---------------------------------------
# LANGUAGE
# ---------------------------------------
lang = st.sidebar.selectbox("Language / भाषा", ["English", "Hindi"])
T = get_text(lang)


# ---------------------------------------
# HEADER BOX (same style as disease page)
# ---------------------------------------
st.markdown(f"""
<div class="header-box">
    <h2 style='margin:0;color:white;'>{T['fert_header']}</h2>
    <p style='margin:0;color:white;'>{T['fert_subheader']}</p>
</div>
""", unsafe_allow_html=True)


# ---------------------------------------
# INPUT FORM
# ---------------------------------------
with st.form("fert_form"):

    col1, col2 = st.columns(2)

    # ------------------ Soil Inputs ------------------
    with col1:
        st.subheader(T["soil_report"])

        soil_n = st.number_input(T["nitrogen"], 0.0, 5000.0, 180.0)
        soil_p = st.number_input(T["phosphorus"], 0.0, 500.0, 20.0)
        soil_k = st.number_input(T["potassium"], 0.0, 1000.0, 150.0)

        c1, c2 = st.columns(2)
        with c1:
            soil_ph = st.number_input(T["soil_ph"], 0.0, 14.0, 7.0)
        with c2:
            soil_ec = st.number_input(T["soil_ec"], 0.0, 50.0, 0.5)

        with st.expander(T["micronutrients"]):
            soil_zn = st.number_input(T["zinc"], 0.0, 10.0, 0.0)
            soil_fe = st.number_input(T["iron"], 0.0, 50.0, 0.0)

    # ------------------ Crop Section ------------------
    with col2:
        st.subheader(T["crop_section"])

        states = [
            "Punjab","Haryana","UP","Bihar","MP","Rajasthan","Gujarat","Maharashtra",
            "Tamil Nadu","Karnataka","AP","Telangana","West Bengal","Odisha",
            "Chhattisgarh","Jharkhand","Assam","Kerala","Uttarakhand","Himachal Pradesh"
        ]

        seasons = ["Kharif", "Rabi", "Zaid"]

        state = st.selectbox(T["state"], states)
        season = st.selectbox(T["season"], seasons)

        # Auto-suggest crops
        suggested = auto_crop.suggest(state, season)
        crop_auto = st.selectbox(T["suggested_crops"], suggested)

        # Custom crop
        crop_custom = st.text_input(T["custom_crop"], "")
        final_crop = crop_custom.strip() if crop_custom.strip() else crop_auto

        # Method
        method = st.radio(T["method"], [T["method_standard"], T["method_stcr"]])

        stcr_key = None
        target_yield = None

        if method == T["method_stcr"]:
            target_yield = st.number_input(
                T["target_yield"], 1.0, 200.0, 40.0
            )

            stcr_key = st.selectbox(
                T["stcr_model"],
                [
                    "rice_alluvial", "rice_south", "wheat_alluvial",
                    "maize_inceptisol", "cotton_bt", "sorghum_vertisol",
                    "pearl_millet_aridisol", "groundnut_alfisol",
                    "soybean_vertisol", "sugarcane_coastal",
                    "tomato_hybrid", "potato_inceptisol",
                    "onion_inceptisol", "brinjal_hybrid",
                    "pumpkin_acidic"
                ]
            )

    # ------------------ Organic Inputs ------------------
    st.subheader(T["organic_inputs"])

    oc1, oc2, oc3 = st.columns(3)
    with oc1:
        fym = st.number_input(T["fym"], 0, 50000, 0)
    with oc2:
        vermi = st.number_input(T["vermi"], 0, 20000, 0)
    with oc3:
        prev_crop = st.selectbox(T["prev_crop"], ["Cereal", "Legume", "Fallow"])

    submit = st.form_submit_button(T["submit_fert"])


# ---------------------------------------
# PROCESSING LOGIC
# ---------------------------------------
if submit:

    soil_data = {
        "N": soil_n, "P": soil_p, "K": soil_k,
        "pH": soil_ph, "EC": soil_ec,
        "Zn": soil_zn, "Fe": soil_fe
    }

    organic_data = {
        "FYM": fym,
        "Vermicompost": vermi
    }

    meta_data = {
        "state": state,
        "season": season,
        "previous_crop_type": prev_crop,
        "stcr_equation_key": stcr_key
    }

    with st.spinner(T["processing"]):
        result = recommender.recommend(
            soil=soil_data,
            crop=final_crop,
            condition="Irrigated",
            target_yield=target_yield,
            organic_inputs=organic_data,
            meta=meta_data
        )

    if result.get("status") == "error":
        st.error(result["message"])
        st.stop()

    # -------------------- SUCCESS --------------------
    st.success(T["fertilizer_engine"])

    fert = result["commercial_fertilizer"]
    bags = fert["bags"]
    kg = fert["kg"]

    # -------------------- FERTILIZER BAGS --------------------
    st.subheader(T["fert_bags"])

    b1, b2, b3 = st.columns(3)
    with b1:
        st.metric("Urea (45 kg bag)", f"{bags['Urea']} 👜", f"{kg['Urea']} kg")
    with b2:
        st.metric("DAP (50 kg bag)", f"{bags['DAP']} 👜", f"{kg['DAP']} kg")
    with b3:
        st.metric("MOP (50 kg bag)", f"{bags['MOP']} 👜", f"{kg['MOP']} kg")

    # -------------------- ALERTS --------------------
    if result["alerts"]:
        st.warning(T["alert_title"])
        for a in result["alerts"]:
            st.write(f"- {a}")

    # -------------------- BREAKDOWN --------------------
    with st.expander(T["breakdown_title"]):

        bd = result["breakdown"]

        st.markdown(f"### {T['breakdown_table_title']}")

        table = {
            "Nutrient": ["N", "P₂O₅", "K₂O"],
            T["base_req"]: [
                bd["base_requirement_kg_ha"]["N"],
                bd["base_requirement_kg_ha"]["P2O5"],
                bd["base_requirement_kg_ha"]["K2O"],
            ],
            T["organic_deduct"]: [
                bd["organic_credits"]["N"],
                bd["organic_credits"]["P2O5"],
                bd["organic_credits"]["K2O"],
            ],
            T["final_req"]: [
                bd["final_elemental_req"]["N"],
                bd["final_elemental_req"]["P2O5"],
                bd["final_elemental_req"]["K2O"],
            ]
        }

        st.table(table)
        st.json(result)
