import pysnooper
from pathlib import Path
from typing import Optional, List, Dict, Any
from datetime import datetime
import threading
import logging

logger = logging.getLogger(__name__)


class DynamicTracer:
    def __init__(self, trace_dir: str = "traces"):
        self.trace_dir = Path(trace_dir)
        self.trace_dir.mkdir(exist_ok=True)
        self.current_trace_file: Optional[Path] = None
        self._lock = threading.Lock()

    def start_trace(self, name: str, variables: Optional[List[str]] = None):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"trace_{name}_{timestamp}.log"
        self.current_trace_file = self.trace_dir / filename

        logger.info(f"Starting trace: {name} -> {filename}")

        return pysnooper.snoop(
            str(self.current_trace_file),
            variables=variables,
            depth=2,
            prefix=f"[{name}] ",
            overwrite=True,
        )

    def get_trace_content(self) -> str:
        if not self.current_trace_file or not self.current_trace_file.exists():
            return ""

        try:
            with open(self.current_trace_file, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            logger.error(f"Error reading trace file: {e}")
            return ""

    def parse_trace_log(self, log_path: Path) -> List[Dict[str, Any]]:
        entries = []
        try:
            with open(log_path, "r", encoding="utf-8") as f:
                current_entry = {}
                for line in f:
                    line = line.strip()
                    if not line:
                        continue

                    parts = line.split(maxsplit=4)
                    if len(parts) >= 4:
                        entries.append(
                            {
                                "raw": line,
                                "timestamp": parts[1] if len(parts) > 1 else "",
                                "type": parts[2] if len(parts) > 2 else "",
                                "line_no": parts[3] if len(parts) > 3 else "",
                            }
                        )

            return entries
        except Exception as e:
            logger.error(f"Error parsing trace log {log_path}: {e}")
            return []
