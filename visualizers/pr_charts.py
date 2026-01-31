from typing import Dict, List, Any
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
from .base_charts import BaseChart


class PRCharts(BaseChart):
    def plot_pr_merge_time(
        self,
        pr_data: List[Dict[str, Any]],
        filename: str = "13_prs_merge_time_box.png",
    ):
        if not pr_data:
            return

        merge_times = []
        for pr in pr_data:
            if pr.get("merged_at") and pr.get("created_at"):
                created = datetime.fromisoformat(
                    pr["created_at"].replace("Z", "+00:00")
                )
                merged = datetime.fromisoformat(pr["merged_at"].replace("Z", "+00:00"))
                hours = (merged - created).total_seconds() / 3600
                merge_times.append(hours)

        if not merge_times:
            return

        plt.figure(figsize=(10, 6))

        plt.boxplot(
            merge_times,
            vert=False,
            patch_artist=True,
            boxprops=dict(facecolor="#E85A4F", color="#4A4A48"),
            capprops=dict(color="#4A4A48"),
            whiskerprops=dict(color="#4A4A48"),
            flierprops=dict(color="#E85A4F", markeredgecolor="#E85A4F"),
            medianprops=dict(color="#4A4A48"),
        )

        plt.title("PR Merge Time Distribution (Hours)", fontsize=16, fontweight="bold")
        plt.xlabel("Hours to Merge", fontsize=12)
        plt.yticks([])
        plt.grid(True, axis="x", alpha=0.3)
        plt.tight_layout()

        return self.save_plot(filename)
