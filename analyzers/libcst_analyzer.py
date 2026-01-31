import libcst as cst
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import json


@dataclass
class TypeAnnotationInfo:
    file_path: str
    function_name: str
    arg_name: str
    annotation: str
    line_no: int


@dataclass
class CoverageStats:
    total_functions: int
    annotated_functions: int
    total_params: int
    annotated_params: int
    return_annotated: int
    coverage_percentage: float


class LibCSTAnalyzer:
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self.type_annotations: List[TypeAnnotationInfo] = []
        self.coverage_data: Dict[str, Any] = {}
        self.errors: List[str] = []

    def parse_file(self, file_path: Path) -> Optional[cst.Module]:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            if not content.strip():
                return None
            return cst.parse_module(content)
        except cst.ParserSyntaxError as e:
            self.errors.append(f"Syntax error in {file_path}: {e}")
            return None
        except Exception as e:
            self.errors.append(f"Error parsing {file_path}: {e}")
            return None

    def analyze_file(self, file_path: Path):
        tree = self.parse_file(file_path)
        if not tree:
            return

        try:
            visitor = TypeCollector(str(file_path.relative_to(self.repo_path)))
            tree.visit(visitor)
            self.type_annotations.extend(visitor.annotations)
            self.coverage_data[str(file_path)] = visitor.coverage_stats
        except Exception as e:
            self.errors.append(f"Error analyzing {file_path}: {e}")

    def get_annotation_stats(self) -> Dict[str, Any]:
        total_annotations = len(self.type_annotations)
        arg_annotations = sum(
            1 for a in self.type_annotations if a.arg_name != "return"
        )
        return_annotations = sum(
            1 for a in self.type_annotations if a.arg_name == "return"
        )

        # Analyze generic types
        generics = {}
        for ann in self.type_annotations:
            if "[" in ann.annotation:
                base_type = ann.annotation.split("[")[0]
                generics[base_type] = generics.get(base_type, 0) + 1

        return {
            "total_annotations": total_annotations,
            "arg_annotations": arg_annotations,
            "return_annotations": return_annotations,
            "errors": len(self.errors),
            "generics": generics,
        }

    def calculate_coverage(self) -> CoverageStats:
        total_funcs = 0
        annotated_funcs = 0
        total_params = 0
        annotated_params = 0
        return_annotated = 0

        for data in self.coverage_data.values():
            total_funcs += data.get("total_functions", 0)
            annotated_funcs += data.get("annotated_functions", 0)
            total_params += data.get("total_params", 0)
            annotated_params += data.get("annotated_params", 0)
            return_annotated += data.get("return_annotated", 0)

        coverage_pct = (
            (annotated_params / total_params * 100) if total_params > 0 else 0
        )

        return CoverageStats(
            total_functions=total_funcs,
            annotated_functions=annotated_funcs,
            total_params=total_params,
            annotated_params=annotated_params,
            return_annotated=return_annotated,
            coverage_percentage=coverage_pct,
        )

    def export_coverage_report(self, output_path: Path):
        stats = self.calculate_coverage()
        report = {
            "coverage_stats": {
                "total_functions": stats.total_functions,
                "annotated_functions": stats.annotated_functions,
                "total_params": stats.total_params,
                "annotated_params": stats.annotated_params,
                "return_annotated": stats.return_annotated,
                "coverage_percentage": round(stats.coverage_percentage, 2),
            },
            "errors": self.errors,
            "annotations": [
                {
                    "file": ann.file_path,
                    "function": ann.function_name,
                    "arg": ann.arg_name,
                    "annotation": ann.annotation,
                }
                for ann in self.type_annotations
            ],
        }
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

    def extract_annotations(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        annotations = []
        for ann in self.type_annotations:
            annotations.append(
                {
                    "file": ann.file_path,
                    "function": ann.function_name,
                    "arg": ann.arg_name,
                    "annotation": ann.annotation,
                }
            )

        if limit:
            return annotations[:limit]
        return annotations


class TypeCollector(cst.CSTVisitor):
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.annotations: List[TypeAnnotationInfo] = []
        self.current_function: Optional[str] = None
        self.total_functions = 0
        self.annotated_functions = 0
        self.total_params = 0
        self.annotated_params = 0
        self.return_annotated = 0

    @property
    def coverage_stats(self) -> Dict[str, int]:
        return {
            "total_functions": self.total_functions,
            "annotated_functions": self.annotated_functions,
            "total_params": self.total_params,
            "annotated_params": self.annotated_params,
            "return_annotated": self.return_annotated,
        }

    def visit_FunctionDef(self, node: cst.FunctionDef):
        self.current_function = node.name.value
        self.total_functions += 1
        has_annotation = False

        if node.returns:
            self._add_annotation("return", node.returns.annotation, node.name.value)
            self.return_annotated += 1
            has_annotation = True

        for param in node.params.params:
            self.total_params += 1
            if param.annotation:
                self.annotated_params += 1
                has_annotation = True

        if has_annotation:
            self.annotated_functions += 1

    def leave_FunctionDef(self, original_node: cst.FunctionDef):
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
