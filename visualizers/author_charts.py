from typing import Dict, List, Any
from collections import Counter
from .base_charts import BaseChart


class AuthorCharts(BaseChart):
    def plot_contribution_pie(
        self,
        commits: List[Dict[str, Any]],
        filename: str = "01_author_contribution_pie.png",
    ):
        author_counts: Counter[str] = Counter()
        for commit in commits:
            if "author" in commit and isinstance(commit["author"], str):
                author_counts[commit["author"]] += 1

        data: Dict[str, float] = {k: float(v) for k, v in author_counts.most_common(10)}

        self.plot_pie(
            data, title="Top 10 Author Contributions", filename=filename, donut=True
        )
