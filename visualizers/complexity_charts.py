from typing import Dict, List, Any
import matplotlib.pyplot as plt
from .base_charts import BaseChart


class ComplexityChart(BaseChart):
    def plot_complexity_dist(
        self,
        functions: List[Dict[str, Any]],
        filename: str = "16_complexity_distribution.png",
    ):
        complexities = [f["complexity"] for f in functions if "complexity" in f]

        if not complexities:
            return None

        plt.figure(figsize=(10, 6))

        plt.hist(
            complexities,
            bins=20,
            color=self._get_color(3),
            edgecolor="white",
            alpha=0.7,
        )

        plt.title("Cyclomatic Complexity Distribution", pad=20)
        plt.xlabel("Complexity")
        plt.ylabel("Frequency")
        plt.grid(True, alpha=0.3)

        mean_val = sum(complexities) / len(complexities)
        plt.axvline(
            mean_val,
            color=self._get_color(0),
            linestyle="--",
            label=f"Mean: {mean_val:.1f}",
        )
        plt.legend()

        return self.save_plot(filename)

    def _get_color(self, index: int):
        from config import WARM_PALETTE

        return WARM_PALETTE[index % len(WARM_PALETTE)]
