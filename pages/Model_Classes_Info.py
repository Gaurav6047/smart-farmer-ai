import streamlit as st
import pandas as pd
import json

from utils.language import get_text
from utils.theme import load_theme
from utils.sidebar import render_sidebar


# ----------------------------------------------------
# PAGE INIT
# ----------------------------------------------------
st.set_page_config(page_title="Model & Engine Info", layout="wide")
load_theme()
render_sidebar()


# ----------------------------------------------------
# LANGUAGE
# ----------------------------------------------------
# AFTER render_sidebar()
lang = st.session_state.get("lang", "English")
T = get_text(lang)
tr = lambda k: T.get(k, k)



# 🔥 TRUE TRANSLATION FUNCTION (REAL DICT ACCESS)
def tr_class(label, dict_key):
    """
    Fetch class translation using deep dictionary from EN/HIN.
    """
    # Hindi → check primary dict
    if lang == "Hindi":
        sub = T._primary.get(dict_key)
        if isinstance(sub, dict):
            return sub.get(label, label)

    # English → no translation needed
    if lang == "English":
        return label

    # If Hindi missing → fallback English dict
    sub_f = T._fallback.get(dict_key)
    if isinstance(sub_f, dict):
        return sub_f.get(label, label)

    return label


# ----------------------------------------------------
# HEADER
# ----------------------------------------------------
st.markdown(f"""
<div class="header-box">
    <h2 style='margin:0;color:white;'>{tr("model_info")}</h2>
</div>
""", unsafe_allow_html=True)


# ----------------------------------------------------
# DESCRIPTION — HTML ENABLED
# ----------------------------------------------------
st.markdown(tr("model_info_desc"), unsafe_allow_html=True)


# ----------------------------------------------------
# SAFE LOADERS
# ----------------------------------------------------
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


# ----------------------------------------------------
# LOAD FILES
# ----------------------------------------------------
plant_df = safe_load_csv("models/Plant Village Disease-class_dict.csv")
pest_df = safe_load_csv("models/pest_classes.csv")
fruit_classes = safe_load_json("models/fruit_class_names.json")


# ----------------------------------------------------
# TABS
# ----------------------------------------------------
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    tr("plant_disease"),
    tr("pest_detection"),
    tr("fruit_classification"),
    tr("fert_engine"),
    tr("irrig_engine"),
    tr("crop_reco_engine")
])


# ======================================================
# TAB 1 — PLANT DISEASE
# ======================================================
with tab1:
    st.subheader(tr("plant_disease"))

    if plant_df is None:
        st.error(tr("err_plant_csv"))
    else:
        df = plant_df.rename(columns={"class": "class_en"})
        df["class_hi"] = df["class_en"].apply(lambda x: tr_class(x, "disease_classes"))

        if lang == "Hindi":
            st.dataframe(df[["class_en", "class_hi"]], hide_index=True)
        else:
            st.dataframe(df[["class_en"]], hide_index=True)

        st.info(tr("hint_leaf_upload"))


# ======================================================
# TAB 2 — PEST DETECTION
# ======================================================
with tab2:
    st.subheader(tr("pest_detection"))

    if pest_df is None:
        st.error(tr("err_pest_csv"))
    else:
        df = pest_df.rename(columns={"class_name": "class_en"})
        df["class_hi"] = df["class_en"].apply(lambda x: tr_class(x, "pest_classes"))

        if lang == "Hindi":
            st.dataframe(df[["class_en", "class_hi"]], hide_index=True)
        else:
            st.dataframe(df[["class_en"]], hide_index=True)

        st.warning(tr("hint_pest_close"))


# ======================================================
# TAB 3 — FRUIT CLASSIFICATION
# ======================================================
with tab3:
    st.subheader(tr("fruit_classification"))

    if fruit_classes is None:
        st.error(tr("err_fruit_json"))
    else:
        df = pd.DataFrame({"class_en": fruit_classes})
        df["class_hi"] = df["class_en"].apply(lambda x: tr_class(x, "fruit_classes"))

        if lang == "Hindi":
            st.dataframe(df[["class_en", "class_hi"]], hide_index=True)
        else:
            st.dataframe(df[["class_en"]], hide_index=True)

        st.info(tr("hint_fruit_center"))


# ======================================================
# TAB 4 — FERTILIZER ENGINE
# ======================================================
with tab4:
    st.subheader(tr("fert_engine"))
    st.markdown(tr("fert_engine_desc"), unsafe_allow_html=True)


# ======================================================
# TAB 5 — IRRIGATION ENGINE
# ======================================================
with tab5:
    st.subheader(tr("irrig_engine"))
    st.markdown(tr("irrig_engine_desc"), unsafe_allow_html=True)


# ======================================================
# TAB 6 — CROP RECO ENGINE
# ======================================================
with tab6:
    st.subheader(tr("crop_reco_engine"))
    st.markdown(tr("crop_reco_desc"), unsafe_allow_html=True)
