#!/usr/bin/env python3
import sys
from pathlib import Path
from typing import Optional, Dict, Any

from config import BASE_DIR, WARM_COLORS, WARM_PALETTE
from constants import TARGET_REPO_PATH, OUTPUT_DIR, DATA_DIR, TRACES_DIR, CommitType
from exceptions import AnalyzerError, ConfigurationError


class RepositoryAnalyzer:
    def __init__(self, repo_path: Optional[str] = None):
        self.repo_path = Path(repo_path) if repo_path else Path(TARGET_REPO_PATH)
        self.output_dir = Path(OUTPUT_DIR)
        self.data_dir = Path(DATA_DIR)
        self.traces_dir = Path(TRACES_DIR)
        self._validate_paths()
        self._setup_directories()

    def _validate_paths(self) -> None:
        if not self.repo_path.exists():
            raise ConfigurationError(
                f"Repository path does not exist: {self.repo_path}"
            )
        if not self.repo_path.is_dir():
            raise ConfigurationError(
                f"Repository path is not a directory: {self.repo_path}"
            )
        git_dir = self.repo_path / ".git"
        if not git_dir.exists():
            raise ConfigurationError(f"Path is not a git repository: {self.repo_path}")

    def _setup_directories(self) -> None:
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.traces_dir.mkdir(parents=True, exist_ok=True)
        (self.data_dir / "csv").mkdir(exist_ok=True)
        (self.data_dir / "json").mkdir(exist_ok=True)
        (self.data_dir / "traces").mkdir(exist_ok=True)

    def analyze(self) -> Dict[str, Any]:
        print("=" * 60)
        print("Typer Repository Analyzer")
        print("=" * 60)
        print(f"Target repo: {self.repo_path}")
        print(f"Output dir: {self.output_dir.absolute()}")
        print(f"Data dir: {self.data_dir.absolute()}")
        print("-" * 60)

        results = {
            "repo_path": str(self.repo_path),
            "output_dir": str(self.output_dir),
            "status": "initialized",
        }

        print("Analysis initialized successfully!")
        print("Ready for data collection and visualization...")
        print("=" * 60)

        return results


def main() -> int:
    try:
        analyzer = RepositoryAnalyzer()
        results = analyzer.analyze()
        print("\nAnalysis complete!")
        return 0
    except ConfigurationError as e:
        print(f"Configuration Error: {e}", file=sys.stderr)
        return 1
    except AnalyzerError as e:
        print(f"Analysis Error: {e}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.", file=sys.stderr)
        return 130
    except Exception as e:
        print(f"Unexpected Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
