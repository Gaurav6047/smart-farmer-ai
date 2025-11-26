import streamlit as st
import pandas as pd
from engines.fertilizer_engine import FertilizerEngine
from utils.language import get_text
from utils.theme import load_theme
from utils.sidebar import render_sidebar

# ----------------------------------------------------
# PAGE INIT
# ----------------------------------------------------
st.set_page_config(page_title="SmartFert", layout="wide")
load_theme()
render_sidebar()

# Language
if "lang" not in st.session_state:
    st.session_state["lang"] = "English"

lang = st.session_state["lang"]
T = get_text(lang)
tr = lambda k: T.get(k, k)

# expose language to engine (for advisory translation)
import os
os.LANG_FERT = lang

# Fertilizer engine instance
FE = FertilizerEngine()

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
# ---------------------- NPK MODE --------------------
# ====================================================
with npk_tab:
    st.subheader(tr("npk_header"))

    # --- State + Crop + Season ---
    if FE.rdf_df.empty:
        st.error(tr("npk_no_states"))
    else:
        states = sorted(FE.rdf_df["State"].dropna().unique())
        sel_state = st.selectbox(tr("select_state"), states)

        crops = sorted(FE.rdf_df[FE.rdf_df["State"] == sel_state]["Crop"].unique())
        sel_crop = st.selectbox(tr("select_crop"), crops)

        seasons = sorted(FE.rdf_df[FE.rdf_df["State"] == sel_state]["Season"].unique())
        sel_season = st.selectbox(tr("select_season"), seasons)

    # --- Soil Test Inputs ---
    st.markdown(f"### {tr('soil_test_details')}")

    col1, col2, col3 = st.columns(3)
    with col1:
        sn = st.number_input(tr("soil_sn"), min_value=0.0, value=0.0)
        oc = st.number_input(tr("soil_oc"), min_value=0.0, value=0.5)
        zn = st.number_input(tr("soil_zn"), min_value=0.0, value=0.0)
    with col2:
        sp = st.number_input(tr("soil_sp"), min_value=0.0, value=0.0)
        ec = st.number_input(tr("soil_ec"), min_value=0.0, value=0.0)
        fe = st.number_input(tr("soil_fe"), min_value=0.0, value=0.0)
    with col3:
        sk = st.number_input(tr("soil_sk"), min_value=0.0, value=0.0)
        ph = st.number_input(tr("soil_ph"), min_value=0.0, value=7.0)
        s_val = st.number_input(tr("soil_s"), min_value=0.0, value=0.0)

    # Micro dict
    micro = {
        "Zinc": zn,
        "Iron": fe,
        "Sulphur": s_val
    }

    # Organic Inputs
    st.markdown(f"### {tr('organic_inputs')}")
    oc_col, qty_col = st.columns(2)
    with oc_col:
        organic_src = st.selectbox(tr("organic_type"), ["None", "FYM", "Vermi", "Sheep Manure"])
    with qty_col:
        organic_qty = st.number_input(tr("organic_qty"), min_value=0.0, value=0.0)

    # Output settings
    st.markdown(f"### {tr('output_settings')}")
    rounding = st.selectbox(
        tr("rounding_mode"),
        [tr("round_exact"), tr("round_field"), tr("round_bag")]
    )

    if st.button(tr("btn_generate")):

        # ----------------- RDF Calculation -----------------
        rdf_res, err = FE.calculate_rdf(sel_crop, sn, sp, sk)

        if err:
            st.error(f"{tr('error_prefix')}: {err}")
        else:
            st.success(tr("success_generated"))

            # ----------------- Display Final Nutrients -----------------
            st.markdown(f"## {tr('final_nutrients')}")

            N_final = rdf_res["N"]
            P_final = rdf_res["P"]
            K_final = rdf_res["K"]

            st.write(f"**{tr('n_val')}:** {N_final} kg")
            st.write(f"**{tr('p_val')}:** {P_final} kg")
            st.write(f"**{tr('k_val')}:** {K_final} kg")

            # ----------------- Organic Credit -----------------
            st.markdown(f"### {tr('organic_credit')}")
            if organic_src != "None" and organic_qty > 0:
                st.info(f"{tr('manure_saved')} {organic_qty} kg")
            else:
                st.warning(tr("no_organic_credit"))

            # ----------------- Micronutrients -----------------
            st.markdown(f"## {tr('micronutrients')}")

            alerts = FE.check_rules(ph, ec, micro)

            # Micro display
            if zn < 0.5:
                st.write("Zinc: ZnSO4_kg: 25kg")
            if fe < 0.5:
                st.write("Iron: FeSO4_kg: 20kg")
            if s_val < 10:
                st.write("Boron: Borax_kg: 5kg")
                st.write("Sulphur: Gypsum_kg: 40kg")

            # ----------------- Advisories -----------------
            st.markdown(f"## {tr('expert_advisories')}")

            if not alerts:
                st.info(tr("no_micro_detected"))
            else:
                for head, msg in alerts:
                    st.markdown(f"• **{head}** — {msg}")

# ====================================================
# ---------------------- STCR MODE -------------------
# ====================================================
with stcr_tab:
    st.subheader(tr("stcr_header"))

    if not FE.stcr_data:
        st.error(tr("stcr_no_states"))
    else:

        st.write(tr("stcr_mandatory"))

        # soil inputs
        colA, colB, colC = st.columns(3)
        with colA:
            sn2 = st.number_input(tr("soil_sn"), min_value=0.0, value=0.0, key="sn2")
        with colB:
            sp2 = st.number_input(tr("soil_sp"), min_value=0.0, value=0.0, key="sp2")
        with colC:
            sk2 = st.number_input(tr("soil_sk"), min_value=0.0, value=0.0, key="sk2")

        target = st.number_input(tr("target_yield"), min_value=0.0, value=100.0)

        # equation_key dropdown
        crop_keys = sorted(FE.stcr_data.get("stcr_equations", {}).get("crops", {}).keys())
        equation_key = st.selectbox(tr("select_crop"), crop_keys)

        if st.button(tr("btn_stcr_calc")):

            if target <= 0:
                st.error(tr("err_target_zero"))
            elif sn2 == 0 and sp2 == 0 and sk2 == 0:
                st.error(tr("err_stcr_empty"))
            else:
                res, err = FE.calculate_stcr(equation_key, target, sn2, sp2, sk2)

                if err:
                    st.error(err)
                else:
                    st.success(tr("success_calculated"))

                    st.markdown(f"### {tr('target_dose')}")
                    st.write(f"**{tr('n_val')}:** {res['N']} kg")
                    st.write(f"**{tr('p_val')}:** {res['P']} kg")
                    st.write(f"**{tr('k_val')}:** {res['K']} kg")

                    st.markdown(f"### {tr('expert_advisories')}")
                    st.write(tr("adv_stcr_mode"))
