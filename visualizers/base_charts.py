import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from typing import Optional, Dict, List, Tuple
from config import WARM_COLORS, WARM_PALETTE


class BaseChart:
    def __init__(self, output_dir: str = "output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self._setup_style()

    def _setup_style(self):
        plt.style.use("seaborn-v0_8-whitegrid")
        sns.set_palette(WARM_PALETTE)

        plt.rcParams.update(
            {
                "font.family": ["sans-serif"],
                "font.sans-serif": ["Microsoft YaHei", "SimHei", "Arial"],
                "axes.unicode_minus": False,
                "figure.figsize": (12, 8),
                "figure.dpi": 150,
                "axes.titlesize": 16,
                "axes.labelsize": 12,
                "xtick.labelsize": 10,
                "ytick.labelsize": 10,
                "legend.fontsize": 10,
                "grid.alpha": 0.3,
                "axes.edgecolor": WARM_COLORS["accent"],
                "text.color": WARM_COLORS["dark"],
                "axes.labelcolor": WARM_COLORS["dark"],
                "xtick.color": WARM_COLORS["dark"],
                "ytick.color": WARM_COLORS["dark"],
            }
        )

    def save_plot(self, filename: str, dpi: int = 150, transparent: bool = False):
        output_path = self.output_dir / filename
        plt.tight_layout()
        plt.savefig(output_path, dpi=dpi, transparent=transparent, bbox_inches="tight")
        plt.close()
        return str(output_path)

    def plot_pie(
        self, data: Dict[str, float], title: str, filename: str, donut: bool = False
    ):
        plt.figure(figsize=(10, 10))

        labels = list(data.keys())
        sizes = list(data.values())

        if donut:
            plt.pie(
                sizes,
                labels=labels,
                autopct="%1.1f%%",
                startangle=90,
                pctdistance=0.85,
                colors=WARM_PALETTE,
                wedgeprops={"width": 0.5, "edgecolor": "white"},
            )
            centre_circle = plt.Circle((0, 0), 0.70, fc="white")
            plt.gca().add_artist(centre_circle)
        else:
            plt.pie(
                sizes,
                labels=labels,
                autopct="%1.1f%%",
                startangle=90,
                colors=WARM_PALETTE,
                wedgeprops={"edgecolor": "white"},
            )

        plt.title(title, pad=20)
        return self.save_plot(filename)
