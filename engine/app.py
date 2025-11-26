# ============================================================
# SmartFert UI — 2025 Production Edition (v21 — FLOAT SAFE)
# Fully aligned with:
#   - STCR Engine v22-R3
#   - Unique Streamlit keys
#   - Float-safe numeric inputs everywhere
#   - Organic Rules JSON
#   - Master Router
# ============================================================

import streamlit as st

from data_loader import load_master_dataset
from final_router import generate_fertilizer_recommendation
from bag_rounder import apply_rounding


# ---------------------------------------------------------
# Load MASTER once
# ---------------------------------------------------------
MASTER = load_master_dataset()
DATA = MASTER["data"]


# ---------------------------------------------------------
# Dynamic Organic Dropdown
# ---------------------------------------------------------
def get_dynamic_organic_sources():
    org = MASTER["organic_rules"]["organic_inputs"]
    manure = [m["name"] for m in org["manure"]]
    cakes  = [m["name"] for m in org["oilseed_cakes"]]
    return ["None"] + manure + cakes

ORGANIC_OPTIONS = get_dynamic_organic_sources()


# ---------------------------------------------------------
# Soil Type Extractor
# ---------------------------------------------------------
def get_soil_types(state, crop):
    entry = DATA[state][crop]
    types = set()

    for row in entry.get("npk", []):
        if row.get("Soil_Type"):
            types.add(row["Soil_Type"].lower())

    for row in entry.get("stcr", []):
        if row.get("Soil_Type"):
            types.add(row["Soil_Type"].lower())

    return sorted(types) or ["standard"]


# ---------------------------------------------------------
# Precompute states
# ---------------------------------------------------------
NPK_STATE_CROPS = {}
STCR_STATE_CROPS = {}

for state, crops in DATA.items():
    for crop, entry in crops.items():
        if entry.get("npk_available"):
            NPK_STATE_CROPS.setdefault(state, []).append(crop)
        if entry.get("stcr_available"):
            STCR_STATE_CROPS.setdefault(state, []).append(crop)

NPK_STATES = sorted(NPK_STATE_CROPS.keys())
STCR_STATES = sorted(STCR_STATE_CROPS.keys())


# ---------------------------------------------------------
# Season Extractor
# ---------------------------------------------------------
def get_available_seasons_for_npk(state, crop):
    npk_list = DATA[state][crop].get("npk", [])
    s = {row.get("Season", "Any") for row in npk_list}
    ordered = [x for x in ["Kharif", "Rabi", "Zaid", "Perennial", "Any"] if x in s]
    return ordered or ["Any"]


# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(page_title="SmartFert — Fertilizer Engine", layout="centered")
st.title("SmartFert — ICAR-grade Fertilizer Recommendation Engine")

tab_npk, tab_stcr = st.tabs(["🔹 NPK Mode", "🔸 STCR Mode"])


# =========================================================
# 🔹 NPK MODE — CLEAN + FLOAT SAFE
# =========================================================
with tab_npk:

    st.subheader("NPK Mode — Standard Recommendations")

    if not NPK_STATES:
        st.error("No NPK states available.")
    else:
        state_npk = st.selectbox("Select State", NPK_STATES, key="npk_state")
        crop_npk  = st.selectbox("Select Crop", sorted(NPK_STATE_CROPS[state_npk]), key="npk_crop")

        season_options = get_available_seasons_for_npk(state_npk, crop_npk)
        season_selected = st.selectbox("Season", season_options, key="npk_season")

        st.markdown("### Optional Soil Test Values (Float Safe)")

        soil_npk = {
            "SN": st.number_input("Available Nitrogen (SN)", min_value=0.0, step=0.1, key="npk_sn"),
            "SP": st.number_input("Available Phosphorus (SP)", min_value=0.0, step=0.1, key="npk_sp"),
            "SK": st.number_input("Available Potassium (SK)", min_value=0.0, step=0.1, key="npk_sk"),
            "Zn": st.number_input("Zinc (ppm)", min_value=0.0, step=0.1, key="npk_zn"),
            "Fe": st.number_input("Iron (ppm)", min_value=0.0, step=0.1, key="npk_fe"),
            "S":  st.number_input("Sulphur (ppm)", min_value=0.0, step=0.1, key="npk_s"),
            "pH": st.number_input("Soil pH", min_value=0.0, step=0.01, key="npk_ph"),
            "EC": st.number_input("EC (dS/m)", min_value=0.0, step=0.01, key="npk_ec"),
            "OC": st.number_input("Organic Carbon (%)", min_value=0.0, step=0.01, key="npk_oc"),
        }

        st.markdown("### Organic Inputs")
        organic_type_npk = st.selectbox("Organic Source", ORGANIC_OPTIONS, key="npk_org_type")
        organic_qty_npk  = st.number_input("Organic applied (kg/ha)", min_value=0.0, step=10.0, key="npk_org_qty")

        rounding_mode_npk = st.selectbox(
            "Rounding Mode",
            ["Exact", "Field (nearest 5 kg)", "Bag (25–50 kg packs)"],
            key="npk_round"
        )

        if st.button("Generate NPK Recommendation", key="npk_btn"):

            result = generate_fertilizer_recommendation(
                state=state_npk,
                crop=crop_npk,
                season=season_selected,
                soil=soil_npk,
                organic_type=organic_type_npk,
                organic_qty_kg=organic_qty_npk,
                target_yield=None,
                mode="NPK",
                master=MASTER
            )

            if "error" in result:
                st.error(result["error"])
            else:
                st.success("NPK Recommendation Generated")

                st.json({"Final NPK": result["final_npk"]})
                st.json({"Organic Contribution": result["organic_used"]})
                st.json({"Micronutrients": result["micronutrients"]})
                st.json({"Advisories": result["advisories"]})

                fert_rounded = apply_rounding(
                    result["fertilizer_recommendation"], rounding_mode_npk.lower()
                )
                st.json({"Fertilizer Requirement": fert_rounded})
                st.json({"Raw NPK": result["raw_npk"]})


# =========================================================
# 🔸 STCR MODE — FULL FLOAT-SAFE + ALIGNED WITH R3
# =========================================================
with tab_stcr:

    st.subheader("STCR Mode — Target Yield Based Recommendation")

    if not STCR_STATES:
        st.error("No STCR states available.")
    else:
        state_stcr = st.selectbox("Select State", STCR_STATES, key="stcr_state")
        crop_stcr  = st.selectbox("Select Crop", sorted(STCR_STATE_CROPS[state_stcr]), key="stcr_crop")

        soil_types = get_soil_types(state_stcr, crop_stcr)
        soil_type_selected = st.selectbox("Soil Type", soil_types, key="stcr_soil_type")

        st.markdown("### Mandatory Soil Test Values (Float Safe)")
        SN = st.number_input("Available N (SN)", min_value=0.0, step=0.1, key="stcr_sn")
        SP = st.number_input("Available P (SP)", min_value=0.0, step=0.1, key="stcr_sp")
        SK = st.number_input("Available K (SK)", min_value=0.0, step=0.1, key="stcr_sk")

        st.markdown("### Optional Organic Soil Values")
        ON = st.number_input("Organic N (ON)", min_value=0.0, step=0.1, key="stcr_on")
        OP = st.number_input("Organic P (OP)", min_value=0.0, step=0.1, key="stcr_op")
        OK = st.number_input("Organic K (OK)", min_value=0.0, step=0.1, key="stcr_ok")

        st.markdown("### Optional Soil Properties (Float Safe)")
        soil_stcr = {
            "SN": SN,
            "SP": SP,
            "SK": SK,
            "ON": ON,
            "OP": OP,
            "OK": OK,
            "Soil_Type": soil_type_selected,

            "pH": st.number_input("Soil pH", min_value=0.0, step=0.01, key="stcr_ph"),
            "EC": st.number_input("EC (dS/m)", min_value=0.0, step=0.01, key="stcr_ec"),
            "OC": st.number_input("Organic Carbon (%)", min_value=0.0, step=0.01, key="stcr_oc"),

            "Zn": st.number_input("Zinc (ppm)", min_value=0.0, step=0.1, key="stcr_zn"),
            "Fe": st.number_input("Iron (ppm)", min_value=0.0, step=0.1, key="stcr_fe"),
            "S":  st.number_input("Sulphur (ppm)", min_value=0.0, step=0.1, key="stcr_s"),
        }

        target_yield = st.number_input("Target Yield (q/ha)", min_value=0.0, step=0.1, key="stcr_t")

        st.markdown("### Organic Inputs")
        organic_type_stcr = st.selectbox("Organic Source", ORGANIC_OPTIONS, key="stcr_org_type")
        organic_qty_stcr  = st.number_input("Organic applied (kg/ha)", min_value=0.0, step=10.0, key="stcr_org_qty")

        rounding_mode_stcr = st.selectbox(
            "Rounding Mode",
            ["Exact", "Field (nearest 5 kg)", "Bag (25–50 kg packs)"],
            key="stcr_round"
        )

        if st.button("Generate STCR Recommendation", key="stcr_btn"):

            result = generate_fertilizer_recommendation(
                state=state_stcr,
                crop=crop_stcr,
                season="Any",
                soil=soil_stcr,
                organic_type=organic_type_stcr,
                organic_qty_kg=organic_qty_stcr,
                target_yield=target_yield,
                mode="STCR",
                master=MASTER
            )

            if "error" in result:
                st.error(result["error"])
            else:
                st.success("STCR Recommendation Generated")

                st.json({"Final NPK": result["final_npk"]})
                st.json({"Organic Contribution": result["organic_used"]})
                st.json({"Micronutrients": result["micronutrients"]})
                st.json({"Advisories": result["advisories"]})

                fert_rounded = apply_rounding(
                    result["fertilizer_recommendation"], rounding_mode_stcr.lower()
                )
                st.json({"Fertilizer Requirement": fert_rounded})
                st.json({"Raw NPK": result["raw_npk"]})
