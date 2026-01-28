import requests
from typing import List, Dict, Any
from dataclasses import dataclass
from datetime import datetime


@dataclass
class IssueInfo:
    number: int
    title: str
    state: str
    created_at: datetime
    closed_at: datetime = None
    author: str = None


class GitHubCollector:
    BASE_URL = "https://api.github.com"

    def __init__(self, token: str = None):
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "TyperAnalyzer"
        }
        if token:
            self.headers["Authorization"] = f"token {token}"
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def get_issues(self, owner: str, repo: str, state: str = "all") -> List[IssueInfo]:
        issues = []
        page = 1
        while True:
            url = f"{self.BASE_URL}/repos/{owner}/{repo}/issues"
            params = {"state": state, "per_page": 100, "page": page}
            resp = self.session.get(url, params=params)
            if resp.status_code != 200:
                break
            data = resp.json()
            if not data:
                break
            for item in data:
                if "pull_request" in item:
                    continue
                issues.append(IssueInfo(
                    number=item["number"],
                    title=item["title"],
                    state=item["state"],
                    created_at=datetime.fromisoformat(item["created_at"].rstrip("Z")),
                    closed_at=datetime.fromisoformat(item["closed_at"].rstrip("Z")) if item.get("closed_at") else None,
                    author=item["user"]["login"]
                ))
            page += 1
        return issues

    def to_dict(self, issue: IssueInfo) -> Dict[str, Any]:
        return {
            "number": issue.number,
            "title": issue.title,
            "state": issue.state,
            "created_at": issue.created_at.isoformat() if issue.created_at else None,
            "closed_at": issue.closed_at.isoformat() if issue.closed_at else None,
            "author": issue.author
        }
