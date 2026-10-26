---
doc: scope
status: approved
---

# ASTRIX EYE

Real-time multi-model object detection for aerial and tactical video (desktop + browser).

## The Unique Kernel

One control panel switches between specialized YOLO models (general, drone, human, VisDrone aerial, weapon) on live camera, file, or RTSP feeds—with threat highlighting when drones or weapons appear.

## Who It's For

Operators and developers who need a quick local demo of detection models without writing CLI commands each time.

## The Core Loop

Open the app → pick model and source → Start Scan → watch annotated video with FPS and class counts → snapshot or record when something matters.

## Inspiration & Identity

Dark tactical UI, cyan accents, “command center” feel (similar to modern security dashboards). References: existing Romeo/Astrix background art in `assets/`.

## Why This Matters to the Learner

Hands-on proof that custom-trained and off-the-shelf YOLO weights run together in one polished tool for demos and coursework.

## What "Working" Looks Like

Desktop app runs on Windows, loads at least one model, shows bounding boxes on webcam or sample video, displays FPS/inference time, and saves a snapshot. Browser UI at `/` runs detection on camera or upload.

## The POC Boundary

Windows desktop (Tkinter) + FastAPI web UI; local `.pt` weights; CPU OpenVINO or GPU when available. No cloud training pipeline in-app.

## Later

Multi-camera grid, Garrison dashboard deep-link presets, TensorRT export, mobile client.

## Explicitly Cut

User accounts, remote model hosting, automatic dataset labeling, production K8s deploy (Docker scaffold only).
