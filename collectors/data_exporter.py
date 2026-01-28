import csv
import json
from typing import List, Dict, Any
from collectors.commit_collector import CommitInfo


class DataExporter:
    def __init__(self, output_dir: str = "data"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def export_commits_csv(self, commits: List[CommitInfo], filename: str = "commits.csv"):
        csv_path = self.output_dir / filename
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'hash', 'author', 'email', 'date', 'message',
                'files_changed', 'insertions', 'deletions'
            ])
            writer.writeheader()
            for commit in commits:
                writer.writerow({
                    'hash': commit.hash,
                    'author': commit.author,
                    'email': commit.email,
                    'date': commit.date.isoformat(),
                    'message': commit.message,
                    'files_changed': commit.files_changed,
                    'insertions': commit.insertions,
                    'deletions': commit.deletions
                })
        return str(csv_path)

    def export_json(self, data: Dict[str, Any], filename: str):
        json_path = self.output_dir / filename
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return str(json_path)
