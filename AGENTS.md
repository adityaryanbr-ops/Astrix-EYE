# ASTRIX EYE — agent guide

This repo includes the **Devpost Learn AI Basics** skill pack ([challengepost/learn-ai-basics](https://github.com/challengepost/learn-ai-basics)) for plan-first development with Cursor.

## Devpost workflow (recommended for new features)

Use the project skills under `.cursor/skills/` in order:

1. **1-start** — learner profile and workspace check  
2. **2-scope** — idea and POC boundaries  
3. **3-prd** — product requirements  
4. **4-spec** — technical plan  
5. **5-build** — incremental build with commits  
6. **6-ship** — demo video and GitHub submission prep  

Planning artifacts live in `devpost/` (personal notes in `devpost/learner-profile.md` are gitignored).

## Application entry points

| Surface | Path |
|--------|------|
| Desktop GUI | `astrix_eye.py`, `run_astrix_eye.bat` |
| Web UI | `uvicorn astrix_eye.server:app --host 0.0.0.0 --port 8000` |
| Training / batch inference | `src/train.py`, `src/inference/*` |

When changing detection UX or performance, read the existing `AstrixEyeApp` pipeline (model cache, OpenVINO on CPU, thread-safe Tk queue) before large refactors.

## Refresh skills

```bash
npx skills add challengepost/learn-ai-basics --all -y
```

Requires Node.js and Git. See `skills-lock.json` for pinned skill versions.
