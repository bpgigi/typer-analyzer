from datetime import datetime
from typing import List, Dict, Any
from pydriller import Repository
from dataclasses import dataclass


@dataclass
class CommitInfo:
    hash: str
    author: str
    email: str
    date: datetime
    message: str
    files_changed: int
    insertions: int
    deletions: int


class CommitCollector:
    def __init__(self, repo_path: str):
        self.repo_path = repo_path

    def collect(self, from_date: datetime = None, to_date: datetime = None) -> List[CommitInfo]:
        commits = []
        for commit in Repository(self.repo_path).traverse_commits():
            if from_date and commit.author_date < from_date:
                continue
            if to_date and commit.author_date > to_date:
                continue
            commits.append(CommitInfo(
                hash=commit.hash,
                author=commit.author.name,
                email=commit.author.email,
                date=commit.author_date,
                message=commit.message,
                files_changed=len(commit.files),
                insertions=commit.insertions,
                deletions=commit.deletions
            ))
        return commits

    def to_dict(self, commit: CommitInfo) -> Dict[str, Any]:
        return {
            "hash": commit.hash,
            "author": commit.author,
            "email": commit.email,
            "date": commit.date.isoformat(),
            "message": commit.message,
            "files_changed": commit.files_changed,
            "insertions": commit.insertions,
            "deletions": commit.deletions
        }
