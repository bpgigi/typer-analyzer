from enum import Enum

class CommitType(str, Enum):
    FEAT = "feat"
    FIX = "fix"
    DOCS = "docs"
    CHORE = "chore"
    REFACTOR = "refactor"
    TEST = "test"
    STYLE = "style"

TARGET_REPO_PATH = "C:/Users/l/Desktop/opensource/group3/typer"
OUTPUT_DIR = "output"
DATA_DIR = "data"
TRACES_DIR = "traces"
