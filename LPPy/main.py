import sympy
from sympy import Eq

from Abstract.simpleSolver import SimpleSolver
from simpleTableau import SimpleTableau
import sysoutPrinter
from simpleConverter import SimpleConverter
from simpleLPP import SimpleLPP
from symEquation import SymEquation

if __name__ == "__main__":
    # # Setup a list of variables
    # vr = sympy.symbols("x1 x2 x3")
    # # Create an objective row as a SymEquation
    # obj_row = SymEquation(-1*vr[0] + 5*vr[1] + 4*vr[2])
    # # Create the first constraint on the given LPP.
    # row_1 = SymEquation((2*vr[0] + 4*vr[1] + vr[2] <= 12))
    # row_2 = SymEquation((vr[0] <= 3))
    #
    # # Create some simple constraints to ensure the LPP can be converted
    # std_const = []
    # for var in vr:
    #     std_const.append(SymEquation(var >= 0))
    #
    # # Create the LPP class
    # test = SimpleLPP(obj_row, [row_1,row_2] + std_const, True, sysoutPrinter.SysoutPrinter())
    #
    # # Use a compacted output method to print out the LPP in text.
    # test.compacted_output()
    #
    # solver = SimpleSolver(test, SimpleConverter)
    # solver.solve([3,4])


    # x = sympy.symbols("x1 x2 x3 x4 x5 x6")
    # obj = SymEquation(x[0] - 2 * x[1] - 3 * x[2] - x[3] - x[4] + 2 * x[5])
    # row_1 = SymEquation(Eq(x[0] + 2 * x[1] + 2 * x[2] + x[3] + x[4], 12))
    # row_2 = SymEquation(Eq(x[0] + 2 * x[1] + 1 * x[2] + x[3] + 2 * x[4] + x[5], 18))
    # row_3 = SymEquation(Eq(3 * x[0] + 6 * x[1] + 2 * x[2] + x[3] + 3 * x[4], 24))
    # std_const = []
    # for var in x:
    #     std_const.append(SymEquation(var >= 0))
    #
    # test = SimpleLPP(obj, [row_1, row_2, row_3] + std_const, True, sysoutPrinter.SysoutPrinter())
    # solver = SimpleSolver(test, SimpleConverter)
    # solver.solve_with_two_phase()

    x = sympy.symbols("x1 x2")
    obj = SymEquation((3*x[0] + (1/2)*x[1]))
    row_1 = SymEquation((x[0] - 2*x[1] >= 0))
    row_2 = SymEquation((x[0] + x[1] <= 3))

    std_const = []
    for var in x:
        std_const.append(SymEquation(var >= 0))

    test = SimpleLPP(obj, [row_1, row_2] + std_const, False, sysoutPrinter.SysoutPrinter())
    test.compacted_output()
    conv = SimpleConverter(test)
    conv.generate_dual().compacted_output()


