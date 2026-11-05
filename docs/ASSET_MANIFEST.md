# PROJECT LWX.EXE — Asset Manifest & Composition Map

Complete catalog of source plates, After Effects compositions, animated GIFs, clickable menu buttons, and SVG engines produced on branch `feat/lwx-exe-profile`.

---

## 1. Adobe After Effects Master Project (`after-effects/`)

- **Master Project**: `after-effects/LWX_EXE_Profile.aep` (Adobe After Effects CC 2019 `v16.0x235`, 100% native effects, no paid third-party plugins)
- **Automated Builder**: `after-effects/compositions/build_aep_project.jsx`
- **Multi-Plane Plate & GIF Compiler**: `after-effects/compositions/pixel_art_engine.py`
- **Authentic Game Sprites Directory**: `after-effects/assets-source/web_authentic/*.png` (Classic Sonic, Sonic.EXE / Exetior, Green Hill Zone sky/mountains/waterfall/bushes/trees/tiles/rings)

| AE Composition | Resolution | Duration / FPS | Primary Output Asset |
| :--- | :--- | :--- | :--- |
| `COMP_01_HERO` | `1200x400` | `3.20s` @ `25fps` | `assets/hero/lwx-exe-hero.gif` |
| `COMP_02_IDENTITY` | `1200x300` | `2.70s` @ `25fps` | `assets/identity/lwx-exe-identity.gif` |
| `COMP_03_DIVIDERS` | `1200x76` | `1.92s` @ `25fps` | `assets/dividers/divider-*.gif` (3 variations) |
| `COMP_04_PROJECTS` | `1200x520` | `2.40s` @ `25fps` | `assets/projects/project-*.gif` + `btn-*.gif` |
| `COMP_05_TECH_LANGUAGES` | `1200x440` | `2.56s` @ `25fps` | `assets/technologies/tech-languages-ghz.gif` |
| `COMP_06_TECH_ECOSYSTEM` | `1200x440` | `2.56s` @ `25fps` | `assets/technologies/tech-ecosystem-ghz.gif` |
| `COMP_07_TECH_TOOLS` | `1200x460` | `2.56s` @ `25fps` | `assets/technologies/tech-tools-ghz.gif` |
| `COMP_08_TROPHY_SELECTION` | `1200x430` | Live SVG + Header | `assets/trophies/trophy-selection-live.svg` |
| `COMP_09_FOOTER` | `1200x200` | `2.40s` @ `25fps` | `assets/footer/lwx-exe-footer-banner.gif` + `btn-*.gif` |

---

## 2. Final README Assets (`assets/`)

### Hero (`assets/hero/`)
- `assets/hero/lwx-exe-hero.gif` — Normal Classic Sonic smiling inside the Golden Ring Emblem over Green Hill Zone, interrupted by a brief **80ms (`2 frames @ 40ms`)** Classic Sonic.EXE swap in the exact same framing. Text: strictly **`OLHE MEU PERFIL.`**

### Identity (`assets/identity/`)
- `assets/identity/lwx-exe-identity.gif` — Replaces `crimson-identity-terminal-v3.svg` (no terminal, no fake OS/code editor). Features authentic Classic Sonic idle animation on a Green Hill pedestal with subtle eye shifts and concise real professional developer metadata (`EVANDRO · @LLEWXAMDEV`, `FULL-STACK DEVELOPER · 2D/3D ANIMATOR`, `SYSTEMS ANALYSIS AND DEVELOPMENT (ADS)`).

### Animated Dividers (`assets/dividers/`)
- `assets/dividers/divider-golden-ring.gif` — **Variation A (Golden Ring)**: Spinning 16-bit golden ring that briefly corrupts to crimson and recovers.
- `assets/dividers/divider-corrupted-ring.gif` — **Variation B (Corrupted Ring)**: Ring scatters into glitch pixels, vanishes briefly, and reconstructs.
- `assets/dividers/divider-green-hill-transition.gif` — **Variation C (Green Hill Transition)**: Horizontal Green Hill grass & checkerboard strip with brief `.EXE` chromatic displacement.

### Projects Showcase (`assets/projects/`)
- `assets/projects/projects-header-exe.gif` — Section banner (`PROJECTS`).
- `assets/projects/card-portfolio.gif` + `assets/projects/btn-portfolio.gif` → `https://www.llewxam.me`
- `assets/projects/card-aegishub.gif` + `assets/projects/btn-aegishub.gif` → `https://github.com/LlewxamDev/AegisHub`
- `assets/projects/card-aegiscore.gif` + `assets/projects/btn-aegiscore.gif` → `https://github.com/LlewxamDev/AegisCore`
- `assets/projects/card-hackerpage.gif` + `assets/projects/btn-hackerpage.gif` → `https://github.com/LlewxamDev/HackerPage`
- `assets/projects/card-soullist.gif` + `assets/projects/btn-soullist.gif` → `https://github.com/LlewxamDev/Soul-List`
- `assets/projects/card-polybech.gif` + `assets/projects/btn-polybech.gif` → `https://github.com/LlewxamDev/Polybech`

### Technologies — Corrupted Green Hill Zone (`assets/technologies/`)
- `assets/technologies/tech-languages-ghz.gif` — 11 languages (`Python`, `JavaScript`, `TypeScript`, `PHP`, `Lua` + learning `Java`, `C++`, `C#`, `Rust`, `Kotlin`, `Assembly`) integrated as Sonic Item Monitors in Green Hill Zone.
- `assets/technologies/tech-ecosystem-ghz.gif` — 13 JS/TS ecosystem tools (`Node.js`, `React`, `Next.js`, `Vue`, `Nuxt`, `Angular`, `Svelte`, `Astro`, `Express`, `NestJS`, `Vite`, `Tailwind`, `Fastify`).
- `assets/technologies/tech-tools-ghz.gif` — 15 Web, Data & Creative tools (`HTML5`, `CSS3`, `Postgres`, `MySQL`, `SQL Server`, `Docker`, `Git`, `GitHub`, `Linux`, `VS Code`, `Visual Studio`, `Blender`, `After Effects`, `Photoshop`, `Houdini`).

### Trophy Selection & Custom Sprite Slots (`assets/trophies/`)
- `assets/trophies/trophy-selection-live.svg` — Full Sonic.EXE `TROPHY SELECTION` board with 8 custom sprite slots and bottom Inspector HUD (`HYPER REPO CREATOR` / `32 REPOSITORIES` / `RANK AA`).
- `assets/trophies/trophy-commit.png`
- `assets/trophies/trophy-repository.png`
- `assets/trophies/trophy-issue.png`
- `assets/trophies/trophy-pull-request.png`
- `assets/trophies/trophy-star.png`
- `assets/trophies/trophy-followers.png`
- `assets/trophies/trophy-secret.png`
- `assets/trophies/trophy-rank-s.png`

### Footer & Real Links (`assets/footer/`)
- `assets/footer/lwx-exe-footer-banner.gif` — Compact Sonic.EXE menu footer banner.
- `assets/footer/btn-github.gif` → `https://github.com/LlewxamDev`
- `assets/footer/btn-portfolio.gif` → `https://www.llewxam.me`
- `assets/footer/btn-linkedin.gif` → `https://www.linkedin.com/in/evandro-silva-amorimm`
