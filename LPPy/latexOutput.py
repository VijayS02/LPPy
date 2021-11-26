from typing import List, Tuple

from Abstract.equation import Equation
from Abstract.outputHandler import OutputHandler
import Abstract.equation as e

symbols = {e.GEQ: "&\geq", e.LEQ: "&\leq", e.LE: "&<", e.GE: "&>", e.EEQ: "&=", e.EQ: "&="}


class LatexOutput(OutputHandler):
    inMathMode: bool

    def write_eq(self, constraint: Equation):
        if self.inMathMode:
            string_eq = symbol_replace(str(constraint))
            print(string_eq)
        else:
            string_eq = str(constraint)
            print(f"${string_eq}$")

    def write(self, output: str) -> None:
        print(output)

    def write_tableau(self, table: List[List], variables: List, basic: List = None, pivot: Tuple = None) -> None:
        end_s = " & "
        print("\\\\")
        var_len = len(variables)
        b = ""
        cols = '|'.join(["c"] * (var_len + 2))

        print("\\begin{center}\\begin{tabular}{ " + cols + " } ")

        print(b, end=end_s)

        for var in variables:
            print(str(var), end=end_s)

        print("\hline")
        i = 0
        for row in table[:-1]:
            if basic is not None:
                print(basic[i], end=end_s)
            else:
                print("", end=end_s)
            for val in row:
                print(str(val), end=end_s)
            i += 1
        print("\hline")
        print("", end=end_s)
        for val in table[-1]:
            print(str(val), end=end_s)
        print("\\end{tabular}\\end{center}")

    def start_equation_group(self):
        print("\\begin{align*}")

    def end_equation_group(self):
        print("\\end{align*}")


def symbol_replace(raw: str):
    new_raw = raw
    for symbol in symbols:
        new_raw = new_raw.replace(symbol, symbols[symbol])
    return new_raw
