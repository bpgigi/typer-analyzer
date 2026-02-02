# Typer Repository Analyzer

基于 Python 的 Typer 仓库静态与动态分析工具，使用 AST、LibCST、PySnooper、Z3 等技术对 [fastapi/typer](https://github.com/fastapi/typer) 进行深度代码分析。

## 功能特性

- **AST 分析**: 函数/类提取、装饰器统计、导入依赖、圈复杂度计算
- **LibCST 分析**: 类型注解覆盖率、泛型使用模式、签名一致性检查
- **PySnooper 追踪**: 动态执行追踪、变量变化记录、性能热点识别
- **Z3 约束求解**: CLI 参数验证、路径可行性分析、类型兼容性检查
- **可视化输出**: 17 张暖色系图表（热力图、饼图、趋势图、词云等）

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 准备目标仓库

```bash
git clone https://github.com/fastapi/typer.git ../typer
```

### 3. 运行分析

```bash
python main.py
```

### 4. 查看结果

- 图表输出: `output/` 目录
- 数据文件: `data/csv/` 和 `data/json/` 目录
- 追踪日志: `data/traces/` 目录

## 项目结构

```
repo/
├── main.py             # 主程序入口
├── config.py           # 配置（暖色系调色板）
├── constants.py        # 常量定义
├── exceptions.py       # 自定义异常
├── requirements.txt    # 依赖清单
│
├── analyzers/          # 代码分析器
│   ├── ast_analyzer.py       # AST 静态分析
│   ├── libcst_analyzer.py    # LibCST 类型分析
│   ├── dynamic_tracer.py     # PySnooper 动态追踪
│   └── z3_analyzer.py        # Z3 约束求解
│
├── collectors/         # 数据采集器
│   ├── commit_collector.py   # Git 提交采集（PyDriller）
│   ├── github_collector.py   # GitHub API 采集
│   └── data_exporter.py      # CSV/JSON 导出
│
├── visualizers/        # 可视化模块
│   ├── base_charts.py        # 基础图表类
│   ├── heatmap.py            # 时间热力图
│   ├── trends.py             # 趋势图
│   ├── author_charts.py      # 作者贡献图
│   ├── generator.py          # 可视化生成器
│   └── ...
│
├── utils/              # 工具模块
├── tests/              # 单元测试
├── data/               # 生成的数据文件
├── output/             # 生成的图表
└── docs/               # 项目文档
```

## 技术栈

| 技术 | 用途 |
|------|------|
| PyDriller | Git 仓库数据挖掘 |
| AST | Python 抽象语法树分析 |
| LibCST | 具体语法树与类型注解分析 |
| PySnooper | 动态执行追踪 |
| Z3-Solver | 符号执行与约束求解 |
| Matplotlib/Seaborn | 静态图表生成 |
| WordCloud | 提交消息词云 |
| Pandas | 数据处理 |

## 输出成果

### 数据文件
- `commits.csv` - 提交历史记录
- `ast_analysis.csv` - AST 分析结果
- `type_coverage.csv` - 类型注解覆盖率
- `execution_summary.csv` - 动态追踪摘要（29条记录）
- `z3_analysis.csv` - Z3 约束分析（30条记录）

### 可视化图表
- 作者贡献饼图、提交时间热力图
- 年度/月度趋势图、累积提交曲线
- 贡献者排行榜、作者时间线
- 文件类型分布、提交类型分布
- 代码复杂度分布、词云图等

## 团队成员

| 姓名 | 学号 | GitHub | 负责模块 |
|------|------|--------|----------|
| -- | -- | bpgigi | 项目架构、主程序、文档 |
| -- | -- | lihuabaiaq | 数据采集、GitHub API |
| -- | -- | Zyl3110568387 | 可视化图表 |
| -- | -- | 194962887gky | AST/LibCST 分析 |
| -- | -- | severus-hbp | PySnooper/Z3 分析、测试 |

## 运行测试

```bash
python run_tests.py
```

## License

MIT License
