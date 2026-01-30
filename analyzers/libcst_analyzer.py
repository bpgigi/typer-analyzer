import libcst as cst
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class TypeAnnotationInfo:
    file_path: str
    function_name: str
    arg_name: str
    annotation: str
    line_no: int


class LibCSTAnalyzer:
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self.type_annotations: List[TypeAnnotationInfo] = []

    def parse_file(self, file_path: Path) -> Optional[cst.Module]:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            return cst.parse_module(content)
        except Exception as e:
            print(f"Error parsing {file_path}: {e}")
            return None

    def analyze_file(self, file_path: Path):
        tree = self.parse_file(file_path)
        if not tree:
            return

        visitor = TypeCollector(str(file_path.relative_to(self.repo_path)))
        tree.visit(visitor)
        self.type_annotations.extend(visitor.annotations)


class TypeCollector(cst.CSTVisitor):
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.annotations: List[TypeAnnotationInfo] = []
        self.current_function: Optional[str] = None

    def visit_FunctionDef(self, node: cst.FunctionDef):
        self.current_function = node.name.value

        if node.returns:
            self._add_annotation("return", node.returns.annotation, node.name.value)

    def leave_FunctionDef(self, node: cst.FunctionDef):
        self.current_function = None

    def visit_Param(self, node: cst.Param):
        if self.current_function and node.annotation:
            self._add_annotation(
                node.name.value, node.annotation.annotation, self.current_function
            )

    def _add_annotation(
        self, arg_name: str, annotation_node: cst.BaseExpression, func_name: str
    ):
        try:
            annotation_str = cst.Module([]).code_for_node(annotation_node).strip()

            self.annotations.append(
                TypeAnnotationInfo(
                    file_path=self.file_path,
                    function_name=func_name,
                    arg_name=arg_name,
                    annotation=annotation_str,
                    line_no=0,
                )
            )
        except Exception:
            pass
