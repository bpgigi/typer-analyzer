"""
AST 静态分析器模块
使用 Python AST 进行函数、类、装饰器和复杂度分析
"""

import ast
import csv
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field


@dataclass
class FunctionInfo:
    """函数信息"""

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
    """类信息"""

    name: str
    lineno: int
    end_lineno: int
    bases: List[str]
    methods: List[FunctionInfo] = field(default_factory=list)
    docstring: Optional[str] = None


class CodeVisitor(ast.NodeVisitor):
    """AST 代码访问器，提取函数和类信息"""

    def __init__(self):
        self.functions: List[FunctionInfo] = []
        self.classes: List[ClassInfo] = []
        self.imports: List[str] = []

    def visit_Import(self, node: ast.Import):
        for alias in node.names:
            self.imports.append(alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        module = node.module or ""
        for alias in node.names:
            self.imports.append(f"{module}.{alias.name}")
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self._process_function(node, is_async=False)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        self._process_function(node, is_async=True)
        self.generic_visit(node)

    def _process_function(self, node, is_async=False):
        args = [a.arg for a in node.args.args]
        decorators = [self._get_decorator_name(d) for d in node.decorator_list]
        docstring = ast.get_docstring(node)

        complexity = self._calculate_complexity(node)

        func_info = FunctionInfo(
            name=node.name,
            lineno=node.lineno,
            end_lineno=getattr(node, "end_lineno", node.lineno) or node.lineno,
            args=args,
            decorators=decorators,
            docstring=docstring,
            complexity=complexity,
            is_async=is_async,
        )
        self.functions.append(func_info)

    def _calculate_complexity(self, node) -> int:
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
            elif isinstance(child, ast.comprehension):
                complexity += 1
        return complexity

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
            end_lineno=getattr(node, "end_lineno", node.lineno) or node.lineno,
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


class ASTAnalyzer:
    """AST 静态分析器"""

    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self.functions: List[FunctionInfo] = []
        self.classes: List[ClassInfo] = []
        self.imports: List[str] = []

    def parse_file(self, file_path: Path) -> Optional[ast.AST]:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            return ast.parse(content)
        except Exception:
            return None

    def analyze_file(self, file_path: Path):
        tree = self.parse_file(file_path)
        if not tree:
            return

        visitor = CodeVisitor()
        visitor.visit(tree)
        self.functions.extend(visitor.functions)
        self.classes.extend(visitor.classes)
        self.imports.extend(visitor.imports)

    def get_results(self) -> Dict[str, Any]:
        return {
            "functions_count": len(self.functions),
            "classes_count": len(self.classes),
            "imports_count": len(self.imports),
            "avg_complexity": sum(f.complexity for f in self.functions)
            / len(self.functions)
            if self.functions
            else 0,
        }

    def export_to_csv(self, output_file: str):
        headers = ["name", "type", "lineno", "args_count", "complexity", "docstring_len", "decorators_count"]

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

