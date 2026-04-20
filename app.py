import sys
import types

mock_cv2 = types.ModuleType("cv2")
sys.modules["cv2"] = mock_cv2


import os
import streamlit as st
from ultralytics import YOLO
from PIL import Image
import numpy as np

st.set_page_config(page_title="YOLOv8 Detection", layout="centered")

st.title("Real-Time Object Detection (YOLOv8)")

@st.cache_resource
def load_model():
    return YOLO("yolov8n.pt")

model = load_model()

uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Input Image")

    with st.spinner("Detecting..."):
        results = model(image)
        output = results[0].plot()

    st.image(output, caption="Detection Result")