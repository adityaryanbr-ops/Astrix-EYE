---
doc: checklist
status: approved
---

# Build Checklist

Build mode: fast (project largely complete; checklist documents shipped slices)

## Slices

- [x] **1. Repository scaffold and model path resolution**
  Becomes usable: Project runs from repo root; weights resolve from `weights/` or Downloads.
  PRD ref: `prd.md > Features and Behavior` (model selection)
  Spec ref: `spec.md > File Structure`
  Commit: Initial Astrix-EYE repository.

- [x] **2. Desktop GUI and thread-safe inference**
  Becomes usable: Start/stop scan, live stats, threat pill, snapshots/recordings.
  PRD ref: `prd.md > The Core Journey`
  Spec ref: `spec.md > Components` (`AstrixEyeApp`)
  Commit: Fix Romeo Eye desktop app and improve speed and GUI (ported to Astrix).

- [x] **3. Web UI (ASTRIX EYE branding)**
  Becomes usable: FastAPI `/` and detection endpoints.
  Spec ref: `spec.md > Components` (`server.py`)
  Commit: ASTRIX EYE web frontend branding.

- [x] **4. Devpost Learn skill pack**
  Becomes usable: `.cursor/skills/1-start` … `6-ship` + `devpost/` planning docs.
  Spec ref: `spec.md > File Structure`
  Commit: Integrate Devpost Learn AI Basics skills.

## Hands-on Checkpoints

- [x] Early: Desktop scan on sample video with Weapon model
- [x] Final: Public GitHub repo and README install instructions

## Revisions

- Migrated branding from Romeo Eye to ASTRIX EYE; created dedicated Astrix-EYE repository.
