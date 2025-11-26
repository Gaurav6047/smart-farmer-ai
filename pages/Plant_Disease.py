import streamlit as st
from PIL import Image
import numpy as np
import tensorflow as tf
import pandas as pd
import base64
from io import BytesIO

# ====================================================
# MUST BE FIRST
# ====================================================
st.set_page_config(layout="wide")

from utils.theme import load_theme
from utils.sidebar import render_sidebar
from utils.language import get_text
from utils.result_box import show_result
from utils.loading import fancy_loader


# ====================================================
# THEME + SIDEBAR (restores global lang)
# ====================================================
load_theme()
render_sidebar()


# ====================================================
# LANGUAGE SYSTEM (sidebar already sets session_state)
# ====================================================
# AFTER render_sidebar()
lang = st.session_state.get("lang", "English")
T = get_text(lang)
tr = lambda k: T.get(k, k)



# ====================================================
# ROUTER CLEANUP
# ====================================================
if not st.session_state.get("from_router", False):
    st.session_state.processed_image = None
else:
    st.session_state.from_router = False


# ====================================================
# RESTORE ROUTER IMAGE
# ====================================================
uploaded_img = None
if st.session_state.get("processed_image"):
    try:
        decoded = base64.b64decode(st.session_state["processed_image"])
        uploaded_img = Image.open(BytesIO(decoded)).convert("RGB")
    except:
        uploaded_img = None


# ====================================================
# HEADER
# ====================================================
st.markdown(f"""
<div class="header-box">
    <h2 style='margin:0;color:white;'>{tr("plant_disease")}</h2>
    <p style='margin:0;color:white;'>{tr("plant_disease_sub")}</p>
</div>
""", unsafe_allow_html=True)


# ====================================================
# LOAD MODEL
# ====================================================
@st.cache_resource
def load_plant_disease_model():
    df = pd.read_csv("models/Plant Village Disease-class_dict.csv")
    class_map = {int(i): c for i, c in zip(df["class_index"], df["class"])}

    inter = tf.lite.Interpreter(model_path="models/plant_desease.tflite")
    inter.allocate_tensors()

    inp = inter.get_input_details()[0]["index"]
    out = inter.get_output_details()[0]["index"]
    size = (224, 224)

    return inter, inp, out, size, class_map


inter, inp_idx, out_idx, IMG_SIZE, CLASS_MAP = load_plant_disease_model()


# ====================================================
# SAFE IMAGE LOADER
# ====================================================
def safe_load_image(file):
    try:
        return Image.open(file).convert("RGB")
    except:
        st.error(tr("invalid_img"))
        return None


# ====================================================
# PREDICTION
# ====================================================
def predict(img):
    img = img.resize(IMG_SIZE)
    arr = np.array(img, dtype=np.float32) / 255.0
    arr = arr[np.newaxis, ...]

    inter.set_tensor(inp_idx, arr)
    inter.invoke()

    pred = inter.get_tensor(out_idx)[0]
    idx = int(np.argmax(pred))
    return CLASS_MAP[idx], float(pred[idx])


# ====================================================
# INPUT SOURCES
# ====================================================
file = st.file_uploader(tr("upload"), type=["jpg","jpeg","png"])
cam  = st.camera_input(tr("capture"))

img = (
    uploaded_img
    if uploaded_img else
    (Image.open(cam).convert("RGB") if cam else None)
)

if not img and file:
    img = safe_load_image(file)


# ====================================================
# UI + OUTPUT
# ====================================================
if img:
    st.image(img, use_container_width=True)

    if st.button(tr("analyze"), use_container_width=True):

        fancy_loader(tr("processing_image"))

        label, conf = predict(img)

        translated = T.get("disease_classes", {}).get(label, label)

        show_result(translated, conf, T)

else:
    st.info(tr("no_image"))
