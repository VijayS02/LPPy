from typing import Tuple, Any

import sympy
import sympy as sp
from sympy.core.relational import Relational

from Abstract.equation import Equation
import Abstract.equation as eq


class SymEquation(Equation):
    """
    Concrete equation built based purely on sympy.core.relational.Relational class
    """
    symq: sp.core.relational

    def set_type(self, mode):
        self.symq = Relational(self.symq.lhs, self.symq.rhs, mode)

    def get_constants(self):
        consts = 0
        if self.get_type() is None:
            return self.symq.coeff(sympy.symbols("x"), 0)
        consts -= self.symq.lhs.coeff(sympy.symbols("x"), 0)
        consts += self.symq.rhs.coeff(sympy.symbols("x"), 0)
        return consts

    def solve_for(self, var):
        return sympy.solve(self.symq, var)

    def add_slack_variable(self, variables) -> Equation:
        i = 1
        new_slack = sympy.symbols(f"y{i}")
        while new_slack in variables:
            i += 1
            new_slack = sympy.symbols(f"y{i}")

        if self.get_type() == eq.LEQ:
            return SymEquation(Relational(self.symq.lhs + new_slack, self.symq.rhs, eq.EEQ))
        elif self.get_type() == eq.GEQ:
            return SymEquation(Relational(self.symq.lhs - new_slack, self.symq.rhs, eq.EEQ))
        else:
            return

    def force_add_slack_variable_return(self, variables) -> Tuple[Equation, Any]:
        i = 1
        new_slack = sympy.symbols(f"y{i}")
        while new_slack in variables:
            i += 1
            new_slack = sympy.symbols(f"y{i}")

        if self.get_type() == eq.LEQ:
            return SymEquation(Relational(self.symq.lhs + new_slack, self.symq.rhs, eq.EEQ)), new_slack
        elif self.get_type() == eq.GEQ:
            return SymEquation(Relational(self.symq.lhs - new_slack, self.symq.rhs, eq.EEQ)), new_slack
        return SymEquation(Relational(self.symq.lhs + new_slack, self.symq.rhs, eq.EEQ)), new_slack

    def __neg__(self):
        if self.get_type() == eq.LEQ:
            new_type = eq.GEQ
        elif self.get_type() == eq.GEQ:
            new_type = eq.LEQ
        else:
            new_type = eq.EEQ
        try:
            return SymEquation(Relational(-self.symq.lhs, -self.symq.rhs, new_type))
        except Exception as e:
            return SymEquation(-self.symq)

    def __init__(self, eq):
        self.symq = eq

    def get_array_form(self, mask):
        if self.get_type() is None:
            focus = self.symq
        else:
            focus = self.symq.lhs

        ret_val = []
        for item in mask:
            ret_val.append(focus.coeff(item))
        return ret_val

    def get_type(self):
        symq_t = type(self.symq)
        if symq_t == sp.core.relational.Le:
            return eq.LEQ
        elif symq_t == sp.core.relational.Ge:
            return eq.GEQ
        elif symq_t == sp.core.relational.Eq:
            return eq.EEQ
        else:
            return None

    def get_lhs(self):
        return self.symq.lhs

    def get_rhs(self):
        return self.symq.rhs

    def substitute(self, old_var, new_var):
        return SymEquation(self.symq.subs(old_var, new_var))

    def __str__(self):
        if self.get_type() is not None:
            return self.symq.lhs.__str__() + " " + self.get_type() + " " + self.symq.rhs.__str__()
        else:
            return self.symq.__str__()

    def get_vars(self):
        return list(self.symq.free_symbols)
