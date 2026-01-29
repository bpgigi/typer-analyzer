from typing import Dict, List, Any
from collections import Counter
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
from .base_charts import BaseChart


class YearlyChart(BaseChart):
    def plot_yearly_commits(
        self, commits: List[Dict[str, Any]], filename: str = "03_yearly_commits_bar.png"
    ):
        years = [datetime.fromisoformat(c["date"]).year for c in commits]
        year_counts = Counter(years)

        if not years:
            return None

        min_year = min(years)
        max_year = max(years)
        all_years = range(min_year, max_year + 1)

        counts = [year_counts.get(y, 0) for y in all_years]

        plt.figure(figsize=(10, 6))
        bars = plt.bar(all_years, counts, color=self._get_color(0))

        for bar in bars:
            height = bar.get_height()
            plt.text(
                bar.get_x() + bar.get_width() / 2.0,
                height,
                f"{int(height)}",
                ha="center",
                va="bottom",
            )

        plt.title("Commits per Year", pad=20)
        plt.xlabel("Year")
        plt.ylabel("Number of Commits")
        plt.xticks(all_years)

        return self.save_plot(filename)

    def _get_color(self, index: int):
        from config import WARM_PALETTE

        return WARM_PALETTE[index % len(WARM_PALETTE)]
