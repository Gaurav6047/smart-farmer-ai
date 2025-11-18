import streamlit as st
import tensorflow as tf
from ultralytics import YOLO
import json
import pandas as pd

@st.cache_resource
def load_tflite(path):
    inter = tf.lite.Interpreter(model_path=path)
    inter.allocate_tensors()
    return inter

@st.cache_resource
def load_yolo(path):
    return YOLO(path)

def load_class_data():
    plant = pd.read_csv("models/plant_classes.csv")
    pest = pd.read_csv("models/pest_classes.csv")
    with open("models/fruit_classes.json") as f:
        fruit = json.load(f)
    return plant, pest, fruit
