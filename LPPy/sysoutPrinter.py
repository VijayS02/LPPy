from typing import List

import numpy as np

from Abstract.equation import Equation
from Abstract.outputHandler import OutputHandler


class SysoutPrinter(OutputHandler):
    """
    Simple console outputter version of outputHandler.
    """

    def write_theta_raitos(self, theta_ratios):
        theta_ratios = [x if x != np.inf else "infinity" for x in theta_ratios]
        print("Theta ratios: ")
        print(theta_ratios)

    def write_variables(self, variables: List, message: str = None):
        str_ver = [str(x) for x in variables]
        print(message, ','.join(str_ver))

    def start_equation_group(self):
        # This doesnt need to do anything
        pass

    def end_equation_group(self):
        # This doesnt need to do anything
        pass

    def write_tableau(self, table, variables, basic=None, pivot=None):
        if basic:
            print(f"{'':^8}", end=" ")
        for i in variables:
            print(f"{str(i):^8}", end=" ")
        print()

        i =0
        for row in table:
            if basic:
                if i == len(table)-1:
                    print(f"{'':^8}", end=" ")
                else:
                    print(f"{str(basic[i]):^8}", end=" ")
            for elem in row:
                print(f"{str(elem):^8}", end=" ")
            print()
            i+=1

    def __init__(self):
        return

    def write_eq(self, eq: Equation):
        print(str(eq))

    def write(self, output):
        print(output)

