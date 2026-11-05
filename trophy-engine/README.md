# LWX.EXE Trophy Selection Engine (`trophy-engine`)

Custom GitHub Profile Trophy renderer engineered for **PROJECT LWX.EXE** (`@LlewxamDev`), inspired by the **Classic Sonic.EXE (2011)** selection screen and **Sega Mega Drive 16-bit** HUD aesthetics while preserving 100% of the calculation logic, rank thresholds, titles, and secret conditions of [`GinWU05/github-profile-trophy`](https://github.com/GinWU05/github-profile-trophy) (originally by [`ryo-ma/github-profile-trophy`](https://github.com/ryo-ma/github-profile-trophy)) under the MIT License.

---

## Architecture & Visual Design

- **Header**: `TROPHY SELECTION` rendered in authentic 16-bit golden/crimson pixel typography.
- **Selectable Trophy Slots (4x2 Grid)**:
  - Each slot represents a real GitHub achievement category (`Commit`, `Repository`, `Issue`, `PullRequest`, `Star`, `Followers`, plus Secret ranks `SSS Rank Hacker` and `Rainbow Lang User`).
  - Zero Sonic character portraits or generic emojis inside trophy slots — each slot loads a dedicated custom pixel sprite (`trophy-*.png`) mapped through [`src/config/sprite-slots.json`](./src/config/sprite-slots.json).
  - Rank-based frame styling (`SECRET` Crimson Glitch, `SSS`/`SS`/`S` Golden Ring, `AAA`/`AA`/`A` Silver Emblem, `B`/`C` Bronze Monitor).
  - Active selection cursor (`◄ ACTIVE SLOT ►`) with subtle scanline & CRT flicker animation.
- **Bottom Inspector HUD**:
  - Displays the highlighted trophy's real rank title (`HYPER REPO CREATOR`), exact live metric (`32 REPOSITORIES`), and rank badge (`RANK AA`), alongside live summary counters (`COMMITS: 1,138 (SS)`, `ISSUES: 41 (AA)`, `PRs: 35 (AA)`).

---

## Preserved Calculation Logic (`src/trophy-core.ts`)

All rank thresholds and secret conditions match `GinWU05/github-profile-trophy` (`src/trophy_list.ts` & `src/trophy.ts`):

| Category | Metric Source | Rank Thresholds (`SSS` / `SS` / `S` / `AAA` / `AA` / `A` / `B` / `C`) |
| :--- | :--- | :--- |
| **Commits** (`TotalCommitTrophy`) | `totalCommitContributions + restrictedContributionsCount` | `4000` / `2000` / `1000` / `500` / `200` / `100` / `10` / `1` |
| **Repositories** (`TotalRepositoryTrophy`) | `repositories.totalCount` | `50` / `45` / `40` / `35` / `30` / `20` / `10` / `1` |
| **Issues** (`TotalIssueTrophy`) | `openIssues.totalCount + closedIssues.totalCount` | `1000` / `500` / `200` / `100` / `50` / `20` / `10` / `1` |
| **PullRequests** (`TotalPullRequestTrophy`) | `pullRequests.totalCount` | `1000` / `500` / `200` / `100` / `50` / `20` / `10` / `1` |
| **Stars** (`TotalStarTrophy`) | Sum of `stargazers.totalCount` (top 100 owner repos) | `2000` / `700` / `200` / `100` / `50` / `20` / `10` / `1` |
| **Followers** (`TotalFollowerTrophy`) | `followers.totalCount` | `1000` / `400` / `200` / `100` / `50` / `20` / `10` / `1` |
| **Reviews** (`TotalReviewsTrophy`) | `totalPullRequestReviewContributions` | `70` / `57` / `45` / `30` / `20` / `10` / `3` / `1` |
| **SecretTrophies** | `AchieveSSSRank`, `MultipleLang` (`>=10`), `LongTimeAccount` (`>=10y`), `AncientAccount` (`<=2010`), `Joined2020`, `AllSuperRank`, `MultipleOrganizations` (`>=3`), `OGAccount` (`<=2008`) | `SECRET` |

---

## Custom Sprite Slots (`src/config/sprite-slots.json`)

Every trophy slot references its visual sprite via `src/config/sprite-slots.json`. To replace any trophy icon with a new custom artwork:

1. Drop the new PNG sprite (`48x48` or `64x64` transparent PNG) into `../assets/trophies/`.
2. Update the corresponding `"spritePath"` in `src/config/sprite-slots.json` (or keep the same filename to hot-swap automatically).
3. Re-run `node scripts/render-local-verify.mjs` (for static snapshot) or redeploy to Vercel.

---

## Local Verification & Vercel Deployment

### 1. Run Local Verification Snapshot
```bash
cd trophy-engine
node scripts/render-local-verify.mjs
```
This validates edge cases (e.g., `19` repositories -> `Middle Repo Creator | Rank B`) and fetches live GitHub GraphQL metrics for `@LlewxamDev`, writing `../assets/trophies/trophy-selection-live.svg`.

### 2. Deploy Serverless Endpoint on Vercel
1. Import repository `LlewxamDev/LlewxamDev` in Vercel and set **Root Directory** to `trophy-engine`.
2. Add environment variable `GITHUB_TOKEN1` (GitHub Personal Access Token with `read:user` scope).
3. Deploy. Your live endpoint will be available at:
   ```markdown
   https://<your-vercel-domain>.vercel.app/api/trophies?username=LlewxamDev
   ```
