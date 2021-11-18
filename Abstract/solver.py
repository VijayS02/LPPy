from Abstract import lpp
from Abstract.converter import Converter
from Abstract.outputHandler import OutputHandler


class Solver:
    outputter: OutputHandler
    problem: lpp
    translator: Converter

    def solve(self):
        raise NotImplementedError

    def row_reduce(self):
        raise NotImplementedError

    def find_pivot(self):
        raise NotImplementedError

    def find_theta_ratios(self):
        raise NotImplementedError
