"""
Git 提交采集器模块
使用 PyDriller 从 Git 仓库中采集提交信息
"""

from datetime import datetime
from typing import List, Dict, Any, Optional
from pydriller import Repository
from dataclasses import dataclass


@dataclass
class CommitInfo:
    """提交信息数据类"""

    hash: str  # 提交哈希值
    author: str  # 作者名称
    email: str  # 作者邮箱
    date: datetime  # 提交日期
    message: str  # 提交消息
    files_changed: int  # 修改文件数
    insertions: int  # 新增行数
    deletions: int  # 删除行数


class CommitCollector:
    """
    提交采集器
    负责从 Git 仓库中采集提交记录
    """

    def __init__(self, repo_path: str):
        """
        初始化采集器

        参数:
            repo_path: Git 仓库路径
        """
        self.repo_path = repo_path

    def collect(
        self, from_date: Optional[datetime] = None, to_date: Optional[datetime] = None
    ) -> List[CommitInfo]:
        """
        采集提交记录

        参数:
            from_date: 起始日期（可选）
            to_date: 结束日期（可选）

        返回:
            提交信息列表
        """
        commits = []
        for commit in Repository(self.repo_path).traverse_commits():
            # 日期过滤
            if from_date and commit.author_date < from_date:
                continue
            if to_date and commit.author_date > to_date:
                continue

            commits.append(
                CommitInfo(
                    hash=commit.hash,
                    author=commit.author.name,
                    email=commit.author.email,
                    date=commit.author_date,
                    message=commit.message,
                    files_changed=len(commit.files),
                    insertions=commit.insertions,
                    deletions=commit.deletions,
                )
            )
        return commits

    def to_dict(self, commit: CommitInfo) -> Dict[str, Any]:
        """
        将提交信息转换为字典格式

        参数:
            commit: 提交信息对象

        返回:
            字典格式的提交信息
        """
        return {
            "哈希": commit.hash,
            "作者": commit.author,
            "邮箱": commit.email,
            "日期": commit.date.isoformat(),
            "消息": commit.message,
            "修改文件数": commit.files_changed,
            "新增行数": commit.insertions,
            "删除行数": commit.deletions,
        }
