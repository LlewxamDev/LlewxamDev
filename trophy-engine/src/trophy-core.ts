/**
 * ============================================================================
 * PROJECT LWX.EXE — TROPHY CORE ENGINE
 * ============================================================================
 * Direct TypeScript/ESM preservation of GinWU05/github-profile-trophy
 * (Copyright (c) 2020 screw-hand, MIT License).
 *
 * All rank thresholds, score calculations, secret trophy unlock conditions,
 * and original achievement titles/messages are 100% preserved without
 * modification.
 * ============================================================================
 */

export const CONSTANTS = {
  CACHE_MAX_AGE: 7200,
  DEFAULT_PANEL_SIZE: 110,
  DEFAULT_MAX_COLUMN: 4,
  DEFAULT_MAX_ROW: 3,
  DEFAULT_MARGIN_W: 12,
  DEFAULT_MARGIN_H: 12,
  DEFAULT_NO_BACKGROUND: false,
  DEFAULT_NO_FRAME: false,
  DEFAULT_GITHUB_API: "https://api.github.com/graphql",
} as const;

export enum RANK {
  SECRET = "SECRET",
  SSS = "SSS",
  SS = "SS",
  S = "S",
  AAA = "AAA",
  AA = "AA",
  A = "A",
  B = "B",
  C = "C",
  UNKNOWN = "UNKNOWN",
}

export const RANK_ORDER: RANK[] = Object.values(RANK);

export function abridgeScore(score: number): string {
  if (Math.abs(score) < 1) {
    return "0pt";
  }
  if (Math.abs(score) > 999) {
    return (Math.sign(score) * (Math.abs(score) / 1000)).toFixed(1) + "kpt";
  }
  return (Math.sign(score) * Math.abs(score)).toString() + "pt";
}

export interface WantFlags {
  AchieveSuperRank: boolean;
  MultipleLang: boolean;
  LongTimeAccount: boolean;
  AncientAccount: boolean;
  NewAccount: boolean;
  MultipleOrganizations: boolean;
}

export const DEFAULT_WANT_FLAGS: WantFlags = {
  AchieveSuperRank: false,
  MultipleLang: false,
  LongTimeAccount: false,
  AncientAccount: false,
  NewAccount: false,
  MultipleOrganizations: false,
};

export type LanguageNode = { name: string };
export type StargazersNode = { totalCount: number };
export type RepositoryNode = {
  languages: { nodes: LanguageNode[] };
  stargazers: StargazersNode;
};

export type GitHubUserRepository = {
  repositories: {
    totalCount: number;
    nodes: RepositoryNode[];
  };
};

export type GitHubUserIssue = {
  openIssues: { totalCount: number };
  closedIssues: { totalCount: number };
};

export type GitHubUserPullRequest = {
  pullRequests: { totalCount: number };
};

export type GitHubUserActivity = {
  createdAt: string;
  contributionsCollection: {
    totalCommitContributions: number;
    restrictedContributionsCount: number;
    totalPullRequestReviewContributions: number;
  };
  organizations: { totalCount: number };
  followers: { totalCount: number };
};

export class UserInfo {
  public readonly totalCommits: number;
  public readonly totalFollowers: number;
  public readonly totalIssues: number;
  public readonly totalOrganizations: number;
  public readonly totalPullRequests: number;
  public readonly totalReviews: number;
  public readonly totalStargazers: number;
  public readonly totalRepositories: number;
  public readonly languageCount: number;
  public readonly durationYear: number;
  public readonly ancientAccount: number;
  public readonly ogAccount: number;
  public readonly newAccount: number;

  constructor(
    userActivity: GitHubUserActivity,
    userIssue: GitHubUserIssue,
    userPullRequest: GitHubUserPullRequest,
    userRepository: GitHubUserRepository,
  ) {
    const totalCommits =
      userActivity.contributionsCollection.restrictedContributionsCount +
      userActivity.contributionsCollection.totalCommitContributions;

    const totalStargazers = userRepository.repositories.nodes.reduce(
      (prev: number, node: RepositoryNode) => prev + node.stargazers.totalCount,
      0,
    );

    const languages = new Set<string>();
    userRepository.repositories.nodes.forEach((node: RepositoryNode) => {
      if (node.languages?.nodes !== undefined) {
        node.languages.nodes.forEach((langNode: LanguageNode) => {
          if (langNode !== undefined && langNode.name) {
            languages.add(langNode.name);
          }
        });
      }
    });

    const durationTime =
      new Date().getTime() - new Date(userActivity.createdAt).getTime();
    const durationYear = new Date(durationTime).getUTCFullYear() - 1970;
    const createdYear = new Date(userActivity.createdAt).getFullYear();
    const ancientAccount = createdYear <= 2010 ? 1 : 0;
    const newAccount = createdYear === 2020 ? 1 : 0;
    const ogAccount = createdYear <= 2008 ? 1 : 0;

    this.totalCommits = totalCommits;
    this.totalFollowers = userActivity.followers.totalCount;
    this.totalIssues =
      userIssue.openIssues.totalCount + userIssue.closedIssues.totalCount;
    this.totalOrganizations = userActivity.organizations.totalCount;
    this.totalPullRequests = userPullRequest.pullRequests.totalCount;
    this.totalReviews =
      userActivity.contributionsCollection.totalPullRequestReviewContributions;
    this.totalStargazers = totalStargazers;
    this.totalRepositories = userRepository.repositories.totalCount;
    this.languageCount = languages.size;
    this.durationYear = durationYear;
    this.ancientAccount = ancientAccount;
    this.newAccount = newAccount;
    this.ogAccount = ogAccount;
  }
}

export class RankCondition {
  constructor(
    readonly rank: RANK,
    readonly message: string,
    readonly requiredScore: number,
  ) {}
}

export class Trophy {
  rankCondition: RankCondition | null = null;
  rank: RANK = RANK.UNKNOWN;
  topMessage = "Unknown";
  bottomMessage = "0";
  title = "";
  filterTitles: Array<string> = [];
  hidden = false;

  constructor(
    public readonly score: number,
    public readonly rankConditions: Array<RankCondition>,
  ) {
    this.bottomMessage = abridgeScore(score);
    this.setRank();
  }

  setRank() {
    const sortedRankConditions = [...this.rankConditions].sort(
      (a, b) => RANK_ORDER.indexOf(a.rank) - RANK_ORDER.indexOf(b.rank),
    );
    const rankCondition = sortedRankConditions.find(
      (r) => this.score >= r.requiredScore,
    );
    if (rankCondition != null) {
      this.rank = rankCondition.rank;
      this.rankCondition = rankCondition;
      this.topMessage = rankCondition.message;
    }
  }

  calculateNextRankPercentage(): number {
    if (this.rank === RANK.UNKNOWN) {
      return 0;
    }
    const nextRankIndex = RANK_ORDER.indexOf(this.rank) - 1;
    if (nextRankIndex < 0 || this.rank === RANK.SSS || this.rank === RANK.SECRET) {
      return 1;
    }
    const nextRank = RANK_ORDER[nextRankIndex];
    const nextRankCondition = this.rankConditions.find(
      (r) => r.rank === nextRank,
    );
    if (!nextRankCondition || !this.rankCondition) {
      return 1;
    }
    const distance =
      nextRankCondition.requiredScore - this.rankCondition.requiredScore;
    if (distance <= 0) return 1;
    const progress = this.score - this.rankCondition.requiredScore;
    return Math.max(0, Math.min(1, progress / distance));
  }

  getNextRankInfo(): { nextRank: string; requiredScore: number | null } {
    if (this.rank === RANK.UNKNOWN) {
      const lowest = this.rankConditions[this.rankConditions.length - 1];
      return {
        nextRank: lowest ? lowest.rank : "C",
        requiredScore: lowest ? lowest.requiredScore : 1,
      };
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

export class MultipleLangTrophy extends Trophy {
  constructor(score: number, want: WantFlags = DEFAULT_WANT_FLAGS) {
    super(score, [
      new RankCondition(RANK.SECRET, "Rainbow Lang User", want.MultipleLang ? 0 : 5),
    ]);
    this.title = "MultiLanguage";
    this.filterTitles = ["MultipleLang", "MultiLanguage"];
    this.hidden = true;
  }
}

export class AllSuperRankTrophy extends Trophy {
  constructor(score: number) {
    super(score, [new RankCondition(RANK.SECRET, "S Rank Hacker", 1)]);
    this.title = "AllSuperRank";
    this.filterTitles = ["AllSuperRank"];
    this.bottomMessage = "All S Rank";
    this.hidden = true;
  }
}

export class AchieveSuperRankTrophy extends Trophy {
  constructor(score: number, want: WantFlags = DEFAULT_WANT_FLAGS) {
    super(score, [
      new RankCondition(RANK.SECRET, "SSS Rank Hacker", want.AchieveSuperRank ? 0 : 1),
    ]);
    this.title = "AchieveSSSRank";
    this.filterTitles = ["AchieveSuperRank", "AchieveSSSRank"];
    this.bottomMessage = "Have SSS Rank";
    this.hidden = true;
  }
}

export class NewAccountTrophy extends Trophy {
  constructor(score: number, want: WantFlags = DEFAULT_WANT_FLAGS) {
    super(score, [
      new RankCondition(RANK.SECRET, "Everything started...", want.NewAccount ? 0 : 1),
    ]);
    this.title = "NewUser";
    this.filterTitles = ["NewUser"];
    this.bottomMessage = "After 2020";
    this.hidden = true;
  }
}

export class AncientAccountTrophy extends Trophy {
  constructor(score: number, want: WantFlags = DEFAULT_WANT_FLAGS) {
    super(score, [
      new RankCondition(RANK.SECRET, "Ancient User", want.AncientAccount ? 0 : 1),
    ]);
    this.title = "AncientUser";
    this.filterTitles = ["AncientUser"];
    this.bottomMessage = "Before 2010";
    this.hidden = true;
  }
}

export class LongTimeAccountTrophy extends Trophy {
  constructor(score: number, want: WantFlags = DEFAULT_WANT_FLAGS) {
    super(score, [
      new RankCondition(RANK.SECRET, "Village Elder", want.LongTimeAccount ? 0 : 3),
    ]);
    this.title = "LongTimeUser";
    this.filterTitles = ["LongTimeUser"];
    this.bottomMessage = score + (score > 0 ? "years" : "year");
    this.hidden = true;
  }
}

export class MultipleOrganizationsTrophy extends Trophy {
  constructor(score: number, want: WantFlags = DEFAULT_WANT_FLAGS) {
    super(score, [
      new RankCondition(
        RANK.SECRET,
        "Jack of all Trades",
        want.MultipleOrganizations ? 0 : 3,
      ),
    ]);
    this.title = "Organizations";
    this.filterTitles = ["Organizations", "Orgs", "Teams"];
    this.hidden = true;
  }
}

export class OGAccountTrophy extends Trophy {
  constructor(score: number) {
    super(score, [new RankCondition(RANK.SECRET, "OG User", 1)]);
    this.title = "OGUser";
    this.filterTitles = ["OGUser"];
    this.bottomMessage = "Joined 2008";
    this.hidden = true;
  }
}

export class TotalReviewsTrophy extends Trophy {
  constructor(score: number) {
    super(score, [
      new RankCondition(RANK.SSS, "God Reviewer", 70),
      new RankCondition(RANK.SS, "Deep Reviewer", 57),
      new RankCondition(RANK.S, "Super Reviewer", 45),
      new RankCondition(RANK.AAA, "Ultra Reviewer", 30),
      new RankCondition(RANK.AA, "Hyper Reviewer", 20),
      new RankCondition(RANK.A, "Active Reviewer", 8),
      new RankCondition(RANK.B, "Intermediate Reviewer", 3),
      new RankCondition(RANK.C, "New Reviewer", 1),
    ]);
    this.title = "Reviews";
    this.filterTitles = ["Review", "Reviews"];
  }
}

export class TotalStarTrophy extends Trophy {
  constructor(score: number) {
    super(score, [
      new RankCondition(RANK.SSS, "Super Stargazer", 1200),
      new RankCondition(RANK.SS, "High Stargazer", 500),
      new RankCondition(RANK.S, "Stargazer", 250),
      new RankCondition(RANK.AAA, "Super Star", 100),
      new RankCondition(RANK.AA, "High Star", 50),
      new RankCondition(RANK.A, "You are a Star", 25),
      new RankCondition(RANK.B, "Middle Star", 10),
      new RankCondition(RANK.C, "First Star", 1),
    ]);
    this.title = "Stars";
    this.filterTitles = ["Star", "Stars"];
  }
}

export class TotalCommitTrophy extends Trophy {
  constructor(score: number) {
    super(score, [
      new RankCondition(RANK.SSS, "God Committer", 2000),
      new RankCondition(RANK.SS, "Deep Committer", 1000),
      new RankCondition(RANK.S, "Super Committer", 700),
      new RankCondition(RANK.AAA, "Ultra Committer", 500),
      new RankCondition(RANK.AA, "Hyper Committer", 200),
      new RankCondition(RANK.A, "High Committer", 100),
      new RankCondition(RANK.B, "Middle Committer", 10),
      new RankCondition(RANK.C, "First Commit", 1),
    ]);
    this.title = "Commits";
    this.filterTitles = ["Commit", "Commits"];
  }
}

export class TotalFollowerTrophy extends Trophy {
  constructor(score: number) {
    super(score, [
      new RankCondition(RANK.SSS, "Super Celebrity", 1000),
      new RankCondition(RANK.SS, "Ultra Celebrity", 400),
      new RankCondition(RANK.S, "Hyper Celebrity", 200),
      new RankCondition(RANK.AAA, "Famous User", 100),
      new RankCondition(RANK.AA, "Active User", 50),
      new RankCondition(RANK.A, "Dynamic User", 20),
      new RankCondition(RANK.B, "Many Friends", 10),
      new RankCondition(RANK.C, "First Friend", 1),
    ]);
    this.title = "Followers";
    this.filterTitles = ["Follower", "Followers"];
  }
}

export class TotalIssueTrophy extends Trophy {
  constructor(score: number) {
    super(score, [
      new RankCondition(RANK.SSS, "God Issuer", 500),
      new RankCondition(RANK.SS, "Deep Issuer", 200),
      new RankCondition(RANK.S, "Super Issuer", 100),
      new RankCondition(RANK.AAA, "Ultra Issuer", 50),
      new RankCondition(RANK.AA, "Hyper Issuer", 20),
      new RankCondition(RANK.A, "High Issuer", 10),
      new RankCondition(RANK.B, "Middle Issuer", 5),
      new RankCondition(RANK.C, "First Issue", 1),
    ]);
    this.title = "Issues";
    this.filterTitles = ["Issue", "Issues"];
  }
}

export class TotalPullRequestTrophy extends Trophy {
  constructor(score: number) {
    super(score, [
      new RankCondition(RANK.SSS, "God Puller", 500),
      new RankCondition(RANK.SS, "Deep Puller", 200),
      new RankCondition(RANK.S, "Super Puller", 100),
      new RankCondition(RANK.AAA, "Ultra Puller", 50),
      new RankCondition(RANK.AA, "Hyper Puller", 20),
      new RankCondition(RANK.A, "High Puller", 10),
      new RankCondition(RANK.B, "Middle Puller", 5),
      new RankCondition(RANK.C, "First Pull", 1),
    ]);
    this.title = "PullRequest";
    this.filterTitles = ["PR", "PullRequest", "Pulls", "Puller"];
  }
}

export class TotalRepositoryTrophy extends Trophy {
  constructor(score: number) {
    super(score, [
      new RankCondition(RANK.SSS, "God Repo Creator", 100),
      new RankCondition(RANK.SS, "Deep Repo Creator", 70),
      new RankCondition(RANK.S, "Super Repo Creator", 50),
      new RankCondition(RANK.AAA, "Ultra Repo Creator", 40),
      new RankCondition(RANK.AA, "Hyper Repo Creator", 30),
      new RankCondition(RANK.A, "High Repo Creator", 20),
      new RankCondition(RANK.B, "Middle Repo Creator", 10),
      new RankCondition(RANK.C, "First Repository", 1),
    ]);
    this.title = "Repositories";
    this.filterTitles = ["Repo", "Repository", "Repositories"];
  }
}

export class TrophyList {
  private trophies = new Array<Trophy>();

  constructor(userInfo: UserInfo, want: WantFlags = DEFAULT_WANT_FLAGS) {
    // Base trophies (7)
    this.trophies.push(
      new TotalStarTrophy(userInfo.totalStargazers),
      new TotalCommitTrophy(userInfo.totalCommits),
      new TotalFollowerTrophy(userInfo.totalFollowers),
      new TotalIssueTrophy(userInfo.totalIssues),
      new TotalPullRequestTrophy(userInfo.totalPullRequests),
      new TotalRepositoryTrophy(userInfo.totalRepositories),
      new TotalReviewsTrophy(userInfo.totalReviews),
    );
    // Secret trophies (8)
    this.trophies.push(
      new AllSuperRankTrophy(this.isAllSRank),
      new AchieveSuperRankTrophy(this.haveSSSRank, want),
      new MultipleLangTrophy(userInfo.languageCount, want),
      new LongTimeAccountTrophy(userInfo.durationYear, want),
      new AncientAccountTrophy(userInfo.ancientAccount, want),
      new OGAccountTrophy(userInfo.ogAccount),
      new NewAccountTrophy(userInfo.newAccount, want),
      new MultipleOrganizationsTrophy(userInfo.totalOrganizations, want),
    );
  }

  get length(): number {
    return this.trophies.length;
  }

  get getArray(): Array<Trophy> {
    return this.trophies;
  }

  private get isAllSRank(): number {
    return this.trophies.every((trophy) => trophy.rank.slice(0, 1) === RANK.S)
      ? 1
      : 0;
  }

  private get haveSSSRank(): number {
    return this.trophies.some((trophy) => trophy.rank.slice(0, 1) === RANK.S)
      ? 1
      : 0;
  }

  filterByHidden(): void {
    this.trophies = this.trophies.filter(
      (trophy) => !trophy.hidden || trophy.rank !== RANK.UNKNOWN,
    );
  }

  filterByTitles(titles: Array<string>): void {
    this.trophies = this.trophies.filter((trophy) =>
      trophy.filterTitles.some((title) => titles.includes(title)),
    );
  }

  filterByRanks(ranks: Array<string>): void {
    if (ranks.filter((rank) => rank.includes("-")).length !== 0) {
      this.trophies = this.trophies.filter(
        (trophy) =>
          !ranks.map((rank) => rank.substring(1)).includes(trophy.rank),
      );
      return;
    }
    this.trophies = this.trophies.filter((trophy) =>
      ranks.includes(trophy.rank),
    );
  }

  sortByRank(): void {
    this.trophies = this.trophies.sort(
      (a: Trophy, b: Trophy) =>
        RANK_ORDER.indexOf(a.rank) - RANK_ORDER.indexOf(b.rank),
    );
  }
}
