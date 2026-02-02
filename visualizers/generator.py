"""
可视化生成器模块
从main.py解耦出来的独立可视化生成逻辑
"""

from pathlib import Path
from typing import Dict, List, Any
from collections import Counter
from datetime import datetime


class VisualizationGenerator:
    """统一管理所有可视化图表的生成"""

    def __init__(self, output_dir: str, data_dir: str, warm_palette: List[str] = None):
        self.output_dir = Path(output_dir)
        self.data_dir = Path(data_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.warm_palette = warm_palette or ["#FF6B6B", "#FF8E53", "#FFA726", "#FFCA28", "#FFE082"]
        self.generated_count = 0

    def generate_all(self, commits, commits_data: List[Dict], complexity_data: List[Dict], repo_path: Path) -> int:
        """生成所有图表，返回成功生成的数量"""
        self.generated_count = 0

        # 基础图表
        self._safe_generate(self._gen_author_pie, commits_data, "01_author_contribution_pie.png")
        self._safe_generate(self._gen_time_heatmap, commits_data, "02_commit_time_heatmap.png")
        self._safe_generate(self._gen_yearly_bar, commits_data, "03_yearly_commits_bar.png")
        self._safe_generate(self._gen_monthly_trend, commits_data, "04_monthly_trend_line.png")
        self._safe_generate(self._gen_code_churn, commits_data, "06_code_churn_trend.png")
        self._safe_generate(self._gen_wordcloud, commits, "08_commit_message_wordcloud.png")
        self._safe_generate(self._gen_file_type_pie, repo_path, "09_file_type_pie.png")
        self._safe_generate(self._gen_contributor_ranking, commits_data, "10_contributor_activity.png")
        self._safe_generate(self._gen_cumulative, commits_data, "11_cumulative_commits.png")
        self._safe_generate(self._gen_weekday_dist, commits_data, "12_weekday_distribution.png")
        self._safe_generate(self._gen_hour_dist, commits_data, "13_hour_distribution.png")
        self._safe_generate(self._gen_author_timeline, commits_data, "14_author_timeline.png")
        self._safe_generate(self._gen_commit_type_pie, commits, "15_commit_type_pie.png")
        self._safe_generate(self._gen_complexity_hist, complexity_data, "16_complexity_distribution.png")
        self._safe_generate(self._gen_yearly_author, commits_data, "17_yearly_author_comparison.png")

        return self.generated_count

    def _safe_generate(self, func, data, filename: str) -> bool:
        try:
            func(data, filename)
            self.generated_count += 1
            print(f"  {filename}")
            return True
        except Exception as e:
            print(f"  {filename} 失败: {e}")
            return False

    def _gen_author_pie(self, commits_data: List[Dict], filename: str) -> None:
        import matplotlib.pyplot as plt
        author_counts = Counter(c["author"] for c in commits_data)
        top = dict(author_counts.most_common(10))
        others = sum(author_counts.values()) - sum(top.values())
        if others > 0:
            top["Others"] = others

        plt.figure(figsize=(10, 10))
        colors = plt.cm.YlOrRd([0.2 + 0.6 * i / len(top) for i in range(len(top))])
        plt.pie(top.values(), labels=top.keys(), autopct="%1.1f%%", colors=colors)
        plt.title("Author Contribution", pad=20)
        plt.tight_layout()
        plt.savefig(self.output_dir / filename, dpi=150, bbox_inches="tight")
        plt.close()

    def _gen_time_heatmap(self, commits_data: List[Dict], filename: str) -> None:
        import matplotlib.pyplot as plt
        import seaborn as sns
        import pandas as pd

        dates = [datetime.fromisoformat(c["date"]) for c in commits_data]
        df = pd.DataFrame({"weekday": [d.weekday() for d in dates], "hour": [d.hour for d in dates]})
        heatmap_data = df.groupby(["weekday", "hour"]).size().unstack(fill_value=0)
        heatmap_data = heatmap_data.reindex(index=range(7), columns=range(24), fill_value=0)

        plt.figure(figsize=(16, 6))
        sns.heatmap(heatmap_data, cmap="YlOrRd", linewidths=0.5)
        weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        plt.yticks([i + 0.5 for i in range(7)], weekdays, rotation=0)
        plt.title("Commit Time Heatmap", pad=20)
        plt.tight_layout()
        plt.savefig(self.output_dir / filename, dpi=150, bbox_inches="tight")
        plt.close()

    def _gen_yearly_bar(self, commits_data: List[Dict], filename: str) -> None:
        import matplotlib.pyplot as plt
        yearly = Counter(datetime.fromisoformat(c["date"]).year for c in commits_data)
        years = sorted(yearly.keys())
        counts = [yearly[y] for y in years]

        plt.figure(figsize=(12, 6))
        plt.bar(years, counts, color=plt.cm.YlOrRd(0.6))
        plt.xlabel("Year")
        plt.ylabel("Commits")
        plt.title("Yearly Commits", pad=20)
        plt.tight_layout()
        plt.savefig(self.output_dir / filename, dpi=150, bbox_inches="tight")
        plt.close()

    def _gen_monthly_trend(self, commits_data: List[Dict], filename: str) -> None:
        import matplotlib.pyplot as plt
        monthly = Counter()
        for c in commits_data:
            d = datetime.fromisoformat(c["date"])
            monthly[f"{d.year}-{d.month:02d}"] += 1
        months = sorted(monthly.keys())
        counts = [monthly[m] for m in months]

        plt.figure(figsize=(14, 6))
        plt.plot(months, counts, marker="o", linewidth=2, color=plt.cm.YlOrRd(0.7))
        plt.fill_between(months, counts, alpha=0.3, color=plt.cm.YlOrRd(0.5))
        plt.xticks(rotation=45)
        plt.title("Monthly Trend", pad=20)
        plt.grid(alpha=0.3)
        plt.tight_layout()
        plt.savefig(self.output_dir / filename, dpi=150, bbox_inches="tight")
        plt.close()

    def _gen_code_churn(self, commits_data: List[Dict], filename: str) -> None:
        import matplotlib.pyplot as plt
        dates = sorted(set(datetime.fromisoformat(c["date"]).date() for c in commits_data))
        churn = [sum(1 for c in commits_data if datetime.fromisoformat(c["date"]).date() == d) for d in dates]

        plt.figure(figsize=(14, 6))
        plt.fill_between(range(len(dates)), churn, alpha=0.7, color=plt.cm.YlOrRd(0.6))
        plt.title("Code Activity Trend", pad=20)
        plt.tight_layout()
        plt.savefig(self.output_dir / filename, dpi=150, bbox_inches="tight")
        plt.close()

    def _gen_wordcloud(self, commits, filename: str) -> None:
        import matplotlib.pyplot as plt
        try:
            from wordcloud import WordCloud
        except ImportError:
            return

        messages = [getattr(c, 'msg', '') or getattr(c, 'message', '') or '' for c in commits]
        text = " ".join(messages)
        if not text.strip():
            return

        wc = WordCloud(width=1200, height=600, background_color="white", colormap="YlOrRd").generate(text)
        plt.figure(figsize=(14, 7))
        plt.imshow(wc, interpolation="bilinear")
        plt.axis("off")
        plt.tight_layout()
        plt.savefig(self.output_dir / filename, dpi=150, bbox_inches="tight")
        plt.close()

    def _gen_file_type_pie(self, repo_path: Path, filename: str) -> None:
        import matplotlib.pyplot as plt
        types = Counter()
        for f in repo_path.rglob("*"):
            if f.is_file() and ".git" not in str(f):
                types[f.suffix or "no_ext"] += 1
        top = dict(types.most_common(10))

        plt.figure(figsize=(10, 10))
        colors = plt.cm.YlOrRd([0.2 + 0.6 * i / len(top) for i in range(len(top))])
        plt.pie(top.values(), labels=top.keys(), autopct="%1.1f%%", colors=colors)
        plt.title("File Types", pad=20)
        plt.tight_layout()
        plt.savefig(self.output_dir / filename, dpi=150, bbox_inches="tight")
        plt.close()

    def _gen_contributor_ranking(self, commits_data: List[Dict], filename: str) -> None:
        import matplotlib.pyplot as plt
        top = dict(Counter(c["author"] for c in commits_data).most_common(15))
        plt.figure(figsize=(12, 8))
        plt.barh(list(top.keys()), list(top.values()), color=plt.cm.YlOrRd(0.6))
        plt.gca().invert_yaxis()
        plt.title("Top Contributors", pad=20)
        plt.tight_layout()
        plt.savefig(self.output_dir / filename, dpi=150, bbox_inches="tight")
        plt.close()

    def _gen_cumulative(self, commits_data: List[Dict], filename: str) -> None:
        import matplotlib.pyplot as plt
        dates = sorted([datetime.fromisoformat(c["date"]) for c in commits_data])
        plt.figure(figsize=(12, 6))
        plt.plot(dates, range(1, len(dates) + 1), linewidth=2, color=plt.cm.YlOrRd(0.7))
        plt.fill_between(dates, range(1, len(dates) + 1), alpha=0.3, color=plt.cm.YlOrRd(0.5))
        plt.title("Cumulative Commits", pad=20)
        plt.tight_layout()
        plt.savefig(self.output_dir / filename, dpi=150, bbox_inches="tight")
        plt.close()

    def _gen_weekday_dist(self, commits_data: List[Dict], filename: str) -> None:
        import matplotlib.pyplot as plt
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        counts = Counter(datetime.fromisoformat(c["date"]).weekday() for c in commits_data)
        plt.figure(figsize=(10, 6))
        plt.bar(days, [counts.get(i, 0) for i in range(7)], color=plt.cm.YlOrRd(0.6))
        plt.title("Weekday Distribution", pad=20)
        plt.tight_layout()
        plt.savefig(self.output_dir / filename, dpi=150, bbox_inches="tight")
        plt.close()

    def _gen_hour_dist(self, commits_data: List[Dict], filename: str) -> None:
        import matplotlib.pyplot as plt
        counts = Counter(datetime.fromisoformat(c["date"]).hour for c in commits_data)
        plt.figure(figsize=(12, 6))
        plt.bar(range(24), [counts.get(h, 0) for h in range(24)], color=plt.cm.YlOrRd(0.6))
        plt.title("Hour Distribution", pad=20)
        plt.tight_layout()
        plt.savefig(self.output_dir / filename, dpi=150, bbox_inches="tight")
        plt.close()

    def _gen_author_timeline(self, commits_data: List[Dict], filename: str) -> None:
        import matplotlib.pyplot as plt
        top_authors = [a for a, _ in Counter(c["author"] for c in commits_data).most_common(8)]
        author_monthly = {a: Counter() for a in top_authors}

        for c in commits_data:
            if c["author"] in author_monthly:
                d = datetime.fromisoformat(c["date"])
                author_monthly[c["author"]][f"{d.year}-{d.month:02d}"] += 1

        months = sorted(set(m for mc in author_monthly.values() for m in mc.keys()))
        plt.figure(figsize=(14, 8))
        colors = plt.cm.YlOrRd([0.3 + 0.5 * i / len(top_authors) for i in range(len(top_authors))])

        for i, author in enumerate(top_authors):
            values = [author_monthly[author].get(m, 0) for m in months]
            plt.plot(months, values, label=author[:20], linewidth=2, color=colors[i])

        plt.legend(loc="upper left", fontsize=7)
        plt.xticks(rotation=45, fontsize=7)
        plt.title("Contributor Timeline", pad=20)
        plt.tight_layout()
        plt.savefig(self.output_dir / filename, dpi=150, bbox_inches="tight")
        plt.close()

    def _gen_commit_type_pie(self, commits, filename: str) -> None:
        import matplotlib.pyplot as plt
        import re
        types = Counter()
        for c in commits:
            msg = getattr(c, 'msg', '') or getattr(c, 'message', '') or ''
            m = re.match(r"^(feat|fix|docs|refactor|test|chore|style|perf|build|ci)[\\(:]", msg.lower())
            types[m.group(1) if m else "other"] += 1

        plt.figure(figsize=(10, 10))
        colors = plt.cm.YlOrRd([0.2 + 0.6 * i / len(types) for i in range(len(types))])
        plt.pie(types.values(), labels=types.keys(), autopct="%1.1f%%", colors=colors)
        plt.title("Commit Types", pad=20)
        plt.tight_layout()
        plt.savefig(self.output_dir / filename, dpi=150, bbox_inches="tight")
        plt.close()

    def _gen_complexity_hist(self, complexity_data: List[Dict], filename: str) -> None:
        import matplotlib.pyplot as plt
        complexities = [f.get("complexity", 0) for f in complexity_data if f.get("complexity")]
        if not complexities:
            return

        plt.figure(figsize=(10, 6))
        plt.hist(complexities, bins=20, color=plt.cm.YlOrRd(0.6), edgecolor="white")
        plt.title("Complexity Distribution", pad=20)
        plt.tight_layout()
        plt.savefig(self.output_dir / filename, dpi=150, bbox_inches="tight")
        plt.close()

    def _gen_yearly_author(self, commits_data: List[Dict], filename: str) -> None:
        import matplotlib.pyplot as plt
        top_authors = [a for a, _ in Counter(c["author"] for c in commits_data).most_common(5)]
        yearly_data = {}

        for c in commits_data:
            year = datetime.fromisoformat(c["date"]).year
            author = c["author"]
            if author in top_authors:
                yearly_data[(year, author)] = yearly_data.get((year, author), 0) + 1

        years = sorted(set(datetime.fromisoformat(c["date"]).year for c in commits_data))
        x = range(len(years))
        width = 0.15
        colors = plt.cm.YlOrRd([0.3 + 0.5 * i / len(top_authors) for i in range(len(top_authors))])

        plt.figure(figsize=(14, 8))
        for i, author in enumerate(top_authors):
            counts = [yearly_data.get((y, author), 0) for y in years]
            offset = (i - len(top_authors) / 2) * width
            plt.bar([xi + offset for xi in x], counts, width, label=author[:15], color=colors[i])

        plt.xticks(x, years)
        plt.legend(loc="upper right", fontsize=8)
        plt.title("Top 5 by Year", pad=20)
        plt.tight_layout()
        plt.savefig(self.output_dir / filename, dpi=150, bbox_inches="tight")
        plt.close()
