import requests
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
from utils.cache import Cache


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

    def __init__(self, token: Optional[str] = None, use_cache: bool = True):
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "TyperAnalyzer",
        }
        if token:
            self.headers["Authorization"] = f"token {token}"
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.cache = Cache() if use_cache else None

    def collect_issues(
        self,
        owner: str,
        repo: str,
        state: str = "all",
        since: Optional[datetime] = None,
    ) -> List[IssueInfo]:
        cache_key = f"issues_{owner}_{repo}_{state}"
        if self.cache:
            try:
                cached_data = self.cache.load_json(f"{cache_key}.json")
                if cached_data:
                    print(f"Loaded {len(cached_data)} issues from cache")
                    return [
                        IssueInfo(
                            number=i["number"],
                            title=i["title"],
                            state=i["state"],
                            created_at=datetime.fromisoformat(i["created_at"]),
                            closed_at=datetime.fromisoformat(i["closed_at"])
                            if i.get("closed_at")
                            else None,
                            author=i["author"],
                            labels=i["labels"],
                            comments_count=i["comments_count"],
                        )
                        for i in cached_data
                    ]
            except Exception as e:
                print(f"Error loading cache: {e}")

        issues = []
        page = 1

        # Use session with retries for robustness
        from requests.adapters import HTTPAdapter
        from urllib3.util.retry import Retry

        try:
            retry_strategy = Retry(
                total=3,
                backoff_factor=1,
                status_forcelist=[429, 500, 502, 503, 504],
            )
            adapter = HTTPAdapter(max_retries=retry_strategy)
            self.session.mount("https://", adapter)
            self.session.mount("http://", adapter)
        except Exception as e:
            print(f"Warning: Could not configure retry strategy: {e}")

        while True:
            url = f"{self.BASE_URL}/repos/{owner}/{repo}/issues"
            params = {"state": state, "per_page": 100, "page": page}
            if since:
                params["since"] = since.isoformat()

            try:
                resp = self.session.get(url, params=params, timeout=30)
                if resp.status_code != 200:
                    print(f"Failed to fetch issues: {resp.status_code}")
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
            except Exception as e:
                print(f"Error collecting issues: {e}")
                break

        if self.cache:
            data_to_cache = [
                {
                    "number": i.number,
                    "title": i.title,
                    "state": i.state,
                    "created_at": i.created_at.isoformat(),
                    "closed_at": i.closed_at.isoformat() if i.closed_at else None,
                    "author": i.author,
                    "labels": i.labels,
                    "comments_count": i.comments_count,
                }
                for i in issues
            ]
            self.cache.save_json(data_to_cache, f"{cache_key}.json")

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
