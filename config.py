"""
配置模块
定义项目的基础路径和暖色系配色方案
"""

from pathlib import Path

# 项目根目录
BASE_DIR = Path(__file__).resolve().parent

# 暖色系主题配色
WARM_COLORS = {
    "primary": "#C8643B",  # 主色调 - 陶土橙
    "secondary": "#E07A5F",  # 次要色 - 珊瑚红
    "tertiary": "#F2D6C7",  # 第三色 - 浅桃色
    "background": "#FAF7F2",  # 背景色 - 米白色
    "accent": "#4C6A6A",  # 强调色 - 青灰色
    "dark": "#2F2A26",  # 深色 - 深棕色
}

# 暖色系调色板（用于图表）
WARM_PALETTE = [
    "#C8643B",  # 陶土橙
    "#E07A5F",  # 珊瑚红
    "#D98C5F",  # 杏橙色
    "#B86F3B",  # 焦糖色
    "#8F4E2E",  # 深褐色
    "#F2C4A0",  # 浅杏色
    "#E5B48C",  # 沙褐色
    "#C9A27B",  # 驼色
    "#9F7A59",  # 土棕色
    "#4C6A6A",  # 青灰色
]
