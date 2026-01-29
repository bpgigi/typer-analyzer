import requests
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class PRInfo:
    number: int
    title: str
    state: str
    created_at: datetime
    closed_at: Optional[datetime]
    merged_at: Optional[datetime]
    author: str
    merged_by: Optional[str]
    additions: int
    deletions: int
    changed_files: int
    base_branch: str
    head_branch: str


class PRsCollector:
    BASE_URL = "https://api.github.com"

    def __init__(self, token: Optional[str] = None):
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "TyperAnalyzer",
        }
        if token:
            self.headers["Authorization"] = f"token {token}"
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def collect_prs(
        self, owner: str, repo: str, state: str = "all", limit: int = 100
    ) -> List[PRInfo]:
        prs = []
        page = 1
        count = 0

        while True:
            if count >= limit:
                break

            url = f"{self.BASE_URL}/repos/{owner}/{repo}/pulls"
            params = {
                "state": state,
                "per_page": 100,
                "page": page,
                "sort": "created",
                "direction": "desc",
            }

            resp = self.session.get(url, params=params)
            if resp.status_code != 200:
                break

            data = resp.json()
            if not data:
                break

            for item in data:
                if count >= limit:
                    break

                pr_url = item["url"]
                detail_resp = self.session.get(pr_url)
                if detail_resp.status_code == 200:
                    detail = detail_resp.json()

                    created = datetime.fromisoformat(
                        item["created_at"].replace("Z", "+00:00")
                    )
                    closed = None
                    if item.get("closed_at"):
                        closed = datetime.fromisoformat(
                            item["closed_at"].replace("Z", "+00:00")
                        )

                    merged = None
                    if item.get("merged_at"):
                        merged = datetime.fromisoformat(
                            item["merged_at"].replace("Z", "+00:00")
                        )

                    merged_by = None
                    if detail.get("merged_by"):
                        merged_by = detail["merged_by"]["login"]

                    prs.append(
                        PRInfo(
                            number=item["number"],
                            title=item["title"],
                            state=item["state"],
                            created_at=created,
                            closed_at=closed,
                            merged_at=merged,
                            author=item["user"]["login"],
                            merged_by=merged_by,
                            additions=detail.get("additions", 0),
                            deletions=detail.get("deletions", 0),
                            changed_files=detail.get("changed_files", 0),
                            base_branch=item["base"]["ref"],
                            head_branch=item["head"]["ref"],
                        )
                    )
                    count += 1

            page += 1
            if page > 10:
                break

        return prs

    def get_pr_stats(self, prs: List[PRInfo]) -> Dict[str, Any]:
        merged_count = sum(1 for p in prs if p.merged_at)
        closed_unmerged = sum(1 for p in prs if p.state == "closed" and not p.merged_at)
        open_count = sum(1 for p in prs if p.state == "open")

        merge_times = []
        for pr in prs:
            if pr.merged_at:
                diff = pr.merged_at - pr.created_at
                merge_times.append(diff.total_seconds() / 3600)

        avg_merge_time = sum(merge_times) / len(merge_times) if merge_times else 0

        return {
            "total": len(prs),
            "merged": merged_count,
            "closed_unmerged": closed_unmerged,
            "open": open_count,
            "avg_merge_time_hours": avg_merge_time,
        }
