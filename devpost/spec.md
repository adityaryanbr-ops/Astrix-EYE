---
doc: spec
status: approved
---

# ASTRIX EYE — Technical Spec

## How This Works, In Plain Language

The **desktop app** (`astrix_eye.py`) is a Tkinter window. A background thread reads video frames, runs YOLO inference, and sends RGB images back to the UI. Models are cached and warmed once; on CPU, weights are exported to OpenVINO in `.model_cache/`.

The **web app** (`astrix_eye/server.py`) is FastAPI: the browser sends JPEG frames or files to `/detect_frame` or `/detect_file`, and the server returns base64 annotated images.

Training and batch tools live under `src/` (same layout as Romeo-EYE).

## The Core Journey Through the System

User clicks Start → main thread starts worker → worker loads model via `ModelCache` → frames from OpenCV → `model.predict` → `res.plot()` → resize for canvas → stats update threat pill → optional snapshot/recording writers.

PRD ref: `prd.md > The Core Journey`.

## Stack

- Python 3.11+
- Ultralytics YOLO 8.x, OpenCV, Pillow, NumPy
- PyTorch (CUDA optional), OpenVINO (CPU acceleration)
- Tkinter (desktop), FastAPI + Uvicorn (web)
- Git for version control

## Where It Runs and How Someone Tries It

**Desktop:** `python astrix_eye.py` or `run_astrix_eye.bat` on Windows (primary target).

**Web:** `uvicorn astrix_eye.server:app --host 0.0.0.0 --port 8000` → `http://127.0.0.1:8000/`

Demo: Weapon or General model on sample video in `astrix_eye/annotated.mp4` or `assets/astrix_bg.jpg`.

Public repo: https://github.com/adityaryanbr-ops/Astrix-EYE

## Look and Feel

Implement per `prd.md > Look and Feel`. Canvas letterboxes video; sidebar uses bordered cards and section dividers.

## Components

### `astrix_eye.py` — `AstrixEyeApp`

Desktop UI, worker thread, `ModelCache`, `LatestFrameReader`.

PRD ref: `prd.md > Features and Behavior`.

### `astrix_eye/server.py`

HTML UI + detection endpoints.

PRD ref: `prd.md > Screens and Layout` (web).

### `src/train.py`, `src/inference/*`

YOLO training and CLI inference (unchanged scaffold).

## Data Model

No database. Ephemeral frame buffers; snapshots/recordings as files on disk. Model cache keyed by weight file hash under `.model_cache/`.

## File Structure

```
Astrix-EYE/
├── astrix_eye.py
├── astrix_eye/
│   ├── server.py
│   └── ws_cam_client.py
├── assets/
├── configs/
├── devpost/           # Hackathon planning docs
├── .cursor/skills/    # Devpost Learn agent skills
├── scripts/
├── src/
├── weights/           # Local .pt (gitignored)
└── requirements.txt
```

## Decisions and Open Issues

- GPU may show unavailable on some drivers; app falls back to CPU OpenVINO.
- Large `.pt` files remain outside git by design.
