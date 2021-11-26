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

