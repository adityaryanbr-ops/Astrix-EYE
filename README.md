# Astrix-EYE

**ASTRIX EYE** — real-time multi-model aerial detection (desktop + browser UI), with the same repository layout as [Romeo-EYE](https://github.com/adityaryanbr-ops/Romeo-EYE): training scripts, Docker, configs, and inference utilities.

## Devpost Learn AI Basics (integrated)

This repo ships the **Build With AI: Basics** agent skill pack for Cursor (plan → PRD → spec → build → ship):

```bash
npx skills add challengepost/learn-ai-basics --all -y
# Windows: .\scripts\install-learn-ai-skills.ps1
```

Skills install to `.cursor/skills/` (`1-start` … `6-ship`). Planning docs go in `devpost/` — see [devpost/README.md](devpost/README.md) and [AGENTS.md](AGENTS.md). Hackathon: [learn-ai-basics.devpost.com](https://learn-ai-basics.devpost.com/resources).

## Devpost Learn — AI skill pack

This repo includes the [Build With AI: Basics](https://learn-ai-basics.devpost.com/) agent skills (`1-start` … `6-ship`) under `.cursor/skills/`. Planning docs live in `devpost/`. Reinstall or refresh:

```powershell
.\scripts\install-learn-ai-skills.ps1
```

In Cursor, ask the agent to run skill **`1-start`** to begin the hackathon flow, or **`6-ship`** when you are ready to publish your demo.

## ASTRIX EYE desktop app

```bash
python -m venv .venv && .venv\Scripts\activate
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu126   # GPU build
pip install -r requirements.txt
python astrix_eye.py            # or double-click run_astrix_eye.bat
```

The five desktop models are already in `weights/` (`yolov8m.pt`, `drone.pt`, `sard_humans.pt`, `visdrone.pt`, `weapon.pt`). Set `ASTRIX_WEIGHTS_DIR` to use another folder. A sample clip is at `astrix_eye/annotated.mp4` (choose Local Video). On CPU, models are cached as OpenVINO exports in `.model_cache/` after the first run.

**Shortcuts:** Space start/stop · S snapshot · R record · F11 fullscreen

## ASTRIX EYE web UI

```bash
uvicorn astrix_eye.server:app --host 0.0.0.0 --port 8000
```

Open `http://127.0.0.1:8000/` for the browser control panel. It loads the same files from `weights/`. If `yolov8m.pt` is missing, the General model downloads `yolov8n.pt` on first use.

## WebSocket client (optional)

```bash
python astrix_eye/ws_cam_client.py --url ws://127.0.0.1:8000/ws --source 0
```

---

This repository gives you a production‑ready template to **train, evaluate, and deploy** a drone detector using the Ultralytics YOLO family (v8/v11). You supply images + annotations; this repo handles the rest.

## Features
- ⚙️ **Training** with Ultralytics YOLO (simple, fast, reproducible)
- 🧪 **Validation**/**mAP** reporting + confusion matrix
- 🚀 **Inference**:
  - batch: images / folders / videos
  - **RTSP/USB webcam** live detection
  - **FastAPI** server for programmatic inference
- 📦 **Export** to ONNX + (optionally) TensorRT
- 🐳 **Dockerfile** for consistent deployment
- 🧰 Utility scripts: dataset split, YOLO data config, basic converters

> Works on Windows / Linux / macOS. For GPU, install CUDA per your system and use a compatible PyTorch build.

---

## 1) Install
```bash
# (Recommended) Create venv
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install deps
pip install -r requirements.txt
```

## 2) Prepare your dataset
Organize images + labels in YOLO format:

```
datasets/drone_yolo/
├── images/
│   ├── train/  *.jpg|*.png
│   ├── val/    *.jpg|*.png
│   └── test/   *.jpg|*.png (optional)
└── labels/
    ├── train/  *.txt  (YOLO txt per image)
    ├── val/    *.txt
    └── test/   *.txt
```

Each `labels/*.txt` file contains lines:  
`<class_id> <x_center> <y_center> <width> <height>` normalized to 0..1.

Update `configs/data.yaml`:
```yaml
path: datasets/drone_yolo
train: images/train
val: images/val
test: images/test
names: [drone]  # or multiple, e.g. [quadcopter, fixed_wing, bird]
```

If you have a single bucket of images/labels, run the splitter:
```bash
python src/data/split_dataset.py   --images_dir datasets/raw/images   --labels_dir datasets/raw/labels   --out_dir datasets/drone_yolo --val 0.2 --test 0.0
```

## 3) Train
```bash
# Quick start with small model (good baseline)
python src/train.py --model yolov8n.pt --data configs/data.yaml --epochs 100 --img 640 --batch 16
```

Artifacts will appear under `runs/detect/<exp_name>` with `weights/best.pt`.

## 4) Validate
```bash
python src/eval/evaluate.py --weights runs/detect/exp/weights/best.pt --data configs/data.yaml --img 640
```

## 5) Inference (batch)
```bash
# Images folder or a single image/video file
python src/inference/detect.py --weights runs/detect/exp/weights/best.pt --source examples/images --conf 0.5
```

## 6) Live stream (RTSP/USB)
```bash
# RTSP
python src/inference/stream.py --weights runs/detect/exp/weights/best.pt --rtsp rtsp://user:pass@cam-ip:554/stream1

# USB cam index (0 by default)
python src/inference/stream.py --weights runs/detect/exp/weights/best.pt --camera 0
```

## 7) FastAPI server (training scaffold)
```bash
uvicorn src.inference.server:app --host 0.0.0.0 --port 8000
# POST /predict with an image -> JSON detections
```

## 8) Export to ONNX
```bash
python scripts/export_onnx.py --weights runs/detect/exp/weights/best.pt --img 640 --opset 12
```

## 9) Docker
```bash
docker build -t astrix-detector:latest -f docker/Dockerfile .
docker run --rm -it -p 8000:8000 -v $PWD:/app astrix-detector:latest
```

---

## Repository layout

```
Astrix-EYE/
├── astrix_eye.py          # Desktop GUI (ASTRIX EYE)
├── astrix_eye/            # Web server, WebSocket client, demo media
├── assets/                # Icons and background art
├── configs/               # YOLO dataset + hyperparams
├── docker/                # Dockerfile + compose
├── drone-detection-starter/  # Legacy starter copy (same as Romeo-EYE)
├── examples/
├── scripts/
├── src/                   # train / eval / inference utilities
├── weights/               # yolov8m, drone, sard_humans, visdrone, weapon
├── run_astrix_eye.bat
└── requirements.txt
```

## Tips for better accuracy
- Annotate hard negatives (birds, kites) as a separate class if often confused.
- Add **mosaic**/**mixup** augmentations (Ultralytics has strong defaults).
- Train at a resolution close to your deployment input (e.g., 640 or 960).
- Curate a val set from the same **domain** (camera, altitude, lighting).

## License
This project is licensed under the MIT License. See [LICENSE](LICENSE).
