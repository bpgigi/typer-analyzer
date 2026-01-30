from typing import Dict, List, Any
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from .base_charts import BaseChart


class FileHeatmap(BaseChart):
    def plot_file_changes(
        self,
        commits: List[Dict[str, Any]],
        filename: str = "05_file_change_heatmap.png",
    ):
        plt.figure(figsize=(12, 8))
        plt.text(
            0.5,
            0.5,
            "File Change Heatmap\n(Data processing to be implemented)",
            ha="center",
            va="center",
            fontsize=16,
        )
        plt.axis("off")

        return self.save_plot(filename)

    def plot_file_type_distribution(
        self,
        file_data: Dict[str, int],
        filename: str = "14_file_type_pie.png",
    ):
        plt.figure(figsize=(10, 8))

        labels = list(file_data.keys())
        sizes = list(file_data.values())
        colors = self.warm_colors[: len(labels)]

        plt.pie(
            sizes,
            labels=labels,
            colors=colors,
            autopct="%1.1f%%",
            startangle=90,
            textprops={"fontsize": 12},
        )
        plt.title("File Type Distribution", fontsize=16, fontweight="bold")
        plt.axis("equal")
        plt.tight_layout()

        return self.save_plot(filename)
