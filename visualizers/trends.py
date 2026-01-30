from typing import Dict, List, Any
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
from .base_charts import BaseChart


class TrendsChart(BaseChart):
    def plot_monthly_trend(
        self, commits: List[Dict[str, Any]], filename: str = "04_monthly_trend_line.png"
    ):
        dates = [datetime.fromisoformat(c["date"]) for c in commits]
        if not dates:
            return None

        df = pd.DataFrame({"date": dates})
        df["month_year"] = df["date"].dt.to_period("M")

        monthly_counts = df.groupby("month_year").size()

        idx = pd.period_range(
            start=df["month_year"].min(), end=df["month_year"].max(), freq="M"
        )
        monthly_counts = monthly_counts.reindex(idx, fill_value=0)

        plt.figure(figsize=(12, 6))

        x_labels = [str(p) for p in monthly_counts.index]
        plt.plot(
            x_labels,
            monthly_counts.values,
            marker="o",
            linewidth=2,
            color=self._get_color(1),
        )

        plt.fill_between(
            x_labels, monthly_counts.values, alpha=0.3, color=self._get_color(1)
        )

        plt.title("Monthly Commit Trend", pad=20)
        plt.xlabel("Month")
        plt.ylabel("Number of Commits")
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)

        return self.save_plot(filename)

    def _get_color(self, index: int):
        from config import WARM_PALETTE

        return WARM_PALETTE[index % len(WARM_PALETTE)]
