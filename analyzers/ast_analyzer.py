import ast
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field


@dataclass
class FunctionInfo:
    name: str
    lineno: int
    end_lineno: int
    args: List[str]
    decorators: List[str]
    docstring: Optional[str]
    complexity: int = 0
    is_async: bool = False


@dataclass
class ClassInfo:
    name: str
    lineno: int
    end_lineno: int
    bases: List[str]
    methods: List[FunctionInfo] = field(default_factory=list)
    docstring: Optional[str] = None


class ASTAnalyzer:
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self.functions: List[FunctionInfo] = []
        self.classes: List[ClassInfo] = []

    def parse_file(self, file_path: Path) -> Optional[ast.AST]:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            return ast.parse(content)
        except Exception as e:
            print(f"Error parsing {file_path}: {e}")
            return None

    def analyze_file(self, file_path: Path):
        tree = self.parse_file(file_path)
        if not tree:
            return

        visitor = CodeVisitor()
        visitor.visit(tree)
        self.functions.extend(visitor.functions)
        self.classes.extend(visitor.classes)
        # Store imports if needed for dependency analysis directly from here

    def analyze_dependencies(self, file_path: Path) -> List[str]:
        # Now uses the optimized visitor if we integrate it,
        # but for backward compatibility we keep the standalone method or refactor it
        # Refactored to use CodeVisitor to avoid re-parsing if integrated
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            tree = ast.parse(content)
            visitor = CodeVisitor()
            visitor.visit(tree)
            return visitor.imports
        except Exception:
            return []

    def calculate_complexity(self, node: ast.AST) -> int:
        complexity = 1
        for child in ast.walk(node):
            if isinstance(
                child,
                (
                    ast.If,
                    ast.While,
                    ast.For,
                    ast.AsyncFor,
                    ast.With,
                    ast.AsyncWith,
                    ast.ExceptHandler,
                    ast.Assert,
                ),
            ):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
        return complexity

    def extract_call_graph(self) -> List[Dict[str, str]]:
        call_graph = []
        for func in self.functions:
            pass
        return call_graph

    def analyze_calls(self, file_path: Path) -> List[Dict[str, str]]:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            tree = ast.parse(content)
            visitor = CallVisitor()
            visitor.visit(tree)
            return visitor.calls
        except Exception:
            return []


class CallVisitor(ast.NodeVisitor):
    def __init__(self):
        self.calls = []
        self.current_function = None

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self.current_function = node.name
        self.generic_visit(node)
        self.current_function = None

    def visit_Call(self, node: ast.Call):
        if self.current_function:
            target_name = "unknown"
            if isinstance(node.func, ast.Name):
                target_name = node.func.id
            elif isinstance(node.func, ast.Attribute):
                target_name = node.func.attr

            self.calls.append({"source": self.current_function, "target": target_name})
        self.generic_visit(node)

    def __init__(self):
        self.functions: List[FunctionInfo] = []
        self.classes: List[ClassInfo] = []

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self._process_function(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        self._process_function(node, is_async=True)

    def _process_function(self, node, is_async=False):
        args = [a.arg for a in node.args.args]
        decorators = [self._get_decorator_name(d) for d in node.decorator_list]
        docstring = ast.get_docstring(node)

        # Calculate complexity
        complexity = 1
        for child in ast.walk(node):
            if isinstance(
                child,
                (
                    ast.If,
                    ast.While,
                    ast.For,
                    ast.AsyncFor,
                    ast.With,
                    ast.AsyncWith,
                    ast.ExceptHandler,
                    ast.Assert,
                ),
            ):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                # Each operator adds complexity
                complexity += len(child.values) - 1
            elif isinstance(child, ast.comprehension):
                complexity += 1

        func_info = FunctionInfo(
            name=node.name,
            lineno=node.lineno,
            end_lineno=node.end_lineno if hasattr(node, "end_lineno") else node.lineno,
            args=args,
            decorators=decorators,
            docstring=docstring,
            complexity=complexity,
            is_async=is_async,
        )
        self.functions.append(func_info)

    def _get_decorator_name(self, node):
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{self._get_decorator_name(node.value)}.{node.attr}"
        elif isinstance(node, ast.Call):
            return self._get_decorator_name(node.func)
        return "unknown"

    def visit_ClassDef(self, node: ast.ClassDef):
        bases = [self._get_base_name(b) for b in node.bases]
        docstring = ast.get_docstring(node)

        class_info = ClassInfo(
            name=node.name,
            lineno=node.lineno,
            end_lineno=node.end_lineno
            if hasattr(node, "end_lineno") and node.end_lineno is not None
            else node.lineno,
            bases=bases,
            docstring=docstring,
        )
        self.classes.append(class_info)
        self.generic_visit(node)

    def _get_base_name(self, node):
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{self._get_base_name(node.value)}.{node.attr}"
        return "unknown"

    def export_to_csv(self, output_file: str):
        import csv

        headers = [
            "name",
            "type",
            "line",
            "args_count",
            "complexity",
            "docstring_len",
            "decorators",
        ]

        with open(output_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)

            for func in self.functions:
                writer.writerow(
                    [
                        func.name,
                        "async_function" if func.is_async else "function",
                        func.lineno,
                        len(func.args),
                        func.complexity,
                        len(func.docstring) if func.docstring else 0,
                        len(func.decorators),
                    ]
                )

            for cls in self.classes:
                writer.writerow(
                    [
                        cls.name,
                        "class",
                        cls.lineno,
                        0,
                        0,
                        len(cls.docstring) if cls.docstring else 0,
                        0,
                    ]
                )
