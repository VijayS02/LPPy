import numpy as np

import LPPy.Abstract.lpp
from LPPy.Abstract.lpp import LPP
from LPPy.Abstract.outputHandler import OutputHandler


class Tableau(LPP):
    """
    An abstract class representing a tableau form of an LPP used in the Simplex Method.
    """
    # An output handler to send the output to.
    outputter: OutputHandler

    def get_form(self) -> str:
        """
        Return the form of the given LPP as canonical because every tableau represents a canonical problem. (APM236)
        :return: lpp.CANONICAL
        """
        return LPPy.Abstract.lpp.CANONICAL

    def get_is_max(self):
        """
        Every tableau is of form maximization when used in the simplex method. This means that this is always true.
        :return: True
        """
        return True

    def set_is_max(self, new_max: bool):
        return False
