import requests
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class IssueInfo:
    number: int
    title: str
    state: str
    created_at: datetime
    closed_at: Optional[datetime]
    author: str
    labels: List[str]
    comments_count: int


class IssuesCollector:
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

    def collect_issues(
        self,
        owner: str,
        repo: str,
        state: str = "all",
        since: Optional[datetime] = None,
    ) -> List[IssueInfo]:
        issues = []
        page = 1

        while True:
            url = f"{self.BASE_URL}/repos/{owner}/{repo}/issues"
            params = {"state": state, "per_page": 100, "page": page}
            if since:
                params["since"] = since.isoformat()

            resp = self.session.get(url, params=params)
            if resp.status_code != 200:
                break

            data = resp.json()
            if not data:
                break

            for item in data:
                if "pull_request" in item:
                    continue

                created = datetime.fromisoformat(
                    item["created_at"].replace("Z", "+00:00")
                )
                closed = None
                if item.get("closed_at"):
                    closed = datetime.fromisoformat(
                        item["closed_at"].replace("Z", "+00:00")
                    )

                labels = [label["name"] for label in item.get("labels", [])]

                issues.append(
                    IssueInfo(
                        number=item["number"],
                        title=item["title"],
                        state=item["state"],
                        created_at=created,
                        closed_at=closed,
                        author=item["user"]["login"],
                        labels=labels,
                        comments_count=item.get("comments", 0),
                    )
                )

            page += 1
            if page > 10:
                break

        return issues

    def get_issue_stats(self, issues: List[IssueInfo]) -> Dict[str, Any]:
        open_count = sum(1 for i in issues if i.state == "open")
        closed_count = sum(1 for i in issues if i.state == "closed")

        label_counts = {}
        for issue in issues:
            for label in issue.labels:
                label_counts[label] = label_counts.get(label, 0) + 1

        return {
            "total": len(issues),
            "open": open_count,
            "closed": closed_count,
            "labels": label_counts,
        }
