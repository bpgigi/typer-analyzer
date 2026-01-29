import csv
import json
from typing import List, Dict, Any
from pathlib import Path
from collectors.commit_collector import CommitInfo


class DataExporter:
    def __init__(self, output_dir: str = "data"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def export_commits_csv(
        self, commits: List[CommitInfo], filename: str = "commits.csv"
    ):
        csv_path = self.output_dir / filename
        with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=[
                    "hash",
                    "author",
                    "email",
                    "date",
                    "message",
                    "files_changed",
                    "insertions",
                    "deletions",
                ],
            )
            writer.writeheader()
            for commit in commits:
                writer.writerow(
                    {
                        "hash": commit.hash,
                        "author": commit.author,
                        "email": commit.email,
                        "date": commit.date.isoformat(),
                        "message": commit.message,
                        "files_changed": commit.files_changed,
                        "insertions": commit.insertions,
                        "deletions": commit.deletions,
                    }
                )
        return str(csv_path)

    def export_issues_csv(self, issues: List[Any], filename: str = "issues.csv"):
        csv_path = self.output_dir / filename
        with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
            if not issues:
                return str(csv_path)

            fieldnames = [
                "number",
                "title",
                "state",
                "created_at",
                "closed_at",
                "author",
                "comments_count",
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for issue in issues:
                writer.writerow(
                    {
                        "number": issue.number,
                        "title": issue.title,
                        "state": issue.state,
                        "created_at": issue.created_at.isoformat()
                        if issue.created_at
                        else "",
                        "closed_at": issue.closed_at.isoformat()
                        if issue.closed_at
                        else "",
                        "author": issue.author,
                        "comments_count": issue.comments_count,
                    }
                )
        return str(csv_path)

    def export_prs_csv(self, prs: List[Any], filename: str = "prs.csv"):
        csv_path = self.output_dir / filename
        with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
            if not prs:
                return str(csv_path)

            fieldnames = [
                "number",
                "title",
                "state",
                "created_at",
                "closed_at",
                "merged_at",
                "author",
                "merged_by",
                "additions",
                "deletions",
                "changed_files",
                "base_branch",
                "head_branch",
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for pr in prs:
                writer.writerow(
                    {
                        "number": pr.number,
                        "title": pr.title,
                        "state": pr.state,
                        "created_at": pr.created_at.isoformat()
                        if pr.created_at
                        else "",
                        "closed_at": pr.closed_at.isoformat() if pr.closed_at else "",
                        "merged_at": pr.merged_at.isoformat() if pr.merged_at else "",
                        "author": pr.author,
                        "merged_by": pr.merged_by,
                        "additions": pr.additions,
                        "deletions": pr.deletions,
                        "changed_files": pr.changed_files,
                        "base_branch": pr.base_branch,
                        "head_branch": pr.head_branch,
                    }
                )
        return str(csv_path)

    def export_json(self, data: Dict[str, Any], filename: str):
        json_path = self.output_dir / filename
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return str(json_path)
