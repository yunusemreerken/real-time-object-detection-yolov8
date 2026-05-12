# AGENTS.md — YOLOv8 Real-Time Object Detection (Docker / Oracle Cloud)

> This file is the instruction guide for Codex and other AI agents.
> This branch is for Oracle Cloud deployment using Docker.
> Do NOT merge with `main` — Streamlit Cloud and Docker deployments are intentionally separate.

---

## Project Structure

```
real-time-object-detection-yolov8/ (docker branch)
├── app.py                  # Main Streamlit app
├── Dockerfile              # Docker image definition
├── docker-compose.yaml     # Multi-service orchestration (Streamlit + MLflow + Nginx)
├── model_registry.py       # MLflow model registry integration
├── requirements.txt        # Python dependencies
├── yolov8n.pt              # YOLOv8 nano model weights
├── assets/                 # Demo GIF and static images
└── samples/                # Sample files for manual testing
```

---

## Setup & Run

```bash
docker-compose up --build
```

- Streamlit runs on port 8501 (internal only — behind Nginx)
- MLflow runs on port 5000 (internal only — no host exposure)
- Nginx handles external traffic on port 80/443

---

## Architecture Overview

| Layer | Detail |
|---|---|
| UI | Streamlit (`app.py`) — image upload, webcam snapshot, video tabs |
| Detection | Ultralytics YOLOv8 — bounding boxes + confidence scores |
| Experiment Tracking | MLflow (`model_registry.py`) — internal network only |
| Reverse Proxy | Nginx — only port 80/443 exposed to internet |
| Orchestration | Docker Compose |
| Cloud | Oracle Cloud Infrastructure |

---

## Coding Rules

1. **Single-file principle:** New features go into `app.py` first. If the file exceeds 300 lines, discuss splitting into modules before proceeding.
2. **Model changes:** If swapping `yolov8n.pt` for another model, update both `requirements.txt` and the model-loading line in `app.py` together.
3. **Streamlit state:** Use `st.session_state` to avoid redundant recomputation on reruns.
4. **Confidence threshold:** The slider value must always be passed as the `conf` parameter to the model — never hardcode it.
5. **Error handling:** Camera and video errors must be shown via `st.error()`. Do not silently swallow exceptions.
6. **Docker services:** Never expose MLflow or Streamlit ports directly to host. All external traffic must go through Nginx.

---

## Testing Instructions

Run these checks after every change:

```bash
# No syntax errors
python -m py_compile app.py

# Docker build succeeds
docker-compose build

# Services start without crashing
docker-compose up -d
sleep 5
docker-compose ps
docker-compose down
```

---

## Tasks

This section grows just-in-time. Add a new task here before asking Codex to implement it.

### [x] Task 4 — Dockerfile Security Analysis
- Switch to `docker` branch before starting
- Review `Dockerfile` and `docker-compose.yaml`
- Check for: root user, exposed secrets, unnecessary ports, outdated base image

### [x] P1 — MLflow Port Exposure (Fixed)
- Removed host port mapping for MLflow (port 5000)
- MLflow is now on internal Docker network only

### [ ] P2 — Containers Run as Root
- Neither app image nor MLflow service declares a non-root user
- Add a dedicated non-root user in `Dockerfile`
- Apply `user:` directive in `docker-compose.yaml` where writable paths are needed

### [ ] P3 — Base Image Not Pinned
- `python:3.11-slim` is a moving tag
- Pin to a specific digest or patch version for repeatable builds
- Example: `python:3.11.9-slim`

### [ ] Task 5 — Nginx Reverse Proxy
- Oracle Cloud instance currently exposes port 8501 directly
- Add Nginx as reverse proxy in `docker-compose.yaml`
- Only ports 80 and 443 should be exposed to the host
- Streamlit and MLflow must remain on internal Docker network only

---

## Hard Rules (Never Break)

- Do **not** delete or overwrite `yolov8n.pt` or any `.pt` file.
- Do **not** expose MLflow, Streamlit, or any service port directly to host. All traffic through Nginx.
- Do **not** put code or scripts inside `assets/` — static media only.
- Do **not** commit `.env` files or hardcoded secrets.
- Do **not** reference model files that don't exist in the repo.
  Only `yolov8n.pt` is available locally. For other models, download must be handled automatically via Ultralytics.
- Do **not** merge with `main` branch — deployments are intentionally separate.
- **Never apply fixes without reporting findings first.**
  Always list what you found and wait for approval before making changes.
- **After every fix, show the exact diff and explicitly ask "Do you approve this change?" before staging or modifying any file.**
- After every task, verify with `git log --oneline -3` that changes are actually committed.

---

## Deployment Notes

- Oracle Cloud instance: only ports 80 and 443 should be open in security rules.
- MLflow is internal only — access via Docker network between containers.
- Webcam tab uses browser snapshot — no server-side streaming.
- Model files (`.pt`) are not committed to repo — downloaded automatically by Ultralytics at runtime.