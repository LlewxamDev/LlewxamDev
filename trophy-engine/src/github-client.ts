/**
 * ============================================================================
 * PROJECT LWX.EXE — GITHUB GRAPHQL & REST FALLBACK DATA CLIENT
 * ============================================================================
 * Queries GitHub GraphQL API using environment token(s) (GITHUB_TOKEN,
 * GITHUB_TOKEN1, GITHUB_TOKEN2) with the exact queries from
 * GinWU05/github-profile-trophy.
 *
 * Also provides a zero-token public REST API fallback so the endpoint
 * remains functional even before a token is configured.
 * ============================================================================
 */

import {
  CONSTANTS,
  UserInfo,
  GitHubUserActivity,
  GitHubUserIssue,
  GitHubUserPullRequest,
  GitHubUserRepository,
} from "./trophy-core.js";

const QUERY_ACTIVITY = `
  query userInfo($username: String!) {
    user(login: $username) {
      createdAt
      contributionsCollection {
        totalCommitContributions
        restrictedContributionsCount
        totalPullRequestReviewContributions
      }
      organizations(first: 1) {
        totalCount
      }
      followers(first: 1) {
        totalCount
      }
    }
  }
`;

const QUERY_ISSUES = `
  query userInfo($username: String!) {
    user(login: $username) {
      openIssues: issues(states: OPEN) {
        totalCount
      }
      closedIssues: issues(states: CLOSED) {
        totalCount
      }
    }
  }
`;

const QUERY_PR = `
  query userInfo($username: String!) {
    user(login: $username) {
      pullRequests(first: 1) {
        totalCount
      }
    }
  }
`;

const QUERY_REPOS = `
  query userInfo($username: String!) {
    user(login: $username) {
      repositories(first: 100, ownerAffiliations: OWNER, orderBy: {direction: DESC, field: STARGAZERS}) {
        totalCount
        nodes {
          languages(first: 3, orderBy: {direction: DESC, field: SIZE}) {
            nodes {
              name
            }
          }
          stargazers {
            totalCount
          }
        }
      }
    }
  }
`;

export class GithubAPIClient {
  constructor(
    private apiEndpoint: string = process.env.GITHUB_API || CONSTANTS.DEFAULT_GITHUB_API,
  ) {}

  private getTokens(): string[] {
    return [
      process.env.GITHUB_TOKEN,
      process.env.GITHUB_TOKEN1,
      process.env.GITHUB_TOKEN2,
      process.env.GH_TOKEN,
    ].filter((t): t is string => Boolean(t && t.trim().length > 0));
  }

  async requestUserInfo(username: string): Promise<UserInfo | null> {
    const tokens = this.getTokens();

    if (tokens.length > 0) {
      const results = await Promise.all([
        this.requestGraphQL<GitHubUserActivity>(QUERY_ACTIVITY, username, tokens),
        this.requestGraphQL<GitHubUserIssue>(QUERY_ISSUES, username, tokens),
        this.requestGraphQL<GitHubUserPullRequest>(QUERY_PR, username, tokens),
        this.requestGraphQL<GitHubUserRepository>(QUERY_REPOS, username, tokens),
      ]);

      if (results.every((r) => r !== null)) {
        return new UserInfo(results[0]!, results[1]!, results[2]!, results[3]!);
      }
    }

    // Fallback to public GitHub REST API if no token is configured yet
    return await this.requestPublicRestFallback(username);
  }

  private async requestGraphQL<T>(
    query: string,
    username: string,
    tokens: string[],
  ): Promise<T | null> {
    for (const token of tokens) {
      try {
        const res = await fetch(this.apiEndpoint, {
          method: "POST",
          headers: {
            Authorization: `bearer ${token}`,
            "Content-Type": "application/json",
            "User-Agent": "LWX-EXE-Trophy-Engine/1.0",
          },
          body: JSON.stringify({ query, variables: { username } }),
        });

        if (!res.ok) continue;
        const json = (await res.json()) as { data?: { user?: T } };
        if (json?.data?.user) {
          return json.data.user;
        }
      } catch {
        // try next token
      }
    }
    return null;
  }

  private async requestPublicRestFallback(username: string): Promise<UserInfo | null> {
    const headers: Record<string, string> = {
      Accept: "application/vnd.github+json",
      "User-Agent": "LWX-EXE-Trophy-Engine/1.0",
    };

    try {
      const [userRes, reposRes, commitsSearchRes, issuesSearchRes, prsSearchRes] =
        await Promise.all([
          fetch(`https://api.github.com/users/${encodeURIComponent(username)}`, { headers }),
          fetch(
            `https://api.github.com/users/${encodeURIComponent(username)}/repos?per_page=100&type=owner`,
            { headers },
          ),
          fetch(
            `https://api.github.com/search/commits?q=author:${encodeURIComponent(username)}&per_page=1`,
            { headers },
          ),
          fetch(
            `https://api.github.com/search/issues?q=author:${encodeURIComponent(username)}+type:issue&per_page=1`,
            { headers },
          ),
          fetch(
            `https://api.github.com/search/issues?q=author:${encodeURIComponent(username)}+type:pr&per_page=1`,
            { headers },
          ),
        ]);

      if (!userRes.ok) return null;
      const userJson = (await userRes.json()) as {
        created_at: string;
        followers: number;
        public_repos: number;
      };
      const reposJson = reposRes.ok
        ? ((await reposRes.json()) as Array<{
            stargazers_count: number;
            language: string | null;
          }>)
        : [];
      const commitsJson = commitsSearchRes.ok
        ? ((await commitsSearchRes.json()) as { total_count?: number })
        : {};
      const issuesJson = issuesSearchRes.ok
        ? ((await issuesSearchRes.json()) as { total_count?: number })
        : {};
      const prsJson = prsSearchRes.ok
        ? ((await prsSearchRes.json()) as { total_count?: number })
        : {};

      const activity: GitHubUserActivity = {
        createdAt: userJson.created_at,
        contributionsCollection: {
          totalCommitContributions: commitsJson.total_count ?? 0,
          restrictedContributionsCount: 0,
          totalPullRequestReviewContributions: 0,
        },
        organizations: { totalCount: 0 },
        followers: { totalCount: userJson.followers ?? 0 },
      };

      const issues: GitHubUserIssue = {
        openIssues: { totalCount: issuesJson.total_count ?? 0 },
        closedIssues: { totalCount: 0 },
      };

      const prs: GitHubUserPullRequest = {
        pullRequests: { totalCount: prsJson.total_count ?? 0 },
      };

      const repos: GitHubUserRepository = {
        repositories: {
          totalCount: userJson.public_repos ?? reposJson.length,
          nodes: reposJson.map((r) => ({
            languages: {
              nodes: r.language ? [{ name: r.language }] : [],
            },
            stargazers: {
              totalCount: r.stargazers_count ?? 0,
            },
          })),
        },
      };

      return new UserInfo(activity, issues, prs, repos);
    } catch {
      return null;
    }
  }
}
