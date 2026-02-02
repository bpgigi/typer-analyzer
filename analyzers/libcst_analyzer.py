"""
LibCST 类型注解分析器模块
使用 LibCST 进行类型注解覆盖率统计和质量分析
"""

import libcst as cst
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import json


@dataclass
class TypeAnnotationInfo:
    """类型注解信息"""

    file_path: str  # 文件路径
    function_name: str  # 函数名称
    arg_name: str  # 参数名称
    annotation: str  # 注解内容
    line_no: int  # 行号


@dataclass
class CoverageStats:
    """覆盖率统计"""

    total_functions: int  # 函数总数
    annotated_functions: int  # 有注解的函数数
    total_params: int  # 参数总数
    annotated_params: int  # 有注解的参数数
    return_annotated: int  # 有返回值注解的函数数
    coverage_percentage: float  # 覆盖率百分比


class LibCSTAnalyzer:
    """
    LibCST 类型注解分析器
    负责分析 Python 代码的类型注解覆盖率和质量
    """

    def __init__(self, repo_path: str):
        """
        初始化分析器

        参数:
            repo_path: 仓库路径
        """
        self.repo_path = Path(repo_path)
        self.type_annotations: List[TypeAnnotationInfo] = []
        self.coverage_data: Dict[str, Any] = {}
        self.errors: List[str] = []

    def parse_file(self, file_path: Path) -> Optional[cst.Module]:
        """
        解析 Python 文件

        参数:
            file_path: 文件路径

        返回:
            解析后的 CST 模块，失败则返回 None
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            if not content.strip():
                return None
            return cst.parse_module(content)
        except cst.ParserSyntaxError as e:
            self.errors.append(f"语法错误 {file_path}: {e}")
            return None
        except Exception as e:
            self.errors.append(f"解析错误 {file_path}: {e}")
            return None

    def analyze_file(self, file_path: Path):
        """
        分析单个文件的类型注解

        参数:
            file_path: 文件路径
        """
        tree = self.parse_file(file_path)
        if not tree:
            return

        try:
            visitor = TypeCollector(str(file_path.relative_to(self.repo_path)))
            tree.visit(visitor)
            self.type_annotations.extend(visitor.annotations)
            self.coverage_data[str(file_path)] = visitor.coverage_stats
        except Exception as e:
            self.errors.append(f"分析错误 {file_path}: {e}")

    def get_annotation_stats(self) -> Dict[str, Any]:
        """
        获取注解统计信息

        返回:
            包含注解统计的字典
        """
        total_annotations = len(self.type_annotations)
        arg_annotations = sum(
            1 for a in self.type_annotations if a.arg_name != "return"
        )
        return_annotations = sum(
            1 for a in self.type_annotations if a.arg_name == "return"
        )

        # 分析泛型类型使用情况
        generics = {}
        for ann in self.type_annotations:
            if "[" in ann.annotation:
                base_type = ann.annotation.split("[")[0]
                generics[base_type] = generics.get(base_type, 0) + 1

        return {
            "注解总数": total_annotations,
            "参数注解数": arg_annotations,
            "返回值注解数": return_annotations,
            "错误数": len(self.errors),
            "泛型类型": generics,
        }

    def calculate_coverage(self) -> CoverageStats:
        """
        计算类型注解覆盖率

        返回:
            覆盖率统计对象
        """
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
        """
        导出覆盖率报告

        参数:
            output_path: 输出文件路径
        """
        stats = self.calculate_coverage()
        report = {
            "覆盖率统计": {
                "函数总数": stats.total_functions,
                "有注解函数数": stats.annotated_functions,
                "参数总数": stats.total_params,
                "有注解参数数": stats.annotated_params,
                "返回值注解数": stats.return_annotated,
                "覆盖率": round(stats.coverage_percentage, 2),
            },
            "错误列表": self.errors,
            "注解详情": [
                {
                    "文件": ann.file_path,
                    "函数": ann.function_name,
                    "参数": ann.arg_name,
                    "注解": ann.annotation,
                }
                for ann in self.type_annotations
            ],
        }
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

    def export_to_csv(self, output_file: str):
        """
        导出注解数据到 CSV 文件

        参数:
            output_file: 输出文件路径
        """
        import csv

        headers = ["文件", "函数", "参数", "注解"]

        with open(output_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()

            for ann in self.type_annotations:
                writer.writerow(
                    {
                        "文件": ann.file_path,
                        "函数": ann.function_name,
                        "参数": ann.arg_name,
                        "注解": ann.annotation,
                    }
                )

    def extract_annotations(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        提取注解列表

        参数:
            limit: 限制返回数量（可选）

        返回:
            注解字典列表
        """
        annotations = []
        for ann in self.type_annotations:
            annotations.append(
                {
                    "文件": ann.file_path,
                    "函数": ann.function_name,
                    "参数": ann.arg_name,
                    "注解": ann.annotation,
                }
            )

        if limit:
            return annotations[:limit]
        return annotations


class TypeCollector(cst.CSTVisitor):
    """
    类型注解收集器
    遍历 CST 收集所有类型注解信息
    """

    def __init__(self, file_path: str):
        """初始化收集器"""
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
        """获取覆盖率统计"""
        return {
            "total_functions": self.total_functions,
            "annotated_functions": self.annotated_functions,
            "total_params": self.total_params,
            "annotated_params": self.annotated_params,
            "return_annotated": self.return_annotated,
        }

    def visit_FunctionDef(self, node: cst.FunctionDef):
        """访问函数定义节点"""
        self.current_function = node.name.value
        self.total_functions += 1
        has_annotation = False

        # 检查返回值注解
        if node.returns:
            self._add_annotation("return", node.returns.annotation, node.name.value)
            self.return_annotated += 1
            has_annotation = True

        # 检查参数注解
        for param in node.params.params:
            self.total_params += 1
            if param.annotation:
                self.annotated_params += 1
                has_annotation = True

        if has_annotation:
            self.annotated_functions += 1

    def leave_FunctionDef(self, original_node: cst.FunctionDef):
        """离开函数定义节点"""
        self.current_function = None

    def visit_Param(self, node: cst.Param):
        """访问参数节点"""
        if self.current_function and node.annotation:
            self._add_annotation(
                node.name.value, node.annotation.annotation, self.current_function
            )

    def _add_annotation(
        self, arg_name: str, annotation_node: cst.BaseExpression, func_name: str
    ):
        """添加注解记录"""
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
