from LPPy.Abstract import lpp
from LPPy.Abstract.converter import Converter
from LPPy.Abstract.outputHandler import OutputHandler


class Solver:
    """
    An abstract class to solve a given LPP
    """
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
