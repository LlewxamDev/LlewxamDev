# PROJECT LWX.EXE — Deployment & Maintenance Guide

This guide explains how to deploy the custom **Trophy Selection Engine** (`trophy-engine/`) to Vercel, how to update or re-render compositions in **Adobe After Effects CC 2019** (`after-effects/LWX_EXE_Profile.aep`), and how to swap custom trophy sprites.

---

## 1. Deploying the Custom Trophy Engine on Vercel

The `trophy-engine/` directory contains a self-contained TypeScript/Node serverless application that preserves 100% of the rank thresholds, secret conditions, and GraphQL queries of [`GinWU05/github-profile-trophy`](https://github.com/GinWU05/github-profile-trophy) while rendering the **Classic Sonic.EXE Trophy Selection Screen**.

### Step-by-Step Vercel Setup

1. Sign in to [Vercel](https://vercel.com) with your GitHub account (`@LlewxamDev`).
2. Click **Add New... → Project** and import `LlewxamDev/LlewxamDev`.
3. Under **Build & Development Settings**:
   - **Root Directory**: `trophy-engine`
   - **Framework Preset**: `Other`
4. Under **Environment Variables**, add:
   - `GITHUB_TOKEN1`: A GitHub Personal Access Token (Classic) with `read:user` scope (used to query GitHub's GraphQL v4 API for live commit, repository, issue, pull request, star, and follower metrics).
5. Click **Deploy**.
6. Once deployed, your live SVG endpoint is served at:
   ```text
   https://<your-vercel-project>.vercel.app/api/trophies?username=LlewxamDev
   ```

### Supported Query Parameters

| Parameter | Default | Description |
| :--- | :--- | :--- |
| `username` | `LlewxamDev` | Target GitHub username to evaluate. |
| `focus` | `Repositories` | Which trophy slot is highlighted in the bottom Inspector HUD (`Repositories`, `Commits`, `Issues`, `PullRequest`, `Stars`, `Followers`). |
| `column` | `4` | Number of columns in the Trophy Selection grid (`1`–`6`). |
| `row` | `2` | Maximum number of rows (`1`–`3`). |

### Updating the Static Live Snapshot (`assets/trophies/trophy-selection-live.svg`)

Whenever you want to refresh the committed SVG snapshot directly from your authenticated GitHub CLI (`gh`) session:

```bash
cd trophy-engine
node scripts/render-local-verify.mjs
```

---

## 2. Customizing Trophy Sprites (`trophy-engine/src/config/sprite-slots.json`)

Every trophy category has an independent sprite slot configured in `trophy-engine/src/config/sprite-slots.json`:

| Slot Key | Default Sprite File | Category |
| :--- | :--- | :--- |
| `TotalCommitTrophy` | `assets/trophies/trophy-commit.png` | Total Commits (`SS` — Deep Committer) |
| `TotalRepositoryTrophy` | `assets/trophies/trophy-repository.png` | Total Repositories (`AA` — Hyper Repo Creator) |
| `TotalIssueTrophy` | `assets/trophies/trophy-issue.png` | Total Issues (`AA` — Hyper Issuer) |
| `TotalPullRequestTrophy` | `assets/trophies/trophy-pull-request.png` | Total Pull Requests (`AA` — Hyper Puller) |
| `TotalStarTrophy` | `assets/trophies/trophy-star.png` | Total Stars (`C` — First Star) |
| `TotalFollowerTrophy` | `assets/trophies/trophy-followers.png` | Total Followers (`C` — First Friend) |
| `MultipleLangTrophy` | `assets/trophies/trophy-secret.png` | Secret Trophy (`Rainbow Lang User`) |
| `AchieveSSSRankTrophy` | `assets/trophies/trophy-rank-s.png` | Secret Trophy (`SSS Rank Hacker`) |

To replace any slot with a new custom pixel-art PNG:
1. Overwrite the target PNG in `assets/trophies/` (recommended size: `48x48` or `64x64` RGBA PNG with nearest-neighbor edges), **or** place a new PNG file and update its `"spritePath"` in `trophy-engine/src/config/sprite-slots.json`.
2. Run `node trophy-engine/scripts/render-local-verify.mjs` to update `assets/trophies/trophy-selection-live.svg`.

---

## 3. Rebuilding After Effects Project & Source Plates (`LWX_EXE_Profile.aep`)

All source plates (`after-effects/assets-source/*.png`), authentic game sprites (`after-effects/assets-source/web_authentic/*.png`), and animated GIFs (`assets/**/*.gif`) are orchestrated by:

- `after-effects/compositions/pixel_art_engine.py` (Python + Pillow compositing & palette-locked GIF compiler)
- `after-effects/compositions/build_aep_project.jsx` (Adobe ExtendScript CC 2019 builder for `LWX_EXE_Profile.aep`)

### Regenerating Source Plates & GIFs
```bash
python after-effects/compositions/pixel_art_engine.py
```

### Rebuilding `after-effects/LWX_EXE_Profile.aep` Headlessly (AE CC 2019)
```powershell
& "C:\Program Files\Adobe\Adobe After Effects CC 2019\Support Files\AfterFX.com" -noui -r "c:\Users\Evandro\Downloads\portfólio_bots\LlewxamDev\after-effects\compositions\build_aep_project.jsx"
```
This opens After Effects CC 2019 (`v16.0`) in `-noui` mode, imports all multi-plane PNG plates into `01_SOURCE_PLATES`, constructs all 9 independent compositions (`COMP_01_HERO` through `COMP_09_FOOTER`) inside `02_COMPOSITIONS`, configures the render queue, exports still verification PNGs to `after-effects/renders/`, and saves `after-effects/LWX_EXE_Profile.aep`.
