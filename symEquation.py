import sympy
import sympy as sp
from sympy.core.relational import Relational
from sympy.core.relational import Eq

import Abstract.equation
from Abstract.equation import Equation


class SymEquation(Equation):
    symq: sp.core.relational

    def set_type(self, mode):
        self.symq = Relational(self.symq.lhs, self.symq.rhs, mode)

    def add_slack_variable(self, variables) -> Equation:
        i = 1
        new_slack = sympy.symbols(f"y{i}")
        while new_slack in variables:
            i += 1
            new_slack = sympy.symbols(f"y{i}")

        if self.get_type() == Abstract.equation.LEQ:
            return SymEquation(Relational(self.symq.lhs + new_slack, self.symq.rhs, Abstract.equation.EEQ))
        elif self.get_type() == Abstract.equation.GEQ:
            return SymEquation(Relational(self.symq.lhs - new_slack, self.symq.rhs, Abstract.equation.EEQ))
        else:
            return self

    def __neg__(self):
        if self.get_type() == Abstract.equation.LEQ:
            new_type = Abstract.equation.GEQ
        elif self.get_type() == Abstract.equation.GEQ:
            new_type = Abstract.equation.LEQ
        else:
            new_type = Abstract.equation.EEQ
        return SymEquation(Relational(-self.symq.lhs, -self.symq.rhs, new_type))

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
            return Abstract.equation.LEQ
        elif symq_t == sp.core.relational.Ge:
            return Abstract.equation.GEQ
        elif symq_t == sp.core.relational.Eq:
            return Abstract.equation.EEQ
        else:
            return None

    def get_lhs(self):
        return self.symq.lhs

    def get_rhs(self):
        return self.symq.rhs

    def substitute(self, old_var, new_var):
        self.symq.subs(old_var, new_var)

    def __str__(self):
        if self.get_type() is not None:
            return self.symq.lhs.__str__() + " " + self.get_type() + " " + self.symq.rhs.__str__()
        else:
            return self.symq.__str__()

    def get_vars(self):
        return list(self.symq.free_symbols)
