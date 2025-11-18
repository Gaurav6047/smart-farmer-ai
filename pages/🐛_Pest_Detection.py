import streamlit as st
from utils.theme import load_theme
load_theme()

from PIL import Image
from ultralytics import YOLO
import pandas as pd
from utils.language import get_text
from utils.result_box import show_result
from utils.draw_boxes import draw_yolo_boxes
import base64
from io import BytesIO
from utils.loading import fancy_loader

# --------------------------------------------------------------------
# When page is opened normally (not from auto router), clear old image
# --------------------------------------------------------------------
if st.session_state.get("from_router", False) is False:
    st.session_state.processed_image = None
else:
    # Reset after first use so image does not persist across pages
    st.session_state.from_router = False


# --------------------------------------------------------------------
# Restore image passed from Auto Routing
# --------------------------------------------------------------------
uploaded_img = None
if st.session_state.get("processed_image"):
    try:
        decoded = base64.b64decode(st.session_state.processed_image)
        uploaded_img = Image.open(BytesIO(decoded)).convert("RGB")
    except:
        uploaded_img = None


# --------------------------------------------------------------------
# Language
# --------------------------------------------------------------------
lang = st.sidebar.selectbox("Language / भाषा", ["English", "Hindi"])
T = get_text(lang)


# --------------------------------------------------------------------
# Header
# --------------------------------------------------------------------
st.markdown(f"""
<div class="header-box">
    <h2 style='margin:0;color:white;'>{T["pest_detection"]}</h2>
    <p style='margin:0;color:white;'>YOLO-based Insect Detection</p>
</div>
""", unsafe_allow_html=True)


# --------------------------------------------------------------------
# Load YOLO model + class map
# --------------------------------------------------------------------
@st.cache_resource
def load_pest_model():
    model = YOLO("models/pest_model.pt")
    df = pd.read_csv("models/pest_classes.csv")
    class_map = dict(zip(df["new_id"], df["class_name"]))
    return model, class_map

model, CLASS_MAP = load_pest_model()


# --------------------------------------------------------------------
# Safe PIL loader (avoids UnidentifiedImageError)
# --------------------------------------------------------------------
def load_image_safely(file):
    try:
        return Image.open(BytesIO(file.read())).convert("RGB")
    except:
        st.error("❌ Invalid image file. Please upload a valid JPG/PNG.")
        return None


# --------------------------------------------------------------------
# YOLO prediction
# --------------------------------------------------------------------
def predict_pest(img):
    results = model(img, verbose=False)
    if len(results[0].boxes) == 0:
        return None, None, 0.0
    box = results[0].boxes[0]
    cls, conf = int(box.cls), float(box.conf)
    label = CLASS_MAP.get(cls, f"class_{cls}")
    return results, label, conf


# --------------------------------------------------------------------
# Input handling (router image → camera → upload)
# --------------------------------------------------------------------
file = st.file_uploader(T["upload"], type=["jpg", "jpeg", "png"])
cam = st.camera_input(T["capture"])

img = None

if uploaded_img:
    img = uploaded_img
elif cam:
    img = Image.open(cam).convert("RGB")
elif file:
    img = load_image_safely(file)


# --------------------------------------------------------------------
# Detection UI
# --------------------------------------------------------------------
if img:
    st.image(img, use_container_width=True)

    if st.button(T["detect"], use_container_width=True):
        fancy_loader("🕷 Detecting pests...")
        results, label, conf = predict_pest(img)

        if results is None:
            st.error("❌ No pest detected!")
        else:
            boxed = draw_yolo_boxes(img.copy(), results, CLASS_MAP)
            st.image(boxed, use_container_width=True)
            show_result(label, conf, T)
