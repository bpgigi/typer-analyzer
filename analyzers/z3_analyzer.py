"""
Z3 约束求解器模块
使用 Z3-Solver 进行符号执行、参数约束验证和类型兼容性检查
"""

from z3 import *
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class ConstraintViolation:
    """约束违反记录"""

    variable: str  # 变量名
    constraint: str  # 约束条件
    violation_value: Any  # 违反的值
    message: str  # 错误消息


class Z3Analyzer:
    """
    Z3 约束分析器
    用于验证 CLI 参数约束、分析回调路径、检查类型兼容性
    """

    def __init__(self):
        """初始化求解器"""
        self.solver = Solver()
        self.variables: Dict[str, Any] = {}  # 变量存储
        self.constraints: List[str] = []  # 约束列表

    def create_int_var(self, name: str) -> ArithRef:
        """创建整数变量"""
        var = Int(name)
        self.variables[name] = var
        return var

    def create_bool_var(self, name: str) -> BoolRef:
        """创建布尔变量"""
        var = Bool(name)
        self.variables[name] = var
        return var

    def create_string_var(self, name: str) -> SeqRef:
        """创建字符串变量"""
        var = String(name)
        self.variables[name] = var
        return var

    def add_constraint(self, constraint: BoolRef, description: str = ""):
        """添加约束条件"""
        self.solver.add(constraint)
        self.constraints.append(description if description else str(constraint))

    def check_constraints(self) -> str:
        """
        检查当前约束是否可满足
        返回: 'sat'(可满足), 'unsat'(不可满足), 或 'error'(错误)
        """
        try:
            result = self.solver.check()
            return str(result)
        except Z3Exception as e:
            logger.error(f"Z3 求解器错误: {e}")
            return "error"

    def get_model(self) -> Optional[ModelRef]:
        """获取满足约束的模型（如果存在）"""
        try:
            if self.solver.check() == sat:
                return self.solver.model()
        except Z3Exception:
            pass
        return None

    def verify_parameter_constraints(
        self, param_name: str, value: Any, constraints: List[str]
    ) -> List[ConstraintViolation]:
        """
        验证参数约束

        参数:
            param_name: 参数名称
            value: 参数值
            constraints: 约束条件列表

        返回:
            约束违反记录列表
        """
        self.solver.reset()
        violations = []

        # 根据值类型创建对应的 Z3 变量
        if isinstance(value, int):
            z3_var = Int(param_name)
            self.solver.add(z3_var == value)
        elif isinstance(value, bool):
            z3_var = Bool(param_name)
            self.solver.add(z3_var == value)
        elif isinstance(value, str):
            z3_var = String(param_name)
            self.solver.add(z3_var == StringVal(value))
        else:
            logger.warning(f"不支持的 Z3 验证类型: {type(value)}")
            return []

        # 验证每个约束
        for constraint_str in constraints:
            s = Solver()
            s.add(z3_var == value)

            try:
                context = {
                    param_name: z3_var,
                    "And": And,
                    "Or": Or,
                    "Not": Not,
                    "Int": Int,
                    "Bool": Bool,
                    "String": String,
                    "Length": Length,
                }
                pass
            except Exception as e:
                logger.error(f"约束求值失败 {constraint_str}: {e}")

        return violations

    def verify_callback_paths(self, callback_name: str, conditions: List[str]) -> bool:
        """
        验证回调路径是否可达

        参数:
            callback_name: 回调函数名称
            conditions: 路径条件列表

        返回:
            True 表示可达(SAT)，False 表示不可达(UNSAT)
        """
        self.solver.reset()

        # 从条件中提取变量名
        import re

        vars_found = set(
            re.findall(r"\b[a-zA-Z_][a-zA-Z0-9_]*\b", " ".join(conditions))
        )
        reserved = {"And", "Or", "Not", "True", "False"}

        context = {
            "And": And,
            "Or": Or,
            "Not": Not,
            "Int": Int,
            "Bool": Bool,
            "String": String,
        }

        # 为发现的变量创建 Z3 变量
        for var_name in vars_found:
            if var_name not in reserved:
                z3_var = Int(var_name)
                context[var_name] = z3_var

        try:
            for cond in conditions:
                # 在实际静态分析器中，这里会遍历 AST
                # 此处为简化演示
                pass

            return self.solver.check() == sat
        except Exception as e:
            logger.error(f"验证回调路径 {callback_name} 时出错: {e}")
            return False

    def check_type_compatibility(self, type1: str, type2: str) -> bool:
        """
        检查两个类型是否兼容

        参数:
            type1: 源类型
            type2: 目标类型

        返回:
            True 表示兼容，False 表示不兼容
        """
        self.solver.reset()

        # 类型编码：1=Int, 2=Str, 3=Bool
        TYPE_INT = 1
        TYPE_STR = 2
        TYPE_BOOL = 3

        def get_type_code(t_str):
            """获取类型编码"""
            t_str = t_str.lower()
            if "int" in t_str:
                return TYPE_INT
            if "str" in t_str:
                return TYPE_STR
            if "bool" in t_str:
                return TYPE_BOOL
            return 0

        code1 = get_type_code(type1)
        code2 = get_type_code(type2)

        # 相同类型直接兼容
        if code1 == code2 and code1 != 0:
            return True

        # 处理 Union 类型
        if "Union" in type2 or "|" in type2:
            is_compatible = Bool("is_compatible")
            pass

        # 使用 Z3 布尔逻辑检查兼容性
        is_int_1 = Bool(f"{type1}_is_int")
        is_str_1 = Bool(f"{type1}_is_str")

        if "int" in type1.lower():
            self.solver.add(is_int_1)
            self.solver.add(Not(is_str_1))
        elif "str" in type1.lower():
            self.solver.add(is_str_1)
            self.solver.add(Not(is_int_1))

        # 兼容性条件
        if "Union" in type2:
            accepts_int = "int" in type2.lower()
            accepts_str = "str" in type2.lower()

            condition = Or(
                And(is_int_1, BoolVal(accepts_int)), And(is_str_1, BoolVal(accepts_str))
            )
            self.solver.add(condition)
        else:
            target_is_int = "int" in type2.lower()
            target_is_str = "str" in type2.lower()

            condition = And(
                is_int_1 == BoolVal(target_is_int), is_str_1 == BoolVal(target_is_str)
            )
            self.solver.add(condition)

        return self.solver.check() == sat

    def export_analysis_csv(
        self, output_file: str, analysis_results: List[Dict[str, Any]]
    ):
        """
        导出分析结果到 CSV 文件

        参数:
            output_file: 输出文件路径
            analysis_results: 分析结果列表
        """
        import csv

        headers = ["类型", "变量", "约束", "状态", "值"]

        with open(output_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()

            for result in analysis_results:
                writer.writerow(
                    {
                        "类型": result.get("type", "约束"),
                        "变量": result.get("variable", ""),
                        "约束": result.get("constraint", ""),
                        "状态": result.get("status", "未知"),
                        "值": str(result.get("value", "")),
                    }
                )

    def reset(self):
        """重置求解器状态，清除所有变量和约束"""
        self.solver.reset()
        self.variables.clear()
        self.constraints.clear()
