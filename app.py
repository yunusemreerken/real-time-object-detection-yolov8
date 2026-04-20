import sys
import types
import numpy as np

mock_cv2 = types.ModuleType("cv2")
mock_cv2.imshow = lambda *args, **kwargs: None
mock_cv2.imread = lambda *args, **kwargs: None
mock_cv2.imwrite = lambda *args, **kwargs: None
mock_cv2.resize = lambda *args, **kwargs: None
mock_cv2.cvtColor = lambda *args, **kwargs: None
mock_cv2.IMREAD_COLOR = 1
mock_cv2.IMREAD_GRAYSCALE = 0
mock_cv2.COLOR_BGR2RGB = 4
mock_cv2.COLOR_RGB2BGR = 4
mock_cv2.VideoCapture = lambda *args, **kwargs: None
mock_cv2.setNumThreads = lambda *args, **kwargs: None
mock_cv2.getNumThreads = lambda *args, **kwargs: 0
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