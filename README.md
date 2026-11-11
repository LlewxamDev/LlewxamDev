<div align="center">

<a href="https://www.llewxam.me">
  <img src="./assets/minimal/hero-banner.gif" width="100%" alt="Minimal Tech Showcase — Evandro Silva Amorim" />
</a>

<br/><br/>

<p align="center">
  <a href="https://www.llewxam.me">
    <img src="./assets/minimal/nav-portfolio.svg" height="42" alt="Portfólio — llewxam.me" />
  </a>
  &nbsp;
  <a href="https://www.linkedin.com/in/evandro-silva-amorimm">
    <img src="./assets/minimal/nav-linkedin.svg" height="42" alt="LinkedIn — Evandro Silva Amorim" />
  </a>
  &nbsp;
  <a href="#03--projetos-em-destaque">
    <img src="./assets/minimal/nav-projects.svg" height="42" alt="Projetos em Destaque" />
  </a>
  &nbsp;
  <a href="https://github.com/LlewxamDev">
    <img src="./assets/minimal/nav-contact.svg" height="42" alt="GitHub — @LlewxamDev" />
  </a>
</p>

</div>

---

## `01` — Sobre mim

Estudante de **Análise e Desenvolvimento de Sistemas (ADS)** e desenvolvedor Full-Stack focado em arquiteturas assíncronas, APIs de alta performance, segurança de aplicações e automação de sistemas. Gosto de projetar soluções completas — desde plataformas de defesa web e analisadores estáticos em **TypeScript** e **Rust** até ecossistemas de bots de alta vazão e interfaces interativas em **React** e **WebGL**. Abordo problemas com mentalidade de engenharia: código limpo, tipagem estrita, baixa latência e decisões técnicas orientadas a produção.

---

## `02` — Tecnologias

Seleção das linguagens, frameworks e ferramentas mais utilizados nos meus projetos e sistemas em produção:

### Linguagens principais

<p align="left"><img src="https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white" alt="TypeScript" /> <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=111111" alt="JavaScript" /> <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" /> <img src="https://img.shields.io/badge/Rust-000000?style=for-the-badge&logo=rust&logoColor=white" alt="Rust" /> <img src="https://img.shields.io/badge/C%2B%2B-00599C?style=for-the-badge&logo=cplusplus&logoColor=white" alt="C++" /> <img src="https://img.shields.io/badge/SQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white" alt="SQL" /></p>

### Back-end, APIs & dados

<p align="left"><img src="https://img.shields.io/badge/Node.js-339933?style=for-the-badge&logo=nodedotjs&logoColor=white" alt="Node.js" /> <img src="https://img.shields.io/badge/NestJS-E0234E?style=for-the-badge&logo=nestjs&logoColor=white" alt="NestJS" /> <img src="https://img.shields.io/badge/Fastify-000000?style=for-the-badge&logo=fastify&logoColor=white" alt="Fastify" /> <img src="https://img.shields.io/badge/Express-000000?style=for-the-badge&logo=express&logoColor=white" alt="Express" /> <img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL" /> <img src="https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white" alt="Redis" /></p>

### Front-end & gráficos

<p align="left"><img src="https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB" alt="React" /> <img src="https://img.shields.io/badge/Next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white" alt="Next.js" /> <img src="https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white" alt="Vite" /> <img src="https://img.shields.io/badge/Tailwind_CSS-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white" alt="Tailwind CSS" /> <img src="https://img.shields.io/badge/Three.js-000000?style=for-the-badge&logo=threedotjs&logoColor=white" alt="Three.js" /> <img src="https://img.shields.io/badge/WebGL-990000?style=for-the-badge&logo=webgl&logoColor=white" alt="WebGL" /></p>

### Ferramentas & ambiente

<p align="left"><img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker" /> <img src="https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white" alt="Git" /> <img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub" /> <img src="https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=111111" alt="Linux" /> <img src="https://img.shields.io/badge/PowerShell-5391FE?style=for-the-badge&logo=powershell&logoColor=white" alt="PowerShell" /> <img src="https://img.shields.io/badge/Blender-E87D0D?style=for-the-badge&logo=blender&logoColor=white" alt="Blender" /></p>

---

## `03` — Projetos em destaque

### 1. AegisCore — Plataforma Híbrida de Defesa Web & Risk Scoring

<table>
  <tr>
    <td width="52%" valign="top">
      <a href="https://github.com/LlewxamDev/AegisCore">
        <img src="./assets/minimal/demo-aegiscore.gif" width="100%" alt="AegisCore — Demonstração do Motor Híbrido TypeScript + Fastify + Rust" />
      </a>
    </td>
    <td width="48%" valign="top">
      <p><strong>Problema:</strong> APIs modernas sofrem com ataques de injeção, abuso de sessão e bursts de requisições onde middlewares puramente em JS introduzem gargalos de latência.</p>
      <p><strong>Solução:</strong> Plataforma modular de defesa web que combina um gateway HTTP em <strong>Fastify</strong> com crates nativos em <strong>Rust</strong> para inspeção de payloads e cálculo de risco em sub-milissegundos.</p>
      <p><strong>Demonstração:</strong> Execução do repositório mostrando o gateway Fastify, a inspeção de payloads e o painel administrativo em funcionamento.</p>
      <p><code>TypeScript</code> · <code>Fastify</code> · <code>Rust</code> · <code>Prisma</code> · <code>Redis</code> · <code>React</code></p>
      <p>
        <a href="https://github.com/LlewxamDev/AegisCore"><strong>Repositório ↗</strong></a>
      </p>
    </td>
  </tr>
</table>

<br/>

### 2. AegisHub — Analisador Estático de Segurança para Repositórios GitHub

<table>
  <tr>
    <td width="52%" valign="top">
      <a href="https://github.com/LlewxamDev/AegisHub">
        <img src="./assets/minimal/demo-aegishub.gif" width="100%" alt="AegisHub — Scanner Estático em Rust, Orquestrador Fastify/BullMQ e Dashboard React" />
      </a>
    </td>
    <td width="48%" valign="top">
      <p><strong>Problema:</strong> Vazamento de credenciais, permissões excessivas em pipelines CI/CD e dependências vulneráveis costumam passar despercebidos antes do merge.</p>
      <p><strong>Solução:</strong> Suite de auditoria automatizada com motor de varredura em <strong>Rust</strong>, CLI dedicada, fila de orquestração em <strong>Fastify + BullMQ</strong> e dashboard analítico em <strong>React</strong>.</p>
      <p><strong>Demonstração:</strong> Execução do repositório mostrando o scanner, a fila de análise e o dashboard de pontuação de segurança.</p>
      <p><code>Rust</code> · <code>TypeScript</code> · <code>Fastify</code> · <code>BullMQ</code> · <code>Prisma</code> · <code>React</code></p>
      <p>
        <a href="https://github.com/LlewxamDev/AegisHub"><strong>Repositório ↗</strong></a>
      </p>
    </td>
  </tr>
</table>

<br/>

### 3. Soul-List & LWX Lab — Ecossistema de Bots & Automação em Tempo Real

<table>
  <tr>
    <td width="52%" valign="top">
      <a href="https://github.com/LlewxamDev/Soul-List">
        <img src="./assets/minimal/soul-list-lwx-lab.png" width="100%" alt="Soul-List e LWX Lab — logos lado a lado" />
      </a>
    </td>
    <td width="48%" valign="top">
      <p><strong>Problema:</strong> Servidores comerciais e grupos de alta concorrência exigem automação de atendimento, triagem de pedidos e execução instantânea de comandos sem bloqueio de Event Loop.</p>
      <p><strong>Solução:</strong> <strong>Soul-List</strong> (motor WhatsApp via WebSockets diretos com mais de 1.400 comandos indexados em <code>O(1)</code>) e <strong>LWX Lab</strong> (automação comercial completa no Discord com tickets, orçamentos, fila de produção e integração com IA).</p>
      <p><strong>Demonstração:</strong> O material visual usa somente as logos dos dois projetos; não representa uma nova implementação nem atribui a criação dos repositórios.</p>
      <p><code>TypeScript</code> · <code>Node.js</code> · <code>Drizzle ORM</code> · <code>Zod</code></p>
      <p>
        <a href="https://github.com/LlewxamDev/Soul-List"><strong>Repositório (Soul-List) ↗</strong></a> &nbsp;·&nbsp;
        <a href="https://www.llewxam.me"><strong>Demonstração no Portfólio ↗</strong></a>
      </p>
    </td>
  </tr>
</table>

<br/>

### 4. HyperFlow 3D & Polybech — Computação Gráfica (Blender 5.2+) & Benchmarks Poliglotas

<table>
  <tr>
    <td width="52%" valign="top">
      <a href="https://github.com/LlewxamDev/blender-hyperflow">
        <img src="./assets/minimal/demo-hyperflow-polybech.gif" width="100%" alt="HyperFlow 3D & Polybech — Suite C++/Python para Blender 5.2+ e Laboratório de Benchmarks" />
      </a>
    </td>
    <td width="48%" valign="top">
      <p><strong>Problema:</strong> Retopologia manual, ruído temporal em renderização path-tracing e comparação empírica de algoritmos entre linguagens de baixo e alto nível exigem ferramentas precisas.</p>
      <p><strong>Solução:</strong> <strong>HyperFlow 3D</strong> entrega retopologia quad guiada por curvatura, baking PBR em 1 clique e denoiser temporal com patches C++ para o Blender 5.2+; <strong>Polybech</strong> executa benchmarks comparativos entre 7 linguagens.</p>
      <p><strong>Formato da demonstração:</strong> Execução do HyperFlow diretamente no Blender; no Polybech, somente a etapa de benchmark e seus resultados finais.</p>
      <p><code>Python</code> · <code>C++</code> · <code>Rust</code> · <code>Assembly x86-64</code> · <code>TypeScript</code></p>
      <p>
        <a href="https://github.com/LlewxamDev/blender-hyperflow"><strong>Repositório (HyperFlow 3D) ↗</strong></a> &nbsp;·&nbsp;
        <a href="https://github.com/LlewxamDev/Polybech"><strong>Repositório (Polybech) ↗</strong></a>
      </p>
    </td>
  </tr>
</table>

<br/>

### 5. LLEWXAM.ME — Portfólio Interativo 2.5D em WebGL & Shaders GLSL

<table>
  <tr>
    <td width="52%" valign="top">
      <a href="https://www.llewxam.me">
        <img src="./assets/minimal/demo-portfolio-webgl.gif" width="100%" alt="LLEWXAM.ME — Portfólio Interativo 2.5D com Shaders GLSL e React" />
      </a>
    </td>
    <td width="48%" valign="top">
      <p><strong>Problema:</strong> Portfólios tradicionais costumam ser páginas estáticas padronizadas que não demonstram domínio real de engenharia front-end, programação gráfica ou arquitetura de estado.</p>
      <p><strong>Solução:</strong> Experiência web autoral construída com pipeline híbrido <strong>WebGL (GLSL Vertex & Fragment Shaders) + Canvas 2D + React 18/TypeScript</strong>, com parallax multi-plano por mapa de profundidade e player físico de flipbook sincronizado a vídeo.</p>
      <p><strong>Formato da demonstração:</strong> Personagem totalmente visível desde o início, movimento lateral do mouse para evidenciar o parallax e o cursor personalizado, finalizando após a abertura da janela de navegação.</p>
      <p><code>TypeScript</code> · <code>React</code> · <code>WebGL / GLSL</code> · <code>Canvas 2D</code> · <code>Vite</code></p>
      <p>
        <a href="https://www.llewxam.me"><strong>Demonstração Ao Vivo (llewxam.me) ↗</strong></a> &nbsp;·&nbsp;
        <a href="https://github.com/LlewxamDev/HackerPage"><strong>Ver também: HackerPage 3D ↗</strong></a>
      </p>
    </td>
  </tr>
</table>

---

## `04` — Em constante evolução

- **Atualmente aprendendo:**
  <img src="https://img.shields.io/badge/Java-E76F00?style=for-the-badge&logo=openjdk&logoColor=white" alt="Java" />
  <img src="https://img.shields.io/badge/C%2B%2B-00599C?style=for-the-badge&logo=cplusplus&logoColor=white" alt="C++" />
  <img src="https://img.shields.io/badge/C%23-68217A?style=for-the-badge&logo=csharp&logoColor=white" alt="C#" />
  <img src="https://img.shields.io/badge/Rust-000000?style=for-the-badge&logo=rust&logoColor=white" alt="Rust" />
  <img src="https://img.shields.io/badge/Kotlin-7F52FF?style=for-the-badge&logo=kotlin&logoColor=white" alt="Kotlin" />
  <img src="https://img.shields.io/badge/Assembly-6E7681?style=for-the-badge&logo=assemblyscript&logoColor=white" alt="Assembly" />

- **Arquitetura Back-end & Sistemas Escaláveis:** Aprofundando padrões de arquitetura modular, injeção de dependência, filas distribuídas e microsserviços com **NestJS**, **Fastify**, **Redis/BullMQ** e bancos relacionais.
- **Engenharia Híbrida de Alta Performance:** Expandindo a integração entre **TypeScript/Node.js** e motores nativos em **Rust** e **C++** para segurança ofensiva/defensiva, parsers de baixa latência e ferramentas de linha de comando.
- **Automação Inteligente & Computação Visual:** Explorando agentes autônomos, workflows comerciais em tempo real e pipelines gráficos acelerados por GPU (**WebGL / GLSL** e automação técnica em **Python**).

<br/>

<div align="center">
  <img src="./assets/minimal/footer-minimal.svg" width="100%" alt="Construindo, aprendendo e evoluindo — Evandro Silva Amorim (@LlewxamDev)" />
</div>
