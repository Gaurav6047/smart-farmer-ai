import streamlit as st
import pandas as pd # Graph ke liye

# =====================================================================
# 1. ENGINE & UTILS SETUP
# =====================================================================
try:
    from data.smart_fertilizer_engine import SmartFertilizerEngine
except ImportError:
    st.error(" Critical Error: Could not import 'SmartFertilizerEngine'. Check folder structure.")
    st.stop()

try:
    from utils.theme import load_theme
    from utils.sidebar import render_sidebar
    from utils.language import get_text
except ImportError:
    def load_theme(): pass
    def render_sidebar(): pass
    def get_text(x): return {}

load_theme()
render_sidebar()

# =====================================================================
# 2. INITIALIZE ENGINE
# =====================================================================
@st.cache_resource
def get_engine():
    eng = SmartFertilizerEngine()
    try:
        eng.load_all_datasets()
        return eng
    except Exception as e:
        st.error(f" Engine Data Loading Error: {e}")
        return None

engine = get_engine()
if not engine: st.stop()

# =====================================================================
# 3. HELPER FUNCTIONS
# =====================================================================
lang = st.session_state.get("lang", "English")
T = get_text(lang)

def tr(key, default_text):
    """
    Robust translation helper.
    """
    if not T: return default_text
    val = T.get(key)
    return val if val else default_text

def make_key(prefix, *parts):
    safe = "_".join(str(x).replace(" ", "_") for x in parts)
    return f"{prefix}_{safe}"

def render_optional_input(col, label, key, default=0.0, step=1.0, help_txt=None):
    val = col.number_input(label, min_value=0.0, value=default, step=step, key=key, help=help_txt)
    return val if val > 0 else None

# Formatter for Title Case (andhra_pradesh -> Andhra Pradesh)
def format_name(name):
    return name.replace("_", " ").title()

# =====================================================================
# 4. HEADER UI
# =====================================================================
st.markdown(f"""
<div class='header-box' style='padding:20px; border-radius:10px; background-color:#2E7D32; color:white; margin-bottom:20px'>
  <h2 style='margin:0; font-size: 24px;'> {tr("fert_title", "Smart Fertilizer Recommendation")}</h2>
  <p style='margin:0; opacity:0.9; font-size: 16px;'>{tr("fert_sub", "ICAR-Grade Precision Nutrient Management")}</p>
</div>
""", unsafe_allow_html=True)

tab_npk, tab_stcr = st.tabs([
    tr("npk_tab", " NPK Recommendation"), 
    tr("stcr_tab", " STCR Recommendation")
])

# =====================================================================
# 5. SHARED RESULT DISPLAY FUNCTION (Fully Translated)
# =====================================================================
def display_results(result):
    st.success(f" {tr('success_generated', 'Recommendation Generated Successfully')}")

    # A. FINAL DOSE & GRAPH
    dose = result["final_fertilizer_dose"]
    
    # Visual Layout: Metrics vs Graph
    c1, c2 = st.columns([1, 1.5])
    
    with c1:
        st.markdown(f"###  {tr('final_dose_title', 'Final Dose')}")
        st.metric(tr("nitrogen", "Nitrogen (N)"), f"{dose.get('N', 0)} kg/ha")
        st.metric(tr("phosphorus", "Phosphorus (P)"), f"{dose.get('P2O5', 0)} kg/ha")
        st.metric(tr("potassium", "Potassium (K)"), f"{dose.get('K2O', 0)} kg/ha")
    
    with c2:
        # Simple Bar Chart for Visual Comparison
        chart_data = pd.DataFrame({
            "Nutrient": ["N", "P", "K"],
            "Kg/Ha": [dose.get('N', 0), dose.get('P2O5', 0), dose.get('K2O', 0)]
        })
        st.markdown(f"###  {tr('nutrient_balance', 'Nutrient Balance')}")
        st.bar_chart(chart_data.set_index("Nutrient"), color="#4CAF50")

    # B. BAG CALCULATION CARDS
    bags = result["fertilizer_bags"]
    st.markdown("---")
    st.subheader(f" {tr('required_bags', 'Required Fertilizer Bags (50kg)')}")
    
    b1, b2, b3 = st.columns(3)
    def bag_card(col, name, count, color):
        col.markdown(f"""
        <div style="background-color:{color}; padding:10px; border-radius:8px; text-align:center; border:1px solid #ddd;">
            <h2 style="margin:0; color:#333;">{count}</h2>
            <p style="margin:0; font-weight:bold; color:#555;">{name}</p>
        </div>
        """, unsafe_allow_html=True)
    
    bag_card(b1, tr("bag_urea", "Urea"), bags.get('Urea_bags', 0), "#E3F2FD") # Blueish
    bag_card(b2, tr("bag_dap", "DAP"), bags.get('DAP_bags', 0), "#FFF9C4")  # Yellowish
    bag_card(b3, tr("bag_mop", "MOP"), bags.get('MOP_bags', 0), "#FFEBEE")  # Reddish

    # C. COST ESTIMATOR (Authentic: Editable Prices)
    st.markdown("---")
    st.subheader(f" {tr('cost_title', 'Estimated Cost Calculator')}")
    st.caption(tr("cost_note", "Default prices are approximate Govt rates. Edit them as per your local market."))
    
    ec1, ec2, ec3, ec4 = st.columns(4)
    u_price = ec1.number_input(tr("price_urea", "Urea Price/Bag"), value=266.0, step=10.0)
    d_price = ec2.number_input(tr("price_dap", "DAP Price/Bag"), value=1350.0, step=50.0)
    m_price = ec3.number_input(tr("price_mop", "MOP Price/Bag"), value=1700.0, step=50.0)
    
    total_cost = (bags.get('Urea_bags', 0) * u_price) + \
                 (bags.get('DAP_bags', 0) * d_price) + \
                 (bags.get('MOP_bags', 0) * m_price)
    
    ec4.metric(tr("total_cost", "Total Approx Cost"), f"₹ {total_cost:,.0f}")

   # D. AUTHENTIC SCHEDULE (Agronomy Logic - TRANSLATED)
    st.markdown("---")
    st.subheader(f" {tr('schedule_title', 'Application Schedule')}")
    
    n_val = dose.get('N', 0)
    # Get translated labels
    lbl_urea = tr("sched_urea", "Urea")
    lbl_pk = tr("sched_full_pk", "Full P & K Dose")

    if n_val > 0:
        # LOGIC: N is split (50% Basal, 25% Veg, 25% Flower). P & K are 100% Basal.
        s1, s2, s3 = st.columns(3)
        with s1:
            st.info(f"**{tr('stage_basal', '1. Basal (At Sowing)')}**\n- {lbl_urea}: {(n_val * 0.5):.1f} kg N\n- {lbl_pk}")
        with s2:
            st.info(f"**{tr('stage_veg', '2. Vegetative Stage')}**\n- {lbl_urea}: {(n_val * 0.25):.1f} kg N")
        with s3:
            st.info(f"**{tr('stage_flowering', '3. Flowering Stage')}**\n- {lbl_urea}: {(n_val * 0.25):.1f} kg N")
    else:
        st.info(tr("schedule_no_n", "No Nitrogen application recommended."))
    # E. ADVISORIES & SOIL HEALTH

    
    # Soil Health Meter (Only if data exists)
    if result.get("soil_fertility_status"):
        with st.expander(f" {tr('soil_health_view', 'View Soil Health Status')}"):
            status = result["soil_fertility_status"]
            sc1, sc2, sc3 = st.columns(3)
            def get_color(val): return "🔴" if val=="Low" else "🟢" if val=="High" else "🟡"
            
            # Using Translated Values from language.py
            if "N_Status" in status: sc1.write(f"**N:** {get_color(status['N_Status'])} {tr(status['N_Status'], status['N_Status'])}")
            if "P_Status" in status: sc2.write(f"**P:** {get_color(status['P_Status'])} {tr(status['P_Status'], status['P_Status'])}")
            if "K_Status" in status: sc3.write(f"**K:** {get_color(status['K_Status'])} {tr(status['K_Status'], status['K_Status'])}")

    # Text Advisories
   # E. ADVISORIES (Smart Translation Logic)
    st.markdown("---")
    st.subheader(f" {tr('expert_advisories', 'Expert Advisories')}")

    if result["advisory"]:
        for adv in result["advisory"]:
            final_text = adv  # Default English

            # --- SMART TRANSLATION FOR DYNAMIC STRINGS ---
            # यह चेक करता है कि अगर हिंदी है, तो इंग्लिश शब्दों को हिंदी से बदल दे
            if lang == "Hindi":
                if "High Salinity" in adv:
                    final_text = adv.replace("High Salinity", "उच्च लवणता") \
                                    .replace("Expect", "अनुमानित") \
                                    .replace("yield reduction", "उपज में कमी") \
                                    .replace("Salt tolerant varieties recommended", "लवण सहनशील किस्में अनुशंसित")
                elif "Acidic Soil" in adv:
                    final_text = adv.replace("Acidic Soil Detected", "अम्लीय मिट्टी पाई गई") \
                                    .replace("Apply Lime", "चूना डालें")
                elif "Alkaline Soil" in adv:
                    final_text = adv.replace("Alkaline Soil Detected", "क्षारीय मिट्टी पाई गई") \
                                    .replace("Apply Gypsum", "जिप्सम डालें")
                elif "Legume Rotation" in adv:
                    final_text = adv.replace("Legume Rotation Credit", "दलहनी फसल क्रेडिट") \
                                    .replace("Reduced Nitrogen dose by", "नाइट्रोजन खुराक कम की गई:")
                elif "Drip Fertigation" in adv:
                    final_text = adv.replace("Drip Fertigation", "ड्रिप फर्टिगेशन") \
                                    .replace("Nutrient dose reduced to", "पोषक तत्व खुराक घटकर") \
                                    .replace("due to high efficiency", "उच्च दक्षता के कारण")
                elif "Micronutrient Deficiency" in adv:
                    final_text = adv.replace("Micronutrient Deficiency", "सूक्ष्म पोषक तत्व की कमी") \
                                    .replace("Apply", "डालें")
                else:
                    # अगर कोई नंबर वाला मैसेज नहीं है, तो डिक्शनरी चेक करें
                    final_text = tr(adv, adv)
            
            # --- DISPLAY WITH COLORS ---
            if "Critical" in adv or "Salinity" in adv or "Acidic" in adv or "Alkaline" in adv:
                st.error(f" {final_text}")
            elif "Deficiency" in adv:
                st.warning(f" {final_text}")
            else:
                st.info(f" {final_text}")
    else:
        st.write(tr("no_specific_adv", "No specific advisories."))

    # F. HIDDEN DEBUG INFO
    with st.expander(f" {tr('debug_view', 'Debug / Calculation Trace')}"):
        st.json(result)

# =====================================================================
# 6. TAB 1: NPK MODE UI
# =====================================================================
with tab_npk:
    st.subheader(tr("npk_header", "Regional Standard (NPK)"))
    st.caption(tr("adv_npk_mode", "Based on government fixed standards for your region."))

    available_states = engine.get_available_states("npk")
    
    if not available_states:
        st.error(tr("npk_no_states", "No NPK Data Available."))
    else:
        c1, c2 = st.columns(2)
        state = c1.selectbox(tr("select_state", "Select State"), available_states, format_func=format_name, key="npk_state")
        
        available_crops = engine.get_available_crops(state, "npk")
        crop = c2.selectbox(tr("select_crop", "Select Crop"), available_crops, format_func=format_name, key=make_key("npk_crop", state))

        config = engine.get_valid_seasons_and_soils(state, crop, "npk")
        c3, c4 = st.columns(2)
        season = c3.selectbox(tr("select_season", "Select Season"), config.get("seasons", ["Any"]), key=make_key("npk_season", state, crop))
        soil_type_input = c4.selectbox(tr("select_soil_type", "Soil Type"), config.get("soils", ["Standard"]), key=make_key("npk_soil", state, crop))

        st.info(tr("npk_note", " Soil Test is **optional** for NPK mode."))
        
        soil_payload = {}
        with st.expander(tr("add_soil_test", "➕ Add Soil Test Report (Optional)"), expanded=False):
            sc1, sc2, sc3 = st.columns(3)
            sn = render_optional_input(sc1, tr("soil_sn", "Nitrogen (N)"), make_key("npk_n", state, crop))
            sp = render_optional_input(sc2, tr("soil_sp", "Phosphorus (P)"), make_key("npk_p", state, crop))
            sk = render_optional_input(sc3, tr("soil_sk", "Potassium (K)"), make_key("npk_k", state, crop))
            
            ph = sc1.number_input(tr("soil_ph", "pH"), 0.0, 14.0, 7.0, 0.1, key=make_key("npk_ph", state, crop))
            if ph != 7.0: soil_payload["pH"] = ph
            
            ec = render_optional_input(sc2, tr("soil_ec", "EC (dS/m)"), make_key("npk_ec", state, crop), 0.0, 0.1)
            if ec: soil_payload["EC"] = ec
            
            oc = render_optional_input(sc3, tr("soil_oc", "Org Carbon (%)"), make_key("npk_oc", state, crop), 0.0, 0.01)
            if oc: soil_payload["OC"] = oc

            if sn: soil_payload["SN"] = sn
            if sp: soil_payload["SP"] = sp
            if sk: soil_payload["SK"] = sk

        st.markdown(f"#### {tr('organic_title', ' Organic Fertilizers (Optional)')}")
        organic_applied = {}
        with st.expander(tr("select_organic", "Select Manures / Compost"), expanded=False):
            oc1, oc2 = st.columns(2)
            manures = engine.data_organic.get("organic_inputs", {}).get("manure", [])
            cakes = engine.data_organic.get("organic_inputs", {}).get("oilseed_cakes", [])
            with oc1:
                for m in manures:
                    val = st.number_input(f"{m['name']} (kg/ha)", 0.0, step=100.0, key=make_key("npk_org", m['name']))
                    if val > 0: organic_applied[m['name']] = val
            with oc2:
                for c in cakes:
                    val = st.number_input(f"{c['name']} (kg/ha)", 0.0, step=50.0, key=make_key("npk_cake", c['name']))
                    if val > 0: organic_applied[c['name']] = val

        if st.button(tr("btn_npk", " Generate NPK Recommendation"), type="primary", use_container_width=True, key="npk_btn_main"):
            payload = {
                "state": state, "crop": crop, "mode": "npk",
                "season": season, "soil_type": soil_type_input,
                "soil_test": soil_payload, "organic_applied": organic_applied,
                "irrigation_type": "Flood", "previous_crop": "None"
            }
            with st.spinner(tr("processing", "Analyzing...")):
                result = engine.generate_final_recommendation(payload)
            display_results(result)

# =====================================================================
# 7. TAB 2: STCR MODE UI
# =====================================================================
with tab_stcr:
    st.subheader(tr("stcr_header", "STCR Recommendation (Target Yield)"))
    st.caption(tr("adv_stcr_mode", "Calculates precise dose based on Soil Test + Target Yield."))

    available_states_stcr = engine.get_available_states("stcr")
    
    if not available_states_stcr:
        st.error(tr("stcr_no_states", "No STCR Data Available."))
    else:
        sc1, sc2 = st.columns(2)
        state_s = sc1.selectbox(tr("select_state", "Select State"), available_states_stcr, format_func=format_name, key="stcr_state")
        available_crops_s = engine.get_available_crops(state_s, "stcr")
        crop_s = sc2.selectbox(tr("select_crop", "Select Crop"), available_crops_s, format_func=format_name, key=make_key("stcr_crop", state_s))

        config_s = engine.get_valid_seasons_and_soils(state_s, crop_s, "stcr")
        sc3, sc4 = st.columns(2)
        soil_type_s = sc3.selectbox(tr("select_soil_type", "Soil Type"), config_s.get("soils", ["Standard"]), key="stcr_soil")
        target_yield = sc4.number_input(tr("target_yield", "Target Yield (q/ha)"), min_value=1.0, value=40.0, step=1.0, key="stcr_yield")

        st.warning(tr("stcr_warn", " Soil Test Values (N, P, K) are **REQUIRED** for STCR."))
        
        soil_payload_stcr = {}
        with st.expander(tr("soil_test_req", " Soil Test Data (Mandatory)"), expanded=True):
            r1, r2, r3 = st.columns(3)
            sn_s = r1.number_input(f"{tr('soil_sn', 'Available N')} *", 0.0, step=10.0, key="stcr_n")
            sp_s = r2.number_input(f"{tr('soil_sp', 'Available P')} *", 0.0, step=1.0, key="stcr_p")
            sk_s = r3.number_input(f"{tr('soil_sk', 'Available K')} *", 0.0, step=10.0, key="stcr_k")

            if sn_s > 0: soil_payload_stcr["SN"] = sn_s
            if sp_s > 0: soil_payload_stcr["SP"] = sp_s
            if sk_s > 0: soil_payload_stcr["SK"] = sk_s

            st.markdown("**Optional Parameters**")
            r4, r5, r6 = st.columns(3)
            ph_s = r4.number_input(tr("soil_ph", "pH"), 0.0, 14.0, 7.0, 0.1, key="stcr_ph")
            if ph_s != 7.0: soil_payload_stcr["pH"] = ph_s
            
            ec_s = render_optional_input(r5, tr("soil_ec", "EC (dS/m)"), "stcr_ec", 0.0, 0.1)
            if ec_s: soil_payload_stcr["EC"] = ec_s

            oc_s = render_optional_input(r6, tr("soil_oc", "Org Carbon (%)"), "stcr_oc", 0.0, 0.01)
            if oc_s: soil_payload_stcr["OC"] = oc_s

        st.markdown(f"#### {tr('organic_title', ' Organic Fertilizers (Optional)')}")
        organic_applied_stcr = {}
        with st.expander(tr("select_organic", "Select Organic Inputs"), expanded=False):
            osc1, osc2 = st.columns(2)
            manures_s = engine.data_organic.get("organic_inputs", {}).get("manure", [])
            cakes_s = engine.data_organic.get("organic_inputs", {}).get("oilseed_cakes", [])
            with osc1:
                for m in manures_s:
                    val = st.number_input(f"{m['name']} (kg/ha)", 0.0, step=100.0, key=make_key("stcr_org", m['name']))
                    if val > 0: organic_applied_stcr[m['name']] = val
            with osc2:
                for c in cakes_s:
                    val = st.number_input(f"{c['name']} (kg/ha)", 0.0, step=50.0, key=make_key("stcr_cake", c['name']))
                    if val > 0: organic_applied_stcr[c['name']] = val

        if st.button(tr("btn_stcr", " Calculate Precision Dose"), type="primary", use_container_width=True, key="stcr_btn_main"):
            if "SN" not in soil_payload_stcr or "SP" not in soil_payload_stcr or "SK" not in soil_payload_stcr:
                st.error(tr("err_stcr_empty", " Cannot Calculate: Missing Soil Values (N, P, K)."))
            else:
                payload_stcr = {
                    "state": state_s, "crop": crop_s, "mode": "stcr",
                    "season": "Any", "soil_type": soil_type_s,
                    "target_yield": target_yield, "soil_test": soil_payload_stcr,
                    "organic_applied": organic_applied_stcr,
                    "irrigation_type": "Flood", "previous_crop": "None"
                }
                with st.spinner(tr("processing", "Solving STCR Equations...")):
                    result_stcr = engine.generate_final_recommendation(payload_stcr)
                display_results(result_stcr)