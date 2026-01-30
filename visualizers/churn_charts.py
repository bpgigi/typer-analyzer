from typing import Dict, List, Any
import matplotlib.pyplot as plt
from datetime import datetime
from .base_charts import BaseChart


class CodeChurnChart(BaseChart):
    def plot_churn_trend(
        self, commits: List[Dict[str, Any]], filename: str = "06_code_churn_trend.png"
    ):
        dates = [datetime.fromisoformat(c["date"]) for c in commits]
        additions = [c["insertions"] for c in commits]
        deletions = [c["deletions"] for c in commits]

        if not dates:
            return None

        plt.figure(figsize=(12, 6))

        plt.plot(
            dates, additions, label="Additions", color=self._get_color(2), alpha=0.7
        )
        plt.plot(
            dates, deletions, label="Deletions", color=self._get_color(0), alpha=0.7
        )

        plt.fill_between(dates, additions, alpha=0.3, color=self._get_color(2))
        plt.fill_between(dates, deletions, alpha=0.3, color=self._get_color(0))

        plt.title("Code Churn Over Time", pad=20)
        plt.xlabel("Date")
        plt.ylabel("Lines Changed")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)

        return self.save_plot(filename)

    def _get_color(self, index: int):
        from config import WARM_PALETTE

        return WARM_PALETTE[index % len(WARM_PALETTE)]
