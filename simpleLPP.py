from typing import List

from Abstract import equation, lpp
from Abstract.lpp import LPP
from Abstract.equation import Equation
from Abstract.outputHandler import OutputHandler


class SimpleLPP(LPP):
    objective: Equation
    constraints: List[Equation]
    is_max: bool
    variables: List
    outputter: OutputHandler

    def __init__(self, objective, constraints, is_max, outputter):
        var_lst = []
        var_lst += objective.get_vars()
        for const in constraints:
            var_lst += const.get_vars()

        variables = set(var_lst)

        self.variables = list(variables)
        self.outputter = outputter
        self.is_max = is_max

        # TODO: add some sort of testing for the inputs to be in either standard form or canonical form
        self.constraints = constraints
        self.objective = objective

    def get_form(self):
        simp, non_simp, valid = self.get_simple_constraints()
        if valid:
            canonical_bool = all([const.get_type() == equation.EQ for const in non_simp])
            standard_bool = all([const.get_type() == equation.LEQ for const in non_simp])
            if canonical_bool:
                return lpp.CANONICAL
            elif standard_bool:
                return lpp.STANDARD
            else:
                return lpp.UNKNOWN

    def get_free_variables(self) -> List:
        simples = []
        seen = []
        for const in self.constraints:
            valid_type = (const.get_type() == equation.GEQ) or (const.get_type() == equation.LEQ)
            if const.get_rhs() == 0 and valid_type:
                mask = [None] * (len(self.variables) - 1)
                expected = [0] * (len(self.variables) - 1) + [1]
                for var in self.variables:
                    new_mask = mask + [var]
                    if const.get_array_form(new_mask) == expected:
                        simples.append(const)
                        seen.append(var)
                        break
        return [x for x in self.variables if x not in seen]

    def get_simple_constraints(self):
        simples = []
        not_simples = []
        seen = []
        for const in self.constraints:
            added = False
            valid_type = (const.get_type() == equation.GEQ) or (const.get_type() == equation.LEQ)
            if const.get_rhs() == 0 and valid_type:
                mask = [None] * (len(self.variables) - 1)
                expected = [0] * (len(self.variables) - 1) + [1]
                for var in self.variables:
                    new_mask = mask + [var]
                    if const.get_array_form(new_mask) == expected:
                        simples.append(const)
                        seen.append(var)
                        added = True
                        break
            if not added:
                not_simples.append(const)

        return simples, not_simples, all([x in self.variables for x in seen])

    def compacted_output(self):
        if self.is_max:
            self.outputter.write("Maximize:")
        else:
            self.outputter.write("Minimize:")

        self.outputter.write_eq(self.objective)
        self.outputter.write("\nSubject to:")

        simp, non_simp, result = self.get_simple_constraints()
        for const in non_simp:
            self.outputter.write_eq(const)
        self.outputter.write("\nWhere:")
        if result:
            varibs = ','.join([str(x) for x in self.variables])
            self.outputter.write(varibs + " " + equation.GEQ + " 0")
        else:
            for const in simp:
                self.outputter.write_eq(const)

    def output(self):
        if self.is_max:
            self.outputter.write("Maximize:\n")
        else:
            self.outputter.write("Minimize:\n")
        self.outputter.write_eq(self.objective)
        self.outputter.write("\nSubject to:")
        for const in self.constraints:
            self.outputter.write_eq(const)

    def set_objective(self, new_objective: Equation):
        assert all([var in self.variables for var in new_objective.get_vars()])
        self.objective = new_objective

    def get_objective(self):
        return self.objective

    def set_constraints(self, constraints: List[Equation]):
        for const in constraints:
            assert all([var in self.variables for var in const.get_vars()])
        self.constraints = constraints

    def get_constraints(self):
        return self.constraints

    def get_is_max(self):
        return self.is_max

    def set_is_max(self, new_max: bool):
        self.is_max = new_max

    def get_variables(self):
        return sorted(self.variables, key=lambda x: str(x))
