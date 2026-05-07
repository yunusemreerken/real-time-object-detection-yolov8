"""
YOLOv8 Real-Time Object Detection
MLflow entegre, temiz mimari
"""

# ── 1. Standart kütüphaneler ──────────────────────────────────────────────────
import os
import sys
import time
import tempfile
import logging
from collections import Counter
from unittest.mock import MagicMock

# ── 2. Üçüncü taraf kütüphaneler ─────────────────────────────────────────────
import numpy as np
import mlflow
import streamlit as st
from PIL import Image
from ultralytics import YOLO

# ── 3. cv2 Mock (Streamlit Cloud / Docker'da cv2 olmayabilir) ─────────────────
def _build_cv2_mock() -> MagicMock:
    """cv2'nin kullanılan parçalarını taklit eder."""
    mock = MagicMock()
    mock.IMREAD_COLOR      = 1
    mock.IMREAD_GRAYSCALE  = 0
    mock.COLOR_BGR2RGB     = 4
    mock.COLOR_RGB2BGR     = 4
    mock.INTER_LINEAR      = 1
    mock.INTER_AREA        = 3
    mock.BORDER_CONSTANT   = 0
    mock.FONT_HERSHEY_SIMPLEX = 0
    mock.getTextSize = lambda text, font, fontScale, thickness: ((len(text) * 10, 20), 5)
    mock.rectangle   = lambda *a, **k: None
    mock.putText     = lambda *a, **k: None

    def _resize(img, size, interpolation=1):
        from PIL import Image as PILImage
        if isinstance(img, np.ndarray):
            pil = PILImage.fromarray(img)
            return np.array(pil.resize(size, PILImage.BILINEAR))
        return img

    def _copy_make_border(img, top, bottom, left, right, borderType, value=None):
        pad = ((top, bottom), (left, right), (0, 0)) if img.ndim == 3 else ((top, bottom), (left, right))
        return np.pad(img, pad, mode="constant")

    mock.resize         = _resize
    mock.copyMakeBorder = _copy_make_border
    return mock

if "cv2" not in sys.modules:
    sys.modules["cv2"] = _build_cv2_mock()

# ── 4. Loglama ────────────────────────────────────────────────────────────────
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

# ── 5. MLflow yapılandırması ─────────────────────────────────────────────────
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
mlflow.set_experiment("yolov8-object-detection")

# ── 6. Model yükleme ──────────────────────────────────────────────────────────
@st.cache_resource
def load_model() -> YOLO:
    logger.info("YOLOv8 modeli yükleniyor...")
    return YOLO("yolov8n.pt")

model = load_model()

# ── 7. Detection yardımcı fonksiyonu ─────────────────────────────────────────
def run_detection(image: Image.Image, confidence: float, input_type: str) -> tuple:
    """
    Verilen PIL Image üzerinde YOLOv8 çalıştırır,
    sonuçları MLflow'a loglar.

    Returns:
        output_image (np.ndarray): bounding box'lı görsel
        detections  (list[str])  : ["person (0.87)", ...]
    """
    with mlflow.start_run():
        # — Inference —
        start = time.time()
        results = model(image, conf=confidence)
        elapsed = time.time() - start

        boxes = results[0].boxes
        names = results[0].names

        # — Sonuçları topla —
        detected_classes: list[str] = []
        confidence_scores: list[float] = []
        detections: list[str] = []

        if boxes is not None and len(boxes) > 0:
            for box in boxes:
                cls_id   = int(box.cls[0])
                cls_name = names[cls_id]
                conf_val = float(box.conf[0])
                detected_classes.append(cls_name)
                confidence_scores.append(conf_val)
                detections.append(f"{cls_name} ({conf_val:.2f})")

        # — MLflow: parametreler —
        mlflow.log_param("model_name",            "yolov8n")
        mlflow.log_param("confidence_threshold",  confidence)
        mlflow.log_param("input_type",            input_type)

        # — MLflow: metrikler —
        mlflow.log_metric("inference_time_seconds", round(elapsed, 4))
        mlflow.log_metric("num_detections",         len(detected_classes))

        if confidence_scores:
            mlflow.log_metric("avg_confidence", round(sum(confidence_scores) / len(confidence_scores), 4))
            mlflow.log_metric("max_confidence", round(max(confidence_scores), 4))

        # Her sınıftan kaç adet bulundu
        for cls_name, count in Counter(detected_classes).items():
            mlflow.log_metric(f"count_{cls_name}", count)

        # — MLflow: etiketler —
        mlflow.set_tag("environment", os.getenv("ENV", "production"))
        mlflow.set_tag("input_type",  input_type)

        logger.info("Detection tamamlandı | input=%s | %d nesne | %.3fs",
                    input_type, len(detected_classes), elapsed)

    output_image = results[0].plot()
    return output_image, detections


# ── 8. Streamlit arayüzü ──────────────────────────────────────────────────────
st.set_page_config(page_title="YOLOv8 Detection", layout="wide")
st.title("Real-Time Object Detection — YOLOv8")

confidence = st.slider("Confidence Threshold", 0.0, 1.0, 0.5, 0.05)

tab1, tab2, tab3 = st.tabs(["🖼 Image", "🎬 Video", "📷 Webcam"])

# ── Tab 1: Image ──────────────────────────────────────────────────────────────
with tab1:
    uploaded_image = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

    if uploaded_image is not None:
        if uploaded_image.size > 10 * 1024 * 1024:
            st.error("Dosya çok büyük. Maksimum 10 MB.")
            st.stop()

        image = Image.open(uploaded_image)
        st.image(image, caption="Yüklenen Görsel")

        with st.spinner("Tespit ediliyor..."):
            output, detections = run_detection(image, confidence, input_type="image")

        if detections:
            st.success("Tespit edilenler: " + ", ".join(detections))
        else:
            st.info("Hiçbir nesne tespit edilemedi.")

        st.image(output, caption="Detection Sonucu")

# ── Tab 2: Video ──────────────────────────────────────────────────────────────
with tab2:
    uploaded_video = st.file_uploader("Upload Video", type=["mp4", "avi", "mov"])

    if uploaded_video is not None:
        if uploaded_video.size > 50 * 1024 * 1024:
            st.error("Dosya çok büyük. Maksimum 50 MB.")
            st.stop()

        import av

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
            tmp.write(uploaded_video.read())
            tmp_path = tmp.name

        st.video(tmp_path)

        with st.spinner("Video kareleri işleniyor..."):
            container   = av.open(tmp_path)
            frames_out  = []
            all_detections: list[str] = []

            for i, frame in enumerate(container.decode(video=0)):
                if i >= 50:
                    break
                img = frame.to_image()
                output, detections = run_detection(img, confidence, input_type="video")
                frames_out.append(output)
                all_detections.extend(detections)

        if frames_out:
            st.image(
                frames_out[::5],
                caption=[f"Kare {i * 5}" for i in range(len(frames_out[::5]))]
            )
        if all_detections:
            st.success(f"Toplam {len(all_detections)} nesne tespit edildi.")

# ── Tab 3: Webcam ─────────────────────────────────────────────────────────────
with tab3:
    st.info("Fotoğraf çek — detection anında çalışır.")
    img_file = st.camera_input("Kamerayı kullan")

    if img_file:
        image = Image.open(img_file)

        with st.spinner("Tespit ediliyor..."):
            output, detections = run_detection(image, confidence, input_type="webcam")

        if detections:
            st.success("Tespit edilenler: " + ", ".join(detections))
        else:
            st.info("Hiçbir nesne tespit edilemedi.")

        st.image(output, caption="Detection Sonucu")
