/**
 * ============================================================================
 * PROJECT LWX.EXE — SONIC.EXE TROPHY SELECTION SVG RENDERER
 * ============================================================================
 * Renders the custom "TROPHY SELECTION" screen inspired by the Sonic.EXE
 * selection menu, using custom sprite slots (without Sonic characters or
 * emojis) and preserving all original GinWU05/github-profile-trophy ranks,
 * titles, and calculations.
 * ============================================================================
 */

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import {
  RANK,
  Trophy,
  TrophyList,
  UserInfo,
  WantFlags,
  DEFAULT_WANT_FLAGS,
} from "./trophy-core.js";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

export interface SpriteSlotEntry {
  spritePath: string;
  unitLabel: string;
  slotCode: string;
}

export interface SpriteSlotsConfig {
  defaultSelectedTrophy: string;
  slots: Record<string, SpriteSlotEntry>;
}

export interface RenderOptions {
  username: string;
  titles?: string[];
  ranks?: string[];
  column?: number;
  row?: number;
  selected?: string;
  want?: WantFlags;
}

function escapeXml(unsafe: string): string {
  return String(unsafe)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&apos;");
}

function loadSpriteSlotsConfig(): SpriteSlotsConfig {
  const candidates = [
    path.resolve(__dirname, "config", "sprite-slots.json"),
    path.resolve(process.cwd(), "src", "config", "sprite-slots.json"),
    path.resolve(process.cwd(), "trophy-engine", "src", "config", "sprite-slots.json"),
  ];
  for (const p of candidates) {
    if (fs.existsSync(p)) {
      try {
        return JSON.parse(fs.readFileSync(p, "utf8")) as SpriteSlotsConfig;
      } catch {
        // continue
      }
    }
  }
  return {
    defaultSelectedTrophy: "Repositories",
    slots: {},
  };
}

function tryLoadCustomSpriteDataUri(relPath: string): string | null {
  if (!relPath) return null;
  const candidates = [
    path.resolve(process.cwd(), relPath),
    path.resolve(process.cwd(), "..", relPath),
    path.resolve(__dirname, "..", relPath),
    path.resolve(__dirname, "..", "..", relPath),
  ];
  for (const fullPath of candidates) {
    if (fs.existsSync(fullPath)) {
      try {
        const buf = fs.readFileSync(fullPath);
        if (buf.length > 0) {
          return `data:image/png;base64,${buf.toString("base64")}`;
        }
      } catch {
        // ignore
      }
    }
  }
  return null;
}

function getRankPalette(rank: RANK): {
  badgeBg: string;
  badgeBorder: string;
  badgeText: string;
  barColor: string;
  glowColor: string;
} {
  switch (rank) {
    case RANK.SSS:
    case RANK.SS:
    case RANK.S:
      return {
        badgeBg: "#2A060D",
        badgeBorder: "#FFD800",
        badgeText: "#FFD800",
        barColor: "#FFD800",
        glowColor: "#FF0F2B",
      };
    case RANK.AAA:
    case RANK.AA:
    case RANK.A:
      return {
        badgeBg: "#1E050B",
        badgeBorder: "#FF1538",
        badgeText: "#FF4D6A",
        barColor: "#FF1538",
        glowColor: "#FF1538",
      };
    case RANK.SECRET:
      return {
        badgeBg: "#1A0726",
        badgeBorder: "#D946EF",
        badgeText: "#F0ABFC",
        barColor: "#D946EF",
        glowColor: "#D946EF",
      };
    case RANK.B:
      return {
        badgeBg: "#0A192F",
        badgeBorder: "#4C88FF",
        badgeText: "#7CA8FF",
        barColor: "#4C88FF",
        glowColor: "#1858D8",
      };
    case RANK.C:
    default:
      return {
        badgeBg: "#14141C",
        badgeBorder: "#8E7A82",
        badgeText: "#D8CFD2",
        barColor: "#28C800",
        glowColor: "#8E7A82",
      };
  }
}

/**
 * Renders either the user's custom PNG sprite (if placed in assets/trophies/...)
 * or a coherent Sonic.EXE Data Select pixel pedestal slot placeholder (NO emojis, NO Sonic characters).
 */
function renderSpriteSlotGraphic(
  cx: number,
  cy: number,
  size: number,
  trophy: Trophy,
  slotCfg: SpriteSlotEntry,
  customDataUri: string | null,
  isSelected: boolean,
): string {
  const half = size / 2;
  const x = cx - half;
  const y = cy - half;
  const pal = getRankPalette(trophy.rank);
  const frameStroke = isSelected ? "#FFD800" : "#8A0018";

  if (customDataUri) {
    return `
      <g>
        <rect x="${x}" y="${y}" width="${size}" height="${size}" fill="#070407" stroke="${frameStroke}" stroke-width="2" />
        <image x="${x + 4}" y="${y + 4}" width="${size - 8}" height="${size - 8}" href="${customDataUri}" preserveAspectRatio="xMidYMid meet" style="image-rendering: pixelated;" />
      </g>
    `;
  }

  // Coherent 16-Bit Data Select Slot Placeholder (Pedestal + Rank Crest + Corner Reticles)
  const pedY = y + size - 18;
  return `
    <g>
      <rect x="${x}" y="${y}" width="${size}" height="${size}" fill="#070306" stroke="${frameStroke}" stroke-width="2" />
      <rect x="${x + 4}" y="${y + 4}" width="${size - 8}" height="${size - 8}" fill="#0C0509" stroke="#281018" stroke-width="1" stroke-dasharray="4 2" />
      <!-- Corner selection brackets -->
      <path d="M ${x + 6} ${y + 14} V ${y + 6} H ${x + 14}" fill="none" stroke="${pal.badgeBorder}" stroke-width="2" />
      <path d="M ${x + size - 14} ${y + 6} H ${x + size - 6} V ${y + 14}" fill="none" stroke="${pal.badgeBorder}" stroke-width="2" />
      <path d="M ${x + 6} ${y + size - 14} V ${y + size - 6} H ${x + 14}" fill="none" stroke="${pal.badgeBorder}" stroke-width="2" />
      <path d="M ${x + size - 14} ${y + size - 6} H ${x + size - 6} V ${y + size - 14}" fill="none" stroke="${pal.badgeBorder}" stroke-width="2" />
      <!-- 16-bit Pixel Trophy Pedestal Silhouette (Placeholder for user's custom sprite) -->
      <rect x="${cx - 20}" y="${pedY}" width="40" height="6" fill="#5A2800" stroke="#C86400" stroke-width="1" />
      <rect x="${cx - 14}" y="${pedY - 5}" width="28" height="5" fill="#8A3E00" />
      <!-- Pixel Trophy Cup / Emblem Geometry -->
      <polygon points="${cx - 14},${y + 16} ${cx + 14},${y + 16} ${cx + 10},${pedY - 12} ${cx - 10},${pedY - 12}" fill="${pal.badgeBg}" stroke="${pal.badgeBorder}" stroke-width="2" />
      <rect x="${cx - 4}" y="${pedY - 12}" width="8" height="7" fill="${pal.badgeBorder}" />
      <text x="${cx}" y="${y + 33}" text-anchor="middle" class="px-rank" fill="${pal.badgeText}" font-size="11">${escapeXml(trophy.rank)}</text>
      <text x="${cx}" y="${pedY + 13}" text-anchor="middle" class="px-tiny" fill="#7A646C" font-size="7">${escapeXml(slotCfg.slotCode)}</text>
    </g>
  `;
}

export function renderTrophySelectionSVG(
  userInfo: UserInfo,
  options: RenderOptions,
): string {
  const config = loadSpriteSlotsConfig();
  const trophyList = new TrophyList(userInfo, options.want ?? DEFAULT_WANT_FLAGS);

  trophyList.filterByHidden();

  if (options.titles && options.titles.length > 0) {
    trophyList.filterByTitles(options.titles);
  }
  if (options.ranks && options.ranks.length > 0) {
    trophyList.filterByRanks(options.ranks);
  }

  trophyList.sortByRank();

  const trophies = trophyList.getArray.slice(0, 8);
  const selectedQuery = (
    options.selected ||
    config.defaultSelectedTrophy ||
    "Repositories"
  ).toLowerCase();

  let selectedTrophy: Trophy =
    trophies.find(
      (t) =>
        t.title.toLowerCase() === selectedQuery ||
        t.filterTitles.some((ft) => ft.toLowerCase() === selectedQuery),
    ) ||
    trophies.find((t) => t.title === "Repositories") ||
    trophies[0] ||
    new Trophy(0, []);

  const W = 1200;
  const H = 560;

  // Grid geometry (4 columns x 2 rows on the left: x=32..792)
  const cols = 4;
  const slotW = 180;
  const slotH = 204;
  const gapX = 14;
  const gapY = 16;
  const gridStartX = 32;
  const gridStartY = 98;

  const slotCardsSvg = trophies
    .map((trophy, idx) => {
      const col = idx % cols;
      const row = Math.floor(idx / cols);
      const sx = gridStartX + col * (slotW + gapX);
      const sy = gridStartY + row * (slotH + gapY);

      const isSelected = trophy.title === selectedTrophy.title;
      const slotCfg: SpriteSlotEntry = config.slots[trophy.title] || {
        spritePath: `assets/trophies/${trophy.title.toLowerCase()}.png`,
        unitLabel: trophy.title.toUpperCase(),
        slotCode: `SLOT 0${idx + 1}`,
      };
      const customUri = tryLoadCustomSpriteDataUri(slotCfg.spritePath);
      const pal = getRankPalette(trophy.rank);
      const pct = Math.round(trophy.calculateNextRankPercentage() * 100);
      const barFillW = Math.max(4, Math.round(((slotW - 28) * pct) / 100));

      const outerStroke = isSelected ? "#FFD800" : "#8A0018";
      const outerWidth = isSelected ? "2.5" : "1.8";
      const headerBg = isSelected ? "#2C0710" : "#16060B";

      return `
        <g transform="translate(${sx}, ${sy})">
          <!-- Slot Frame -->
          <rect x="0" y="0" width="${slotW}" height="${slotH}" fill="#0B0508" stroke="${outerStroke}" stroke-width="${outerWidth}" />
          <rect x="4" y="4" width="${slotW - 8}" height="${slotH - 8}" fill="none" stroke="${isSelected ? "#FF1538" : "#261018"}" stroke-width="1" />
          <!-- Slot Top Bar -->
          <rect x="6" y="6" width="${slotW - 12}" height="22" fill="${headerBg}" />
          <text x="12" y="21" class="px-meta" fill="${isSelected ? "#FFD800" : "#B89EA6"}" font-size="10">${escapeXml(slotCfg.slotCode)}</text>
          <!-- Rank Pill -->
          <rect x="${slotW - 58}" y="8" width="48" height="18" fill="${pal.badgeBg}" stroke="${pal.badgeBorder}" stroke-width="1.2" />
          <text x="${slotW - 34}" y="20" text-anchor="middle" class="px-rank" fill="${pal.badgeText}" font-size="10">${escapeXml(trophy.rank)}</text>

          <!-- Custom Sprite Slot Viewport -->
          ${renderSpriteSlotGraphic(slotW / 2, 76, 76, trophy, slotCfg, customUri, isSelected)}

          <!-- Original Achievement Title -->
          <text x="${slotW / 2}" y="132" text-anchor="middle" class="px-title" fill="#FFFFFF" font-size="13">${escapeXml(trophy.title.toUpperCase())}</text>
          <!-- Original Rank Condition Message -->
          <text x="${slotW / 2}" y="150" text-anchor="middle" class="px-sub" fill="${pal.badgeText}" font-size="10.5">${escapeXml(trophy.topMessage)}</text>
          <!-- Real Score & Exact Metric -->
          <text x="${slotW / 2}" y="168" text-anchor="middle" class="px-score" fill="#E8DFE2" font-size="11">${escapeXml(trophy.bottomMessage)} · ${trophy.score} ${escapeXml(slotCfg.unitLabel)}</text>

          <!-- Next Rank Progress Bar -->
          <rect x="14" y="180" width="${slotW - 28}" height="8" fill="#180B10" stroke="#381620" stroke-width="1" />
          <rect x="14" y="180" width="${barFillW}" height="8" fill="${pal.barColor}" />
        </g>
      `;
    })
    .join("\n");

  // Inspector Panel on Right (x=812..1168, y=98..522)
  const inspX = 812;
  const inspY = 98;
  const inspW = 356;
  const inspH = 424;
  const selCfg: SpriteSlotEntry = config.slots[selectedTrophy.title] || {
    spritePath: `assets/trophies/${selectedTrophy.title.toLowerCase()}.png`,
    unitLabel: selectedTrophy.title.toUpperCase(),
    slotCode: "SELECTED",
  };
  const selCustomUri = tryLoadCustomSpriteDataUri(selCfg.spritePath);
  const selPal = getRankPalette(selectedTrophy.rank);
  const selPct = Math.round(selectedTrophy.calculateNextRankPercentage() * 100);
  const selNext = selectedTrophy.getNextRankInfo();
  const selBarW = Math.max(6, Math.round(((inspW - 56) * selPct) / 100));

  return `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" role="img" aria-label="TROPHY SELECTION — @${escapeXml(options.username)}">
  <defs>
    <pattern id="crtScanlines" width="4" height="3" patternUnits="userSpaceOnUse">
      <rect width="4" height="1" fill="#000000" opacity="0.28" />
    </pattern>
    <pattern id="ghzCheckTrim" width="32" height="16" patternUnits="userSpaceOnUse">
      <rect x="0" y="0" width="16" height="16" fill="#5A2600" />
      <rect x="16" y="0" width="16" height="16" fill="#321200" />
    </pattern>
    <style>
      .px-head { font-family: 'Press Start 2P', 'VT323', 'Courier New', monospace; font-weight: 900; letter-spacing: 2px; }
      .px-title { font-family: 'JetBrains Mono', 'Consolas', 'Courier New', monospace; font-weight: 800; letter-spacing: 1px; }
      .px-rank { font-family: 'JetBrains Mono', 'Consolas', 'Courier New', monospace; font-weight: 900; letter-spacing: 1px; }
      .px-sub { font-family: 'JetBrains Mono', 'Consolas', 'Courier New', monospace; font-weight: 700; }
      .px-score { font-family: 'JetBrains Mono', 'Consolas', 'Courier New', monospace; font-weight: 700; }
      .px-meta { font-family: 'JetBrains Mono', 'Consolas', 'Courier New', monospace; font-weight: 700; letter-spacing: 1px; }
      .px-tiny { font-family: 'JetBrains Mono', 'Consolas', 'Courier New', monospace; font-weight: 700; letter-spacing: 0.5px; }
      @keyframes pulseBorder {
        0%, 100% { stroke-opacity: 1; }
        50% { stroke-opacity: 0.45; }
      }
      @keyframes cursorBlink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.25; }
      }
      .pulse-stroke { animation: pulseBorder 2.2s infinite ease-in-out; }
      .cursor-arrow { animation: cursorBlink 1.1s infinite steps(2, end); }
    </style>
  </defs>

  <!-- Abyssal Sonic.EXE Menu Void Background -->
  <rect width="${W}" height="${H}" fill="#050305" />
  <rect x="14" y="14" width="${W - 28}" height="${H - 28}" fill="#080407" stroke="#8A0018" stroke-width="3" />
  <rect x="20" y="20" width="${W - 40}" height="${H - 40}" fill="none" stroke="#2C0D16" stroke-width="1.5" />

  <!-- Top Menu Header Bar -->
  <rect x="32" y="28" width="${W - 64}" height="54" fill="#12050A" stroke="#FF1538" stroke-width="2" />
  <polygon points="52,48 64,55 52,62" fill="#FFD800" class="cursor-arrow" />
  <text x="76" y="61" class="px-head" fill="#FFD800" font-size="20">TROPHY SELECTION</text>
  <text x="${W - 48}" y="52" text-anchor="end" class="px-meta" fill="#FF4D6A" font-size="12">USER: @${escapeXml(options.username.toUpperCase())}</text>
  <text x="${W - 48}" y="69" text-anchor="end" class="px-tiny" fill="#9E8C92" font-size="10">ENGINE: GINWU05/GITHUB-PROFILE-TROPHY · VERIFIED THRESHOLDS</text>

  <!-- Left 4x2 Trophy Selection Grid -->
  ${slotCardsSvg}

  <!-- Right Selected Trophy Inspector Panel (Sonic.EXE Data Select Inspector) -->
  <g transform="translate(${inspX}, ${inspY})">
    <rect x="0" y="0" width="${inspW}" height="${inspH}" fill="#0D0509" stroke="#FFD800" stroke-width="2.5" class="pulse-stroke" />
    <rect x="6" y="6" width="${inspW - 12}" height="${inspH - 12}" fill="none" stroke="#FF1538" stroke-width="1.2" />

    <!-- Inspector Header -->
    <rect x="8" y="8" width="${inspW - 16}" height="32" fill="#26060E" />
    <polygon points="20,19 29,24 20,29" fill="#FFD800" class="cursor-arrow" />
    <text x="36" y="28" class="px-title" fill="#FFD800" font-size="12">SELECTED TROPHY DATA</text>
    <text x="${inspW - 18}" y="28" text-anchor="end" class="px-meta" fill="#FF4D6A" font-size="11">${escapeXml(selCfg.slotCode)}</text>

    <!-- Large Custom Sprite Slot Preview (116x116) -->
    ${renderSpriteSlotGraphic(inspW / 2, 112, 112, selectedTrophy, selCfg, selCustomUri, true)}

    <!-- Primary 3-Line Readout (Exact format from Section 10 specification) -->
    <rect x="20" y="182" width="${inspW - 40}" height="108" fill="#070306" stroke="#8A0018" stroke-width="1.5" />
    <text x="${inspW / 2}" y="210" text-anchor="middle" class="px-title" fill="#FFFFFF" font-size="16">${escapeXml(selectedTrophy.topMessage.toUpperCase())}</text>
    <line x1="40" y1="222" x2="${inspW - 40}" y2="222" stroke="#4A0A18" stroke-width="1.5" />
    <text x="${inspW / 2}" y="248" text-anchor="middle" class="px-head" fill="#FFD800" font-size="17">${selectedTrophy.score} ${escapeXml(selCfg.unitLabel)}</text>
    <rect x="${inspW / 2 - 58}" y="260" width="116" height="22" fill="${selPal.badgeBg}" stroke="${selPal.badgeBorder}" stroke-width="1.5" />
    <text x="${inspW / 2}" y="275" text-anchor="middle" class="px-rank" fill="${selPal.badgeText}" font-size="13">RANK ${escapeXml(selectedTrophy.rank)}</text>

    <!-- Secondary Telemetry & Progress to Next Rank -->
    <text x="24" y="314" class="px-meta" fill="#D8CFD2" font-size="11">CATEGORY: ${escapeXml(selectedTrophy.title.toUpperCase())} (${escapeXml(selectedTrophy.bottomMessage)})</text>
    <text x="24" y="334" class="px-meta" fill="#9E8C92" font-size="11">NEXT RANK: ${escapeXml(selNext.nextRank)}${selNext.requiredScore !== null ? ` (REQ: ${selNext.requiredScore} ${escapeXml(selCfg.unitLabel)})` : " (MAX TIER UNLOCKED)"}</text>

    <rect x="24" y="346" width="${inspW - 48}" height="14" fill="#18090E" stroke="#5A1222" stroke-width="1.2" />
    <rect x="28" y="349" width="${selBarW}" height="8" fill="${selPal.barColor}" />
    <text x="${inspW - 24}" y="375" text-anchor="end" class="px-tiny" fill="#FFD800" font-size="10">PROGRESS: ${selPct}%</text>

    <!-- Custom Sprite Slot File Binding Info -->
    <rect x="20" y="384" width="${inspW - 40}" height="26" fill="#12060A" stroke="#38121C" stroke-width="1" />
    <text x="${inspW / 2}" y="401" text-anchor="middle" class="px-tiny" fill="#8E7A82" font-size="9.5">SLOT: ${escapeXml(selCfg.spritePath)}</text>
  </g>

  <!-- Subtle Corrupted Green Hill Checkerboard Bottom Trim -->
  <rect x="22" y="${H - 30}" width="${W - 44}" height="8" fill="url(#ghzCheckTrim)" opacity="0.75" />
  <rect x="22" y="${H - 33}" width="${W - 44}" height="3" fill="#2A4018" />

  <!-- Global CRT Scanline Overlay -->
  <rect width="${W}" height="${H}" fill="url(#crtScanlines)" pointer-events="none" />
</svg>`;
}

export function renderErrorSVG(title: string, detail: string): string {
  return `<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="220" viewBox="0 0 1200 220" role="img" aria-label="Trophy Renderer Notice">
  <rect width="1200" height="220" fill="#050305" />
  <rect x="16" y="16" width="1168" height="188" fill="#0D0509" stroke="#FF1538" stroke-width="2.5" />
  <text x="600" y="88" text-anchor="middle" font-family="monospace" font-weight="900" font-size="22" fill="#FFD800">TROPHY SELECTION — ${escapeXml(title)}</text>
  <text x="600" y="130" text-anchor="middle" font-family="monospace" font-size="14" fill="#E8DFE2">${escapeXml(detail)}</text>
</svg>`;
}
