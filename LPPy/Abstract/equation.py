from __future__ import annotations
# Equation type constants
from typing import List, Any

EQ = "="
LEQ = "<="
GEQ = ">="
NEQ = "!="
GE = ">"
LE = "<"
EEQ = "=="


def invert_type(type):
    if type == EQ:
        return EQ
    elif type == GEQ:
        return LEQ
    elif type == LEQ:
        return GEQ
    elif type == GE:
        return LE
    elif type == LE:
        return GE


class Equation:
    """
    An abstract class to define a certain type of equation of form LHS <type> RHS. E.g.
    3x + 2 >= 10, where LHS = 3x + 2, RHS = 10 and TYPE = equation.GEQ
    """

    def get_array_form(self, mask: List) -> List:
        """
        Generates an array of coefficients based on the mask.
        :param mask: The indexes and variables that coefficients are required for.
        :return: the i'th element of this output array corresponds to the coefficient of the i-th variable provided in
        mask.
        """
        # Note that this only gets the array form of the LHS of the equation.
        raise NotImplementedError

    def remove_variables(self, variables):
        raise NotImplementedError

    def get_type(self) -> str:
        """
        Get the type of equation as defined by constants at the top of equation.py.
        :return: the operator type.
        """
        raise NotImplementedError

    def get_lhs(self) -> Any:
        """
        Get the left hand side of this equation.
        :return: The left hand side of the equation object.
        """
        raise NotImplementedError

    def get_rhs(self) -> Any:
        """
        Get the right hand side of this equation.
        :return: The right hand side of the equation object.
        """
        raise NotImplementedError

    def substitute(self, old_var: Any, new_var: Any) -> Any:
        """
        Substitute a variable in this equation with an expression
        :param old_var: The variable to substitute.
        :param new_var: What to substitute with.
        :return: Nothing.
        """
        raise NotImplementedError

    def __str__(self) -> str:
        """
        :return: A string representation of the current object.
        """
        raise NotImplementedError

    def get_vars(self) -> List:
        """
        Gets a list of variables in this equation.
        E.g. "3x_2 + 5x_1 = 10y" would return ["x_2", "x_1", "y"] but type of variable may vary depending on
        implementation details.
        :return: A list of variables
        """
        raise NotImplementedError

    def solve_for(self, var):
        raise NotImplementedError

    def get_constants(self, vars):
        raise NotImplementedError

    def set_type(self, mode: str) -> None:
        """
        Changes the operator in this equation
        :param mode: The new operator to set the equation to
        :return: Nothing.
        """
        raise NotImplementedError

    def add_slack_variable(self, variables) -> Equation:
        """
        Check if the equation is of type equation.LEQ or equation.GEQ and then add a slack variable to convert the
        equation to type equation.EEQ.
        :param variables: A list of used variables to avoid using the same variable name twice.
        :return: A new equation with the slack variable implemented.
        """
        raise NotImplementedError

    def force_add_slack_variable_return(self, variables) -> Tuple[Equation, Any]:
        raise NotImplementedError

    def __neg__(self) -> Equation:
        """
        Negate the given equation (flip the sign and negate both sides)
        :return: The negated equation.
        """
        raise NotImplementedError
