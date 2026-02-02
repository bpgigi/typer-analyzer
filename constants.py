"""
常量定义模块
定义提交类型枚举和项目路径常量
"""

from enum import Enum


class CommitType(str, Enum):
    """Git 提交类型枚举"""

    FEAT = "feat"  # 新功能
    FIX = "fix"  # 错误修复
    DOCS = "docs"  # 文档更新
    CHORE = "chore"  # 杂项任务
    REFACTOR = "refactor"  # 代码重构
    TEST = "test"  # 测试相关
    STYLE = "style"  # 代码风格


# 目标仓库路径（Typer 源码）
TARGET_REPO_PATH = "C:/Users/l/Desktop/opensource/group3/typer"

# 输出目录
OUTPUT_DIR = "output"  # 图表输出目录
DATA_DIR = "data"  # 数据文件目录
TRACES_DIR = "traces"  # 追踪日志目录
