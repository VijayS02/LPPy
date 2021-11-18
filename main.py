import sympy

from simpleTableau import SimpleTableau
import sysoutPrinter
from simpleConverter import SimpleConverter
from simpleLPP import SimpleLPP
from symEquation import SymEquation

if __name__ == "__main__":
    # Setup a list of variables
    vr = sympy.symbols("x1 x2 x3 x4 x5")
    # Create an objective row as a SymEquation
    obj_row = SymEquation(4*vr[1] + 3*vr[0] + 2*vr[3] -10*vr[4])
    # Create the first constraint on the given LPP.
    row_1 = SymEquation((vr[1] + vr[2] <= 10))

    # Create some simple constraints to ensure the LPP can be converted
    std_const = []
    for var in vr:
        std_const.append(SymEquation(var >= 0))

    # Create the LPP class
    test = SimpleLPP(obj_row, [row_1]+std_const,True, sysoutPrinter.SysoutPrinter())

    # Use a compacted output method to print out the LPP in text.
    test.compacted_output()

    # Now testing of conversion to canonical form
    converter = SimpleConverter(test)
    canon = converter.convert_to_canonical()
    canon.compacted_output()

    # we can see that U-1 has been added to the list of variables
    v = canon.get_variables()

    table = converter.generate_tableau(SimpleTableau)
    table.output()
    print(v)
    #print(canon.get_objective().get_array_form(v))
    # print(canon.get_form())


