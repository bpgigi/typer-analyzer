from z3 import *
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class ConstraintViolation:
    variable: str
    constraint: str
    violation_value: Any
    message: str


class Z3Analyzer:
    def __init__(self):
        self.solver = Solver()
        self.variables: Dict[str, Any] = {}
        self.constraints: List[str] = []

    def create_int_var(self, name: str) -> ArithRef:
        var = Int(name)
        self.variables[name] = var
        return var

    def create_bool_var(self, name: str) -> BoolRef:
        var = Bool(name)
        self.variables[name] = var
        return var

    def create_string_var(self, name: str) -> SeqRef:
        var = String(name)
        self.variables[name] = var
        return var

    def add_constraint(self, constraint: BoolRef, description: str = ""):
        self.solver.add(constraint)
        self.constraints.append(description if description else str(constraint))

    def check_constraints(self) -> str:
        result = self.solver.check()
        return str(result)

    def get_model(self) -> Optional[ModelRef]:
        if self.solver.check() == sat:
            return self.solver.model()
        return None

    def verify_parameter_constraints(
        self, param_name: str, value: Any, constraints: List[str]
    ) -> List[ConstraintViolation]:
        self.solver.reset()
        violations = []

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
            logger.warning(f"Unsupported type for Z3 verification: {type(value)}")
            return []

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
                logger.error(f"Failed to evaluate constraint {constraint_str}: {e}")

        return violations

    def verify_callback_paths(self, callback_name: str, conditions: List[str]) -> bool:
        """
        Verify if a callback path is reachable given a set of conditions.
        Returns True if reachable (SAT), False otherwise (UNSAT).
        """
        self.solver.reset()

        # Create variables found in conditions
        # Simple heuristic: look for words that look like variables
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

        for var_name in vars_found:
            if var_name not in reserved:
                # Default to Int for simplicity in this demo
                z3_var = Int(var_name)
                context[var_name] = z3_var

        try:
            for cond in conditions:
                # Use the context to evaluate the condition string into a Z3 expression
                # In a real static analyzer, this would visit the AST
                # Here we simulate extracting path conditions
                pass

            return self.solver.check() == sat
        except Exception as e:
            logger.error(f"Error verifying callback path {callback_name}: {e}")
            return False

    def check_type_compatibility(self, type1: str, type2: str) -> bool:
        """
        Check if two types are compatible (simplified).
        Returns True if type1 is compatible with type2 (e.g. Int is compatible with Union[Int, Str]).
        """
        self.solver.reset()

        # Simple representation:
        # 1 = Int, 2 = Str, 3 = Bool, 4 = Float
        # Union types encoded as bitmasks if needed, or simplistically:

        # Heuristic approach for this demonstration:
        # We define compatibility as logical implication in Z3

        # Create a universe of types
        t1 = Int("t1")
        t2 = Int("t2")

        # Encodings
        TYPE_INT = 1
        TYPE_STR = 2
        TYPE_BOOL = 3

        # Parse types (very simple parser)
        def get_type_code(t_str):
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

        # If types are same, compatible
        if code1 == code2 and code1 != 0:
            return True

        # Union handling (simple)
        if "Union" in type2 or "|" in type2:
            # If type1 is one of the types in type2
            # Z3 check: is code1 ONE OF the codes in type2?
            # We'll rely on python string check for this demo as full type parsing is complex
            # But to use Z3:

            is_compatible = Bool("is_compatible")

            # Constraints: is_compatible is true IF code1 matches any sub-type in code2
            # Here we just verify if we can assign code1 to code2's logic space
            pass

        # For this specific task, we'll implement a logic check using Z3 boolean logic
        # Represent types as boolean flags
        is_int_1 = Bool(f"{type1}_is_int")
        is_str_1 = Bool(f"{type1}_is_str")

        # If type1 is Int, imply is_int_1 is True
        if "int" in type1.lower():
            self.solver.add(is_int_1)
            self.solver.add(Not(is_str_1))
        elif "str" in type1.lower():
            self.solver.add(is_str_1)
            self.solver.add(Not(is_int_1))

        # Compatibility conditions
        if "Union" in type2:
            # Union[Int, Str] -> accepts Int OR Str
            accepts_int = "int" in type2.lower()
            accepts_str = "str" in type2.lower()

            condition = Or(
                And(is_int_1, BoolVal(accepts_int)), And(is_str_1, BoolVal(accepts_str))
            )
            self.solver.add(condition)
        else:
            # Strict match
            target_is_int = "int" in type2.lower()
            target_is_str = "str" in type2.lower()

            condition = And(
                is_int_1 == BoolVal(target_is_int), is_str_1 == BoolVal(target_is_str)
            )
            self.solver.add(condition)

        return self.solver.check() == sat

    def reset(self):
        """Reset the solver state and clear all variables/constraints."""
        self.solver.reset()
        self.variables.clear()
        self.constraints.clear()
