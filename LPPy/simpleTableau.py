import numpy as np
from sympy import Rational

from Abstract.equation import Equation
from Abstract.lpp import LPP
from Abstract.outputHandler import OutputHandler
from Abstract.tableau import Tableau
from simpleLPP import SimpleLPP
import numpy.ma as ma


class SimpleTableau(Tableau):
    """
    Concrete Tableau class built using Sympy symbols and NP arrays.
    """
    table: np.array
    outputter: OutputHandler
    originalLPP: LPP
    basics: np.array
    pivot: tuple

    def __init__(self, objective, constraints, basic_vars, outputter, ):
        # create a simpleLPP class which can help grab specific attributes like simple constraints
        temporary = SimpleLPP(objective, constraints, True, outputter)
        self.outputter = outputter

        _, eq_constraints, _ = temporary.get_simple_constraints()
        eq_objective = objective

        variables = temporary.get_variables()
        new_obj = equation_to_array(eq_objective, variables) + [eq_objective.get_constants()]
        new_obj = [-x for x in new_obj]
        store = [equation_to_array(x, variables) for x in eq_constraints] + [new_obj]
        self.table = np.array(store, dtype=object)
        self.originalLPP = temporary
        self.basics = basic_vars

    def find_pivot(self):
        objective_row = self.table[-1][:-1]
        masked_objective_row = ma.masked_where(objective_row >= 0, objective_row)
        # lowest_entry_in_objective = masked_objective_row.argmin()
        # This doesnt seem to work because of object array type
        list_ver = list(masked_objective_row)
        lowest_entry_in_objective_pos = list_ver.index(min(list_ver))

        if type(lowest_entry_in_objective_pos) == ma.core.MaskedConstant:
            return False

        lowest_entry_column = self.table[:-1, lowest_entry_in_objective_pos]

        masked_lec = ma.masked_where(lowest_entry_column < 0, lowest_entry_column)

        final_column = self.table[:-1, -1]

        theta_ratios = np.divide(final_column, masked_lec).filled(np.inf)
        self.outputter.write_theta_raitos(list(theta_ratios))

        pivot_col = lowest_entry_in_objective_pos
        # pivot_row = theta_ratios.argmin() Doesnt work either.
        list_theta = list(theta_ratios)
        pivot_row = list_theta.index(min(list_theta))
        if type(pivot_row) == ma.core.MaskedConstant:
            return False

        self.pivot = (pivot_row, pivot_col)
        return True

    def row_reduce(self):
        assert self.pivot[0] is not None and self.pivot[1] is not None

        pivot_row = self.pivot[0]
        pivot_col = self.pivot[1]

        departing = self.basics[pivot_row]
        incoming = self.get_variables()[pivot_col]
        self.outputter.write(f"Departing variable: {departing}"
                             f"\nIncomming variable: {incoming}")

        self.basics[pivot_row] = incoming

        pivot_value = self.table[pivot_row][pivot_col]
        new_pivot_row = self.table[pivot_row] / pivot_value
        self.table[pivot_row] = new_pivot_row
        pivot_value = self.table[pivot_row][pivot_col]

        for i in range(len(self.table)):
            multiplier = self.table[i][pivot_col] / pivot_value
            if i != pivot_row:
                self.table[i] = self.table[i] - (self.table[pivot_row] * multiplier)

        self.pivot = (None, None)

    def step_forward(self):
        if self.find_pivot():
            self.row_reduce()
        else:
            self.outputter.write("All objective entries are positive.")

    def step_backwards(self, pivot):
        self.pivot = pivot
        self.row_reduce()

    def get_simple_constraints(self):
        return self.originalLPP.get_simple_constraints()

    def output(self):
        self.outputter.write_tableau(self.table, self.get_variables(), self.basics)

    def set_objective(self, new_objective):
        pass

    def get_objective(self):
        pass

    def set_constraints(self, constraints):
        pass

    def get_constraints(self):
        pass

    def get_variables(self):
        return self.originalLPP.get_variables()


def equation_to_array(eq: Equation, variables):
    ret_val = []
    ret_val += eq.get_array_form(variables)
    if eq.get_type() is not None:
        ret_val += [eq.get_rhs()]

    # Convert to rationals so that sympy can show all calculations
    rationalized = [Rational(x) for x in ret_val]

    return rationalized
