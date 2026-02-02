# 安装指南

## 系统要求

- Python 3.9+
- Git
- Windows/Linux/macOS

## 安装步骤

### 1. 克隆仓库

```bash
git clone https://github.com/bpgigi/typer-analyzer.git
cd typer-analyzer
```

### 2. 创建虚拟环境（推荐）

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 准备目标仓库

```bash
git clone https://github.com/fastapi/typer.git ../typer
```

### 5. 验证安装

```bash
python -c "from main import RepositoryAnalyzer; print('OK')"
```

## 依赖说明

| 包 | 版本 | 用途 |
|----|------|------|
| pydriller | >=2.0 | Git 数据挖掘 |
| libcst | >=1.0 | 具体语法树分析 |
| pysnooper | >=1.0 | 动态追踪 |
| z3-solver | >=4.8 | 符号执行 |
| matplotlib | >=3.5 | 图表生成 |
| seaborn | >=0.12 | 统计图表 |
| pandas | >=1.5 | 数据处理 |
| wordcloud | >=1.8 | 词云生成 |

## 常见问题

### Q: 中文乱码？
A: 确保字体配置正确，参见 `utils/font_config.py`

### Q: Z3 安装失败？
A: 使用 `pip install z3-solver` 而非 `z3`

### Q: 图表生成报错？
A: 检查 matplotlib 后端配置，可设置 `matplotlib.use('Agg')`
