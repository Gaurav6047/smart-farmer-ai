import numpy as np
from PIL import Image
import tensorflow as tf

# ----------------------------------------------------
# LOAD ROUTER MODEL SAFELY (cached)
# ----------------------------------------------------
def load_router():
    inter = tf.lite.Interpreter(model_path="models/router_model.tflite")
    inter.allocate_tensors()

    inp = inter.get_input_details()[0]["index"]
    out = inter.get_output_details()[0]["index"]
    size = inter.get_input_details()[0]["shape"][1:3]

    return inter, inp, out, tuple(size)

router_inter, router_inp, router_out, ROUTER_IMG_SIZE = load_router()

# ----------------------------------------------------
# CLASS NAMES (must match training dataset)
# ----------------------------------------------------
ROUTER_CLASSES = {
    0: "background",
    1: "fruit",
    2: "leaf",
    3: "pest"
}

# ----------------------------------------------------
# PREPROCESS
# ----------------------------------------------------
def preprocess_router(img: Image.Image):
    img_resized = img.resize(ROUTER_IMG_SIZE)
    arr = np.array(img_resized, dtype=np.float32) / 255.0
    arr = np.expand_dims(arr, axis=0)
    return arr

# ----------------------------------------------------
# PREDICT TYPE FUNCTION (CALLED FROM AUTO ROUTER PAGE)
# ----------------------------------------------------
def predict_type(img: Image.Image):
    """
    Returns: (type_name, confidence)
    type_name = 'leaf' / 'pest' / 'fruit' / 'background'
    """

    arr = preprocess_router(img)

    router_inter.set_tensor(router_inp, arr)
    router_inter.invoke()

    pred = router_inter.get_tensor(router_out)[0]

    idx = int(np.argmax(pred))
    conf = float(pred[idx])

    return ROUTER_CLASSES[idx], conf
