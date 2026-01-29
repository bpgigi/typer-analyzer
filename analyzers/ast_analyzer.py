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

    def extract_functions(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Extract function information.

        Args:
            limit: Maximum number of functions to return.

        Returns:
            List of function details.
        """
        functions = []
        for func in self.functions:
            functions.append(
                {
                    "name": func.name,
                    "lineno": func.lineno,
                    "end_lineno": func.end_lineno,
                    "args_count": len(func.args),
                    "args": func.args,
                    "decorators_count": len(func.decorators),
                    "decorators": func.decorators,
                    "is_async": func.is_async,
                    "complexity": func.complexity,
                    "docstring_length": len(func.docstring) if func.docstring else 0,
                }
            )

        if limit:
            return functions[:limit]
        return functions

    def get_function_stats(self) -> Dict[str, Any]:
        """
        Get statistics about functions.
        """
        if not self.functions:
            return {
                "total_functions": 0,
                "async_functions": 0,
                "avg_args": 0,
                "avg_length": 0,
            }

        total_args = sum(len(f.args) for f in self.functions)
        total_length = sum(f.end_lineno - f.lineno for f in self.functions)
        async_count = sum(1 for f in self.functions if f.is_async)

        return {
            "total_functions": len(self.functions),
            "async_functions": async_count,
            "avg_args": total_args / len(self.functions),
            "avg_length": total_length / len(self.functions),
        }

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


class CodeVisitor(ast.NodeVisitor):
    def __init__(self):
        self.functions: List[FunctionInfo] = []
        self.classes: List[ClassInfo] = []

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self._process_function(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        self._process_function(node, is_async=True)

    def _process_function(self, node: Any, is_async: bool = False):
        decorators = [self._get_decorator_name(d) for d in node.decorator_list]

        args = [arg.arg for arg in node.args.args]

        # Ensure lineno and end_lineno are not None
        lineno = node.lineno if hasattr(node, "lineno") else 0
        end_lineno = (
            node.end_lineno
            if hasattr(node, "end_lineno") and node.end_lineno is not None
            else lineno
        )

        func_info = FunctionInfo(
            name=node.name,
            lineno=lineno,
            end_lineno=end_lineno,
            args=args,
            decorators=decorators,
            docstring=ast.get_docstring(node),
            is_async=is_async,
        )
        self.functions.append(func_info)
        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef):
        bases = [self._get_name(base) for base in node.bases]

        class_visitor = CodeVisitor()
        for child in node.body:
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                class_visitor.visit(child)

        # Ensure lineno and end_lineno are not None
        lineno = node.lineno if hasattr(node, "lineno") else 0
        end_lineno = (
            node.end_lineno
            if hasattr(node, "end_lineno") and node.end_lineno is not None
            else lineno
        )

        class_info = ClassInfo(
            name=node.name,
            lineno=lineno,
            end_lineno=end_lineno,
            bases=bases,
            methods=class_visitor.functions,
            docstring=ast.get_docstring(node),
        )
        self.classes.append(class_info)

    def _get_decorator_name(self, node: ast.AST) -> str:
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{self._get_name(node.value)}.{node.attr}"
        elif isinstance(node, ast.Call):
            return self._get_decorator_name(node.func)
        return "unknown"

    def _get_name(self, node: ast.AST) -> str:
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{self._get_name(node.value)}.{node.attr}"
        return "unknown"
