from Abstract.equation import Equation
from Abstract.outputHandler import OutputHandler


class SysoutPrinter(OutputHandler):
    """
    Simple console outputter version of outputHandler.
    """
    def write_tableau(self, table, variables, basic=None, pivot=None):
        for i in variables:
            print(f"{str(i):^8}", end=" ")
        print()

        for row in table:
            for elem in row:
                print(f"{str(elem):^8}", end=" ")
            print()

    def __init__(self):
        return

    def write_eq(self, eq: Equation):
        print(str(eq))

    def write(self, output):
        print(output)

