import streamlit as st
from utils.theme import load_theme
load_theme()

from PIL import Image
import numpy as np
import tensorflow as tf
import pandas as pd
from utils.language import get_text
from utils.result_box import show_result
import base64
from io import BytesIO
from utils.loading import fancy_loader


# ----------------------------------------------------
# CLEAN ROUTER STATE IF NECESSARY
# ----------------------------------------------------
if st.session_state.get("from_router", False) is False:
    st.session_state.processed_image = None
else:
    st.session_state.from_router = False   # prevent image from sticking on next pages


# ----------------------------------------------------
# RESTORE IMAGE (Auto Router → Plant Page)
# ----------------------------------------------------
uploaded_img = None
if st.session_state.get("processed_image"):
    try:
        decoded = base64.b64decode(st.session_state.processed_image)
        uploaded_img = Image.open(BytesIO(decoded)).convert("RGB")
    except:
        uploaded_img = None


# ----------------------------------------------------
# LANGUAGE SELECTOR
# ----------------------------------------------------
lang = st.sidebar.selectbox("Language / भाषा", ["English", "Hindi"])
T = get_text(lang)


# ----------------------------------------------------
# HEADER
# ----------------------------------------------------
st.markdown(f"""
<div class="header-box">
    <h2 style='margin:0;color:white;'>{T['plant_disease']}</h2>
    <p style='margin:0;color:white;'>AI Based Leaf Disease Detection</p>
</div>
""", unsafe_allow_html=True)


# ----------------------------------------------------
# LOAD MODEL
# ----------------------------------------------------
@st.cache_resource
def load_plant_model():
    model_path = "models/plant_desease.tflite"
    csv_path   = "models/Plant Village Disease-class_dict.csv"

    df = pd.read_csv(csv_path)
    class_map = {int(i): c for i, c in zip(df["class_index"], df["class"])}

    inter = tf.lite.Interpreter(model_path=model_path)
    inter.allocate_tensors()

    inp = inter.get_input_details()[0]["index"]
    out = inter.get_output_details()[0]["index"]
    img_size = (224, 224)

    return inter, inp, out, img_size, class_map

inter, inp_idx, out_idx, IMG_SIZE, CLASS_MAP = load_plant_model()


# ----------------------------------------------------
# SAFE IMAGE LOADER
# ----------------------------------------------------
def load_uploaded_image(file):
    try:
        return Image.open(BytesIO(file.read())).convert("RGB")
    except:
        st.error("❌ Invalid or corrupted image. Upload JPG/PNG.")
        return None


# ----------------------------------------------------
# PREDICT FUNCTION
# ----------------------------------------------------
def predict_plant(img):
    img = img.resize(IMG_SIZE)
    arr = np.array(img, dtype=np.float32) / 255.0
    arr = arr[np.newaxis, ...]

    inter.set_tensor(inp_idx, arr)
    inter.invoke()

    pred = inter.get_tensor(out_idx)[0]
    idx = int(np.argmax(pred))

    return CLASS_MAP[idx], float(pred[idx])


# ----------------------------------------------------
# IMAGE INPUTS
# ----------------------------------------------------
file = st.file_uploader(T["upload"], type=["jpg","png","jpeg"])
cam  = st.camera_input(T["capture"])

img = None

if uploaded_img:
    img = uploaded_img
elif cam:
    img = Image.open(cam).convert("RGB")
elif file:
    img = load_uploaded_image(file)


# ----------------------------------------------------
# DISPLAY + ANALYZE
# ----------------------------------------------------
if img:
    st.image(img, use_container_width=True)

    if st.button(T["analyze"], use_container_width=True):
        fancy_loader("🔍 Analyzing image...")
        label, conf = predict_plant(img)
        show_result(label, conf, T)
