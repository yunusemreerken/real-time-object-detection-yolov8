# Real-Time Object Detection — YOLOv8

A real-time object detection web app built with YOLOv8 and Streamlit. Detects objects from images, videos, and webcam input directly in the browser.

🔗 **Live Demo:** [real-time-object-detection-yolov8.streamlit.app](https://real-time-object-detection-yolov8-agkwdbsxfg7enjzxayk2cb.streamlit.app/)

---

## What It Does

- Detects objects in uploaded **images** (JPG, PNG)
- Processes uploaded **video files** frame by frame (MP4, AVI, MOV)
- Runs detection on **webcam snapshots** directly in the browser
- Displays detected class names and confidence scores
- Adjustable **confidence threshold** slider

---

## Tech Stack

| Component | Technology |
|-----------|------------|
| Object Detection | YOLOv8n (Ultralytics) |
| Web Interface | Streamlit |
| Image Processing | PIL, NumPy |
| Video Processing | PyAV |
| Deployment | Streamlit Cloud |

---

## Screenshot

> _Add a GIF or screenshot here showing detection in action_
> `![Detection Demo](assets/demo.gif)`

---

## How to Run

### Local

```bash
git clone https://github.com/yunusemreerken/real-time-object-detection-yolov8
cd real-time-object-detection-yolov8
pip install -r requirements.txt
streamlit run app.py
```

### Requirements

- Python 3.11
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

## Sample Files
Test the app with provided samples in the `/samples` folder.

---

## Author

**Yunus Emre Erken**
[GitHub](https://github.com/yunusemreerken) · [LinkedIn](https://linkedin.com/in/yunus-emre-erken)