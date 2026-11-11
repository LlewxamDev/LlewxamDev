# MINIMAL TECH SHOWCASE — DESIGN SYSTEM & ART DIRECTION (`@LlewxamDev`)

> **Nota sobre Branches:**
> - **`main` (Atual):** Direção **Minimal Tech Showcase (Crimson & Obsidian Edition)** — portfólio técnico enxuto, sofisticado e orientado a entrevistas de engenharia.
> - **`sonic-exe-showcase`:** Edição temática **PROJECT LWX.EXE (Classic Sonic / Sonic.EXE 16-Bit Showcase)** preservada integralmente com todos os seus sprites, troféus e composições.

---

## 1. Visão Artística e Conceito Central

A direção **Minimal Tech Showcase** foi projetada para que recrutadores técnicos, tech leads e engenheiros compreendam imediatamente quem é **Evandro Silva Amorim (`@LlewxamDev`)**, quais tecnologias domina na prática e quais problemas reais seus sistemas resolvem:

1. **Fundo Escuro Exclusivo no Banner e Demos:** Sem tentar controlar o fundo inteiro do GitHub, garantindo integração limpa tanto no GitHub Dark Mode quanto no Light Mode.
2. **Paleta Minimalista Vermelho & Preto Sofisticado (Crimson & Obsidian):**
   - **Obsidian Void (`#09090C`) & Graphite Surface (`#111116` / `#17171F`)** para superfícies técnicas.
   - **Sophisticated Crimson (`#E11D48` / `#FF2E5C`)** como único destaque cromático de precisão.
   - **Alabaster White (`#F4F4F6`) & Technical Silver (`#A8A8B3`)** para tipografia limpa e contraste superior a 10:1 (WCAG AAA).
3. **Animações Pontuais e Funcionais (Sem Poluição Visual):**
   - **Banner Superior (`assets/minimal/hero-banner.gif`):** Movimento lento e contínuo de trilhas de circuito e conexões nodais em carmesim, com apenas o título principal em destaque. Remover subtítulos, descrições e texto repetido; sem efeito de digitação infinito e sem elementos piscando.
   - **Projetos em Destaque (`assets/minimal/demo-*.gif`):** Demonstrações curtas e leves (< 350 KB nas interfaces de console) exibindo os sistemas funcionando na prática.

4. **Regra CIE para o banner:** O Creative Intelligence Engine deve tratar o banner como uma peça de identidade visual, não como área de conteúdo. Manter o título principal com destaque e remover somente os textos auxiliares ou repetidos que já aparecem no README.

---

## 2. Pipeline Adobe Photoshop 2022 & After Effects CC 2019

- **Adobe Photoshop 2022 (`photoshop/`):**
  - `photoshop/LLEW_Minimal_Hero_Banner.psd`: Documento master multi-camadas (`1200 × 340`) com camadas independentes para o fundo Obsidian + Rim Light Carmesim, trilhas de circuito arquitetônicas e tipografia.
  - `photoshop/LLEW_Minimal_Project_Showcase.psd`: Documento master multi-camadas (`640 × 360`) com os painéis dos 5 projetos principais.
  - `photoshop/build_minimal_showcase_psd.jsx`: Script ExtendScript para reconstrução automatizada no Photoshop.
- **Adobe After Effects CC 2019 (`after-effects/`):**
  - `after-effects/LLEW_Minimal_Tech_Showcase.aep`: Projeto editável com câmera 2.5D multi-plano, keyframes Bezier e efeitos nativos (`ADBE Glo2`), gerado via `after-effects/compositions/build_minimal_showcase_aep.jsx`.

## 3. Conteúdo e evidência

- As tecnologias devem ser divididas em quatro categorias e exibidas com logos: linguagens principais; back-end, APIs e dados; front-end e gráficos; ferramentas e ambiente.
- A lista deve representar as tecnologias mais utilizadas e evitar tecnologias que não sejam relevantes para apresentação profissional.
- Demos de projetos devem ser descritas como execução/registro do repositório, nunca como criação de um projeto quando apenas houve clonagem, execução e gravação.
- Soul-List e LWX Lab usam uma única imagem composta, dividida em duas metades lado a lado, para evitar falhas de renderização do GitHub com duas imagens aninhadas.
- HyperFlow 3D deve ser demonstrado no Blender; Polybech deve mostrar apenas a execução dos benchmarks e os resultados finais.
- A seção final deve separar tecnologias em aprendizado das tecnologias mais utilizadas e exibir logos também nessa seção.
