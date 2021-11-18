from typing import List, Tuple

from Abstract.equation import Equation
from Abstract.outputHandler import OutputHandler

CANONICAL = 'canonical form'
STANDARD = 'standard form'
UNKNOWN = "unknown form"


class LPP:
    outputter: OutputHandler

    def __init__(self, objective, constraints, is_max, outputter):
        raise NotImplementedError

    def get_simple_constraints(self) -> Tuple[List[Equation], List[Equation], bool]:
        raise NotImplementedError

    def get_free_variables(self):
        raise NotImplementedError

    def output(self):
        raise NotImplementedError

    def set_objective(self, new_objective):
        raise NotImplementedError

    def get_objective(self):
        raise NotImplementedError

    def set_constraints(self, constraints):
        raise NotImplementedError

    def get_constraints(self):
        raise NotImplementedError

    def get_is_max(self):
        raise NotImplementedError

    def set_is_max(self, new_max: bool):
        raise NotImplementedError

    def get_form(self):
        raise NotImplementedError

    def get_variables(self):
        raise NotImplementedError
