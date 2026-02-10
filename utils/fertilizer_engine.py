import streamlit as st
from engine.final_router import generate_fertilizer_recommendation
from utils.language import get_text
from utils.theme import load_theme
from utils.sidebar import render_sidebar
import os

# ----------------------------------------------------
# PAGE INIT
# ----------------------------------------------------
st.set_page_config(page_title="SmartFert", layout="wide")
load_theme()
render_sidebar()

# ----------------------------------------------------
# LANGUAGE
# ----------------------------------------------------
if "lang" not in st.session_state:
    st.session_state["lang"] = "English"

lang = st.session_state["lang"]
T = get_text(lang)
tr = lambda k: T.get(k, k)

# expose language to engine
os.LANG_FERT = lang

# ----------------------------------------------------
# HEADER
# ----------------------------------------------------
st.markdown(f"""
<div class="header-box">
    <h2 style="color:white;margin:0">{tr("fert_title")}</h2>
</div>
""", unsafe_allow_html=True)

st.write(tr("fert_sub"))

# ----------------------------------------------------
# TABS
# ----------------------------------------------------
npk_tab, stcr_tab = st.tabs([tr("npk_tab"), tr("stcr_tab")])

# ====================================================
# ===================== NPK MODE =====================
# ====================================================
with npk_tab:
    st.subheader(tr("npk_header"))

    # ----------------- STATE / CROP / SEASON -----------------
    sel_state = st.text_input(tr("select_state"), "")
    sel_crop = st.text_input(tr("select_crop"), "")
    sel_season = st.selectbox(tr("select_season"), ["Kharif", "Rabi", "Zaid", "Any"])

    # ----------------- SOIL INPUT -----------------
    st.markdown(f"### {tr('soil_test_details')}")
    c1, c2, c3 = st.columns(3)

    with c1:
        sn = st.number_input(tr("soil_sn"), min_value=0.0, value=0.0)
        oc = st.number_input(tr("soil_oc"), min_value=0.0, value=0.5)
        zn = st.number_input(tr("soil_zn"), min_value=0.0, value=0.0)

    with c2:
        sp = st.number_input(tr("soil_sp"), min_value=0.0, value=0.0)
        ec = st.number_input(tr("soil_ec"), min_value=0.0, value=0.0)
        fe = st.number_input(tr("soil_fe"), min_value=0.0, value=0.0)

    with c3:
        sk = st.number_input(tr("soil_sk"), min_value=0.0, value=0.0)
        ph = st.number_input(tr("soil_ph"), min_value=0.0, value=7.0)
        s_val = st.number_input(tr("soil_s"), min_value=0.0, value=0.0)

    prev_crop = st.text_input(tr("prev_crop"), "")

    # ----------------- ORGANIC -----------------
    st.markdown(f"### {tr('organic_inputs')}")
    organic_src = st.text_input(tr("organic_type"), "")
    organic_qty = st.number_input(tr("organic_qty"), min_value=0.0, value=0.0)

    # ----------------- ROUNDING -----------------
    st.markdown(f"### {tr('output_settings')}")
    rounding = st.selectbox(tr("rounding_mode"), ["exact", "field", "bag"])

    # ----------------- BUTTON -----------------
    if st.button(tr("btn_generate")):

        res = generate_fertilizer_recommendation(
            state=sel_state,
            crop=sel_crop,
            season=sel_season,
            soil={
                "SN": sn, "SP": sp, "SK": sk,
                "pH": ph, "EC": ec, "OC": oc,
                "Zn": zn, "Fe": fe, "S": s_val,
                "Soil_Type": "Any",
                "Condition": "Any",
                "Previous_Crop": prev_crop
            },
            organic_type=organic_src,
            organic_qty_kg=organic_qty,
            mode="NPK",
            tr=tr
        )

        if res["status"] != "success":
            st.error(res["error"])
            st.stop()

        st.success(tr("success_generated"))

        # ----------------- FINAL NUTRIENTS -----------------
        st.markdown(f"## {tr('final_nutrients')}")
        st.json(res["nutrients_required_kg_ha"])

        # ----------------- FINAL FERTILIZERS -----------------
        st.markdown(f"## {tr('final_fertilizers')}")
        st.json(res["fertilizers_recommended_kg_ha"])

        # ----------------- MICRONUTRIENTS -----------------
        st.markdown(f"## {tr('micronutrients')}")
        if not res["micronutrients"]:
            st.info(tr("no_micro_detected"))
        else:
            st.json(res["micronutrients"])

        # ----------------- ADVISORIES -----------------
        st.markdown(f"## {tr('expert_advisories')}")
        for adv in res["advisories"]:
            st.markdown(f"• {adv}")

        # ----------------- ✅ FULL AUDIT -----------------
        with st.expander("🔍 Show How It Works (Full Steps)"):
            for step in res["steps"]:
                st.json(step)


# ====================================================
# ===================== STCR MODE ====================
# ====================================================
with stcr_tab:
    st.subheader(tr("stcr_header"))

    sel_state = st.text_input(tr("select_state"), key="st_state")
    sel_crop = st.text_input(tr("select_crop"), key="st_crop")
    sel_season = st.selectbox(tr("select_season"), ["Kharif", "Rabi", "Zaid", "Any"], key="st_season")

    st.markdown(f"### {tr('soil_test_details')}")
    sn2 = st.number_input(tr("soil_sn"), min_value=0.0, value=0.0, key="sn2")
    sp2 = st.number_input(tr("soil_sp"), min_value=0.0, value=0.0, key="sp2")
    sk2 = st.number_input(tr("soil_sk"), min_value=0.0, value=0.0, key="sk2")
    ph2 = st.number_input(tr("soil_ph"), min_value=0.0, value=7.0, key="ph2")

    target = st.number_input(tr("target_yield"), min_value=0.0, value=10.0)

    if st.button(tr("btn_stcr_calc")):

        res = generate_fertilizer_recommendation(
            state=sel_state,
            crop=sel_crop,
            season=sel_season,
            soil={
                "SN": sn2, "SP": sp2, "SK": sk2,
                "pH": ph2,
                "Soil_Type": "Any",
                "Condition": "Any"
            },
            organic_type="",
            organic_qty_kg=0,
            target_yield=target,
            mode="STCR",
            tr=tr
        )

        if res["status"] != "success":
            st.error(res["error"])
            st.stop()

        st.success(tr("success_calculated"))

        st.markdown(f"### {tr('target_dose')}")
        st.json(res["nutrients_required_kg_ha"])

        st.markdown(f"## {tr('final_fertilizers')}")
        st.json(res["fertilizers_recommended_kg_ha"])

        st.markdown(f"## {tr('expert_advisories')}")
        for adv in res["advisories"]:
            st.markdown(f"• {adv}")

        # ✅ FULL AUDIT
        with st.expander("🔍 Show How It Works (Full Steps)"):
            for step in res["steps"]:
                st.json(step)
