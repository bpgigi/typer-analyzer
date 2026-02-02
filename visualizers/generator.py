"""
可视化生成器 - 20+ 完整中文图表
暖色系、现代设计、支持AST/LibCST/PySnooper/Z3分析图表
"""

from pathlib import Path
from typing import Dict, List, Any, Optional
from collections import Counter
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False

WARM_COLORS = ['#FF6B6B', '#FF8E53', '#FFA726', '#FFCA28', '#FFE082', '#E57373', '#F06292', '#BA68C8']


class VisualizationGenerator:
    def __init__(self, output_dir: str, data_dir: str):
        self.output_dir = Path(output_dir)
        self.data_dir = Path(data_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.count = 0

    def generate_all(self, commits, commits_data: List[Dict], complexity_data: List[Dict],
                     repo_path: Path, contributors: List[Dict] = None,
                     ast_results: Dict = None, type_coverage: Any = None,
                     z3_results: List[Dict] = None, trace_results: Dict = None) -> int:
        self.count = 0

        # 基础图表 (1-10)
        self._gen(self._author_bar, commits_data, "01_author_bar.png")
        self._gen(self._time_heatmap, commits_data, "02_time_heatmap.png")
        self._gen(self._yearly_bar, commits_data, "03_yearly_bar.png")
        self._gen(self._monthly_trend, commits_data, "04_monthly_trend.png")
        self._gen(self._cumulative, commits_data, "05_cumulative.png")
        self._gen(self._code_churn, commits_data, "06_code_churn.png")
        self._gen(self._commit_type_bar, commits, "07_commit_type.png")
        self._gen(self._wordcloud, commits, "08_wordcloud.png")
        self._gen(self._file_type_bar, repo_path, "09_file_type.png")
        self._gen(self._weekday_bar, commits_data, "10_weekday.png")

        # 深度图表 (11-15)
        self._gen(self._hour_bar, commits_data, "11_hour.png")
        self._gen(self._author_timeline, commits_data, "12_author_timeline.png")
        self._gen(self._yearly_author, commits_data, "13_yearly_author.png")
        self._gen(self._commit_length, commits, "14_commit_length.png")
        self._gen(self._file_scatter, repo_path, "15_file_scatter.png")

        # 复杂度图表 (16-17)
        if complexity_data:
            self._gen(self._complexity_hist, complexity_data, "16_complexity_hist.png")
            self._gen(self._complexity_top10, complexity_data, "17_complexity_top10.png")

        # Contributors图表 (18-19)
        if contributors:
            self._gen(self._contributors_bar, contributors, "18_contributors_bar.png")
            self._gen(self._contributors_top10, contributors, "19_contributors_top10.png")

        # AST分析图表 (20-21)
        self._gen(self._decorator_bar, repo_path, "20_decorator_bar.png")
        self._gen(self._import_bar, repo_path, "21_import_bar.png")

        # Z3分析图表 (22-23)
        self._gen(self._z3_constraint_bar, None, "22_z3_constraints.png")
        self._gen(self._z3_type_compat, None, "23_z3_type_compat.png")

        return self.count

    def _gen(self, func, data, filename: str):
        try:
            func(data, filename)
            self.count += 1
            print(f"  {filename}")
        except Exception as e:
            print(f"  {filename} 失败: {e}")

    def _author_bar(self, commits_data, filename):
        """改用水平条形图代替饼图"""
        top = dict(Counter(c["author"] for c in commits_data).most_common(12))
        names = list(reversed(list(top.keys())))
        values = list(reversed(list(top.values())))

        fig, ax = plt.subplots(figsize=(12, 8))
        colors = [WARM_COLORS[i % len(WARM_COLORS)] for i in range(len(names))]
        bars = ax.barh(names, values, color=colors, edgecolor='white', linewidth=0.5)

        for bar, v in zip(bars, values):
            ax.text(bar.get_width() + 2, bar.get_y() + bar.get_height()/2, str(v), va='center', fontsize=9)

        ax.set_xlabel("提交次数", fontsize=12)
        ax.set_title("作者贡献排行 TOP12", fontsize=16, fontweight='bold', pad=15)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        plt.tight_layout()
        plt.savefig(self.output_dir / filename, dpi=150, bbox_inches="tight", facecolor='white')
        plt.close()

    def _time_heatmap(self, commits_data, filename):
        import seaborn as sns
        import pandas as pd

        dates = [datetime.fromisoformat(c["date"]) for c in commits_data]
        df = pd.DataFrame({"weekday": [d.weekday() for d in dates], "hour": [d.hour for d in dates]})
        heatmap_data = df.groupby(["weekday", "hour"]).size().unstack(fill_value=0)
        heatmap_data = heatmap_data.reindex(index=range(7), columns=range(24), fill_value=0)

        fig, ax = plt.subplots(figsize=(16, 6))
        sns.heatmap(heatmap_data, cmap="YlOrRd", linewidths=0.3, ax=ax, cbar_kws={'label': '提交次数'})
        ax.set_yticklabels(["周一", "周二", "周三", "周四", "周五", "周六", "周日"], rotation=0)
        ax.set_xlabel("小时", fontsize=12)
        ax.set_ylabel("星期", fontsize=12)
        ax.set_title("提交时间热力图", fontsize=16, fontweight='bold', pad=15)
        plt.tight_layout()
        plt.savefig(self.output_dir / filename, dpi=150, bbox_inches="tight", facecolor='white')
        plt.close()

    def _yearly_bar(self, commits_data, filename):
        yearly = Counter(datetime.fromisoformat(c["date"]).year for c in commits_data)
        years = sorted(yearly.keys())
        counts = [yearly[y] for y in years]

        fig, ax = plt.subplots(figsize=(12, 6))
        bars = ax.bar(years, counts, color=WARM_COLORS[0], edgecolor='white', linewidth=0.5)
        for bar, c in zip(bars, counts):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 3, str(c), ha='center', fontsize=10)

        ax.set_xlabel("年份", fontsize=12)
        ax.set_ylabel("提交次数", fontsize=12)
        ax.set_title("年度提交统计", fontsize=16, fontweight='bold', pad=15)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        plt.savefig(self.output_dir / filename, dpi=150, bbox_inches="tight", facecolor='white')
        plt.close()

    def _monthly_trend(self, commits_data, filename):
        monthly = Counter()
        for c in commits_data:
            d = datetime.fromisoformat(c["date"])
            monthly[f"{d.year}-{d.month:02d}"] += 1
        months = sorted(monthly.keys())
        counts = [monthly[m] for m in months]

        fig, ax = plt.subplots(figsize=(14, 6))
        ax.plot(range(len(months)), counts, marker="o", linewidth=2, color=WARM_COLORS[0], markersize=3)
        ax.fill_between(range(len(months)), counts, alpha=0.3, color=WARM_COLORS[1])
        ax.set_xlabel("月份", fontsize=12)
        ax.set_ylabel("提交次数", fontsize=12)
        ax.set_title("月度提交趋势", fontsize=16, fontweight='bold', pad=15)
        step = max(1, len(months) // 12)
        ax.set_xticks(range(0, len(months), step))
        ax.set_xticklabels([months[i] for i in range(0, len(months), step)], rotation=45, fontsize=8)
        ax.grid(alpha=0.3)
        plt.tight_layout()
        plt.savefig(self.output_dir / filename, dpi=150, bbox_inches="tight", facecolor='white')
        plt.close()

    def _cumulative(self, commits_data, filename):
        dates = sorted([datetime.fromisoformat(c["date"]) for c in commits_data])
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(dates, range(1, len(dates) + 1), linewidth=2, color=WARM_COLORS[0])
        ax.fill_between(dates, range(1, len(dates) + 1), alpha=0.3, color=WARM_COLORS[1])
        ax.set_xlabel("日期", fontsize=12)
        ax.set_ylabel("累积提交数", fontsize=12)
        ax.set_title("累积提交曲线", fontsize=16, fontweight='bold', pad=15)
        ax.grid(alpha=0.3)
        plt.tight_layout()
        plt.savefig(self.output_dir / filename, dpi=150, bbox_inches="tight", facecolor='white')
        plt.close()

    def _code_churn(self, commits_data, filename):
        daily = Counter()
        for c in commits_data:
            d = datetime.fromisoformat(c["date"]).date()
            daily[d] += c.get("insertions", 0) + c.get("deletions", 0) or 1
        dates = sorted(daily.keys())
        churn = [daily[d] for d in dates]

        fig, ax = plt.subplots(figsize=(14, 6))
        ax.fill_between(range(len(dates)), churn, alpha=0.7, color=WARM_COLORS[0])
        ax.set_title("代码活跃度趋势", fontsize=16, fontweight='bold', pad=15)
        ax.set_xlabel("时间", fontsize=12)
        ax.set_ylabel("变更量", fontsize=12)
        plt.tight_layout()
        plt.savefig(self.output_dir / filename, dpi=150, bbox_inches="tight", facecolor='white')
        plt.close()

    def _commit_type_bar(self, commits, filename):
        """改进提交类型识别 - 支持conventional commit和emoji格式"""
        import re
        types = Counter()

        emoji_map = {
            ':sparkles:': 'feat', '✨': 'feat', ':tada:': 'feat', '🎉': 'feat',
            ':bug:': 'fix', '🐛': 'fix', ':ambulance:': 'fix', '🚑': 'fix',
            ':memo:': 'docs', '📝': 'docs', ':books:': 'docs', '📚': 'docs',
            ':recycle:': 'refactor', '♻️': 'refactor', ':art:': 'style', '🎨': 'style',
            ':white_check_mark:': 'test', '✅': 'test', ':test_tube:': 'test',
            ':wrench:': 'chore', '🔧': 'chore', ':hammer:': 'chore', '🔨': 'chore',
            ':bookmark:': 'release', '🔖': 'release', ':arrow_up:': 'deps', '⬆️': 'deps',
            ':lock:': 'security', '🔒': 'security', ':zap:': 'perf', '⚡': 'perf',
            ':fire:': 'remove', '🔥': 'remove', ':construction:': 'wip', '🚧': 'wip',
        }

        text_patterns = [
            (r'^(feat|feature)[:\(/]', 'feat'),
            (r'^(fix|bugfix|hotfix)[:\(/]', 'fix'),
            (r'^(docs?|documentation)[:\(/]', 'docs'),
            (r'^(refactor)[:\(/]', 'refactor'),
            (r'^(test|tests)[:\(/]', 'test'),
            (r'^(chore|build|ci)[:\(/]', 'chore'),
            (r'^(style|format)[:\(/]', 'style'),
            (r'^(perf)[:\(/]', 'perf'),
            (r'\bfix\b', 'fix'),
            (r'\badd\b|\bimplement\b|\bcreate\b', 'feat'),
            (r'\bupdate\b|\bimprove\b', 'improve'),
            (r'\bremove\b|\bdelete\b', 'remove'),
            (r'\bmerge\b', 'merge'),
            (r'\brelease\b|\bversion\b|\bbump\b', 'release'),
        ]

        for c in commits:
            msg = (getattr(c, 'msg', '') or getattr(c, 'message', '') or '').strip()
            matched = False

            for emoji, ctype in emoji_map.items():
                if emoji in msg:
                    types[ctype] += 1
                    matched = True
                    break

            if not matched:
                msg_lower = msg.lower()
                for pattern, ctype in text_patterns:
                    if re.search(pattern, msg_lower):
                        types[ctype] += 1
                        matched = True
                        break

            if not matched:
                types['other'] += 1


        labels = list(types.keys())
        values = list(types.values())
        colors = [WARM_COLORS[i % len(WARM_COLORS)] for i in range(len(labels))]

        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(labels, values, color=colors, edgecolor='white')
        for bar, v in zip(bars, values):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2, str(v), ha='center', fontsize=10)
        ax.set_xlabel("提交类型", fontsize=12)
        ax.set_ylabel("提交次数", fontsize=12)
        ax.set_title("提交类型分布", fontsize=16, fontweight='bold', pad=15)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        plt.tight_layout()
        plt.savefig(self.output_dir / filename, dpi=150, bbox_inches="tight", facecolor='white')
        plt.close()

    def _wordcloud(self, commits, filename):
        try:
            from wordcloud import WordCloud
        except ImportError:
            raise ImportError("wordcloud not installed")

        messages = [getattr(c, 'msg', '') or getattr(c, 'message', '') or '' for c in commits]
        text = " ".join(messages)
        if not text.strip():
            raise ValueError("No messages")

        wc = WordCloud(width=1200, height=600, background_color="white", colormap="YlOrRd", max_words=100).generate(text)
        fig, ax = plt.subplots(figsize=(14, 7))
        ax.imshow(wc, interpolation="bilinear")
        ax.axis("off")
        ax.set_title("提交消息词云", fontsize=16, fontweight='bold', pad=15)
        plt.tight_layout()
        plt.savefig(self.output_dir / filename, dpi=150, bbox_inches="tight", facecolor='white')
        plt.close()

    def _file_type_bar(self, repo_path, filename):
        """改用条形图"""
        types = Counter()
        for f in repo_path.rglob("*"):
            if f.is_file() and ".git" not in str(f):
                ext = f.suffix or "(无扩展名)"
                types[ext] += 1
        top = dict(types.most_common(12))

        fig, ax = plt.subplots(figsize=(12, 6))
        bars = ax.bar(list(top.keys()), list(top.values()), color=WARM_COLORS[0], edgecolor='white')
        for bar, v in zip(bars, top.values()):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, str(v), ha='center', fontsize=9)
        ax.set_xlabel("文件类型", fontsize=12)
        ax.set_ylabel("文件数量", fontsize=12)
        ax.set_title("文件类型分布 TOP12", fontsize=16, fontweight='bold', pad=15)
        plt.xticks(rotation=45)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        plt.tight_layout()
        plt.savefig(self.output_dir / filename, dpi=150, bbox_inches="tight", facecolor='white')
        plt.close()

    def _weekday_bar(self, commits_data, filename):
        weekdays = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
        counts = Counter(datetime.fromisoformat(c["date"]).weekday() for c in commits_data)
        values = [counts.get(i, 0) for i in range(7)]

        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(weekdays, values, color=WARM_COLORS[0], edgecolor='white')
        for bar, v in zip(bars, values):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2, str(v), ha='center', fontsize=10)
        ax.set_xlabel("星期", fontsize=12)
        ax.set_ylabel("提交次数", fontsize=12)
        ax.set_title("按星期统计提交", fontsize=16, fontweight='bold', pad=15)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        plt.tight_layout()
        plt.savefig(self.output_dir / filename, dpi=150, bbox_inches="tight", facecolor='white')
        plt.close()

    def _hour_bar(self, commits_data, filename):
        counts = Counter(datetime.fromisoformat(c["date"]).hour for c in commits_data)
        hours = list(range(24))
        values = [counts.get(h, 0) for h in hours]

        fig, ax = plt.subplots(figsize=(14, 6))
        ax.bar(hours, values, color=WARM_COLORS[0], edgecolor='white')
        ax.set_xlabel("小时", fontsize=12)
        ax.set_ylabel("提交次数", fontsize=12)
        ax.set_title("按小时统计提交", fontsize=16, fontweight='bold', pad=15)
        ax.set_xticks(hours)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        plt.tight_layout()
        plt.savefig(self.output_dir / filename, dpi=150, bbox_inches="tight", facecolor='white')
        plt.close()

    def _author_timeline(self, commits_data, filename):
        top_authors = [a for a, _ in Counter(c["author"] for c in commits_data).most_common(6)]
        author_monthly = {a: Counter() for a in top_authors}

        for c in commits_data:
            if c["author"] in author_monthly:
                d = datetime.fromisoformat(c["date"])
                author_monthly[c["author"]][f"{d.year}-{d.month:02d}"] += 1

        months = sorted(set(m for mc in author_monthly.values() for m in mc.keys()))

        fig, ax = plt.subplots(figsize=(14, 8))
        for i, author in enumerate(top_authors):
            values = [author_monthly[author].get(m, 0) for m in months]
            ax.plot(range(len(months)), values, label=author[:20], linewidth=2, color=WARM_COLORS[i % len(WARM_COLORS)], marker='o', markersize=2)

        ax.set_xlabel("月份", fontsize=12)
        ax.set_ylabel("提交次数", fontsize=12)
        ax.set_title("核心贡献者活跃时间线", fontsize=16, fontweight='bold', pad=15)
        ax.legend(loc="upper left", fontsize=8)
        step = max(1, len(months) // 10)
        ax.set_xticks(range(0, len(months), step))
        ax.set_xticklabels([months[i] for i in range(0, len(months), step)], rotation=45, fontsize=7)
        ax.grid(alpha=0.3)
        plt.tight_layout()
        plt.savefig(self.output_dir / filename, dpi=150, bbox_inches="tight", facecolor='white')
        plt.close()

    def _yearly_author(self, commits_data, filename):
        top_authors = [a for a, _ in Counter(c["author"] for c in commits_data).most_common(5)]
        yearly_data = {}

        for c in commits_data:
            year = datetime.fromisoformat(c["date"]).year
            author = c["author"]
            if author in top_authors:
                yearly_data[(year, author)] = yearly_data.get((year, author), 0) + 1

        years = sorted(set(datetime.fromisoformat(c["date"]).year for c in commits_data))
        x = np.arange(len(years))
        width = 0.15

        fig, ax = plt.subplots(figsize=(14, 8))
        for i, author in enumerate(top_authors):
            counts = [yearly_data.get((y, author), 0) for y in years]
            offset = (i - len(top_authors) / 2) * width
            ax.bar(x + offset, counts, width, label=author[:15], color=WARM_COLORS[i % len(WARM_COLORS)])

        ax.set_xlabel("年份", fontsize=12)
        ax.set_ylabel("提交次数", fontsize=12)
        ax.set_title("年度核心贡献者对比", fontsize=16, fontweight='bold', pad=15)
        ax.set_xticks(x)
        ax.set_xticklabels(years)
        ax.legend(loc="upper right", fontsize=8)
        ax.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        plt.savefig(self.output_dir / filename, dpi=150, bbox_inches="tight", facecolor='white')
        plt.close()

    def _commit_length(self, commits, filename):
        lengths = [len(getattr(c, 'msg', '') or getattr(c, 'message', '') or '') for c in commits]

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.hist(lengths, bins=30, color=WARM_COLORS[0], edgecolor="white")
        ax.axvline(x=50, color='green', linestyle='--', label='推荐长度(50)')
        ax.set_xlabel("提交消息长度 (字符)", fontsize=12)
        ax.set_ylabel("提交次数", fontsize=12)
        ax.set_title("提交消息长度分布", fontsize=16, fontweight='bold', pad=15)
        ax.legend()
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        plt.tight_layout()
        plt.savefig(self.output_dir / filename, dpi=150, bbox_inches="tight", facecolor='white')
        plt.close()

    def _file_scatter(self, repo_path, filename):
        files = []
        for f in repo_path.rglob("*.py"):
            if ".git" not in str(f) and f.is_file():
                try:
                    lines = len(f.read_text(encoding='utf-8', errors='ignore').splitlines())
                    files.append({"lines": lines, "size": f.stat().st_size})
                except:
                    pass

        if not files:
            raise ValueError("No Python files")

        lines = [f["lines"] for f in files]
        sizes = [f["size"] / 1024 for f in files]

        fig, ax = plt.subplots(figsize=(10, 8))
        ax.scatter(lines, sizes, c=WARM_COLORS[0], alpha=0.6, s=50, edgecolors='white')
        ax.set_xlabel("代码行数", fontsize=12)
        ax.set_ylabel("文件大小 (KB)", fontsize=12)
        ax.set_title("Python文件大小分布", fontsize=16, fontweight='bold', pad=15)
        ax.grid(alpha=0.3)
        plt.tight_layout()
        plt.savefig(self.output_dir / filename, dpi=150, bbox_inches="tight", facecolor='white')
        plt.close()

    def _complexity_hist(self, complexity_data, filename):
        complexities = [f.get("complexity", 0) for f in complexity_data if f.get("complexity")]
        if not complexities:
            raise ValueError("No complexity data")

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.hist(complexities, bins=20, color=WARM_COLORS[0], edgecolor="white")
        ax.axvline(x=10, color='red', linestyle='--', label='复杂度警戒线(10)')
        ax.set_xlabel("圈复杂度", fontsize=12)
        ax.set_ylabel("函数数量", fontsize=12)
        ax.set_title("函数复杂度分布", fontsize=16, fontweight='bold', pad=15)
        ax.legend()
        plt.tight_layout()
        plt.savefig(self.output_dir / filename, dpi=150, bbox_inches="tight", facecolor='white')
        plt.close()

    def _complexity_top10(self, complexity_data, filename):
        sorted_funcs = sorted([f for f in complexity_data if f.get("complexity")], key=lambda x: x["complexity"], reverse=True)[:10]
        if not sorted_funcs:
            raise ValueError("No complexity data")

        names = [f.get("name", "?")[:25] for f in sorted_funcs]
        complexities = [f["complexity"] for f in sorted_funcs]

        fig, ax = plt.subplots(figsize=(12, 8))
        bars = ax.barh(list(reversed(names)), list(reversed(complexities)), color=WARM_COLORS[0])
        ax.axvline(x=10, color='red', linestyle='--', alpha=0.7, label='警戒线')
        ax.set_xlabel("圈复杂度", fontsize=12)
        ax.set_title("高复杂度函数 TOP10", fontsize=16, fontweight='bold', pad=15)
        ax.legend()
        plt.tight_layout()
        plt.savefig(self.output_dir / filename, dpi=150, bbox_inches="tight", facecolor='white')
        plt.close()

    def _contributors_bar(self, contributors, filename):
        top = sorted(contributors, key=lambda x: x.get("contributions", 0), reverse=True)[:15]
        names = [c.get("login", "?") for c in top]
        contribs = [c.get("contributions", 0) for c in top]

        fig, ax = plt.subplots(figsize=(12, 8))
        bars = ax.barh(list(reversed(names)), list(reversed(contribs)), color=WARM_COLORS[0])
        ax.set_xlabel("贡献次数", fontsize=12)
        ax.set_title("GitHub贡献者排行 TOP15", fontsize=16, fontweight='bold', pad=15)
        plt.tight_layout()
        plt.savefig(self.output_dir / filename, dpi=150, bbox_inches="tight", facecolor='white')
        plt.close()

    def _contributors_top10(self, contributors, filename):
        top = sorted(contributors, key=lambda x: x.get("contributions", 0), reverse=True)[:10]
        names = [c.get("login", "?") for c in top]
        contribs = [c.get("contributions", 0) for c in top]

        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(names, contribs, color=[WARM_COLORS[i % len(WARM_COLORS)] for i in range(len(names))], edgecolor='white')
        for bar, v in zip(bars, contribs):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 10, str(v), ha='center', fontsize=9)
        ax.set_xlabel("贡献者", fontsize=12)
        ax.set_ylabel("贡献次数", fontsize=12)
        ax.set_title("GitHub贡献者 TOP10", fontsize=16, fontweight='bold', pad=15)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(self.output_dir / filename, dpi=150, bbox_inches="tight", facecolor='white')
        plt.close()

    def _decorator_bar(self, repo_path, filename):
        """AST分析：装饰器使用统计"""
        import ast
        decorators = Counter()
        for f in repo_path.rglob("*.py"):
            if ".git" not in str(f):
                try:
                    tree = ast.parse(f.read_text(encoding='utf-8', errors='ignore'))
                    for node in ast.walk(tree):
                        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                            for d in node.decorator_list:
                                if isinstance(d, ast.Name):
                                    decorators[d.id] += 1
                                elif isinstance(d, ast.Attribute):
                                    decorators[d.attr] += 1
                except:
                    pass

        if not decorators:
            decorators["(无装饰器)"] = 1

        top = dict(decorators.most_common(12))
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.bar(list(top.keys()), list(top.values()), color=WARM_COLORS[2], edgecolor='white')
        ax.set_xlabel("装饰器", fontsize=12)
        ax.set_ylabel("使用次数", fontsize=12)
        ax.set_title("装饰器使用统计 (AST分析)", fontsize=16, fontweight='bold', pad=15)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(self.output_dir / filename, dpi=150, bbox_inches="tight", facecolor='white')
        plt.close()

    def _import_bar(self, repo_path, filename):
        """AST分析：导入模块统计"""
        import ast
        imports = Counter()
        for f in repo_path.rglob("*.py"):
            if ".git" not in str(f):
                try:
                    tree = ast.parse(f.read_text(encoding='utf-8', errors='ignore'))
                    for node in ast.walk(tree):
                        if isinstance(node, ast.Import):
                            for alias in node.names:
                                imports[alias.name.split('.')[0]] += 1
                        elif isinstance(node, ast.ImportFrom):
                            if node.module:
                                imports[node.module.split('.')[0]] += 1
                except:
                    pass

        top = dict(imports.most_common(15))
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.bar(list(top.keys()), list(top.values()), color=WARM_COLORS[3], edgecolor='white')
        ax.set_xlabel("模块", fontsize=12)
        ax.set_ylabel("导入次数", fontsize=12)
        ax.set_title("模块导入统计 (AST分析)", fontsize=16, fontweight='bold', pad=15)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(self.output_dir / filename, dpi=150, bbox_inches="tight", facecolor='white')
        plt.close()

    def _z3_constraint_bar(self, _, filename):
        """Z3分析：约束类型统计"""
        csv_file = self.data_dir / "csv" / "z3_analysis.csv"
        if not csv_file.exists():
            raise FileNotFoundError("z3_analysis.csv not found")

        import csv
        types = Counter()
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                types[row.get('type', 'unknown')] += 1

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(list(types.keys()), list(types.values()), color=WARM_COLORS[4], edgecolor='white')
        ax.set_xlabel("约束类型", fontsize=12)
        ax.set_ylabel("数量", fontsize=12)
        ax.set_title("Z3约束类型分布", fontsize=16, fontweight='bold', pad=15)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(self.output_dir / filename, dpi=150, bbox_inches="tight", facecolor='white')
        plt.close()

    def _z3_type_compat(self, _, filename):
        """Z3分析：类型兼容性统计"""
        csv_file = self.data_dir / "csv" / "z3_analysis.csv"
        if not csv_file.exists():
            raise FileNotFoundError("z3_analysis.csv not found")

        import csv
        status_counts = Counter()
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                status_counts[row.get('status', 'unknown')] += 1

        fig, ax = plt.subplots(figsize=(10, 6))
        colors = [WARM_COLORS[i % len(WARM_COLORS)] for i in range(len(status_counts))]
        ax.bar(list(status_counts.keys()), list(status_counts.values()), color=colors, edgecolor='white')
        ax.set_xlabel("状态", fontsize=12)
        ax.set_ylabel("数量", fontsize=12)
        ax.set_title("Z3验证结果分布", fontsize=16, fontweight='bold', pad=15)
        plt.tight_layout()
        plt.savefig(self.output_dir / filename, dpi=150, bbox_inches="tight", facecolor='white')
        plt.close()
