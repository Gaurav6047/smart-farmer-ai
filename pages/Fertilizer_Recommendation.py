import streamlit as st

# ENGINE IMPORTS
from engine.data_loader import load_master_dataset
from engine.final_router import generate_fertilizer_recommendation
from engine.bag_rounder import apply_rounding
from engine.fertilizer_convert import convert_to_fertilizers
from engine.advisory_engine import generate_advisories

# UTILS
try:
    from utils.theme import load_theme
    from utils.sidebar import render_sidebar
    from utils.language import get_text
except:
    def load_theme(): pass
    def render_sidebar(): pass
    def get_text(x): return {}

# =====================================================================
# INIT
# =====================================================================
load_theme()
render_sidebar()
# AFTER render_sidebar()
lang = st.session_state.get("lang", "English")
T = get_text(lang)
tr = lambda k: T.get(k, k)


# ============= UNIQUE KEY FIX =============
def make_key(prefix, *parts):
    safe = "_".join(str(x).replace(" ", "_") for x in parts)
    return f"{prefix}_{safe}"

# =====================================================================
# LOAD DATA
# =====================================================================
@st.cache_resource
def get_data():
    return load_master_dataset()

MASTER = get_data()
DATA = MASTER["data"]

# =====================================================================
# DROPDOWN HELPERS
# =====================================================================
def get_seasons(state, crop):
    if state not in DATA or crop not in DATA[state]:
        return ["Any"]
    lst = DATA[state][crop].get("npk", [])
    s = {r.get("Season", "Any") for r in lst}
    order = ["Kharif", "Rabi", "Zaid", "Perennial", "Any"]
    return [x for x in order if x in s] or ["Any"]

def get_soil_types(state, crop):
    entry = DATA.get(state, {}).get(crop, {})
    s = {r.get("Soil_Type") for r in entry.get("stcr", []) if r.get("Soil_Type")}
    s |= {r.get("Soil_Type") for r in entry.get("npk", []) if r.get("Soil_Type")}
    return sorted(s) or ["Standard"]

# State → crop maps
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

# Organic
ORG = MASTER["organic_rules"]["organic_inputs"]
ORG_OPTIONS = ["None"] + [x["name"] for x in ORG["manure"]] + [x["name"] for x in ORG["oilseed_cakes"]]

# =====================================================================
# HEADER
# =====================================================================
st.markdown(f"""
<div class='header-box'>
  <h2 style='color:white;margin:0'>{tr("fert_title")}</h2>
  <p style='color:white;margin:0'>{tr("fert_sub")}</p>
</div>
""", unsafe_allow_html=True)

tab_npk, tab_stcr = st.tabs([tr("npk_tab"), tr("stcr_tab")])

# =====================================================================
# ============================ NPK MODE ================================
# =====================================================================
with tab_npk:

    st.subheader(tr("npk_header"))
    if not NPK_STATES:
        st.error(tr("npk_no_states"))
    else:
        col1, col2 = st.columns(2)

        state = col1.selectbox(tr("select_state"), NPK_STATES, key="npk_state")
        crop = col2.selectbox(tr("select_crop"),
                              sorted(NPK_STATE_CROPS[state]),
                              key=make_key("npk_crop", state))

        seasons = get_seasons(state, crop)
        season = st.selectbox(tr("select_season"),
                              seasons,
                              key=make_key("npk_season", state, crop))

        st.info(tr("npk_enter_soil"))

        # Soil Inputs
        with st.expander(tr("soil_test_details"), True):
            c1, c2, c3 = st.columns(3)

            SN = c1.number_input(tr("soil_sn"), 0.0, key=make_key("npk", state, crop, "SN"))
            SP = c2.number_input(tr("soil_sp"), 0.0, key=make_key("npk", state, crop, "SP"))
            SK = c3.number_input(tr("soil_sk"), 0.0, key=make_key("npk", state, crop, "SK"))

            pH = c1.number_input(tr("soil_ph"), 0.0, 14.0, 7.0, 0.1,
                                 key=make_key("npk", state, crop, "pH"))
            OC = c2.number_input(tr("soil_oc"), 0.0, step=0.01, key=make_key("npk", state, crop, "OC"))
            EC = c3.number_input(tr("soil_ec"), 0.0, step=0.01, key=make_key("npk", state, crop, "EC"))

            Zn = c1.number_input(tr("soil_zn"), 0.0, key=make_key("npk", state, crop, "Zn"))
            Fe = c2.number_input(tr("soil_fe"), 0.0, key=make_key("npk", state, crop, "Fe"))
            S  = c3.number_input(tr("soil_s"), 0.0, key=make_key("npk", state, crop, "S"))

        soil = {"SN": SN, "SP": SP, "SK": SK,
                "pH": pH, "OC": OC, "EC": EC,
                "Zn": Zn, "Fe": Fe, "S": S}

        # Organic
        st.markdown(f"#### {tr('organic_inputs')}")
        o1, o2 = st.columns([2, 1])
        org_type = o1.selectbox(tr("organic_type"), ORG_OPTIONS,
                                key=make_key("npk_org", state, crop))
        org_qty  = o2.number_input(tr("organic_qty"), 0.0,
                                   key=make_key("npk_org_qty", state, crop))

        # Rounding
        round_choices = [
            ("exact", tr("round_exact")),
            ("field", tr("round_field")),
            ("bag", tr("round_bag"))
        ]
        round_label = st.selectbox(tr("rounding_mode"),
                                   [x[1] for x in round_choices],
                                   key=make_key("npk_round", state, crop))
        round_mode = [x[0] for x in round_choices if x[1] == round_label][0]

        # Button
        if st.button(tr("btn_generate"), key=make_key("npk_btn", state, crop)):
            result = generate_fertilizer_recommendation(
                state=state, crop=crop, season=season,
                soil=soil, organic_type=org_type, organic_qty_kg=org_qty,
                target_yield=None, mode="NPK", master=MASTER
            )

            if "error" in result:
                st.error(f"{tr('error_prefix')}: {result['error']}")
            else:
                st.success(tr("success_generated"))

                raw = result["nutrients_required_kg_ha"]
                fert_raw = convert_to_fertilizers(raw)
                fert_final = apply_rounding(fert_raw, round_mode)

                L, R = st.columns(2)

                # LEFT
                with L:
                    st.markdown("### " + tr("final_nutrients"))
                    st.write(f"{tr('n_val')}: {raw['N']} kg")
                    st.write(f"{tr('p_val')}: {raw['P2O5']} kg")
                    st.write(f"{tr('k_val')}: {raw['K2O']} kg")

                    st.markdown("### " + tr("organic_credit"))
                    oc = result["organic_credit_kg"]
                    if oc["N"] > 0:
                        st.info(
                            f"{tr('manure_saved')} "
                            f"N {oc['N']:.1f}, P {oc['P2O5']:.1f}, K {oc['K2O']:.1f}"
                        )
                    else:
                        st.write(tr("no_organic_credit"))

                # RIGHT
                with R:
                    st.markdown("### " + tr("fert_recommend"))
                    st.dataframe(fert_final, use_container_width=True)

                    st.markdown("### " + tr("micronutrients"))
                    if result["micronutrients"]:
                        for k, v in result["micronutrients"].items():
                            st.warning(
                                f"{k}: {', '.join([f'{x}: {y}kg' for x,y in v.items()])}"
                            )
                    else:
                        st.write(tr("no_micro_detected"))

                # Advisories
                st.markdown("---")
                st.markdown("### " + tr("expert_advisories"))
                advs = generate_advisories(
                    soil, result.get("micronutrients", {}),
                    "NPK", MASTER, tr
                )
                for a in advs:
                    st.write("• " + a)

# =====================================================================
# ============================ STCR MODE ===============================
# =====================================================================
with tab_stcr:

    st.subheader(tr("stcr_header"))
    if not STCR_STATES:
        st.error(tr("stcr_no_states"))
    else:
        c1, c2 = st.columns(2)
        state = c1.selectbox(tr("select_state"), STCR_STATES, key="stcr_state")
        crop  = c2.selectbox(tr("select_crop"),
                             sorted(STCR_STATE_CROPS[state]),
                             key=make_key("stcr_crop", state))

        soil_types = get_soil_types(state, crop)
        soil_type = st.selectbox(tr("select_soil_type"),
                                 soil_types,
                                 key=make_key("stcr_soiltype", state, crop))

        # Target Yield
        TY1, TY2 = st.columns([1, 2])
        Tyield = TY1.number_input(
            tr("target_yield"), 0.0, step=1.0, value=40.0,
            key=make_key("stcr_ty", state, crop))
        TY2.caption(tr("target_yield_note"))

        st.info(tr("stcr_mandatory"))

        with st.expander(tr("soil_test_values"), True):
            c1, c2, c3 = st.columns(3)

            SN = c1.number_input(tr("soil_sn"), 0.0,
                                 key=make_key("stcr", state, crop, "SN"))
            SP = c2.number_input(tr("soil_sp"), 0.0,
                                 key=make_key("stcr", state, crop, "SP"))
            SK = c3.number_input(tr("soil_sk"), 0.0,
                                 key=make_key("stcr", state, crop, "SK"))

            pH = c1.number_input(tr("soil_ph_opt"), 0.0, 14.0, 7.0, 0.1,
                                 key=make_key("stcr", state, crop, "pH"))
            OC = c2.number_input(tr("soil_oc"), 0.0, step=0.01,
                                 key=make_key("stcr", state, crop, "OC"))

            Zn = c1.number_input(tr("soil_zn"), 0.0,
                                 key=make_key("stcr", state, crop, "Zn"))
            Fe = c2.number_input(tr("soil_fe"), 0.0,
                                 key=make_key("stcr", state, crop, "Fe"))
            S  = c3.number_input(tr("soil_s"), 0.0,
                                 key=make_key("stcr", state, crop, "S"))

        soil = {"SN": SN, "SP": SP, "SK": SK,
                "Soil_Type": soil_type, "pH": pH, "OC": OC,
                "Zn": Zn, "Fe": Fe, "S": S}

        # Organic
        st.markdown("#### " + tr("organic_inputs"))
        o1, o2 = st.columns([2,1])
        org_type = o1.selectbox(tr("organic_type"), ORG_OPTIONS,
                                key=make_key("stcr_org", state, crop))
        org_qty  = o2.number_input(tr("organic_qty"), 0.0,
                                   key=make_key("stcr_org_qty", state, crop))

        # Rounding
        round_label = st.selectbox(tr("rounding_mode"),
                                   [x[1] for x in round_choices],
                                   key=make_key("stcr_round", state, crop))
        round_mode = [x[0] for x in round_choices if x[1] == round_label][0]

        # BUTTON
        if st.button(tr("btn_stcr_calc"), key=make_key("stcr_btn", state, crop)):

            if Tyield <= 0:
                st.error(tr("err_target_zero"))
            elif SN == 0 and SP == 0 and SK == 0:
                st.error(tr("err_stcr_empty"))
            else:
                result = generate_fertilizer_recommendation(
                    state=state, crop=crop, season="Any",
                    soil=soil, organic_type=org_type, organic_qty_kg=org_qty,
                    target_yield=Tyield, mode="STCR", master=MASTER
                )

                if "error" in result:
                    st.error(result["error"])
                else:
                    st.success(tr("success_calculated"))

                    raw = result["nutrients_required_kg_ha"]
                    fert_raw = convert_to_fertilizers(raw)
                    fert_final = apply_rounding(fert_raw, round_mode)

                    L, R = st.columns(2)

                    with L:
                        st.markdown("### " + tr("target_dose"))
                        st.write(f"{tr('n_val')}: {raw['N']} kg")
                        st.write(f"{tr('p_val')}: {raw['P2O5']} kg")
                        st.write(f"{tr('k_val')}: {raw['K2O']} kg")

                        st.markdown("### " + tr("organic_credit"))
                        oc = result["organic_credit_kg"]
                        st.write(
                            f"{tr('manure_supplied')} "
                            f"N-{oc['N']:.1f}, P-{oc['P2O5']:.1f}, K-{oc['K2O']:.1f}"
                        )

                    with R:
                        st.markdown("### " + tr("fert_recommend"))
                        st.dataframe(fert_final, use_container_width=True)

                        if result["micronutrients"]:
                            st.markdown("### " + tr("micronutrients"))
                            for k, v in result["micronutrients"].items():
                                st.warning(
                                    f"{k}: {', '.join([f'{x}: {y}kg' for x,y in v.items()])}"
                                )

                    # Advisories
                    st.markdown("---")
                    st.markdown("### " + tr("advisory_title"))
                    advs = generate_advisories(
                        soil, result.get("micronutrients", {}),
                        "STCR", MASTER, tr
                    )
                    for a in advs:
                        st.write("• " + a)
