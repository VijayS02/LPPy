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

    def solve(self, basics):
        raise NotImplementedError
