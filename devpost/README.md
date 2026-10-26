# Devpost — Build With AI: Basics

This folder holds **your** planning documents for the [Learn AI Basics](https://learn-ai-basics.devpost.com/) hackathon workflow.

The Cursor agent skills in `.cursor/skills/` read and write files here as you progress:

| File | Skill | Purpose |
|------|--------|---------|
| `learner-profile.md` | 1-start | Your background and goals (**private**, not committed) |
| `scope.md` | 2-scope | POC idea and boundaries |
| `prd.md` | 3-prd | How the app should look and behave |
| `spec.md` | 4-spec | Technical plan |
| `checklist.md` | 5-build | Build slices and progress |

## Suggested project focus

**ASTRIX EYE** — real-time multi-model aerial detection (desktop + browser), already scaffolded in this repo. Use the skills to refine the next slice (e.g. GPU deployment, new model, or dashboard polish) rather than starting from zero.

## Getting started in Cursor

Open the Agent chat and say: **“Run the 1-start skill”** or **“Begin Devpost Learn workflow.”**

Install or update skills:

```bash
npx skills add challengepost/learn-ai-basics --all -y
```
