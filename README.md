# Typer Repository Analyzer

基于 Python 的 Typer 仓库静态与动态分析工具，使用 AST、LibCST、PySnooper、Z3 等技术对 [fastapi/typer](https://github.com/fastapi/typer) 进行深度代码分析。

## 功能特性

- **AST 分析**: 函数/类提取、装饰器统计、导入依赖、圈复杂度计算
- **LibCST 分析**: 类型注解覆盖率、泛型使用模式、签名一致性检查
- **PySnooper 追踪**: 动态执行追踪、变量变化记录、性能热点识别
- **Z3 约束求解**: CLI 参数验证、路径可行性分析、类型兼容性检查
- **可视化输出**: 41 张暖色系图表（热力图、饼图、网络图、桑基图等）

## 项目结构

```
repo/
├── analyzers/          # 代码分析器
│   ├── ast_analyzer.py       # AST 静态分析
│   ├── libcst_analyzer.py    # LibCST 类型分析
│   ├── dynamic_tracer.py     # PySnooper 动态追踪
│   └── z3_analyzer.py        # Z3 约束求解
├── collectors/         # 数据采集器
│   ├── commit_collector.py   # Git 提交采集
│   ├── github_collector.py   # GitHub API 采集
│   └── data_exporter.py      # 数据导出
├── visualizers/        # 可视化模块
│   ├── base_charts.py        # 基础图表类
│   ├── heatmap.py            # 热力图
│   ├── creative_charts.py    # 创意图表
│   └── ...
├── utils/              # 工具模块
├── tests/              # 单元测试
├── data/               # 生成的数据文件
├── output/             # 生成的图表
└── docs/               # 项目文档
```

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行分析

```bash
python main.py
```

### 运行测试

```bash
python run_tests.py
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
| Plotly | 交互式图表 |

## 输出成果

- **CSV 数据**: 5 个核心数据文件
- **JSON 持久化**: 3 个完整数据文件
- **追踪日志**: 20 个 .log 文件
- **可视化图表**: 41 张 PNG 图表

## 团队成员

| 角色 | 负责模块 |
|------|----------|
| 组长 | 项目架构、主程序、文档 |
| 组员1 | 数据采集、GitHub API |
| 组员2 | 可视化图表 |
| 组员3 | AST/LibCST 分析 |
| 组员4 | PySnooper/Z3 分析、测试 |

## License

MIT License
