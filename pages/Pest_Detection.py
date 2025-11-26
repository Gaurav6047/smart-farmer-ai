import streamlit as st
import cv2
import numpy as np
from ultralytics import YOLO
from PIL import Image
import pandas as pd
from io import BytesIO

from utils.theme import load_theme
from utils.language import get_text
from utils.sidebar import render_sidebar
from utils.result_box import show_result
from utils.draw_boxes import draw_yolo_boxes
from utils.loading import fancy_loader


# ====================================================
# GLOBAL INIT
# ====================================================
st.set_page_config(page_title="Pest Detection", layout="wide")
load_theme()
render_sidebar()

lang = st.session_state.get("lang", "English")
T = get_text(lang)
tr = lambda k: T.get(k, k)


# ====================================================
# HEADER
# ====================================================
subtitle = tr("pest_subtitle")
st.markdown(
    f"""
<div class="header-box">
    <h2 style='margin:0;color:white;'>{tr("pest_detection")}</h2>
    <p style='margin:0;color:white;'>{subtitle}</p>
</div>
""",
    unsafe_allow_html=True
)


# ====================================================
# LOAD YOLO MODEL
# ====================================================
@st.cache_resource
def load_pest_model():
    model = YOLO("models/pest_model.pt")
    df = pd.read_csv("models/pest_classes.csv")
    class_map = dict(zip(df["new_id"], df["class_name"]))
    return model, class_map

model, CLASS_MAP = load_pest_model()


# ====================================================
# SAFE CAMERA SESSION CONTROL
# ====================================================
if "live_running" not in st.session_state:
    st.session_state.live_running = False


# ====================================================
# LIVE DETECTION UI (SAME UI)
# ====================================================
live_mode = st.checkbox("Live Pest Detection")

# Safe toggling
if live_mode and not st.session_state.live_running:
    st.session_state.live_running = True
elif not live_mode and st.session_state.live_running:
    st.session_state.live_running = False


# ====================================================
# LIVE DETECTION (SAFE + NO CAMERA LOCK)
# ====================================================
if st.session_state.live_running:

    FRAME_WINDOW = st.image([])
    st.warning("")

    # VERY IMPORTANT: use DSHOW → avoids MSMF errors
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if not cap.isOpened():
        st.error("Camera not available. Close other apps using the camera.")
        st.session_state.live_running = False
        st.stop()

    while st.session_state.live_running:
        ret, frame = cap.read()
        if not ret:
            continue

        frame = cv2.flip(frame, 1)

        results = model(frame, conf=0.45, imgsz=640, verbose=False)
        r = results[0]

        for box in r.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cls = int(box.cls)
            conf = float(box.conf)
            label = f"{CLASS_MAP.get(cls, 'NA')} {conf:.2f}"

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
            cv2.putText(frame, label, (x1, y1 - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        FRAME_WINDOW.image(rgb, width="stretch")

        # IMPORTANT: Stop when checkbox is turned off
        if not st.session_state.live_running:
            break


    cap.release()
    cv2.destroyAllWindows()
    st.stop()


# ====================================================
# STATIC IMAGE DETECTION
# ====================================================
file = st.file_uploader(tr("upload"), type=["jpg", "jpeg", "png"])
cam = st.camera_input(tr("capture"))

img = None

if cam:
    img = Image.open(cam).convert("RGB")
elif file:
    try:
        img = Image.open(file).convert("RGB")
    except:
        st.error("Invalid image")

# STATIC MODE
if img:
    st.image(img, width="stretch")

    if st.button(tr("detect"), use_container_width=True):
        fancy_loader(tr("pest_loading"))

        results = model(img, conf=0.45, imgsz=640, verbose=False)
        r = results[0]
        boxes = r.boxes

        if len(boxes) == 0:
            st.error(tr("no_pest_found"))
        else:
            boxed = draw_yolo_boxes(img.copy(), results, CLASS_MAP)
            st.image(boxed, width="stretch")

            st.subheader(tr("detected_pests"))
            for box in boxes:
                cls = int(box.cls)
                conf = float(box.conf)
                name = CLASS_MAP.get(cls, f"class_{cls}")
                show_result(name, conf, T)
