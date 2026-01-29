from typing import Dict, List, Any
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
from .base_charts import BaseChart


class TimeHeatmap(BaseChart):
    def plot_commit_heatmap(
        self,
        commits: List[Dict[str, Any]],
        filename: str = "02_commit_time_heatmap.png",
    ):
        dates = [datetime.fromisoformat(c["date"]) for c in commits]

        df = pd.DataFrame(
            {"weekday": [d.weekday() for d in dates], "hour": [d.hour for d in dates]}
        )

        heatmap_data = df.groupby(["weekday", "hour"]).size().unstack(fill_value=0)

        for h in range(24):
            if h not in heatmap_data.columns:
                heatmap_data[h] = 0

        heatmap_data = heatmap_data.reindex(
            index=range(7), columns=range(24), fill_value=0
        )

        heatmap_data = heatmap_data.sort_index(axis=1)

        plt.figure(figsize=(16, 6))
        sns.heatmap(
            heatmap_data,
            cmap="YlOrRd",
            linewidths=0.5,
            fmt="d",
            cbar_kws={"label": "Commits"},
        )

        weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        plt.yticks([i + 0.5 for i in range(7)], weekdays, rotation=0)
        plt.xticks(
            [i + 0.5 for i in range(24)], [f"{h:02d}" for h in range(24)], rotation=0
        )

        plt.title("Commit Frequency by Day and Hour", pad=20)
        plt.xlabel("Hour of Day")
        plt.ylabel("Day of Week")

        return self.save_plot(filename)
