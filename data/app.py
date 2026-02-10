import streamlit as st
import json
import pandas as pd
from smart_fertilizer_engine import SmartFertilizerEngine

# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="Smart Fertilizer Recommendation System",
    page_icon="🌱",
    layout="wide"
)

# ---------------------------------------------------------
# ENGINE INITIALIZATION
# ---------------------------------------------------------
@st.cache_resource
def get_engine():
    """
    Initializes the engine and loads datasets only once.
    """
    eng = SmartFertilizerEngine()
    try:
        eng.load_all_datasets()
        return eng
    except Exception as e:
        st.error(f"CRITICAL ERROR: Failed to initialize engine. {str(e)}")
        st.stop()
        return None

engine = get_engine()

# ---------------------------------------------------------
# TITLE & HEADER
# ---------------------------------------------------------
st.title("🌱 Smart Fertilizer Recommendation System")
st.markdown("### ICAR-Grade Precision Nutrient Management")
st.markdown("---")

# ---------------------------------------------------------
# SIDEBAR: CONFIGURATION & INPUTS
# ---------------------------------------------------------
st.sidebar.header("⚙️ Configuration")

# 1. Mode Selection (Moved to Sidebar for dynamic control)
mode_options = ["npk", "stcr"]
selected_mode = st.sidebar.selectbox("Select Mode", mode_options, format_func=lambda x: x.upper())

st.sidebar.markdown("---")

# 2. Dynamic Soil Test Inputs
st.sidebar.header("🧪 Soil Test Report")

soil_test_inputs = {}

def render_optional_input(label, key, default=0.0, step=1.0, help_text=""):
    """Helper to render input and return None if 0/empty"""
    val = st.number_input(label, min_value=0.0, value=default, step=step, key=key, help=help_text)
    return val if val > 0 else None

# --- Logic for NPK Mode (Everything is Optional) ---
if selected_mode == "npk":
    st.sidebar.info("ℹ️ **NPK Mode:** Recommendations are based on Region, Crop & Season. Soil test data is **optional** but helps in generating a Health Card.")
    
    with st.sidebar.expander("➕ Add Soil Test Data (Optional)", expanded=False):
        st.markdown("**Macronutrients**")
        sn = render_optional_input("Available Nitrogen (N) [kg/ha]", "npk_N", 0.0, 10.0)
        sp = render_optional_input("Available Phosphorus (P) [kg/ha]", "npk_P", 0.0, 1.0)
        sk = render_optional_input("Available Potassium (K) [kg/ha]", "npk_K", 0.0, 10.0)
        
        if sn is not None: soil_test_inputs["SN"] = sn
        if sp is not None: soil_test_inputs["SP"] = sp
        if sk is not None: soil_test_inputs["SK"] = sk

        st.markdown("**Physico-chemical**")
        ph = st.number_input("pH", min_value=0.0, max_value=14.0, value=0.0, step=0.1, help="Leave 0 if unknown")
        if ph > 0: soil_test_inputs["pH"] = ph
        
        ec = render_optional_input("EC (dS/m)", "npk_EC", 0.0, 0.1)
        if ec is not None: soil_test_inputs["EC"] = ec
        
        oc = render_optional_input("Organic Carbon (%)", "npk_OC", 0.0, 0.01)
        if oc is not None: soil_test_inputs["OC"] = oc

# --- Logic for STCR Mode (N, P, K are Required) ---
elif selected_mode == "stcr":
    st.sidebar.info("ℹ️ **STCR Mode:** Soil Test values are **REQUIRED** for calculation.")
    
    st.sidebar.markdown("### 🔴 Required Inputs")
    sn = st.sidebar.number_input("Available Nitrogen (SN) [kg/ha]", min_value=0.0, value=0.0, step=10.0)
    sp = st.sidebar.number_input("Available Phosphorus (SP) [kg/ha]", min_value=0.0, value=0.0, step=1.0)
    sk = st.sidebar.number_input("Available Potassium (SK) [kg/ha]", min_value=0.0, value=0.0, step=10.0)
    
    # Validation for STCR
    if sn > 0: soil_test_inputs["SN"] = sn
    if sp > 0: soil_test_inputs["SP"] = sp
    if sk > 0: soil_test_inputs["SK"] = sk
    
    st.sidebar.markdown("### 🟢 Optional Inputs")
    with st.sidebar.expander("Physico-chemical (pH, EC, OC)"):
        ph = st.number_input("pH", min_value=0.0, max_value=14.0, value=0.0, step=0.1, key="stcr_ph")
        if ph > 0: soil_test_inputs["pH"] = ph
        
        ec = render_optional_input("EC (dS/m)", "stcr_ec", 0.0, 0.1)
        if ec is not None: soil_test_inputs["EC"] = ec
        
        oc = render_optional_input("Organic Carbon (%)", "stcr_oc", 0.0, 0.01)
        if oc is not None: soil_test_inputs["OC"] = oc

# --- Micronutrients (Always Optional for both) ---
with st.sidebar.expander("🧪 Micronutrients (Optional)", expanded=False):
    st.caption("Leave as 0 if not tested.")
    zn = render_optional_input("Zinc (Zn)", "micro_zn", 0.0, 0.1)
    if zn: soil_test_inputs["Zn"] = zn
    
    fe = render_optional_input("Iron (Fe)", "micro_fe", 0.0, 0.1)
    if fe: soil_test_inputs["Fe"] = fe
    
    mn = render_optional_input("Manganese (Mn)", "micro_mn", 0.0, 0.1)
    if mn: soil_test_inputs["Mn"] = mn
    
    cu = render_optional_input("Copper (Cu)", "micro_cu", 0.0, 0.1)
    if cu: soil_test_inputs["Cu"] = cu
    
    b = render_optional_input("Boron (B)", "micro_b", 0.0, 0.1)
    if b: soil_test_inputs["B"] = b
    
    s = render_optional_input("Sulphur (S)", "micro_s", 0.0, 1.0)
    if s: soil_test_inputs["S"] = s


# ---------------------------------------------------------
# MAIN PANEL: CROP & LOCATION CONFIGURATION
# ---------------------------------------------------------
col1, col2, col3 = st.columns(3)

# Dynamic Data Loading based on Sidebar Mode
available_states = engine.get_available_states(selected_mode)

with col1:
    st.subheader("1️⃣ Location")
    selected_state = st.selectbox("Select State", available_states)

with col2:
    st.subheader("2️⃣ Crop Details")
    # Dynamic Crop Selection
    if selected_state:
        available_crops = engine.get_available_crops(selected_state, selected_mode)
        selected_crop = st.selectbox("Select Crop", available_crops)
    else:
        selected_crop = None
        st.warning("Select a State first.")

    # Dynamic Season & Soil
    season_opts, soil_opts = [], []
    if selected_state and selected_crop:
        valid_config = engine.get_valid_seasons_and_soils(selected_state, selected_crop, selected_mode)
        season_opts = valid_config.get("seasons", [])
        soil_opts = valid_config.get("soils", [])
    
    selected_season = st.selectbox("Season", season_opts)
    selected_soil = st.selectbox("Soil Type", soil_opts)

with col3:
    st.subheader("3️⃣ Farm Practices")
    irrigation_type = st.selectbox("Irrigation Type", ["Flood", "Drip"])
    previous_crop = st.selectbox("Previous Crop", ["None", "Legume", "Cereal", "Oilseed"])
    
    target_yield = 0.0
    # Target Yield is ONLY relevant/required for STCR
    if selected_mode == "stcr":
        st.markdown("**Target Yield (Required)**")
        target_yield = st.number_input("Enter Target Yield (q/ha or t/ha)", min_value=0.0, value=40.0, step=1.0)
        
        # Yield Guidance Logic
        if selected_crop:
            c_lower = selected_crop.lower()
            if any(x in c_lower for x in ['rice', 'wheat', 'maize', 'bajra', 'jowar', 'cereal']):
                st.caption("ℹ️ Typical Cereal Yield: **40-60 q/ha**")
            elif any(x in c_lower for x in ['cotton']):
                st.caption("ℹ️ Typical Cotton Yield: **20-35 q/ha**")
            elif any(x in c_lower for x in ['sugarcane']):
                st.caption("ℹ️ Typical Sugarcane Yield: **800-1200 q/ha**")
            elif any(x in c_lower for x in ['vegetable', 'tomato', 'potato']):
                st.caption("ℹ️ Typical Vegetable Yield: **200-400 q/ha**")
    else:
        st.info("Target Yield not required for standard NPK mode.")

# ---------------------------------------------------------
# ORGANIC INPUTS SECTION
# ---------------------------------------------------------
st.markdown("### 🍂 Organic Fertilizers Applied (Optional)")
st.caption("Enter quantity applied (kg/ha). Engine will automatically subtract nutrient credit.")

organic_applied = {}
if engine.data_organic:
    try:
        organic_expander = st.expander("Select Organic Inputs", expanded=False)
        with organic_expander:
            org_col1, org_col2 = st.columns(2)
            
            # Manure Inputs
            with org_col1:
                st.markdown("**Manures**")
                manures = engine.data_organic.get("organic_inputs", {}).get("manure", [])
                for m in manures:
                    val = st.number_input(f"{m['name']} (kg/ha)", min_value=0.0, step=100.0, key=f"org_{m['name']}")
                    if val > 0:
                        organic_applied[m['name']] = val
            
            # Oilcake Inputs
            with org_col2:
                st.markdown("**Oilseed Cakes**")
                cakes = engine.data_organic.get("organic_inputs", {}).get("oilseed_cakes", [])
                for c in cakes:
                    val = st.number_input(f"{c['name']} (kg/ha)", min_value=0.0, step=50.0, key=f"org_{c['name']}")
                    if val > 0:
                        organic_applied[c['name']] = val
    except Exception as e:
        st.error(f"Error loading organic inputs: {e}")

# ---------------------------------------------------------
# GENERATION LOGIC
# ---------------------------------------------------------
st.markdown("---")
generate_btn = st.button("🚀 Generate Fertilizer Recommendation", type="primary", use_container_width=True)

if generate_btn:
    # Basic Validation
    if not selected_state or not selected_crop:
        st.error("Please select a valid State and Crop configuration.")
    # STCR Specific Validation
    elif selected_mode == "stcr" and target_yield <= 0:
        st.error("⚠️ **Error:** Target Yield is required for STCR mode.")
    elif selected_mode == "stcr" and ("SN" not in soil_test_inputs or "SP" not in soil_test_inputs or "SK" not in soil_test_inputs):
        st.error("⚠️ **Error:** Soil Nitrogen (SN), Phosphorus (SP), and Potassium (SK) are REQUIRED for STCR calculations.")
    else:
        # Build Payload
        payload = {
            "state": selected_state,
            "crop": selected_crop,
            "mode": selected_mode,
            "season": selected_season,
            "soil_type": selected_soil,
            "target_yield": target_yield,
            "irrigation_type": irrigation_type,
            "previous_crop": previous_crop,
            "soil_test": soil_test_inputs, # Contains only non-None values
            "organic_applied": organic_applied
        }

        try:
            # CALL ENGINE
            result = engine.generate_final_recommendation(payload)
            
            # -----------------------------------------------------
            # DISPLAY RESULTS
            # -----------------------------------------------------
            
            st.success("✅ Recommendation Generated Successfully")
            
            # Check for anomalies
            final_dose = result.get("final_fertilizer_dose", {})
            fertility_stats = result.get("soil_fertility_status", {})
            is_low_fertility = any(stat in ["Low", "Medium"] for stat in fertility_stats.values())
            is_zero_result = all(v == 0 for v in final_dose.values())

            # Warning if STCR gave 0 despite low fertility (usually means equation missing)
            if selected_mode == "stcr" and is_zero_result and target_yield > 0:
                 st.warning("⚠️ **Note:** The calculated dose is 0 kg/ha. This might happen if the STCR equation for this specific soil type/crop combo is unavailable, or if your soil fertility is already sufficient for the target yield.")

            # 1. Final Dose Metrics
            st.subheader("🎯 Final Fertilizer Dose (kg/ha)")
            res_col1, res_col2, res_col3 = st.columns(3)
            
            res_col1.metric("Nitrogen (N)", f"{final_dose.get('N', 0)} kg", delta_color="normal")
            res_col2.metric("Phosphorus (P₂O₅)", f"{final_dose.get('P2O5', 0)} kg", delta_color="normal")
            res_col3.metric("Potassium (K₂O)", f"{final_dose.get('K2O', 0)} kg", delta_color="normal")
            
            # 2. Fertilizer Bags
            st.markdown("---")
            st.subheader("🛍️ Estimated Fertilizer Bags (50kg)")
            st.caption("Based on standard grades: Urea (46% N), DAP (18-46-0), MOP (60% K2O)")
            
            bags = result.get("fertilizer_bags", {})
            bag_col1, bag_col2, bag_col3 = st.columns(3)
            
            bag_col1.metric("Urea Bags", f"{bags.get('Urea_bags', 0)}", help="Fulfils remaining Nitrogen")
            bag_col2.metric("DAP Bags", f"{bags.get('DAP_bags', 0)}", help="Fulfils Phosphorus + some Nitrogen")
            bag_col3.metric("MOP Bags", f"{bags.get('MOP_bags', 0)}", help="Fulfils Potassium")
            st.markdown("---")

            # 3. Analysis Columns
            ana_col1, ana_col2 = st.columns(2)
            
            with ana_col1:
                st.subheader("📉 Organic Credits Applied")
                credits = result.get("organic_credit_applied", {})
                if any(v > 0 for v in credits.values()):
                    credit_df = pd.DataFrame([credits])
                    st.dataframe(credit_df, hide_index=True)
                else:
                    st.info("No organic inputs applied.")

                if fertility_stats:
                    st.subheader("🧪 Soil Status")
                    st.json(fertility_stats)

            with ana_col2:
                st.subheader("⚙️ Special Adjustments")
                adjustments = result.get("special_adjustments", {})
                if adjustments:
                    st.json(adjustments)
                else:
                    st.info("No special adjustments triggered.")

                st.subheader("⚠️ Deficiency Report")
                defs = result.get("deficiency_report", {})
                def_only = {k: v for k, v in defs.items() if v == "Deficient"}
                if def_only:
                    st.error(f"Deficiencies Detected: {', '.join(def_only.keys())}")
                    st.dataframe(pd.DataFrame(list(def_only.items()), columns=["Nutrient", "Status"]), hide_index=True)
                else:
                    if not defs:
                        st.write("No soil test data for micronutrients provided.")
                    else:
                        st.success("No micronutrient deficiencies detected.")

            # 4. Advisory Section
            st.subheader("📢 Agronomic Advisory")
            advisories = result.get("advisory", [])
            if advisories:
                for line in advisories:
                    if "no chemical fertilizer is required" in line:
                         st.success(f"🌱 {line}")
                    else:
                        st.info(f"• {line}")
            else:
                st.write("No specific advisories.")

            # 5. Raw Output
            with st.expander("🔍 View Trace & Raw Output"):
                st.markdown("**Input Payload Sent to Engine:**")
                st.json(payload)
                
                if "calculation_trace" in result:
                    st.markdown("**Calculation Trace:**")
                    st.json(result["calculation_trace"])
                
                st.markdown("**Full Response JSON:**")
                st.json(result)

        except Exception as e:
            st.error(f"An error occurred during calculation: {str(e)}")
            st.exception(e)

# Footer
st.markdown("---")
st.caption("Powered by SmartFertilizerEngine v1.0 | ICAR-Grade Architecture")