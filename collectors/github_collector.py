"""
GitHub API 采集器模块
从 GitHub API 获取 Issues、PRs 等信息
"""

import requests
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


@dataclass
class IssueInfo:
    """Issue 信息数据类"""

    number: int  # Issue 编号
    title: str  # 标题
    state: str  # 状态（open/closed）
    created_at: datetime  # 创建时间
    closed_at: Optional[datetime] = None  # 关闭时间
    author: Optional[str] = None  # 作者


class GitHubCollector:
    """
    GitHub API 采集器
    负责从 GitHub API 获取仓库的 Issues、PRs 等数据
    """

    BASE_URL = "https://api.github.com"

    def __init__(self, token: Optional[str] = None):
        """
        初始化采集器

        参数:
            token: GitHub API 令牌（可选，用于提高速率限制）
        """
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "TyperAnalyzer",
        }
        if token:
            self.headers["Authorization"] = f"token {token}"
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def get_issues(self, owner: str, repo: str, state: str = "all") -> List[IssueInfo]:
        """
        获取仓库的所有 Issues

        参数:
            owner: 仓库所有者
            repo: 仓库名称
            state: Issue 状态过滤（all/open/closed）

        返回:
            Issue 信息列表
        """
        issues = []
        page = 1

        while True:
            try:
                url = f"{self.BASE_URL}/repos/{owner}/{repo}/issues"
                params = {"state": state, "per_page": 100, "page": page}

                resp = self.session.get(url, params=params, timeout=30)
                resp.raise_for_status()

                data = resp.json()
                if not data:
                    break

                for item in data:
                    # 跳过 Pull Request（API 会将 PR 也返回在 issues 端点）
                    if "pull_request" in item:
                        continue
                    issues.append(
                        IssueInfo(
                            number=item["number"],
                            title=item["title"],
                            state=item["state"],
                            created_at=datetime.fromisoformat(
                                item["created_at"].rstrip("Z")
                            ),
                            closed_at=datetime.fromisoformat(
                                item["closed_at"].rstrip("Z")
                            )
                            if item.get("closed_at")
                            else None,
                            author=item["user"]["login"],
                        )
                    )

                # 检查是否有下一页
                if "next" not in resp.links:
                    break

                page += 1

            except requests.Timeout:
                logger.error(f"获取第 {page} 页超时: {url}")
                break
            except Exception as e:
                logger.error(f"获取 Issues 第 {page} 页出错: {e}")
                break

        return issues

    def to_dict(self, issue: IssueInfo) -> Dict[str, Any]:
        """
        将 Issue 信息转换为字典格式（英文key）

        参数:
            issue: Issue 信息对象

        返回:
            字典格式的 Issue 信息
        """
        return {
            "number": issue.number,
            "title": issue.title,
            "state": issue.state,
            "created_at": issue.created_at.isoformat() if issue.created_at else None,
            "closed_at": issue.closed_at.isoformat() if issue.closed_at else None,
            "author": issue.author,
        }

    def get_contributors(self, owner: str, repo: str, max_count: int = 500) -> List[Dict[str, Any]]:
        """
        获取仓库的贡献者列表

        参数:
            owner: 仓库所有者
            repo: 仓库名称
            max_count: 最大获取数量

        返回:
            贡献者信息列表
        """
        contributors = []
        page = 1

        while len(contributors) < max_count:
            try:
                url = f"{self.BASE_URL}/repos/{owner}/{repo}/contributors"
                params = {"per_page": 100, "page": page}

                resp = self.session.get(url, params=params, timeout=30)
                resp.raise_for_status()

                data = resp.json()
                if not data:
                    break

                for item in data:
                    contributors.append({
                        "login": item.get("login"),
                        "id": item.get("id"),
                        "contributions": item.get("contributions"),
                        "avatar_url": item.get("avatar_url"),
                        "type": item.get("type"),
                    })

                if "next" not in resp.links:
                    break

                page += 1

            except requests.Timeout:
                logger.error(f"获取贡献者第 {page} 页超时")
                break
            except Exception as e:
                logger.error(f"获取贡献者第 {page} 页出错: {e}")
                break

        return contributors[:max_count]
