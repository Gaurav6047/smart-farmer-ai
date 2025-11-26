import streamlit as st
from PIL import Image
import base64
from io import BytesIO

from utils.theme import load_theme
from utils.sidebar import render_sidebar
from utils.language import get_text
from router import predict_type

# ----------------------------------------------------
# LOAD THEME + SIDEBAR (Handles global language state)
# ----------------------------------------------------
load_theme()
render_sidebar()

# ----------------------------------------------------
# LANGUAGE
# ----------------------------------------------------
# AFTER render_sidebar()
lang = st.session_state.get("lang", "English")
T = get_text(lang)
tr = lambda k: T.get(k, k)


# ----------------------------------------------------
# HEADER
# ----------------------------------------------------
st.markdown(f"""
<div class="header-box">
    <h2 style='margin:0;color:white;'>{tr('auto_route')}</h2>
    <p style='margin:0;color:white;'>{tr('auto_sub')}</p>
</div>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# SESSION VARIABLES
# ----------------------------------------------------
st.session_state.setdefault("router_image", None)
st.session_state.setdefault("processed_image", None)
st.session_state.setdefault("from_router", False)

# ----------------------------------------------------
# IMAGE INPUT
# ----------------------------------------------------
cam_input = st.camera_input(tr("capture_img"))
file_input = st.file_uploader(tr("upload"), type=["jpg", "jpeg", "png"])

if cam_input:
    st.session_state.router_image = cam_input
elif file_input:
    st.session_state.router_image = file_input

# ----------------------------------------------------
# LOAD IMAGE
# ----------------------------------------------------
img = None
if st.session_state.router_image:
    try:
        img = Image.open(st.session_state.router_image).convert("RGB")
    except:
        st.error(tr("invalid_img"))
        st.session_state.router_image = None

# ----------------------------------------------------
# DISPLAY + PROCESS
# ----------------------------------------------------
if img:

    st.image(img, use_container_width=True)

    if st.button(tr("process"), use_container_width=True):

        st.info(tr("processing"))

        img_type, conf = predict_type(img)
        img_type = img_type.lower().strip()

        # show predicted type
        st.success(f"{tr('result')}: {tr(img_type)} ({conf:.2f})")

        if conf < 0.55:
            st.warning(tr("low_conf"))
            st.stop()

        # Encode image to pass to next page
        buffer = BytesIO()
        img.save(buffer, format="JPEG")
        encoded = base64.b64encode(buffer.getvalue()).decode("utf-8")

        st.session_state.processed_image = encoded
        st.session_state.from_router = True

        # ROUTING
        if img_type == "leaf":
            st.switch_page("pages/Plant_Disease.py")

        elif img_type == "fruit":
            st.switch_page("pages/Fruit_Classification.py")

        elif img_type == "pest":
            st.switch_page("pages/Pest_Detection.py")

        else:
            st.error(tr("background_msg"))
            st.stop()

else:
    st.info(tr("upload"))
