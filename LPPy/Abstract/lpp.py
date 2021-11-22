from typing import List, Tuple

from LPPy.Abstract.equation import Equation
from LPPy.Abstract.outputHandler import OutputHandler

# Constants for the different forms
CANONICAL = 'canonical form'
STANDARD = 'standard form'
UNKNOWN = "unknown form"


class LPP:
    """
    An abstract class defining a linear programming problem.
    """
    # Output handling
    outputter: OutputHandler

    def __init__(self, objective: Equation, constraints: List[Equation], is_max: bool, outputter: OutputHandler):
        """
        Initialization method
        :param objective: The objective function
        :param constraints: The constraints on the LPP
        :param is_max: if the LPP is of type "Maximization" this value should be set to true.
        :param outputter: The output handler to send outputs to.
        """
        raise NotImplementedError

    def get_table_form(self) -> List[List]:
        raise NotImplementedError

    def get_simple_constraints(self) -> Tuple[List[Equation], List[Equation], bool]:
        """
        A function to scan through the different constraints of the LPP.
        A simple constraint is a constraint defined by a constraint of the form "cx @ b" where c,b are real numbers and
        @ is either equation.GEQ or equation.LEQ.
        :return: A list of simple constraints, non simple constraints, boolean value representing if every variable in
        the lpp has a corresponding simple constraint.
        """
        raise NotImplementedError

    def get_free_variables(self) -> List:
        """
        Get a list of free variables.
        :return: A list of variables with no simple constraints in the given LPP.
        """
        raise NotImplementedError

    def output(self) -> None:
        """
        Output the current LPP
        :return: Nothing
        """
        raise NotImplementedError

    def set_objective(self, new_objective) -> None:
        """
        Set the objective function of this LPP.
        :param new_objective: The new objective function
        :return: Nothing.
        """
        raise NotImplementedError

    def get_objective(self) -> Equation:
        """
        Get the objective function of this LPP.
        :return: The objective function.
        """
        raise NotImplementedError

    def set_constraints(self, constraints: List[Equation]):
        """
        Set the constraints on the given LPP
        :param constraints: A list of equation constraints
        :return: Nothing.
        """
        raise NotImplementedError

    def get_constraints(self) -> List[Equation]:
        """
        Get the list of constraints applied to the given LPP.
        :return: A list of equation constraints for the given LPP.
        """
        raise NotImplementedError

    def get_is_max(self) -> bool:
        """
        Get the boolean value that represents if this LPP is a maximization problem or not.
        :return: the boolean attribute is_max.
        """
        raise NotImplementedError

    def set_is_max(self, new_max: bool):
        """
        Set the is_max parameter of this given LPP. I.e. define if this LPP is of type maximization or minimization.
        :param new_max: A boolean value representing whether the LPP should be a maximization problem.
        :return: nothing.
        """
        raise NotImplementedError

    def get_form(self) -> str:
        """
        Attempt to find the form of this LPP defined by constants at the top of lpp.py.
        :return: A string representing what form the given LPP is.
        """
        raise NotImplementedError

    def get_variables(self) -> List:
        """
        Get a List of variables used in this LPP
        :return: A list of variables used in the LPP
        """
        raise NotImplementedError

    def compacted_output(self) -> None:
        """
        Similar to the output method, this compacts the simple constraints into a more condensed form easier to
        read by humans.
        :return: Nothing.
        """
        raise NotImplementedError
