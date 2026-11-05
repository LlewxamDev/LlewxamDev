# PROJECT LWX.EXE — DESIGN SYSTEM & ART DIRECTION

## 1. Visão Artística e Conceito Central

**PROJECT LWX.EXE** reconstrói integralmente a identidade visual do perfil GitHub de **Evandro (`@LlewxamDev`)** sob a estética do **Classic Sonic.EXE (Creepypasta original de 2011 / MY5TCrimson)** e da **Green Hill Zone (Sega Mega Drive / Genesis, 1991)** em estado de corrupção psicológica sutil.

### Regra de Ouro (Forma vs. Conteúdo)
- **A estética visual pertence ao universo de Sonic Clássico / Sonic.EXE**: sprites em 16-bit autênticos, anéis dourados e corrompidos, caixas de monitor de itens, folhagens, palmeiras, solo quadriculado da Green Hill Zone, menus inspirados na tela de *Data Select* e interferências subliminares de 60–100 ms.
- **O conteúdo textual pertence estritamente ao perfil profissional real de desenvolvedor Full-Stack & Animador 2D/3D**: sem narrativas de RPG, sem mensagens de entidade fictícia, sem termos como *PLAYER STATUS* ou *WELCOME TO MY WORLD*, e com o Hero apresentando exclusivamente **`OLHE MEU PERFIL.`**

---

## 2. Paleta Cromática Oficial

A direção de arte preserva o contraste essencial entre a superfície vibrante e nostálgica do Sonic clássico de 1991 e o vazio abissal carmesim da versão `.EXE`:

### A. Superfície Clássica (16-Bit Sega Genesis / Green Hill Normal)
| Token | Hex | Aplicação |
| :--- | :--- | :--- |
| `sonic-cobalt-base` | `#1858D8` | Pelagem principal do Sonic clássico |
| `sonic-cobalt-hi` | `#4C88FF` | Luz de recorte e brilho superior nos espinhos |
| `sonic-cobalt-shadow` | `#0C2478` | Sombras profundas da silhueta |
| `sonic-muzzle-peach` | `#F8B880` | Focinho, braços e pálpebras |
| `ghz-sky-azure` | `#2048C8` | Céu diurno superior da Green Hill Zone |
| `ghz-sky-horizon` | `#5890FF` | Horizonte luminoso sobre as montanhas |
| `ghz-grass-bright` | `#28C800` | Topo da grama vibrante |
| `ghz-grass-mid` | `#008800` | Camada intermediária de vegetação |
| `ghz-soil-ochre` | `#C86400` | Blocos claros do terreno xadrez |
| `ghz-soil-umber` | `#783400` | Blocos escuros do terreno xadrez |
| `ring-gold-core` | `#FFD800` | Anéis dourados e cursores de seleção |
| `ring-gold-spec` | `#FFF890` | Brilho especular de 16-bit |

### B. Estado Corrompido (Classic Sonic.EXE 2011 / Menu Select)
| Token | Hex | Aplicação |
| :--- | :--- | :--- |
| `exe-void-black` | `#050305` | Fundo abissal, esclera do Sonic.EXE e vazios de tela |
| `exe-panel-obsidian` | `#0E070A` | Preenchimento interno dos painéis e monitores |
| `exe-pupil-crimson` | `#FF0F2B` | Pupilas emissivas do Sonic.EXE e alertas ativos |
| `exe-crimson-mid` | `#B8001C` | Bordas de seleção, molduras de menu e glitch |
| `exe-blood-dark` | `#6E000E` | Detalhes estilizados sob os olhos e sombras carmesim |
| `exe-fur-midnight` | `#0B1D52` | Pelagem escurecida na transformação `.EXE` |
| `ghz-corrupt-moss` | `#2A3818` | Grama dessaturada durante interferências |
| `ghz-corrupt-soil` | `#26120B` | Terreno escurecido durante falhas de cenário |
| `ui-text-crisp` | `#F2ECEE` | Tipografia principal de alta legibilidade |
| `ui-text-muted` | `#9E8C92` | Subtítulos técnicos e metadados reais |

---

## 3. Tipografia e Hierarquia

- **Display / Títulos de Seção e Menus (`16-Bit Pixel Grid`)**:
  - Desenhados sobre matriz de pixels inteiros inspirada nas fontes de HUD do Mega Drive (*Sonic the Hedgehog* Title Card / *Data Select*).
  - Aplicada em `OLHE MEU PERFIL.`, cabeçalhos de seção (`PROJECTS`, `LANGUAGES`, `JS / TS ECOSYSTEM`, `WEB / DATA / CREATIVE TOOLS`, `TROPHY SELECTION`) e botões de ação.
- **Dados Técnicos e Leitura Rápida (`Monospace Pixel-Clean`)**:
  - Pilha tipográfica SVG/ Sistema: `'Press Start 2P', 'VT323', 'JetBrains Mono', 'Consolas', monospace`.
  - Textos curtos, diretos, em caixa alta controlada, garantindo contraste superior a 7:1 (WCAG AAA) sobre os fundos `#050305` e `#0E070A`.

---

## 4. Linguagem de Interface, Monitores e Botões

1. **Botões de Menu (`Sonic.EXE Menu Buttons`)**:
   - Proporção retangular clássica com chanfro pixelado duplo (borda externa `#6E000E`, filete interno `#FF0F2B` / `#FFD800`, fundo `#0E070A`).
   - Marcador lateral em seta pixelada (`►`) com micro-pulsação e varredura de scanline CRT.
   - Exportados como imagens independentes (`.gif` / `.png`) envolvidas por links Markdown (`[![Label](path)](url)`), garantindo funcionamento nativo no GitHub README sem depender de JavaScript.
2. **Monitores de Tecnologias (`Green Hill Item Monitors`)**:
   - Em vez de badges genéricas coladas sobre o fundo, cada linguagem, framework e ferramenta é abrigada em uma **Caixa de Monitor CRT 16-bit** (inspirada nos monitores de item de *Sonic 1*) integrada ao solo quadriculado da Green Hill Zone.
3. **Tela de Seleção de Troféus (`TROPHY SELECTION`)**:
   - Estruturada sobre o layout da tela de seleção do Sonic.EXE, onde cada slot representa uma conquista real calculada pelo motor original (`GinWU05/github-profile-trophy`), exibindo o sprite customizável da conquista, seu título original, rank (`SSS` a `C` / `SECRET`) e painel lateral de inspeção detalhada.
