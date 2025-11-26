import streamlit as st
from utils.theme import load_theme
from utils.sidebar import render_sidebar
from utils.language import get_text
from utils.result_box import show_result
from utils.loading import fancy_loader

from PIL import Image
import numpy as np
import tensorflow as tf
import json
import base64
from io import BytesIO


# ----------------------------------------------------
# GLOBAL THEME + SIDEBAR (persistent language)
# ----------------------------------------------------
load_theme()
render_sidebar()      # <<< IMPORTANT

# AFTER render_sidebar()
lang = st.session_state.get("lang", "English")
T = get_text(lang)
tr = lambda k: T.get(k, k)

# ----------------------------------------------------
# ROUTER STATE CLEANUP
# ----------------------------------------------------
if not st.session_state.get("from_router", False):
    st.session_state.processed_image = None
else:
    st.session_state.from_router = False


# ----------------------------------------------------
# RESTORE ROUTED IMAGE
# ----------------------------------------------------
uploaded_img = None
if st.session_state.get("processed_image"):
    try:
        decoded = base64.b64decode(st.session_state["processed_image"])
        uploaded_img = Image.open(BytesIO(decoded)).convert("RGB")
    except:
        uploaded_img = None


# ----------------------------------------------------
# HEADER
# ----------------------------------------------------
st.markdown(f"""
<div class="header-box">
    <h2 style='margin:0;color:white;'>{tr("fruit_classification")}</h2>
    <p style='margin:0;color:white;'>{tr("fruit_subtitle")}</p>
</div>
""", unsafe_allow_html=True)


# ----------------------------------------------------
# LOAD MODEL
# ----------------------------------------------------
@st.cache_resource
def load_fruit_model():
    interpreter = tf.lite.Interpreter(model_path="models/fruit_model.tflite")
    interpreter.allocate_tensors()

    with open("models/fruit_class_names.json", "r") as f:
        classes = json.load(f)

    inp = interpreter.get_input_details()[0]["index"]
    out = interpreter.get_output_details()[0]["index"]
    size = interpreter.get_input_details()[0]["shape"][1:3]

    return interpreter, inp, out, size, classes

interpreter, inp_idx, out_idx, IMG_SIZE, CLASS_NAMES = load_fruit_model()


# ----------------------------------------------------
# SAFE IMAGE LOADER
# ----------------------------------------------------
def load_uploaded_image(file):
    try:
        return Image.open(BytesIO(file.read())).convert("RGB")
    except:
        st.error(tr("invalid_fruit_image"))
        return None


# ----------------------------------------------------
# PREDICT FRUIT
# ----------------------------------------------------
def predict_fruit(img):
    img = img.resize(IMG_SIZE)
    arr = np.array(img, dtype=np.float32) / 255.0
    arr = arr[np.newaxis, ...]

    interpreter.set_tensor(inp_idx, arr)
    interpreter.invoke()

    pred = interpreter.get_tensor(out_idx)[0]
    idx = int(np.argmax(pred))

    return CLASS_NAMES[idx], float(pred[idx])


# ----------------------------------------------------
# INPUT HANDLING
# ----------------------------------------------------
file = st.file_uploader(tr("upload"), type=["jpg", "jpeg", "png"])
cam  = st.camera_input(tr("capture"))

img = uploaded_img or (Image.open(cam).convert("RGB") if cam else None)

if not img and file:
    img = load_uploaded_image(file)


# ----------------------------------------------------
# UI + CLASSIFICATION
# ----------------------------------------------------
if img:
    st.image(img, use_container_width=True)

    if st.button(tr("classify"), use_container_width=True):

        fancy_loader(tr("fruit_loading"))

        label, conf = predict_fruit(img)

        translated = T.get("fruit_classes", {}).get(label, label)

        show_result(translated, conf, T)

else:
    st.info(tr("upload"))
