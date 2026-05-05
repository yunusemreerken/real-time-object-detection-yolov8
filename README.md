# Real-Time Object Detection — YOLOv8

A real-time object detection web app built with YOLOv8 and Streamlit. Detects objects from images, videos, and webcam input directly in the browser.

🔗 **Live Demo (Streamlit Cloud):** [real-time-object-detection-yolov8.streamlit.app](https://real-time-object-detection-yolov8-agkwdbsxfg7enjzxayk2cb.streamlit.app/)

🐳 **Live Demo (Docker / Oracle Cloud):** [http://141.148.226.97:8501](http://141.148.226.97:8501)

---

## What It Does

- Detects objects in uploaded **images** (JPG, PNG)
- Processes uploaded **video files** frame by frame (MP4, AVI, MOV)
- Runs detection on **webcam snapshots** directly in the browser
- Displays detected class names and confidence scores
- Adjustable **confidence threshold** slider

---

## Architecture

```
User
 │
 ▼
Streamlit UI
 │
 ▼
YOLOv8n Model (Ultralytics)
 │
 ▼
Detection Results (Bounding Box + Confidence Score)

Deployment Options:
├── v1.0 → Streamlit Cloud (managed)
└── v2.0 → Docker → Oracle Cloud (self-hosted, 1GB RAM + 2GB Swap)
```

---

## Tech Stack

| Component | Technology |
|-----------|------------|
| Object Detection | YOLOv8n (Ultralytics) |
| Web Interface | Streamlit |
| Image Processing | PIL, NumPy |
| Video Processing | PyAV |
| Containerization | Docker |
| Cloud Deployment | Oracle Cloud Free Tier |
| Managed Deployment | Streamlit Cloud |

---

## Screenshot

![Detection Demo](assets/demo.gif)

---

## How to Run

### Local

```bash
git clone https://github.com/yunusemreerken/real-time-object-detection-yolov8
cd real-time-object-detection-yolov8
pip install -r requirements.txt
streamlit run app.py
```

### Docker

```bash
git clone -b docker https://github.com/yunusemreerken/real-time-object-detection-yolov8
cd real-time-object-detection-yolov8
docker build -t yolov8-app .
docker run -p 8501:8501 yolov8-app
```

### Requirements

- Python 3.11
- Docker (for containerized deployment)
- See `requirements.txt` for full dependency list

---

## Output Example

Detection results include:
- Bounding boxes drawn on the image
- Class label + confidence score for each detected object
- Summary list: `Detected: person (0.87), cell phone (0.65)`

---

## Notes

- First run downloads `yolov8n.pt` model automatically (~6MB)
- Max upload size: 10MB for images, 50MB for videos
- Webcam tab uses browser camera input (no server-side stream)
- Docker deployment optimized for 1GB RAM with 2GB swap on Oracle Cloud Free Tier

---

## Sample Files
Test the app with provided samples in the `/samples` folder.

---

## Changelog

### v2.0 — Docker Branch
- Containerized with Docker
- Deployed on Oracle Cloud Free Tier
- Optimized for low-memory environments (1GB RAM + 2GB swap)
- Self-hosted, full infrastructure control

### v1.0 — Main Branch
- Initial release
- Streamlit Cloud deployment
- Image, video, and webcam support
- Confidence threshold slider

---

## Versions

| Version | Branch | Deployment | Demo |
|---------|--------|------------|------|
| v1.0 | main | Streamlit Cloud | [Demo](https://...streamlit.app) |
| v2.0 | docker | Oracle Cloud + Docker | [Demo](http://141.148.226.97:8501) |


## Author

**Yunus Emre Erken**
[GitHub](https://github.com/yunusemreerken) · [LinkedIn](https://linkedin.com/in/yunus-emre-erken)


