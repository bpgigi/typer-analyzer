from typing import Dict, List, Any
import matplotlib.pyplot as plt
import pandas as pd
from .base_charts import BaseChart


class HighComplexityChart(BaseChart):
    def plot_top_complexity(
        self,
        functions: List[Dict[str, Any]],
        filename: str = "17_high_complexity_top10.png",
    ):
        sorted_funcs = sorted(
            [f for f in functions if "complexity" in f],
            key=lambda x: x["complexity"],
            reverse=True,
        )[:10]

        if not sorted_funcs:
            return None

        names = [f["name"] for f in sorted_funcs]
        complexities = [f["complexity"] for f in sorted_funcs]

        plt.figure(figsize=(12, 8))

        bars = plt.barh(names, complexities, color=self._get_color(4))
        plt.gca().invert_yaxis()

        for bar in bars:
            width = bar.get_width()
            plt.text(
                width + 0.5,
                bar.get_y() + bar.get_height() / 2.0,
                f"{int(width)}",
                ha="left",
                va="center",
            )

        plt.title("Top 10 Most Complex Functions", pad=20)
        plt.xlabel("Cyclomatic Complexity")
        plt.grid(axis="x", alpha=0.3)

        return self.save_plot(filename)

    def _get_color(self, index: int):
        from config import WARM_PALETTE

        return WARM_PALETTE[index % len(WARM_PALETTE)]
