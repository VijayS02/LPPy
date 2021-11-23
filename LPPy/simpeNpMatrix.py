import numbers
from fractions import Fraction
from typing import Tuple
import numpy.ma as ma
import numpy as np

CELL_SIZE = 10
"""
DISCLAIMER:-----------------------------------------------------------------------------------------------------
This is a scratch messy version of the rest of this program. I initially wrote this to test out the idea and see 
the viability of the program.
"""

class Tableau:
    basics: np.array
    table: np.array
    pivot: Tuple[int, int]
    theta_ratios = []

    def __init__(self, table, basics):
        """

        :param table:
        :param basics: the i's for which X_i is a basic variable
        NOTE THAT THIS FUNCTION AUTOMATICALLY Subtracts 1 from the basics to make it an index.
        """
        for i in range(len(table)):
            tmp_data = []
            for x in table[i]:
                if isinstance(x, numbers.Number):
                    tmp_data.append(Fraction(x))
                else:
                    tmp_data.append(x)
            table[i] = tmp_data

        self.table = table
        self.basics = np.array(basics) - 1
        self.pivot = (-1, -1)

        self.changing_vars = [-1, -1]

    def find_pivot(self):
        raw = self.table[-1][:-1]
        # masked = ma.masked_where(type(raw) != float, raw)
        masked2 = ma.masked_where(raw == 0, raw)
        lowest_col = np.argmin(masked2)
        column_vals = self.table[:, lowest_col][:-1]
        # Modify to only account for positive values
        r = 0
        store = []
        for value in column_vals:
            if value > 0:
                store.append(self.table[r][-1] / value)
            else:
                store.append(np.Infinity)
            r += 1
        pivot_row = np.argmin(store)
        self.theta_ratios = store

        pivot = (pivot_row, lowest_col)
        self.pivot = pivot

        pcol = pivot[1]
        prow = pivot[0]

        self.changing_vars[0] = self.basics[prow]
        self.changing_vars[1] = pcol
        return pivot

    def row_reduce(self):
        if self.pivot == (-1, -1):
            self.find_pivot()
        pivot = self.pivot

        pcol = pivot[1]
        prow = pivot[0]
        self.basics[prow] = pcol

        new_r = self.table[prow] / self.table[prow][pcol]
        self.table[prow] = new_r
        for row in range(len(self.table)):
            if row != prow:
                mult = self.table[row][pcol] / self.table[prow][pcol]
                self.table[row] = self.table[row] - mult * self.table[prow]
        self.pivot = (-1, -1)

    def latex_row(self, row, basic, i=-1):
        if basic != "":
            print(f"x_{basic} & ", end='')
        else:
            print(" & ")
        y = 0
        end_v = " & "
        for elem in row:
            try:
                elem = round(elem, 3)
            except:
                pass

            if y == len(row) - 1:
                end_v = "\\\\\n"

            if i == self.pivot[0] and y == self.pivot[1]:
                start = "{\\textit{"
                print(f"\\textbf{start + latex_cleaner(elem) + '}}'}", end=end_v)
            else:
                print(f"{latex_cleaner(elem)} ", end=end_v)
            y += 1

    def latex_print(self):
        print("\\\\")

        len_x = len(table[0])
        b = ""
        cols = '|'.join(["c"] * (len_x + 1))

        print("\\begin{center}\\begin{tabular}{ " + cols + " } ")

        print(b, end=" & ")

        for i in range(len_x - 1):
            if i == len_x - 2:
                print(f"{'x_' + str(i + 1)}", end='\\\\\n')
            else:
                print(f"{'x_' + str(i + 1)}", end=' & ')

        print("\hline")

        i = 0
        for row in table[:-1]:
            self.latex_row(row, self.basics[i] + 1, i=i)
            i += 1

        print("\hline")

        self.latex_row(table[-1], "")
        print("\\end{tabular}\\end{center}")

    def print_row(self, row, basic, i=-1):
        print(f"{basic:^{CELL_SIZE}}", end='')
        y = 0
        for elem in row:
            try:
                elem = round(elem, 3)
            except:
                pass

            if i == self.pivot[0] and y == self.pivot[1]:
                print(f"{'|' + str(elem) + '|':^{CELL_SIZE}}", end='')
            else:
                print(f"{str(elem):^{CELL_SIZE}}", end='')
            y += 1
        # if i != -1:
        # print(f"{str(self.theta_ratios[i]):^{CELL_SIZE}}", end='')

    def print(self):
        print("\n\nTABLEAU:")
        len_x = len(table[0])
        b = "Basic"
        print(b.center(10), end="")
        for i in range(len_x - 1):
            print(f"{'x' + str(i + 1):^{CELL_SIZE}}", end='')

        print("\n", "-" * (10 * (len_x + 1)))
        i = 0
        for row in table[:-1]:
            self.print_row(row, self.basics[i] + 1, i=i)
            print()
            i += 1
        print("-" * (10 * (len_x + 1)))
        self.print_row(table[-1], "-")
        print()

    def latex_solve(self):
        while not all([x >= 0 for x in self.table[-1]]):
            # for i in range(3):
            # try:
            self.find_pivot()
            # except Exception as e:
            # print(e)
            # break
            self.latex_print()
            print("\\\\")
            print("$\Theta$ ratios = \\begin{bmatrix} ")
            for val in self.theta_ratios:
                print(val, end="\\\\")
            print()
            print("\\end{bmatrix}")
            print(
                f"Departing variable: $x_{self.changing_vars[0] + 1}$, incoming variable: $x_{self.changing_vars[1] + 1}$")
            self.row_reduce()
            print("\\\\Tablaeu after row reduction:\\\\")
            self.latex_print()

    def solve(self):
        while not all([x >= 0 for x in self.table[-1]]):
            try:
                self.find_pivot()
            except:
                break
            self.print()
            print(
                f"Departing variable: x_{self.changing_vars[0] + 1}, incoming variable: x_{self.changing_vars[1] + 1}")
            self.row_reduce()
            self.print()


def latex_cleaner(elem):
    stri = str(elem)
    stri = stri.replace("*", '\\cdot ')
    return stri


def original_cost_to_new(original_cost, observed_cost):
    # Make the entries of the basic variables 0 on the cost row
    raise NotImplementedError


if __name__ == "__main__":
    # x = symbols("x")
    # row_1 = np.array([1.0,1.0,x,0.0,12.0])
    # row_2 = np.array([2.0, 1.0, 0.0, 1.0, 16.0])
    # obj_row = np.array([-40.0,-30.0,0.0,0.0,0.0])

    # row1 = np.array([1, 1, 1, 1, 0, 8], dtype=float)
    # row2 = np.array([1, 0, 0, 0, 1, 4], dtype=float)
    # obj = np.array([-5, 1, -3, 0, 0, 0], dtype=float)

    row1 = np.array([2, 4, 1, 1, 0, 12], dtype=float)
    row2 = np.array([1, 0, 0, 0, 1, 3], dtype=float)
    obj = np.array([1, -5, -4, 0, 0, 0], dtype=float)

    # Question 4
    # row1 = np.array([1, 2, 1,0, 8], dtype=float)
    # row2 = np.array([3, -1, 0, 1, 3], dtype=float)
    # obj = np.array([4, -1, 0, 0, 0], dtype=float)

    # Question 6
    # row1 = np.array([2, 1, 4, 1,1,0,0,300], dtype=float)
    # row2 = np.array([4,1,1,1,0,1,0,500], dtype=float)
    # row3 = np.array([3,2,5,1,0,0,1,200], dtype=float)
    # obj = np.array([-4,-11,-15,-3,0,0,0,0], dtype=float)
    # a = symbols("a")
    # b = symbols("b")
    # row1 = np.array([1,1,1], dtype=float)
    # row2 = np.array([1, 0, 0, 1, 0, 1], dtype=float)
    # row3 = np.array([0,1, 0, 0, 1, 1], dtype=float)
    # obj = np.array([-(a-b), 0.0, 0.0])
    table = np.array([row1, row2, obj])
    t = Tableau(table, [4, 5])
    # t.latex_print()
    t.print()
    t.latex_solve()
