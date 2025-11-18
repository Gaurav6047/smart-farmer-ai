import streamlit as st
from utils.theme import load_theme
load_theme()

from PIL import Image
import base64
from io import BytesIO
from router import predict_type
from utils.language import get_text

# --------------------------------------------------------------------
# Language selection
# --------------------------------------------------------------------
lang = st.sidebar.selectbox("Language / भाषा", ["English", "Hindi"])
T = get_text(lang)

# --------------------------------------------------------------------
# Page heading
# --------------------------------------------------------------------
st.markdown(f"""
<div class="header-box">
    <h2 style='margin:0;color:white;'>{T['auto_route']}</h2>
    <p style='margin:0;color:white;'>{T['capture']}</p>
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------------------------
# Session values used for routing and restoring images
# --------------------------------------------------------------------
st.session_state.setdefault("router_image", None)
st.session_state.setdefault("processed_image", None)
st.session_state.setdefault("from_router", False)

# --------------------------------------------------------------------
# Input sources (camera has priority on mobile devices)
# --------------------------------------------------------------------
cam_input = st.camera_input("")
file_input = st.file_uploader(T["upload"], type=["jpg", "jpeg", "png"])

if cam_input:
    st.session_state.router_image = cam_input
elif file_input:
    st.session_state.router_image = file_input

# --------------------------------------------------------------------
# Load the captured/uploaded image
# --------------------------------------------------------------------
img = None
if st.session_state.router_image:
    try:
        img = Image.open(st.session_state.router_image).convert("RGB")
    except:
        st.error(T["invalid_img"])
        st.session_state.router_image = None

# --------------------------------------------------------------------
# Display + Route
# --------------------------------------------------------------------
if img:
    st.image(img, width="stretch")

    if st.button(T["process"], use_container_width=True):

        st.write("⏳ Processing...")

        # Get the predicted category from the router model
        img_type, conf = predict_type(img)
        img_type = img_type.lower().strip()

        st.success(f"{T['result']}: {img_type} ({conf:.2f})")

        # Skip low-confidence results
        if conf < 0.55:
            st.warning(T["low_conf"])
            st.stop()

        # Encode image to move it to the target page
        buffer = BytesIO()
        img.save(buffer, format="JPEG")
        encoded = base64.b64encode(buffer.getvalue()).decode("utf-8")

        st.session_state.processed_image = encoded
        st.session_state.from_router = True

        # Route based on predicted type
        if img_type == "leaf":
            st.switch_page("pages/🌿_Plant_Disease.py")

        elif img_type == "fruit":
            st.switch_page("pages/🍎_Fruit_Classification.py")

        elif img_type == "pest":
            st.switch_page("pages/🐛_Pest_Detection.py")

        else:
            st.error(T["background_msg"])
            st.stop()

else:
    st.info(T["upload"])
