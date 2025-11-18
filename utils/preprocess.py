import numpy as np

def preprocess_tflite(img, size):
    img = img.resize(size)
    arr = np.array(img, dtype=np.float32) / 255.0
    return arr[np.newaxis, ...]
