import requests
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ContributorInfo:
    login: str
    id: int
    avatar_url: str
    contributions: int
    html_url: str


class ContributorsCollector:
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

    def get_contributors(self, owner: str, repo: str) -> List[ContributorInfo]:
        contributors = []
        page = 1
        while True:
            url = f"{self.BASE_URL}/repos/{owner}/{repo}/contributors"
            params = {"per_page": 100, "page": page}
            resp = self.session.get(url, params=params)
            if resp.status_code != 200:
                break
            data = resp.json()
            if not data:
                break
            for item in data:
                contributors.append(
                    ContributorInfo(
                        login=item.get("login", ""),
                        id=item.get("id", 0),
                        avatar_url=item.get("avatar_url", ""),
                        contributions=item.get("contributions", 0),
                        html_url=item.get("html_url", ""),
                    )
                )
            page += 1
        return contributors

    def to_dict(self, contributor: ContributorInfo) -> Dict[str, Any]:
        return {
            "login": contributor.login,
            "id": contributor.id,
            "avatar_url": contributor.avatar_url,
            "contributions": contributor.contributions,
            "html_url": contributor.html_url,
        }
