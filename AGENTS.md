# AGENTS.md — YOLOv8 Real-Time Object Detection

> This file is the instruction guide for Codex and other AI agents.
> Rules apply project-wide. Task sections grow just-in-time as new features are needed.

---

## Project Structure

```
real-time-object-detection-yolov8/
├── app.py              # Main Streamlit app — all UI and detection logic lives here
├── yolov8n.pt          # YOLOv8 nano model weights
├── requirements.txt    # Python dependencies
├── packages.txt        # System-level dependencies (for Streamlit Cloud)
├── runtime.txt         # Python version pin (3.11)
├── DockerFile          # Docker setup
├── assets/             # Demo GIF and static images
└── samples/            # Sample files for manual testing
```

---

## Setup & Run

```bash
git clone https://github.com/yunusemreerken/real-time-object-detection-yolov8
cd real-time-object-detection-yolov8
pip install -r requirements.txt
streamlit run app.py
```

- Requires Python 3.11.
- On first run, `yolov8n.pt` is downloaded automatically (~6MB).

---

## Architecture Overview

| Layer | Detail |
|---|---|
| UI | Streamlit (`app.py`) — image upload, webcam snapshot, video tabs |
| Detection | Ultralytics YOLOv8 — bounding boxes + confidence scores |
| Image processing | PIL, NumPy |
| Video processing | PyAV — frame-by-frame detection |
| Deployment | Streamlit Cloud / Docker |

---

## Coding Rules

1. **Single-file principle:** New features go into `app.py` first. If the file exceeds 300 lines, discuss splitting into modules before proceeding.
2. **Model changes:** If swapping `yolov8n.pt` for another model, update both `requirements.txt` and the model-loading line in `app.py` together.
3. **Streamlit state:** Use `st.session_state` to avoid redundant recomputation on reruns.
4. **Confidence threshold:** The slider value must always be passed as the `conf` parameter to the model — never hardcode it.
5. **Error handling:** Camera and video errors must be shown via `st.error()`. Do not silently swallow exceptions.

## Branches

- `main` — Streamlit Cloud deployment, primary branch
- `docker` — Oracle Cloud deployment, Docker based. Review this branch before any infrastructure changes.

---

## Testing Instructions

Run these checks after every change:

```bash
# No syntax errors
python -m py_compile app.py

# Dependencies are consistent
pip install -r requirements.txt --dry-run

# App starts without crashing (wait 3s, then kill)
streamlit run app.py &
sleep 3 && kill %1
```

Use files in `samples/` for manual image and video testing.

---

## Tasks

This section grows just-in-time. Add a new task here before asking Codex to implement it.

### [ ] Task 1 — Model Selector
- User should be able to choose between `yolov8n`, `yolov8s`, `yolov8m` from the sidebar
- Selected model name stored in `st.session_state['model_name']`
- When selection changes, reload model and clear old cache

### [ ] Task 2 — Download Result Button
- After detection, user should be able to download the annotated image as PNG
- Use `st.download_button`
- Output filename: `detected_{original_filename}`

### [ ] Task 3 — Class Filter
- User should be able to select which classes to display via `st.multiselect`
- If no filter applied, show all classes (preserve current behavior)

---

## Hard Rules (Never Break)

- Do **not** delete or overwrite `yolov8n.pt` or any `.pt` file.
- Do **not** change the Python version in `runtime.txt` without also updating `requirements.txt`.
- Do **not** put code or scripts inside `assets/` — static media only.
- Do **not** commit `.env` files or hardcoded secrets.
- Do **not** reference model files that don't exist in the repo. 
  Only `yolov8n.pt` is available locally. For other models, download must be handled automatically via Ultralytics.

---

## Deployment Notes

- Streamlit Cloud upload limits: images 10MB, videos 50MB.
- Webcam tab uses browser snapshot — no server-side streaming.
- For Docker deployment use `DockerFile`; for Streamlit Cloud use `packages.txt`.
