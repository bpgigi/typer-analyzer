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
