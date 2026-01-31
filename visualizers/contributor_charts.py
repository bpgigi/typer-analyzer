from typing import Dict, List, Any
import matplotlib.pyplot as plt
import numpy as np
from .base_charts import BaseChart


class ContributorRadarChart(BaseChart):
    def plot_activity_radar(
        self,
        contributor_data: Dict[str, Dict[str, float]],
        filename: str = "09_contributor_activity_radar.png",
    ):
        if not contributor_data:
            return

        categories = list(next(iter(contributor_data.values())).keys())
        N = len(categories)

        angles = [n / float(N) * 2 * np.pi for n in range(N)]
        angles += angles[:1]

        plt.figure(figsize=(10, 10))
        ax = plt.subplot(111, polar=True)

        # Ensure labels are placed correctly
        plt.xticks(angles[:-1], categories, color="grey", size=10)

        # Fix radial label position
        ax.set_rlabel_position(30)
        plt.yticks(
            [0.2, 0.4, 0.6, 0.8, 1.0],
            ["0.2", "0.4", "0.6", "0.8", "1.0"],
            color="grey",
            size=8,
        )
        plt.ylim(0, 1.1)

        colors = self.warm_colors
        for i, (name, stats) in enumerate(contributor_data.items()):
            values = list(stats.values())
            values += values[:1]

            color = colors[i % len(colors)]
            ax.plot(
                angles, values, linewidth=2, linestyle="solid", label=name, color=color
            )
            ax.fill(angles, values, color=color, alpha=0.15)

        plt.title("Contributor Activity Radar", size=20, y=1.05, fontweight="bold")
        plt.legend(loc="upper right", bbox_to_anchor=(1.2, 1.0))
        plt.tight_layout()

        return self.save_plot(filename)
