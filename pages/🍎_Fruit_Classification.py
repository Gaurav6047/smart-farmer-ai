import streamlit as st
from utils.theme import load_theme
load_theme()

from PIL import Image
import numpy as np
import tensorflow as tf
import json
from utils.language import get_text
from utils.result_box import show_result
import base64
from io import BytesIO
from utils.loading import fancy_loader

# ----------------------------------------------------
# ROUTER STATE CLEANUP
# ----------------------------------------------------
# If user did NOT come from auto router → clear last image
if st.session_state.get("from_router", False) is False:
    st.session_state.processed_image = None
else:
    # Reset immediately so image does not persist after this page
    st.session_state.from_router = False


# ----------------------------------------------------
# RESTORE IMAGE FROM AUTO ROUTING
# ----------------------------------------------------
uploaded_img = None
if st.session_state.get("processed_image"):
    try:
        decoded = base64.b64decode(st.session_state.processed_image)
        uploaded_img = Image.open(BytesIO(decoded)).convert("RGB")
    except:
        uploaded_img = None


# ----------------------------------------------------
# LANGUAGE
# ----------------------------------------------------
lang = st.sidebar.selectbox("Language / भाषा", ["English", "Hindi"])
T = get_text(lang)


# ----------------------------------------------------
# HEADER
# ----------------------------------------------------
st.markdown(f"""
    <div class="header-box">
        <h2 style='margin:0;color:white;'>{T['fruit_classification']}</h2>
        <p style='margin:0;color:white;'>AI-based Fruit & Vegetable Recognition</p>
    </div>
""", unsafe_allow_html=True)


# ----------------------------------------------------
# LOAD FRUIT MODEL
# ----------------------------------------------------
@st.cache_resource
def load_fruit_model():
    inter = tf.lite.Interpreter(model_path="models/fruit_model.tflite")
    inter.allocate_tensors()

    with open("models/fruit_class_names.json", "r") as f:
        classes = json.load(f)

    inp = inter.get_input_details()[0]["index"]
    out = inter.get_output_details()[0]["index"]
    size = inter.get_input_details()[0]["shape"][1:3]

    return inter, inp, out, size, classes

inter, inp_idx, out_idx, IMG_SIZE, CLASS_NAMES = load_fruit_model()


# ----------------------------------------------------
# SAFE LOADER (prevents PIL errors)
# ----------------------------------------------------
def load_uploaded_image(file):
    try:
        return Image.open(BytesIO(file.read())).convert("RGB")
    except:
        st.error("❌ Invalid or corrupted image. Please upload JPG/PNG.")
        return None


# ----------------------------------------------------
# PREDICT
# ----------------------------------------------------
def predict_fruit(img):
    img = img.resize(IMG_SIZE)
    arr = np.array(img, dtype=np.float32) / 255.0
    arr = arr[np.newaxis, ...]

    inter.set_tensor(inp_idx, arr)
    inter.invoke()
    pred = inter.get_tensor(out_idx)[0]

    idx = int(np.argmax(pred))
    return CLASS_NAMES[idx], float(pred[idx])


# ----------------------------------------------------
# INPUTS
# ----------------------------------------------------
file = st.file_uploader(T["upload"], type=["jpg", "jpeg", "png"])
cam = st.camera_input(T["capture"])

img = None

if uploaded_img:
    img = uploaded_img
elif cam:
    img = Image.open(cam).convert("RGB")
elif file:
    img = load_uploaded_image(file)


# ----------------------------------------------------
# UI + PREDICT
# ----------------------------------------------------
if img:
    st.image(img, use_container_width=True)

    if st.button(T["classify"], use_container_width=True):
        fancy_loader("🍎 Classifying fruit...")
        label, conf = predict_fruit(img)
        show_result(label, conf, T)
