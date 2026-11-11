# MINIMAL TECH SHOWCASE — AFTER EFFECTS & PHOTOSHOP PRODUCTION GUIDE

## 1. Arquitetura de Produção (Photoshop 2022 + After Effects CC 2019)

- **Adobe Photoshop 2022 (`photoshop/`):**
  - `LLEW_Minimal_Hero_Banner.psd` (`1200 × 340`, RGBA Multi-Layer):
    - `01_OBSIDIAN_AND_CRIMSON_RIM` — Fundo Obsidian (`#09090C`) com malha técnica de 32px e luz de recorte atmosférica carmesim (`#E11D48`).
    - `02_CIRCUIT_TRACES_LAYER` — Trilhas de circuito arquitetônicas em grafite e terminais carmesim.
    - `03_TYPOGRAPHY_EVANDRO_SILVA` — Tipografia limpa e hierarquizada com chips das tecnologias principais.
  - `LLEW_Minimal_Project_Showcase.psd` (`640 × 360`, RGBA Multi-Layer):
    - Camadas independentes para os 5 projetos em destaque (`AegisCore`, `AegisHub`, `Soul-List & LWX Lab`, `HyperFlow 3D & Polybech`, `LLEWXAM.ME WebGL`).
- **Adobe After Effects CC 2019 (`after-effects/LLEW_Minimal_Tech_Showcase.aep`):**
  - Construído automatizadamente por `after-effects/compositions/build_minimal_showcase_aep.jsx`.
  - Utiliza apenas dois pontos focais de animação discreta no README:
    1. `COMP_01_HERO_MINIMAL_CRIMSON` (`1200 × 340`, `18 fps`, loop contínuo de `3.0s`): câmera 2.5D multi-plano, pulsos luminosos carmesim percorrendo trilhas de circuito e conexões nodais com movimento senoidal suave.
    2. `COMP_02` a `COMP_06` (`640 × 360`, `16 fps`, loops leves de `3.0s`): demonstrações funcionais dos projetos reais operando em tempo real.
