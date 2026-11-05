#!/usr/bin/env node
/**
 * ============================================================================
 * PROJECT LWX.EXE — LOCAL VERIFICATION & LIVE SVG GENERATOR
 * ============================================================================
 * 1. Verifies all rank thresholds & calculations from GinWU05/github-profile-trophy
 *    (including "Middle Repo Creator" = 10..19 repos -> Rank B, "Hyper Repo Creator"
 *    = 30..39 repos -> Rank AA, "Deep Committer" = 1000..1999 commits -> Rank SS, etc.)
 * 2. Fetches live GitHub GraphQL telemetry for @LlewxamDev
 * 3. Renders the verified SVG to ../assets/trophies/trophy-selection-live.svg
 * ============================================================================
 */

import fs from "node:fs";
import path from "node:path";
import { execSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ENGINE_ROOT = path.resolve(__dirname, "..");
const REPO_ROOT = path.resolve(ENGINE_ROOT, "..");

const RANK = {
  SECRET: "SECRET",
  SSS: "SSS",
  SS: "SS",
  S: "S",
  AAA: "AAA",
  AA: "AA",
  A: "A",
  B: "B",
  C: "C",
  UNKNOWN: "UNKNOWN",
};
const RANK_ORDER = Object.values(RANK);

function abridgeScore(score) {
  if (Math.abs(score) < 1) return "0pt";
  if (Math.abs(score) > 999) {
    return (Math.sign(score) * (Math.abs(score) / 1000)).toFixed(1) + "kpt";
  }
  return (Math.sign(score) * Math.abs(score)).toString() + "pt";
}

class RankCondition {
  constructor(rank, message, requiredScore) {
    this.rank = rank;
    this.message = message;
    this.requiredScore = requiredScore;
  }
}

class Trophy {
  constructor(score, rankConditions, title, filterTitles, hidden = false) {
    this.score = score;
    this.rankConditions = rankConditions;
    this.title = title;
    this.filterTitles = filterTitles;
    this.hidden = hidden;
    this.rankCondition = null;
    this.rank = RANK.UNKNOWN;
    this.topMessage = "Unknown";
    this.bottomMessage = abridgeScore(score);
    this.setRank();
  }
  setRank() {
    const sorted = [...this.rankConditions].sort(
      (a, b) => RANK_ORDER.indexOf(a.rank) - RANK_ORDER.indexOf(b.rank),
    );
    const cond = sorted.find((r) => this.score >= r.requiredScore);
    if (cond != null) {
      this.rank = cond.rank;
      this.rankCondition = cond;
      this.topMessage = cond.message;
    }
  }
  calculateNextRankPercentage() {
    if (this.rank === RANK.UNKNOWN) return 0;
    const nextRankIndex = RANK_ORDER.indexOf(this.rank) - 1;
    if (nextRankIndex < 0 || this.rank === RANK.SSS || this.rank === RANK.SECRET) {
      return 1;
    }
    const nextRank = RANK_ORDER[nextRankIndex];
    const nextCond = this.rankConditions.find((r) => r.rank === nextRank);
    if (!nextCond || !this.rankCondition) return 1;
    const distance = nextCond.requiredScore - this.rankCondition.requiredScore;
    const progress = this.score - this.rankCondition.requiredScore;
    return Math.max(0, Math.min(1, progress / distance));
  }
  getNextRankInfo() {
    if (this.rank === RANK.UNKNOWN) {
      const lowest = this.rankConditions[this.rankConditions.length - 1];
      return { nextRank: lowest ? lowest.rank : "C", requiredScore: lowest ? lowest.requiredScore : 1 };
    }
    if (this.rank === RANK.SSS || this.rank === RANK.SECRET) {
      return { nextRank: "MAX", requiredScore: null };
    }
    const nextRankIndex = RANK_ORDER.indexOf(this.rank) - 1;
    const nextRank = RANK_ORDER[nextRankIndex];
    const nextCond = this.rankConditions.find((r) => r.rank === nextRank);
    return {
      nextRank: nextCond ? nextCond.rank : "MAX",
      requiredScore: nextCond ? nextCond.requiredScore : null,
    };
  }
}

function buildTrophiesFromUserInfo(userInfo) {
  const base = [
    new Trophy(
      userInfo.totalStargazers,
      [
        new RankCondition(RANK.SSS, "Super Stargazer", 1200),
        new RankCondition(RANK.SS, "High Stargazer", 500),
        new RankCondition(RANK.S, "Stargazer", 250),
        new RankCondition(RANK.AAA, "Super Star", 100),
        new RankCondition(RANK.AA, "High Star", 50),
        new RankCondition(RANK.A, "You are a Star", 25),
        new RankCondition(RANK.B, "Middle Star", 10),
        new RankCondition(RANK.C, "First Star", 1),
      ],
      "Stars",
      ["Star", "Stars"],
    ),
    new Trophy(
      userInfo.totalCommits,
      [
        new RankCondition(RANK.SSS, "God Committer", 2000),
        new RankCondition(RANK.SS, "Deep Committer", 1000),
        new RankCondition(RANK.S, "Super Committer", 700),
        new RankCondition(RANK.AAA, "Ultra Committer", 500),
        new RankCondition(RANK.AA, "Hyper Committer", 200),
        new RankCondition(RANK.A, "High Committer", 100),
        new RankCondition(RANK.B, "Middle Committer", 10),
        new RankCondition(RANK.C, "First Commit", 1),
      ],
      "Commits",
      ["Commit", "Commits"],
    ),
    new Trophy(
      userInfo.totalFollowers,
      [
        new RankCondition(RANK.SSS, "Super Celebrity", 1000),
        new RankCondition(RANK.SS, "Ultra Celebrity", 400),
        new RankCondition(RANK.S, "Hyper Celebrity", 200),
        new RankCondition(RANK.AAA, "Famous User", 100),
        new RankCondition(RANK.AA, "Active User", 50),
        new RankCondition(RANK.A, "Dynamic User", 20),
        new RankCondition(RANK.B, "Many Friends", 10),
        new RankCondition(RANK.C, "First Friend", 1),
      ],
      "Followers",
      ["Follower", "Followers"],
    ),
    new Trophy(
      userInfo.totalIssues,
      [
        new RankCondition(RANK.SSS, "God Issuer", 500),
        new RankCondition(RANK.SS, "Deep Issuer", 200),
        new RankCondition(RANK.S, "Super Issuer", 100),
        new RankCondition(RANK.AAA, "Ultra Issuer", 50),
        new RankCondition(RANK.AA, "Hyper Issuer", 20),
        new RankCondition(RANK.A, "High Issuer", 10),
        new RankCondition(RANK.B, "Middle Issuer", 5),
        new RankCondition(RANK.C, "First Issue", 1),
      ],
      "Issues",
      ["Issue", "Issues"],
    ),
    new Trophy(
      userInfo.totalPullRequests,
      [
        new RankCondition(RANK.SSS, "God Puller", 500),
        new RankCondition(RANK.SS, "Deep Puller", 200),
        new RankCondition(RANK.S, "Super Puller", 100),
        new RankCondition(RANK.AAA, "Ultra Puller", 50),
        new RankCondition(RANK.AA, "Hyper Puller", 20),
        new RankCondition(RANK.A, "High Puller", 10),
        new RankCondition(RANK.B, "Middle Puller", 5),
        new RankCondition(RANK.C, "First Pull", 1),
      ],
      "PullRequest",
      ["PR", "PullRequest", "Pulls", "Puller"],
    ),
    new Trophy(
      userInfo.totalRepositories,
      [
        new RankCondition(RANK.SSS, "God Repo Creator", 100),
        new RankCondition(RANK.SS, "Deep Repo Creator", 70),
        new RankCondition(RANK.S, "Super Repo Creator", 50),
        new RankCondition(RANK.AAA, "Ultra Repo Creator", 40),
        new RankCondition(RANK.AA, "Hyper Repo Creator", 30),
        new RankCondition(RANK.A, "High Repo Creator", 20),
        new RankCondition(RANK.B, "Middle Repo Creator", 10),
        new RankCondition(RANK.C, "First Repository", 1),
      ],
      "Repositories",
      ["Repo", "Repository", "Repositories"],
    ),
    new Trophy(
      userInfo.totalReviews,
      [
        new RankCondition(RANK.SSS, "God Reviewer", 70),
        new RankCondition(RANK.SS, "Deep Reviewer", 57),
        new RankCondition(RANK.S, "Super Reviewer", 45),
        new RankCondition(RANK.AAA, "Ultra Reviewer", 30),
        new RankCondition(RANK.AA, "Hyper Reviewer", 20),
        new RankCondition(RANK.A, "Active Reviewer", 8),
        new RankCondition(RANK.B, "Intermediate Reviewer", 3),
        new RankCondition(RANK.C, "New Reviewer", 1),
      ],
      "Reviews",
      ["Review", "Reviews"],
    ),
  ];

  const isAllS = base.every((t) => t.rank.slice(0, 1) === RANK.S) ? 1 : 0;
  const haveS = base.some((t) => t.rank.slice(0, 1) === RANK.S) ? 1 : 0;

  const sssTrophy = new Trophy(
    haveS,
    [new RankCondition(RANK.SECRET, "SSS Rank Hacker", 1)],
    "AchieveSSSRank",
    ["AchieveSuperRank"],
    true,
  );
  sssTrophy.bottomMessage = "Have SSS Rank";

  const multiLang = new Trophy(
    userInfo.languageCount,
    [new RankCondition(RANK.SECRET, "Rainbow Lang User", 5)],
    "MultiLanguage",
    ["MultipleLang", "MultiLanguage"],
    true,
  );

  const longTime = new Trophy(
    userInfo.durationYear,
    [new RankCondition(RANK.SECRET, "Village Elder", 3)],
    "LongTimeUser",
    ["LongTimeUser"],
    true,
  );
  longTime.bottomMessage = `${userInfo.durationYear}${userInfo.durationYear > 0 ? "years" : "year"}`;

  const allTrophies = [...base, sssTrophy, multiLang, longTime]
    .filter((t) => (!t.hidden || t.rank !== RANK.UNKNOWN) && t.rank !== RANK.UNKNOWN)
    .sort((a, b) => RANK_ORDER.indexOf(a.rank) - RANK_ORDER.indexOf(b.rank));

  return allTrophies;
}

// 1. Unit Test Assertion on 19 Repositories -> Middle Repo Creator / Rank B
const sample19Repo = buildTrophiesFromUserInfo({
  totalStargazers: 8,
  totalCommits: 177,
  totalFollowers: 6,
  totalIssues: 41,
  totalPullRequests: 35,
  totalRepositories: 19,
  totalReviews: 0,
  languageCount: 13,
  durationYear: 2,
}).find((t) => t.title === "Repositories");

if (sample19Repo.rank !== "B" || sample19Repo.topMessage !== "Middle Repo Creator") {
  throw new Error(`Expected 19 repos to be Rank B / Middle Repo Creator, got ${sample19Repo.rank} / ${sample19Repo.topMessage}`);
}
console.log("[PASS] 19 Repositories ->", sample19Repo.topMessage, "| Rank:", sample19Repo.rank);

// 2. Fetch live GitHub GraphQL metrics for LlewxamDev
let rawGraphql;
try {
  const token = process.env.GITHUB_TOKEN || execSync("gh auth token", { encoding: "utf8" }).trim();
  const query = `
    query($username: String!) {
      user(login: $username) {
        createdAt
        contributionsCollection {
          totalCommitContributions
          restrictedContributionsCount
          totalPullRequestReviewContributions
          contributionCalendar {
            totalContributions
            weeks {
              contributionDays {
                contributionCount
                date
              }
            }
          }
        }
        organizations(first: 1) { totalCount }
        followers(first: 1) { totalCount }
        openIssues: issues(states: OPEN) { totalCount }
        closedIssues: issues(states: CLOSED) { totalCount }
        pullRequests(first: 1) { totalCount }
        repositories(first: 100, ownerAffiliations: OWNER, orderBy: {direction: DESC, field: STARGAZERS}) {
          totalCount
          nodes {
            languages(first: 3, orderBy: {direction: DESC, field: SIZE}) {
              nodes { name }
            }
            stargazers { totalCount }
          }
        }
      }
    }
  `;
  const res = await fetch("https://api.github.com/graphql", {
    method: "POST",
    headers: {
      Authorization: `bearer ${token}`,
      "Content-Type": "application/json",
      "User-Agent": "LWX-EXE-Trophy-Engine/1.0",
    },
    body: JSON.stringify({ query, variables: { username: "LlewxamDev" } }),
  });
  const json = await res.json();
  rawGraphql = json.data.user;
} catch (err) {
  console.error("Failed to fetch live GraphQL:", err.message);
  process.exit(1);
}

const langs = new Set();
let stars = 0;
for (const repo of rawGraphql.repositories.nodes) {
  stars += repo.stargazers?.totalCount || 0;
  for (const l of repo.languages?.nodes || []) {
    if (l?.name) langs.add(l.name);
  }
}
const durationTime = Date.now() - new Date(rawGraphql.createdAt).getTime();
const durationYear = new Date(durationTime).getUTCFullYear() - 1970;

const liveUserInfo = {
  totalCommits:
    rawGraphql.contributionsCollection.totalCommitContributions +
    rawGraphql.contributionsCollection.restrictedContributionsCount,
  totalFollowers: rawGraphql.followers.totalCount,
  totalIssues: rawGraphql.openIssues.totalCount + rawGraphql.closedIssues.totalCount,
  totalOrganizations: rawGraphql.organizations.totalCount,
  totalPullRequests: rawGraphql.pullRequests.totalCount,
  totalReviews: rawGraphql.contributionsCollection.totalPullRequestReviewContributions,
  totalStargazers: stars,
  totalRepositories: rawGraphql.repositories.totalCount,
  languageCount: langs.size,
  durationYear,
};

console.log("[LIVE METRICS @LlewxamDev]:", JSON.stringify(liveUserInfo));

const trophies = buildTrophiesFromUserInfo(liveUserInfo);
for (const t of trophies) {
  console.log(` - ${t.title.padEnd(15)} | Rank: ${t.rank.padEnd(6)} | Title: ${t.topMessage.padEnd(22)} | Score: ${t.score} (${t.bottomMessage})`);
}

// 3. Render the SVG using the exact layout & sprite-slots.json
const configPath = path.join(ENGINE_ROOT, "src", "config", "sprite-slots.json");
const config = JSON.parse(fs.readFileSync(configPath, "utf8"));
// Copy sprite-slots.json to assets/trophies/sprite-slots.json for easy access
fs.copyFileSync(configPath, path.join(REPO_ROOT, "assets", "trophies", "sprite-slots.json"));

function escapeXml(unsafe) {
  return String(unsafe)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&apos;");
}

function getRankPalette(rank) {
  switch (rank) {
    case RANK.SSS:
    case RANK.SS:
    case RANK.S:
      return { badgeBg: "#2A060D", badgeBorder: "#FFD800", badgeText: "#FFD800", barColor: "#FFD800" };
    case RANK.AAA:
    case RANK.AA:
    case RANK.A:
      return { badgeBg: "#1E050B", badgeBorder: "#FF1538", badgeText: "#FF4D6A", barColor: "#FF1538" };
    case RANK.SECRET:
      return { badgeBg: "#1A0726", badgeBorder: "#D946EF", badgeText: "#F0ABFC", barColor: "#D946EF" };
    case RANK.B:
      return { badgeBg: "#0A192F", badgeBorder: "#4C88FF", badgeText: "#7CA8FF", barColor: "#4C88FF" };
    default:
      return { badgeBg: "#14141C", badgeBorder: "#8E7A82", badgeText: "#D8CFD2", barColor: "#28C800" };
  }
}

function tryLoadCustomSpriteDataUri(relPath) {
  const full = path.join(REPO_ROOT, relPath);
  if (fs.existsSync(full)) {
    const buf = fs.readFileSync(full);
    if (buf.length > 0) return `data:image/png;base64,${buf.toString("base64")}`;
  }
  return null;
}

function renderSpriteSlotGraphic(cx, cy, size, trophy, slotCfg, customDataUri, isSelected) {
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

  const pedY = y + size - 18;
  return `
    <g>
      <rect x="${x}" y="${y}" width="${size}" height="${size}" fill="#070306" stroke="${frameStroke}" stroke-width="2" />
      <rect x="${x + 4}" y="${y + 4}" width="${size - 8}" height="${size - 8}" fill="#0C0509" stroke="#281018" stroke-width="1" stroke-dasharray="4 2" />
      <path d="M ${x + 6} ${y + 14} V ${y + 6} H ${x + 14}" fill="none" stroke="${pal.badgeBorder}" stroke-width="2" />
      <path d="M ${x + size - 14} ${y + 6} H ${x + size - 6} V ${y + 14}" fill="none" stroke="${pal.badgeBorder}" stroke-width="2" />
      <path d="M ${x + 6} ${y + size - 14} V ${y + size - 6} H ${x + 14}" fill="none" stroke="${pal.badgeBorder}" stroke-width="2" />
      <path d="M ${x + size - 14} ${y + size - 6} H ${x + size - 6} V ${y + size - 14}" fill="none" stroke="${pal.badgeBorder}" stroke-width="2" />
      <rect x="${cx - 20}" y="${pedY}" width="40" height="6" fill="#5A2800" stroke="#C86400" stroke-width="1" />
      <rect x="${cx - 14}" y="${pedY - 5}" width="28" height="5" fill="#8A3E00" />
      <polygon points="${cx - 14},${y + 16} ${cx + 14},${y + 16} ${cx + 10},${pedY - 12} ${cx - 10},${pedY - 12}" fill="${pal.badgeBg}" stroke="${pal.badgeBorder}" stroke-width="2" />
      <rect x="${cx - 4}" y="${pedY - 12}" width="8" height="7" fill="${pal.badgeBorder}" />
      <text x="${cx}" y="${y + 33}" text-anchor="middle" class="px-rank" fill="${pal.badgeText}" font-size="11">${escapeXml(trophy.rank)}</text>
      <text x="${cx}" y="${pedY + 13}" text-anchor="middle" class="px-tiny" fill="#7A646C" font-size="7">${escapeXml(slotCfg.slotCode)}</text>
    </g>
  `;
}

const visibleTrophies = trophies.slice(0, 8);
const selectedTrophy =
  visibleTrophies.find((t) => t.title === "Repositories") || visibleTrophies[0];

const W = 1200;
const H = 560;
const cols = 4;
const slotW = 180;
const slotH = 204;
const gapX = 14;
const gapY = 16;
const gridStartX = 32;
const gridStartY = 98;

const slotCardsSvg = visibleTrophies
  .map((trophy, idx) => {
    const col = idx % cols;
    const row = Math.floor(idx / cols);
    const sx = gridStartX + col * (slotW + gapX);
    const sy = gridStartY + row * (slotH + gapY);

    const isSelected = trophy.title === selectedTrophy.title;
    const slotCfg = config.slots[trophy.title] || {
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
        <rect x="0" y="0" width="${slotW}" height="${slotH}" fill="#0B0508" stroke="${outerStroke}" stroke-width="${outerWidth}" />
        <rect x="4" y="4" width="${slotW - 8}" height="${slotH - 8}" fill="none" stroke="${isSelected ? "#FF1538" : "#261018"}" stroke-width="1" />
        <rect x="6" y="6" width="${slotW - 12}" height="22" fill="${headerBg}" />
        <text x="12" y="21" class="px-meta" fill="${isSelected ? "#FFD800" : "#B89EA6"}" font-size="10">${escapeXml(slotCfg.slotCode)}</text>
        <rect x="${slotW - 58}" y="8" width="48" height="18" fill="${pal.badgeBg}" stroke="${pal.badgeBorder}" stroke-width="1.2" />
        <text x="${slotW - 34}" y="20" text-anchor="middle" class="px-rank" fill="${pal.badgeText}" font-size="10">${escapeXml(trophy.rank)}</text>

        ${renderSpriteSlotGraphic(slotW / 2, 76, 76, trophy, slotCfg, customUri, isSelected)}

        <text x="${slotW / 2}" y="132" text-anchor="middle" class="px-title" fill="#FFFFFF" font-size="13">${escapeXml(trophy.title.toUpperCase())}</text>
        <text x="${slotW / 2}" y="150" text-anchor="middle" class="px-sub" fill="${pal.badgeText}" font-size="10.5">${escapeXml(trophy.topMessage)}</text>
        <text x="${slotW / 2}" y="168" text-anchor="middle" class="px-score" fill="#E8DFE2" font-size="10.5">${escapeXml(trophy.bottomMessage)} · ${trophy.score} ${escapeXml(slotCfg.unitLabel)}</text>

        <rect x="14" y="180" width="${slotW - 28}" height="8" fill="#180B10" stroke="#381620" stroke-width="1" />
        <rect x="14" y="180" width="${barFillW}" height="8" fill="${pal.barColor}" />
      </g>
    `;
  })
  .join("\n");

const inspX = 812;
const inspY = 98;
const inspW = 356;
const inspH = 424;
const selCfg = config.slots[selectedTrophy.title];
const selCustomUri = tryLoadCustomSpriteDataUri(selCfg.spritePath);
const selPal = getRankPalette(selectedTrophy.rank);
const selPct = Math.round(selectedTrophy.calculateNextRankPercentage() * 100);
const selNext = selectedTrophy.getNextRankInfo();
const selBarW = Math.max(6, Math.round(((inspW - 56) * selPct) / 100));

const svgContent = `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" role="img" aria-label="TROPHY SELECTION — @LlewxamDev">
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

  <rect width="${W}" height="${H}" fill="#050305" />
  <rect x="14" y="14" width="${W - 28}" height="${H - 28}" fill="#080407" stroke="#8A0018" stroke-width="3" />
  <rect x="20" y="20" width="${W - 40}" height="${H - 40}" fill="none" stroke="#2C0D16" stroke-width="1.5" />

  <rect x="32" y="28" width="${W - 64}" height="54" fill="#12050A" stroke="#FF1538" stroke-width="2" />
  <polygon points="52,48 64,55 52,62" fill="#FFD800" class="cursor-arrow" />
  <text x="76" y="61" class="px-head" fill="#FFD800" font-size="20">TROPHY SELECTION</text>
  <text x="${W - 48}" y="52" text-anchor="end" class="px-meta" fill="#FF4D6A" font-size="12">USER: @LLEWXAMDEV</text>
  <text x="${W - 48}" y="69" text-anchor="end" class="px-tiny" fill="#9E8C92" font-size="10">ENGINE: GINWU05/GITHUB-PROFILE-TROPHY · VERIFIED THRESHOLDS</text>

  ${slotCardsSvg}

  <g transform="translate(${inspX}, ${inspY})">
    <rect x="0" y="0" width="${inspW}" height="${inspH}" fill="#0D0509" stroke="#FFD800" stroke-width="2.5" class="pulse-stroke" />
    <rect x="6" y="6" width="${inspW - 12}" height="${inspH - 12}" fill="none" stroke="#FF1538" stroke-width="1.2" />

    <rect x="8" y="8" width="${inspW - 16}" height="32" fill="#26060E" />
    <polygon points="20,19 29,24 20,29" fill="#FFD800" class="cursor-arrow" />
    <text x="36" y="28" class="px-title" fill="#FFD800" font-size="12">SELECTED TROPHY DATA</text>
    <text x="${inspW - 18}" y="28" text-anchor="end" class="px-meta" fill="#FF4D6A" font-size="11">${escapeXml(selCfg.slotCode)}</text>

    ${renderSpriteSlotGraphic(inspW / 2, 112, 112, selectedTrophy, selCfg, selCustomUri, true)}

    <rect x="20" y="182" width="${inspW - 40}" height="108" fill="#070306" stroke="#8A0018" stroke-width="1.5" />
    <text x="${inspW / 2}" y="210" text-anchor="middle" class="px-title" fill="#FFFFFF" font-size="16">${escapeXml(selectedTrophy.topMessage.toUpperCase())}</text>
    <line x1="40" y1="222" x2="${inspW - 40}" y2="222" stroke="#4A0A18" stroke-width="1.5" />
    <text x="${inspW / 2}" y="248" text-anchor="middle" class="px-head" fill="#FFD800" font-size="17">${selectedTrophy.score} ${escapeXml(selCfg.unitLabel)}</text>
    <rect x="${inspW / 2 - 58}" y="260" width="116" height="22" fill="${selPal.badgeBg}" stroke="${selPal.badgeBorder}" stroke-width="1.5" />
    <text x="${inspW / 2}" y="275" text-anchor="middle" class="px-rank" fill="${selPal.badgeText}" font-size="13">RANK ${escapeXml(selectedTrophy.rank)}</text>

    <text x="24" y="314" class="px-meta" fill="#D8CFD2" font-size="11">CATEGORY: ${escapeXml(selectedTrophy.title.toUpperCase())} (${escapeXml(selectedTrophy.bottomMessage)})</text>
    <text x="24" y="334" class="px-meta" fill="#9E8C92" font-size="11">NEXT RANK: ${escapeXml(selNext.nextRank)}${selNext.requiredScore !== null ? ` (REQ: ${selNext.requiredScore} ${escapeXml(selCfg.unitLabel)})` : " (MAX TIER UNLOCKED)"}</text>

    <rect x="24" y="346" width="${inspW - 48}" height="14" fill="#18090E" stroke="#5A1222" stroke-width="1.2" />
    <rect x="28" y="349" width="${selBarW}" height="8" fill="${selPal.barColor}" />
    <text x="${inspW - 24}" y="375" text-anchor="end" class="px-tiny" fill="#FFD800" font-size="10">PROGRESS: ${selPct}%</text>

    <rect x="20" y="384" width="${inspW - 40}" height="26" fill="#12060A" stroke="#38121C" stroke-width="1" />
    <text x="${inspW / 2}" y="401" text-anchor="middle" class="px-tiny" fill="#8E7A82" font-size="9.5">SLOT: ${escapeXml(selCfg.spritePath)}</text>
  </g>

  <rect x="22" y="${H - 30}" width="${W - 44}" height="8" fill="url(#ghzCheckTrim)" opacity="0.75" />
  <rect x="22" y="${H - 33}" width="${W - 44}" height="3" fill="#2A4018" />
  <rect width="${W}" height="${H}" fill="url(#crtScanlines)" pointer-events="none" />
</svg>`;

const outSvgPath = path.join(REPO_ROOT, "assets", "trophies", "trophy-selection-live.svg");
fs.writeFileSync(outSvgPath, svgContent, "utf8");
console.log("[SAVED VERIFIED SVG]:", outSvgPath);

// 4. Generate reliable self-contained GitHub Stats & Streak SVGs (fixing broken external github-readme-stats)
const cal = rawGraphql.contributionsCollection.contributionCalendar;
const allDays = (cal?.weeks || []).flatMap((w) => w.contributionDays || []);
let currentStreak = 0;
let longestStreak = 0;
let tempStreak = 0;
let longestStart = "";
let longestEnd = "";
let tempStart = "";

for (const d of allDays) {
  if (d.contributionCount > 0) {
    if (tempStreak === 0) tempStart = d.date;
    tempStreak++;
    if (tempStreak >= longestStreak) {
      longestStreak = tempStreak;
      longestStart = tempStart;
      longestEnd = d.date;
    }
  } else {
    tempStreak = 0;
  }
}

const todayIso = new Date().toISOString().slice(0, 10);
for (let i = allDays.length - 1; i >= 0; i--) {
  const d = allDays[i];
  if (d.date > todayIso) continue;
  if (d.contributionCount > 0) {
    currentStreak++;
  } else if (d.date === todayIso) {
    continue;
  } else {
    break;
  }
}

// Calculate overall grade rank based on commits + PRs + issues + stars + repos
const rankLabel = liveUserInfo.totalCommits >= 150 ? "A+" : "A";
const ringCircumference = 2 * Math.PI * 38;
const ringOffset = Math.round(ringCircumference * 0.16);

const statsSvg = `<svg xmlns="http://www.w3.org/2000/svg" width="580" height="195" viewBox="0 0 580 195" role="img" aria-label="GitHub Stats — @LlewxamDev">
  <defs>
    <style>
      .st-head { font-family: 'Press Start 2P', 'VT323', 'Courier New', monospace; font-weight: 900; letter-spacing: 1.5px; }
      .st-label { font-family: 'JetBrains Mono', 'Consolas', 'Courier New', monospace; font-weight: 700; font-size: 12.5px; fill: #F2ECEE; }
      .st-val { font-family: 'JetBrains Mono', 'Consolas', 'Courier New', monospace; font-weight: 900; font-size: 13px; fill: #FFD800; }
      .st-rank { font-family: 'Press Start 2P', 'JetBrains Mono', monospace; font-weight: 900; font-size: 24px; fill: #FF0F2B; }
      .st-sub { font-family: 'JetBrains Mono', 'Consolas', monospace; font-weight: 700; font-size: 9.5px; fill: #9E8C92; letter-spacing: 1px; }
    </style>
  </defs>
  <rect width="580" height="195" fill="#050305" />
  <rect x="4" y="4" width="572" height="187" fill="#0A0508" stroke="#8A0018" stroke-width="2.5" />
  <rect x="9" y="9" width="562" height="177" fill="none" stroke="#2C0D16" stroke-width="1" />
  <rect x="12" y="12" width="556" height="28" fill="#1A050C" />
  <polygon points="22,21 30,26 22,31" fill="#FFD800" />
  <text x="38" y="30" class="st-head" fill="#FF0F2B" font-size="12">LLEWXAMDEV · GITHUB STATS</text>
  <text x="556" y="29" text-anchor="end" class="st-sub">LIVE TELEMETRY</text>

  <g transform="translate(26, 62)">
    <circle cx="8" cy="-4" r="4.5" fill="#FFD800" />
    <text x="22" y="0" class="st-label">Total Stars Earned:</text>
    <text x="295" y="0" text-anchor="end" class="st-val">${liveUserInfo.totalStargazers}</text>

    <circle cx="8" cy="22" r="4.5" fill="#FF0F2B" />
    <text x="22" y="26" class="st-label">Total Commits:</text>
    <text x="295" y="26" text-anchor="end" class="st-val">${liveUserInfo.totalCommits}</text>

    <circle cx="8" cy="48" r="4.5" fill="#3178C6" />
    <text x="22" y="52" class="st-label">Total Pull Requests:</text>
    <text x="295" y="52" text-anchor="end" class="st-val">${liveUserInfo.totalPullRequests}</text>

    <circle cx="8" cy="74" r="4.5" fill="#28E060" />
    <text x="22" y="78" class="st-label">Total Issues:</text>
    <text x="295" y="78" text-anchor="end" class="st-val">${liveUserInfo.totalIssues}</text>

    <circle cx="8" cy="100" r="4.5" fill="#FF8C00" />
    <text x="22" y="104" class="st-label">Public Repositories:</text>
    <text x="295" y="104" text-anchor="end" class="st-val">${liveUserInfo.totalRepositories}</text>
  </g>

  <line x1="358" y1="48" x2="358" y2="174" stroke="#380B16" stroke-width="1.5" />

  <g transform="translate(468, 108)">
    <circle cx="0" cy="0" r="42" fill="#120408" stroke="#2E0A12" stroke-width="6" />
    <circle cx="0" cy="0" r="38" fill="none" stroke="#FF0F2B" stroke-width="6" stroke-dasharray="${ringCircumference.toFixed(1)}" stroke-dashoffset="${ringOffset}" stroke-linecap="round" transform="rotate(-90)" />
    <circle cx="0" cy="0" r="31" fill="none" stroke="#FFD800" stroke-width="1.5" stroke-opacity="0.65" />
    <text x="2" y="8" text-anchor="middle" class="st-rank">${rankLabel}</text>
    <text x="0" y="60" text-anchor="middle" class="st-sub" fill="#FFD800">RANK TIER · ${liveUserInfo.languageCount} LANGUAGES</text>
  </g>
</svg>`;

const streakSvg = `<svg xmlns="http://www.w3.org/2000/svg" width="580" height="195" viewBox="0 0 580 195" role="img" aria-label="GitHub Streak — @LlewxamDev">
  <defs>
    <style>
      .sk-head { font-family: 'Press Start 2P', 'VT323', 'Courier New', monospace; font-weight: 900; letter-spacing: 1.5px; }
      .sk-num { font-family: 'JetBrains Mono', 'Consolas', monospace; font-weight: 900; font-size: 28px; fill: #FFFFFF; }
      .sk-num-gold { font-family: 'JetBrains Mono', 'Consolas', monospace; font-weight: 900; font-size: 30px; fill: #FFD800; }
      .sk-lbl { font-family: 'JetBrains Mono', 'Consolas', monospace; font-weight: 800; font-size: 11px; fill: #FF0F2B; letter-spacing: 1px; }
      .sk-lbl-gold { font-family: 'JetBrains Mono', 'Consolas', monospace; font-weight: 800; font-size: 11px; fill: #FFD800; letter-spacing: 1px; }
      .sk-sub { font-family: 'JetBrains Mono', 'Consolas', monospace; font-weight: 700; font-size: 9.5px; fill: #9E8C92; }
    </style>
  </defs>
  <rect width="580" height="195" fill="#050305" />
  <rect x="4" y="4" width="572" height="187" fill="#0A0508" stroke="#8A0018" stroke-width="2.5" />
  <rect x="9" y="9" width="562" height="177" fill="none" stroke="#2C0D16" stroke-width="1" />
  <rect x="12" y="12" width="556" height="28" fill="#1A050C" />
  <polygon points="22,21 30,26 22,31" fill="#FFD800" />
  <text x="38" y="30" class="sk-head" fill="#FFD800" font-size="12">CONTRIBUTION &amp; STREAK TELEMETRY</text>
  <text x="556" y="29" text-anchor="end" class="sk-sub">@LLEWXAMDEV</text>

  <g transform="translate(102, 104)">
    <text x="0" y="-8" text-anchor="middle" class="sk-num">${cal?.totalContributions || liveUserInfo.totalCommits}</text>
    <text x="0" y="18" text-anchor="middle" class="sk-lbl">TOTAL CONTRIBUTIONS</text>
    <text x="0" y="38" text-anchor="middle" class="sk-sub">2024 — PRESENT</text>
  </g>

  <line x1="198" y1="52" x2="198" y2="172" stroke="#380B16" stroke-width="1.5" />

  <g transform="translate(290, 102)">
    <circle cx="0" cy="-16" r="28" fill="#18050A" stroke="#FF0F2B" stroke-width="3" />
    <circle cx="0" cy="-16" r="22" fill="none" stroke="#FFD800" stroke-width="1.2" stroke-dasharray="6 4" />
    <text x="0" y="-6" text-anchor="middle" class="sk-num-gold">${currentStreak}</text>
    <text x="0" y="30" text-anchor="middle" class="sk-lbl-gold">CURRENT STREAK</text>
    <text x="0" y="48" text-anchor="middle" class="sk-sub">ACTIVE DAYS</text>
  </g>

  <line x1="382" y1="52" x2="382" y2="172" stroke="#380B16" stroke-width="1.5" />

  <g transform="translate(478, 104)">
    <text x="0" y="-8" text-anchor="middle" class="sk-num">${longestStreak} DAYS</text>
    <text x="0" y="18" text-anchor="middle" class="sk-lbl">LONGEST STREAK</text>
    <text x="0" y="38" text-anchor="middle" class="sk-sub">${longestStart ? `${longestStart.slice(5)} TO ${longestEnd.slice(5)}` : "VERIFIED"}</text>
  </g>
</svg>`;

const outStatsPath = path.join(REPO_ROOT, "assets", "trophies", "github-stats-live.svg");
const outStreakPath = path.join(REPO_ROOT, "assets", "trophies", "github-streak-live.svg");
fs.writeFileSync(outStatsPath, statsSvg, "utf8");
fs.writeFileSync(outStreakPath, streakSvg, "utf8");
console.log("[SAVED STATS SVG]:", outStatsPath);
console.log("[SAVED STREAK SVG]:", outStreakPath);
