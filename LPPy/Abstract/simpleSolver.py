from Abstract.converter import Converter
from Abstract.lpp import LPP
from Abstract.outputHandler import OutputHandler
from Abstract.solver import Solver
from Abstract.tableau import Tableau
from simpleTableau import SimpleTableau


class SimpleSolver(Solver):
    problem: LPP
    translator: Converter
    outputter: OutputHandler

    def __init__(self, probl: LPP, conv):
        self.problem = probl
        self.translator = conv(probl)
        self.outputter = probl.outputter

    def solve(self, basics):
        problem: Tableau = self.translator.generate_tableau(SimpleTableau, basics)
        problem.output()
        obj_row = problem.table[-1]
        # Finish masking n stuff
        masked_obj = obj_row
        while not all([x >= 0 for x in masked_obj]):
            problem.step_forward()
            problem.output()

    def solve_with_two_phase(self):
        self.problem.compacted_output()
        problem, new_vars = self.translator.generate_auxiliary()
        vars = problem.get_variables()
        basic_indexes = [vars.index(x) for x in new_vars]
        problem.compacted_output()
        tableau = self.translator.generate_tableau(SimpleTableau, basic_indexes)
        tableau.output()

        while tableau.get_cost() != 0:
            tableau.step_forward()
            tableau.output()

        new_var_indexes = [vars.index(x) for x in new_vars]
        self.outputter.write("Remove artificial variables from tableau.")
        tableau.remove_variables(new_var_indexes)

        obj = tableau.get_eq_array(self.problem.get_objective(), self.problem.get_variables()) + [0]
        basic_indexes = []
        i = 0
        for basic in tableau.get_basics():
            basic_index = tableau.get_variables().index(basic)
            basic_indexes.append(basic_index)
            mult = obj[basic_index]/tableau.table[i][basic_index]
            obj -= tableau.table[i] * mult
            i += 1

        tableau.set_objective(obj)
        self.problem = tableau

        tableau.output()
        obj_row = tableau.table[-1]
        # Finish masking n stuff
        masked_obj = obj_row
        while not all([x >= 0 for x in masked_obj]):
            tableau.step_forward()
            tableau.output()


