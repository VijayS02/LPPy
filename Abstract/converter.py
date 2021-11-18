from typing import Callable

from Abstract.lpp import LPP
from Abstract.tableau import Tableau


class Converter:
    """
    An abstract class used to convert between different forms of LPPs.
    """
    def convert_to_canonical(self) -> LPP:
        """
        Converts a given LPP to canonical form.
        :return: The new canonical LPP.
        """
        raise NotImplementedError

    def convert_to_standard(self) -> LPP:
        """
        Converts a given LPP to standard form.
        :return: The new standard LPP
        """
        raise NotImplementedError

    def generate_tableau(self, tableauClass: Callable) -> Tableau:
        """
        Generates a tableau from an LPP.
        :param tableauClass: The type of tableau that is to be initialized.
        :return: the new Tableau of class tableauClass.
        """
        raise NotImplementedError

    def generate_dual(self) -> LPP:
        """
        Generates the dual of the given LPP.
        Assuming the provided LPP is the primal LPP.
        :return: The dual LPP
        """
        raise NotImplementedError
