import numpy as np

import Abstract.lpp
from Abstract.lpp import LPP
from Abstract.outputHandler import OutputHandler


class Tableau(LPP):
    outputter: OutputHandler

    def get_form(self):
        return Abstract.lpp.CANONICAL

    def get_is_max(self):
        return True

    def set_is_max(self, new_max: bool):
        return False
