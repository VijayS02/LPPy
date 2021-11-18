import numpy as np
from sympy import Rational

from Abstract.equation import Equation
from Abstract.lpp import LPP
from Abstract.outputHandler import OutputHandler
from Abstract.tableau import Tableau
from simpleLPP import SimpleLPP
import numpy.ma as ma


class SimpleTableau(Tableau):
    table: np.array
    outputter: OutputHandler
    originalLPP: LPP
    basics: np.array
    pivot: tuple

    def __init__(self, objective, constraints, is_max, outputter):
        # create a simpleLPP class which can help grab specific attributes like simple constraints
        temporary = SimpleLPP(objective, constraints, is_max, outputter)
        self.outputter = outputter

        _, eq_constraints, _ = temporary.get_simple_constraints()
        eq_objective = objective

        variables = temporary.get_variables()
        new_obj = equation_to_array(eq_objective, variables)
        store = [equation_to_array(x, variables) for x in eq_constraints]
        self.table = np.array(store + [new_obj], dtype=object)
        self.originalLPP = temporary

    def find_pivot(self):
        objective_row = self.table[-1]
        objective_row = ma.masked_where(objective_row >= 0, objective_row)
        lowest_entry_in_objective = objective_row.argmin()

        lowest_entry_column = self.table[:, lowest_entry_in_objective]

        # Remove objective row
        lowest_entry_column = lowest_entry_column[:-1]

        masked_lec = ma.masked_where(lowest_entry_column > 0, lowest_entry_column)

        final_column = self.table[:, -1]

        theta_ratios = np.divide(final_column, masked_lec)
        self.outputter.write("Theta ratios:" + str(theta_ratios))
        self.outputter.write(theta_ratios)

        pivot_col = lowest_entry_column
        pivot_row = theta_ratios.argmin()
        self.pivot = (pivot_row, pivot_col)

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

        for i in range(len(self.table) - 1):
            multiplier = self.table[i][pivot_col] / pivot_value
            self.table[i] = self.table[i] - (self.table[pivot_row] * multiplier)

        self.pivot = (None, None)

    def step_forward(self):
        self.find_pivot()
        self.row_reduce()

    def step_backwards(self, pivot):
        self.pivot = pivot
        self.row_reduce()

    def solve(self):
        obj_row = self.table[-1]
        # Finish masking n stuff
        masked_obj = obj_row
        while not all([x >= 0 for x in masked_obj]):
            self.step_forward()

    def get_simple_constraints(self):
        return self.originalLPP.get_simple_constraints()

    def output(self):
        self.outputter.write_tableau(self.table, self.get_variables())

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

    return np.array(rationalized)
