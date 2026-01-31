from typing import Dict, List, Any
import matplotlib.pyplot as plt
import numpy as np
from .base_charts import BaseChart


class CreativeCharts(BaseChart):
    def plot_violin_distribution(
        self,
        data: List[float],
        title: str,
        filename: str = "34_execution_duration_violin.png",
    ):
        if not data:
            return

        plt.figure(figsize=(10, 6))

        parts = plt.violinplot(
            data, showmeans=False, showmedians=True, showextrema=True
        )

        for pc in parts["bodies"]:
            pc.set_facecolor("#E85A4F")
            pc.set_edgecolor("#4A4A48")
            pc.set_alpha(0.7)

        for partname in ("cbars", "cmins", "cmaxes", "cmedians"):
            vp = parts[partname]
            vp.set_edgecolor("#4A4A48")
            vp.set_linewidth(1.5)

        plt.title(title, fontsize=16, fontweight="bold")
        plt.grid(True, axis="y", alpha=0.3)
        plt.tight_layout()

        return self.save_plot(filename)
