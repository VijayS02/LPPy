import sympy
from sympy import Eq

from Abstract.simpleSolver import SimpleSolver
from simpleTableau import SimpleTableau
import sysoutPrinter
from simpleConverter import SimpleConverter
from simpleLPP import SimpleLPP
from symEquation import SymEquation

if __name__ == "__main__":
    # Setup a list of variables
    vr = sympy.symbols("x1 x2 x3")
    # Create an objective row as a SymEquation
    obj_row = SymEquation(-1*vr[0] + 5*vr[1] + 4*vr[2])
    # Create the first constraint on the given LPP.
    row_1 = SymEquation((2*vr[0] + 4*vr[1] + vr[2] <= 12))
    row_2 = SymEquation((vr[0] <= 3))

    # Create some simple constraints to ensure the LPP can be converted
    std_const = []
    for var in vr:
        std_const.append(SymEquation(var >= 0))

    # Create the LPP class
    test = SimpleLPP(obj_row, [row_1,row_2] + std_const, True, sysoutPrinter.SysoutPrinter())

    # Use a compacted output method to print out the LPP in text.
    test.compacted_output()

    solver = SimpleSolver(test, SimpleConverter)
    solver.solve([3,4])


