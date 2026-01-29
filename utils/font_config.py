from matplotlib import font_manager
import matplotlib.pyplot as plt
from pathlib import Path
import os
import platform
import logging

logger = logging.getLogger(__name__)


def configure_fonts():
    system = platform.system()

    font_candidates = [
        "Microsoft YaHei",
        "SimHei",
        "Arial Unicode MS",
        "PingFang SC",
        "Heiti SC",
        "WenQuanYi Micro Hei",
        "Noto Sans CJK SC",
    ]

    found_font = None

    if system == "Windows":
        font_dir = Path("C:/Windows/Fonts")
        if font_dir.exists():
            for font_name in ["msyh.ttc", "simhei.ttf", "arialuni.ttf"]:
                font_path = font_dir / font_name
                if font_path.exists():
                    try:
                        font_manager.fontManager.addfont(str(font_path))
                        plt.rcParams["font.family"] = ["sans-serif"]
                        plt.rcParams["font.sans-serif"] = [
                            font_name.split(".")[0]
                        ] + font_candidates
                        found_font = font_path
                        logger.info(f"Loaded Windows font: {font_path}")
                        break
                    except Exception as e:
                        logger.warning(f"Failed to load font {font_path}: {e}")

    if not found_font:
        available_fonts = set(f.name for f in font_manager.fontManager.ttflist)
        for font in font_candidates:
            if font in available_fonts:
                plt.rcParams["font.sans-serif"] = [font] + plt.rcParams[
                    "font.sans-serif"
                ]
                found_font = font
                logger.info(f"Using system font: {font}")
                break

    plt.rcParams["axes.unicode_minus"] = False

    if not found_font:
        logger.warning(
            "No Chinese font found! Charts may display squares for Chinese characters."
        )


def get_font_path(font_name: str) -> str:
    try:
        font_file = font_manager.findfont(font_name)
        return font_file
    except Exception:
        return ""
