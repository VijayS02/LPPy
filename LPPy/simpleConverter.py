import sympy
from sympy.core.relational import Relational

from Abstract import lpp, equation
from Abstract.converter import Converter
from Abstract.lpp import LPP
from Abstract.tableau import Tableau
from symEquation import SymEquation


class SimpleConverter(Converter):
    """
    Concrete version of Converter class.
    """

    # The original LPP
    problem: lpp.LPP

    def __init__(self, problem):
        self.problem = problem

    def convert_to_canonical(self) -> LPP:
        if self.problem.get_form() == lpp.CANONICAL:
            return self.problem

        new_objective = self.problem.get_objective()
        if not self.problem.get_is_max():
            new_objective = -new_objective

        simple, non_simple, _ = self.problem.get_simple_constraints()

        final_constraints = []
        final_constraints += simple

        for constraint in non_simple:
            if constraint.get_type() != LPPy.Abstract.equation.EQ:
                # Add slack variables wherever necessary
                final_constraints.append(constraint.add_slack_variable(self.problem.get_variables()))
            else:
                final_constraints.append(constraint)

        return self.problem.__class__(new_objective, final_constraints, True, self.problem.outputter)

    def convert_to_standard(self) -> LPP:
        raise NotImplementedError

    def generate_tableau(self, tableauClass, basic_indexes=None) -> Tableau:
        problem = self.problem
        if not problem.get_form() == lpp.CANONICAL:
            problem = self.convert_to_canonical()

        # Do auxilery stuffs
        simple, non_simple, _ = problem.get_simple_constraints()

        # This just takes the last m variables and sets them as the basic vars
        if not basic_indexes:
            basic_vars = problem.get_variables()[-(len(non_simple)):]
        else:
            variables = problem.get_variables()
            basic_vars = [variables[i] for i in basic_indexes]

        return tableauClass(problem.get_objective(), non_simple, basic_vars, problem.outputter)

    def generate_dual(self):
        if self.problem.get_is_max():
            raise ValueError("Cannot create dual LPP from maximization problem. Primal needs to be Minimization.")

        new_constraints = []
        simples, non_simples, _ = self.problem.get_simple_constraints()
        for const in non_simples:
            if const.get_type() != equation.EEQ:
                var = sympy.symbols(f"p{i}")
                eq = SymEquation(Relational(var, 0, const.get_type()))
                new_constraints.append(eq)

        for const in simples:
            pass

        # TODO: Not finished.
