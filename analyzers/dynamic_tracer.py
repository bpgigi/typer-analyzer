import pysnooper
from pathlib import Path
from typing import Optional, List, Dict, Any, Callable
from dataclasses import dataclass, field
from datetime import datetime
import threading
import logging
import json

logger = logging.getLogger(__name__)


@dataclass
class TraceEvent:
    timestamp: str
    function_name: str
    event_type: str
    line_no: int
    source_line: str
    locals: Dict[str, Any]


@dataclass
class CallbackTrace:
    callback_name: str
    trigger_event: str
    execution_path: List[TraceEvent] = field(default_factory=list)
    start_time: Optional[str] = None
    end_time: Optional[str] = None


class DynamicTracer:
    def __init__(self, trace_dir: str = "traces"):
        self.trace_dir = Path(trace_dir)
        self.trace_dir.mkdir(exist_ok=True)
        self.current_trace_file: Optional[Path] = None
        self._lock = threading.Lock()

    def start_trace(self, name: str, watch: Optional[List[str]] = None):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"trace_{name}_{timestamp}.log"
        self.current_trace_file = self.trace_dir / filename

        logger.info(f"Starting trace: {name} -> {filename}")

        return pysnooper.snoop(
            str(self.current_trace_file),
            watch=watch,
            depth=2,
            prefix=f"[{name}] ",
            overwrite=True,
        )

    def trace_typer_core(self):
        variables = ["app", "command", "typer_instance"]

        with self.start_trace("typer_core", watch=variables):
            try:
                import typer

                app = typer.Typer()

                @app.command()
                def hello(name: str):
                    print(f"Hello {name}")

            except ImportError:
                print("Typer not installed, skipping trace")
            except Exception as e:
                print(f"Error in typer trace: {e}")

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

    def trace_callback(self, callback_func: Callable, trigger: str) -> CallbackTrace:
        trace = CallbackTrace(
            callback_name=callback_func.__name__,
            trigger_event=trigger,
            start_time=datetime.now().isoformat(),
        )

        output_file = self.trace_dir / f"callback_{callback_func.__name__}.log"

        @pysnooper.snoop(
            str(output_file),
            depth=3,
            prefix=f"CALLBACK[{callback_func.__name__}]",
        )
        def wrapper(*args, **kwargs):
            return callback_func(*args, **kwargs)

        trace.end_time = datetime.now().isoformat()
        return trace

    def trace_function_vars(
        self, func: Callable, watch_vars: List[str] = None
    ) -> CallbackTrace:
        trace = CallbackTrace(
            callback_name=func.__name__,
            trigger_event="function_call",
            start_time=datetime.now().isoformat(),
        )

        output_file = self.trace_dir / f"vars_{func.__name__}.log"

        @pysnooper.snoop(
            str(output_file), watch=watch_vars, depth=2, prefix=f"VARS[{func.__name__}]"
        )
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        trace.end_time = datetime.now().isoformat()
        return trace

    def export_callback_report(self, output_path: Path):
        report = {
            "trace_directory": str(self.trace_dir),
            "total_traces": len(list(self.trace_dir.glob("*.log"))),
        }

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

    def trace_typer_callback(
        self, app, callback_type: str = "default"
    ) -> CallbackTrace:
        trace = CallbackTrace(
            callback_name=f"typer_{callback_type}_callback",
            trigger_event="app_execution",
            start_time=datetime.now().isoformat(),
        )

        output_file = self.trace_dir / f"typer_callback_{callback_type}.log"

        if hasattr(app, "callback") and app.callback:
            original_callback = app.callback

            @pysnooper.snoop(
                str(output_file),
                depth=2,
                prefix="TYPER_CALLBACK",
            )
            def traced_callback(*args, **kwargs):
                return original_callback(*args, **kwargs)

            trace.end_time = datetime.now().isoformat()

        return trace

    def analyze_callback_patterns(self) -> Dict[str, Any]:
        patterns = {
            "total_callbacks": 0,
            "callback_types": {},
            "common_locals": [],
        }

        for trace_file in self.trace_dir.glob("callback_*.log"):
            patterns["total_callbacks"] += 1
            callback_type = trace_file.stem.replace("callback_", "").split("_")[0]
            patterns["callback_types"][callback_type] = (
                patterns["callback_types"].get(callback_type, 0) + 1
            )

        return patterns

    def get_trace_summary(self) -> Dict[str, Any]:
        return {
            "total_traces": len(list(self.trace_dir.glob("*.log"))),
            "trace_directory": str(self.trace_dir),
            "callback_traces": len(list(self.trace_dir.glob("callback_*.log"))),
            "typer_traces": len(list(self.trace_dir.glob("typer_*.log"))),
        }
