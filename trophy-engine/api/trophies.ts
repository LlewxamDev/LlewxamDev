/**
 * ============================================================================
 * PROJECT LWX.EXE — VERCEL SERVERLESS ENDPOINT (/api/trophies)
 * ============================================================================
 * Endpoint usage:
 *   GET /api/trophies?username=LlewxamDev
 *   GET /api/trophies?username=LlewxamDev&selected=Repositories
 *   GET /api/trophies?username=LlewxamDev&title=Commits,Repositories,Issues
 * ============================================================================
 */

import { CONSTANTS, DEFAULT_WANT_FLAGS, WantFlags } from "../src/trophy-core.js";
import { GithubAPIClient } from "../src/github-client.js";
import { renderErrorSVG, renderTrophySelectionSVG } from "../src/svg-renderer.js";

const client = new GithubAPIClient();

function parseBoolean(val: string | null): boolean {
  return val !== null && val.toLowerCase() === "true";
}

export default async function handler(req: any, res?: any): Promise<any> {
  // Support both Web Standard Request (Edge/Fetch) and Node IncomingMessage (Vercel Node runtime)
  const rawUrl = typeof req.url === "string" ? req.url : "/";
  const url = new URL(rawUrl, "https://localhost");
  const params = url.searchParams;

  const username = params.get("username") || "LlewxamDev";
  const selected = params.get("selected") || undefined;

  const titles = params
    .getAll("title")
    .flatMap((r) => r.split(","))
    .map((r) => r.trim())
    .filter(Boolean);

  const ranks = params
    .getAll("rank")
    .flatMap((r) => r.split(","))
    .map((r) => r.trim())
    .filter(Boolean);

  const wantAll = parseBoolean(params.get("wantAll"));
  const want: WantFlags = {
    AchieveSuperRank: wantAll || parseBoolean(params.get("wantAchieveSuperRank")),
    MultipleLang: wantAll || parseBoolean(params.get("wantMultipleLang")),
    LongTimeAccount: wantAll || parseBoolean(params.get("wantLongTimeAccount")),
    AncientAccount: wantAll || parseBoolean(params.get("wantAncientAccount")),
    NewAccount: wantAll || parseBoolean(params.get("wantNewAccount")),
    MultipleOrganizations:
      wantAll || parseBoolean(params.get("wantMultipleOrganizations")) || DEFAULT_WANT_FLAGS.MultipleOrganizations,
  };

  const headers = {
    "Content-Type": "image/svg+xml; charset=utf-8",
    "Cache-Control": `public, max-age=${CONSTANTS.CACHE_MAX_AGE}, s-maxage=${CONSTANTS.CACHE_MAX_AGE}, stale-while-revalidate=86400`,
  };

  const userInfo = await client.requestUserInfo(username);
  if (!userInfo) {
    const errSvg = renderErrorSVG(
      "USER TELEMETRY UNAVAILABLE",
      `Could not retrieve GitHub data for "${username}". Configure GITHUB_TOKEN in Vercel environment variables if rate-limited.`,
    );
    if (res && typeof res.setHeader === "function") {
      res.statusCode = 404;
      Object.entries(headers).forEach(([k, v]) => res.setHeader(k, v));
      res.end(errSvg);
      return;
    }
    return new Response(errSvg, { status: 404, headers });
  }

  const svg = renderTrophySelectionSVG(userInfo, {
    username,
    titles,
    ranks,
    selected,
    want,
  });

  if (res && typeof res.setHeader === "function") {
    res.statusCode = 200;
    Object.entries(headers).forEach(([k, v]) => res.setHeader(k, v));
    res.end(svg);
    return;
  }

  return new Response(svg, { status: 200, headers });
}
