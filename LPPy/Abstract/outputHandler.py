from typing import List, Tuple

from LPPy.Abstract.equation import Equation


class OutputHandler:
    """
    An abstract class used to send outputs to a given area.
    """
    def write_eq(self, constraint: Equation):
        """
        Output an equation
        :param constraint: the equation to output
        :return: Nothing.
        """
        raise NotImplementedError

    def write_variables(self,variables: List, message: str = None):
        raise NotImplementedError

    def start_equation_group(self):
        """
        Start the equation environment
        :return: nothing
        """
        raise NotImplementedError

    def end_equation_group(self):
        """
        Stop the equation environment
        :return: Nothing
        """
        raise NotImplementedError

    def write(self, output: str) -> None:
        """
        Simply pass the given string to the output and display it
        :param output: The string to be outputted
        :return: Nothing.
        """

        raise NotImplementedError

    def write_tableau(self, table: List[List], variables: List, basic: List = None, pivot: Tuple = None) -> None:
        """
        Write a tableau to the output
        :param table: The 2D List representing the constraints on the LPP.
        :param variables: The list of variables in the LPP which the table corresponds to (in matching index order).
        :param basic: (Optional) A list of basic variables in the given tableau
        :param pivot: (Optional) The selected pivot when computing the simplex method of the tableau.
        :return: Nothing
        """
        raise NotImplementedError

    def write_theta_raitos(self, theta_ratios):
        raise NotImplementedError
