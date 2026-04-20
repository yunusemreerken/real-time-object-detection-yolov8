import sys
from unittest.mock import MagicMock

mock_cv2 = MagicMock()
mock_cv2.IMREAD_COLOR = 1
mock_cv2.IMREAD_GRAYSCALE = 0
mock_cv2.COLOR_BGR2RGB = 4
mock_cv2.COLOR_RGB2BGR = 4
mock_cv2.INTER_LINEAR = 1
mock_cv2.INTER_AREA = 3
mock_cv2.BORDER_CONSTANT = 0
sys.modules["cv2"] = mock_cv2

import os
import tempfile
import streamlit as st
import numpy as np
from PIL import Image
from ultralytics import YOLO

st.set_page_config(page_title="YOLOv8 Detection", layout="wide")
st.title("Real-Time Object Detection (YOLOv8)")

@st.cache_resource
def load_model():
    return YOLO("yolov8n.pt")

model = load_model()

confidence = st.slider("Confidence Threshold", 0.0, 1.0, 0.5, 0.05)

tab1, tab2, tab3 = st.tabs(["Image", "Video", "Webcam"])

with tab1:
    uploaded_image = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])
    if uploaded_image:
        image = Image.open(uploaded_image)
        st.image(image, caption="Input Image")
        with st.spinner("Detecting..."):
            results = model(image, conf=confidence)
            output = results[0].plot()
        st.image(output, caption="Detection Result")

with tab2:
    uploaded_video = st.file_uploader("Upload Video", type=["mp4", "avi", "mov"])
    if uploaded_video:
        import av
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
            tmp.write(uploaded_video.read())
            tmp_path = tmp.name
        st.video(tmp_path)
        with st.spinner("Processing video frames..."):
            container = av.open(tmp_path)
            frames_out = []
            for i, frame in enumerate(container.decode(video=0)):
                if i >= 50:
                    break
                img = frame.to_image()
                results = model(img, conf=confidence)
                output = results[0].plot()
                frames_out.append(output)
        if frames_out:
            st.image(frames_out[::5], caption=[f"Frame {i*5}" for i in range(len(frames_out[::5]))])

with tab3:
    st.info("Webcam: fotoğraf çek, detection anında çalışır.")
    img_file = st.camera_input("Kamerayı kullan")
    if img_file:
        image = Image.open(img_file)
        with st.spinner("Detecting..."):
            results = model(image, conf=confidence)
            output = results[0].plot()
        st.image(output, caption="Detection Result")