#!/usr/bin/env python3
"""Typer Repository Analyzer - Main Entry Point"""

import sys
from pathlib import Path

from config import BASE_DIR, WARM_COLORS, WARM_PALETTE
from constants import TARGET_REPO_PATH, OUTPUT_DIR, DATA_DIR
from exceptions import AnalyzerError


def main():
    """Main entry point for the analyzer."""
    print("=" * 50)
    print("Typer Repository Analyzer")
    print("=" * 50)
    print(f"Target repo: {TARGET_REPO_PATH}")
    print(f"Output dir: {OUTPUT_DIR}")
    print(f"Data dir: {DATA_DIR}")
    print("-" * 50)
    print("Starting analysis...")
    print("=" * 50)


if __name__ == "__main__":
    try:
        main()
    except AnalyzerError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
