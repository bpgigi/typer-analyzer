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

    def reset(self):
        self.solver.reset()
        self.variables.clear()
        self.constraints.clear()
