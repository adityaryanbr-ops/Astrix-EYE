---
doc: prd
status: approved
---

# ASTRIX EYE — Product Requirements

Multi-model detection control panel for desktop and browser. Source: `scope.md > The Core Loop`.

## The Core Journey

1. User launches `astrix_eye.py` or opens the web UI.
2. They select a detection model (General, Drone, Operational, Drone View, Weapon, or custom `.pt`).
3. They select input: laptop camera, video/image file, or RTSP/HTTP URL.
4. They adjust confidence and inference size, then press **Start Scan**.
5. Annotated video appears with labels, stats (FPS, ms, object count, resolution), and detection list.
6. Threat badge turns red when drone/weapon classes are detected; otherwise green CLEAR.
7. User may snapshot to `snapshots/` or record to `recordings/`, then stop scan.

## Screens and Layout

**Desktop:** Header (brand, device badge, LIVE/THREAT pills) · left control sidebar · main video canvas · bottom metrics bar.

**Web:** Centered controls (model, source, start/stop) · canvas for annotated output.

## Look and Feel

Dark navy background (`#0a0e14`), cyan accent (`#22d3ee`), green start / red stop, Segoe UI, monospace detection list. Maximized window on launch; placeholder uses dimmed background art.

## Features and Behavior

### Model and source selection

- Dropdowns for model and source; URL field enabled only for IP/RTSP.
- Model path status line shows resolved weights or error.

### Live inference

- Thread-safe pipeline: worker inference, UI updates via queue.
- Latest-frame reader for live sources to reduce lag.
- OpenVINO cache on CPU; CUDA FP16 when GPU works.

### Capture

- Snapshot (S) and record (R) with on-screen REC indicator.

## States and Boundaries

- **Idle** — placeholder art and STANDBY/OFFLINE pills.
- **Scanning** — LIVE pill, controls locked except stop.
- **Error** — dialog + status bar message (missing weights, bad source).
- **No detections** — empty detection panel copy, CLEAR threat state.

## Product Decisions

- Rebrand from Romeo Eye to ASTRIX EYE for desktop and web.
- Keep Romeo-EYE repo layout (train/eval/docker) for parity.
- Do not commit `.pt` weights; document `weights/` and Downloads fallbacks.

## What We're Building

Desktop GUI, web UI, model path resolution, performance optimizations, GitHub repo, Devpost skill integration.

## Deferred From the POC

Cloud API, multi-user auth, automated retraining UI, VisDrone-only production tuning.
