# PROJECT LWX.EXE — AFTER EFFECTS ANIMATION & PRODUCTION GUIDE

## 1. Estratégia de Produção e Hardware

- **Ambiente**: Adobe After Effects CC 2019 (`v16.0`) instalado localmente em `C:\Program Files\Adobe\Adobe After Effects CC 2019\Support Files`.
- **Hardware Auditado**: Intel Core i3-3110M (2.40 GHz) · 8 GB RAM · Intel HD Graphics 4000.
- **Estratégia de Engenharia de Render**:
  - Todas as camadas-fonte (`after-effects/assets-source/`) são geradas em pixel-art 16-bit nítida com canal Alpha transparente (nearest-neighbor).
  - O projeto principal editável `after-effects/LWX_EXE_Profile.aep` organiza todas as 9 composições principais (`COMP_01_HERO` a `COMP_09_FOOTER`) e precompositions reutilizáveis em camadas independentes, com keyframes Bezier, máscaras, Displacement Maps, Wave Warp, Venetian Blinds (CRT scanlines), câmera 2.5D e ajustes de iluminação.
  - Os GIFs finais em `assets/` são otimizados com paleta adaptativa global + dithering controlado para manter nitidez de pixel art e carregamento rápido no GitHub README.

---

## 2. Arquitetura de Composições (`LWX_EXE_Profile.aep`)

| Composição | Dimensões | FPS | Duração | Descrição Técnica |
| :--- | :--- | :--- | :--- | :--- |
| `COMP_01_HERO` | `1200 × 400` | `25 fps` | `4.00s` (100f) | Sonic clássico sorrindo em loop na Green Hill Zone; em `t = 2.36s` ocorre uma interferência de **80 ms (2 frames)** que substitui o personagem pela versão Classic Sonic.EXE no exato mesmo enquadramento, retornando sem corte perceptível. Texto único: **`OLHE MEU PERFIL.`** |
| `COMP_02_IDENTITY` | `1200 × 320` | `20 fps` | `4.00s` (80f) | Apresentação gráfica limpa sem terminal/editor: Sonic clássico em animação idle (respiração, piscada natural, desvio sutil do olhar e micro-interferência de 1 frame) ao lado do quadro enxuto com nome e atuação real (`EVANDRO · FULL-STACK DEVELOPER & 2D/3D ANIMATOR`). |
| `COMP_03_DIVIDERS` | `1200 × 80` | `20 fps` | `3.00s` (60f) | Contém as 3 sub-composições de divisores: **A. Golden Ring** (rotação + corrupção vermelha breve), **B. Corrupted Ring** (falha de pixels e desaparecimento/reconstrução), **C. Green Hill Transition** (faixa de cenário com glitch rápido). |
| `COMP_04_PROJECTS` | `1200 × 220` | `20 fps` | `3.50s` (70f) | Banner de abertura do mostruário de projetos em estilo menu *Data Select* + composições de cards animados (`580 × 250`) e botões gráficos (`280 × 54`) para os projetos públicos reais. |
| `COMP_05_TECH_LANGUAGES` | `1200 × 440` | `20 fps` | `4.00s` (80f) | Cenário multi-plano Green Hill Zone corrompida (céu, montanhas, cachoeira, palmeiras com brisa sutil, criaturas estáticas discretas sem gore no plano de fundo e monitores 16-bit) exibindo as 11 linguagens reais do perfil. |
| `COMP_06_TECH_ECOSYSTEM` | `1200 × 420` | `20 fps` | `4.00s` (80f) | Segundo setor da Green Hill Zone com variação de iluminação crepuscular/carmesim e monitores integrados para os 13 itens do ecossistema JavaScript/TypeScript. |
| `COMP_07_TECH_TOOLS` | `1200 × 420` | `20 fps` | `4.00s` (80f) | Terceiro setor da Green Hill Zone com parallax e interferência periódica, abrigando os 15 itens de Web, Bancos de Dados, DevOps e Softwares Criativos. |
| `COMP_08_TROPHY_SELECTION` | `1200 × 180` | `20 fps` | `3.50s` (70f) | Cabeçalho animado da seção `TROPHY SELECTION` sincronizado visualmente com o renderizador SVG dinâmico (`trophy-engine/`). |
| `COMP_09_FOOTER` | `1200 × 150` | `20 fps` | `3.50s` (70f) | Composição final compacta em linguagem de menu do Sonic.EXE + botões gráficos clicáveis para GitHub, Portfolio e LinkedIn. |

---

## 3. Efeitos Nativos Utilizados (Compatibilidade AE 2019)

Para garantir abertura 100% livre de erros em qualquer instalação do **After Effects CC 2019** sem exigir compras externas:
- `ADBE Displacement Map` (Deslocamento horizontal de pixels durante os frames de corrupção `.EXE`)
- `ADBE Wave Warp` (Movimento orgânico sutil nas folhas das palmeiras e reflexos da água da Green Hill)
- `ADBE Turbulent Displace` (Distorção localizada no pulso de transição)
- `ADBE Venetian Blinds` (Scanlines de monitor CRT retrô)
- `ADBE Glo2` (Brilho vermelho nas pupilas do Sonic.EXE e nos anéis dourados; compatível nativamente, podendo opcionalmente receber `Deep Glow 2` instalado na máquina)
- `ADBE HUE SATURATION` & `ADBE CurvesCustom` (Transição entre a paleta alegre da Green Hill e a atmosfera dessaturada/carmesim)
