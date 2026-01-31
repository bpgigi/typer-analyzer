from typing import Dict, List, Any
import matplotlib.pyplot as plt
from .base_charts import BaseChart


class IssuesChart(BaseChart):
    def plot_state_distribution(
        self,
        issues_data: Dict[str, int],
        filename: str = "11_issues_state_pie.png",
    ):
        plt.figure(figsize=(10, 8))

        labels = list(issues_data.keys())
        sizes = list(issues_data.values())

        # Use warm colors for specific states
        colors = []
        for label in labels:
            if label.lower() == "open":
                colors.append("#E85A4F")  # Red-ish
            elif label.lower() == "closed":
                colors.append("#8E8D8A")  # Grey-ish
            else:
                colors.append("#D8C3A5")  # Beige

        plt.pie(
            sizes,
            labels=labels,
            colors=colors,
            autopct="%1.1f%%",
            startangle=90,
            explode=(0.05, 0) if len(sizes) == 2 else None,
            textprops={"fontsize": 12},
        )

        plt.title("Issues State Distribution", fontsize=16, fontweight="bold")
        plt.axis("equal")
        plt.tight_layout()

        return self.save_plot(filename)

    def plot_timeline(
        self,
        timeline_data: Dict[str, Dict[str, int]],
        filename: str = "10_issues_timeline.png",
    ):
        plt.figure(figsize=(14, 8))

        dates = sorted(timeline_data.keys())
        opened = [timeline_data[d].get("opened", 0) for d in dates]
        closed = [timeline_data[d].get("closed", 0) for d in dates]

        plt.plot(
            dates, opened, label="Opened", color="#E85A4F", linewidth=2, marker="o"
        )
        plt.plot(
            dates, closed, label="Closed", color="#8E8D8A", linewidth=2, marker="x"
        )

        plt.title("Issues Activity Timeline", fontsize=16, fontweight="bold")
        plt.xlabel("Date", fontsize=12)
        plt.ylabel("Number of Issues", fontsize=12)
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()

        return self.save_plot(filename)
