import numpy as np
import sympy
from sympy.core.relational import Relational

from Abstract import lpp, equation
from Abstract.converter import Converter
from Abstract.lpp import LPP
from Abstract.outputHandler import OutputHandler
from Abstract.tableau import Tableau
from symEquation import SymEquation


class SimpleConverter(Converter):
    """
    Concrete version of Converter class.
    """

    # The original LPP
    problem: lpp.LPP
    outputter: OutputHandler

    def __init__(self, problem):
        self.problem = problem
        self.outputter = problem.outputter

    def convert_to_canonical(self) -> LPP:
        if self.problem.get_form() == lpp.CANONICAL:
            return self.problem

        new_objective = self.problem.get_objective()
        if not self.problem.get_is_max():
            new_objective = -new_objective
            self.outputter.write("Convert the LPP from minimization to maximization. Generating the following objective"
                                 "function to be maximized:")
            self.outputter.write_eq(new_objective)

        simple, non_simple, _ = self.problem.get_simple_constraints()

        final_constraints = []
        final_constraints += simple

        old_vars = self.problem.get_variables()
        new_vars = []

        for constraint in non_simple:
            if constraint.get_type() != equation.EQ:
                # Add slack variables wherever necessary
                new_const = constraint.add_slack_variable(new_vars + old_vars)
                new_vars += list(set(new_const.get_vars()) - set(old_vars))
                final_constraints.append(new_const)
            else:
                final_constraints.append(constraint)

        new_problem = self.problem.__class__(new_objective, final_constraints, True, self.outputter)
        added_vars = list(set(new_problem.get_variables()) - set(old_vars))

        self.outputter.write_variables(added_vars, "Introducing slack variables.")
        self.problem = new_problem
        return new_problem

    def convert_to_standard(self) -> LPP:
        raise NotImplementedError

    def generate_tableau(self, tableauClass, basic_indexes=None) -> Tableau:

        problem = self.problem
        if not problem.get_form() == lpp.CANONICAL:
            self.outputter.write("In order to generate a tableau, the LPP needs to be in canonical form.")
            problem = self.convert_to_canonical()

        # Do auxiliary stuffs
        simple, non_simple, _ = problem.get_simple_constraints()

        # This just takes the last m variables and sets them as the basic vars
        if not basic_indexes:
            basic_vars = problem.get_variables()[-(len(non_simple)):]
        else:
            variables = problem.get_variables()
            basic_vars = [variables[i] for i in basic_indexes]
        return tableauClass(problem.get_objective(), non_simple, basic_vars, problem.outputter)

    def invert(self) -> LPP:
        new_obj = -self.problem.get_objective()
        self.outputter.write("New objective function")
        self.outputter.write_eq(new_obj)
        self.problem = self.problem.__class__(new_obj, self.problem.get_constraints(), False, self.problem.outputter)
        return self.problem

    def generate_auxiliary(self) -> tuple[LPP, list]:
        assert self.problem.get_form() == lpp.CANONICAL
        self.outputter.write("Create auxiliary problem in order to find tableau.")
        simple, non_simple, _ = self.problem.get_simple_constraints()

        variables = self.problem.get_variables()

        new_vars = []
        new_consts = []

        for const in non_simple:
            try:
                if const.get_rhs() < 0:
                    const = -const
            except:
                print("Cannot determine if rhs is <0")

            new_eq, new_var = const.force_add_slack_variable_return(variables + new_vars)
            new_vars.append(new_var)
            new_consts.append(new_eq)

        new_consts += simple

        for var in new_vars:
            new_consts.append(SymEquation(Relational(var, 0, equation.GEQ)))

        obj_eq = SymEquation(-sum(new_vars))
        subbed_obj = obj_eq
        for i in range(len(new_vars)):
            rearranged_eq = new_consts[i].solve_for(new_vars[i])[0]
            subbed_obj = subbed_obj.substitute(new_vars[i], rearranged_eq)

        self.outputter.write_variables(new_vars, "Create artificial variables")

        self.outputter.write("Create a new objective function from artificial variables.")
        self.outputter.write_eq(obj_eq)
        self.outputter.write("Substitute y's with solved values to eliminate them from the objective.")
        self.outputter.write_eq(subbed_obj)

        self.problem = self.problem.__class__(subbed_obj, new_consts, True, self.problem.outputter)
        return self.problem, new_vars

    def generate_dual(self):
        # This breaks a lot of coding rules but its just for practice.
        self.outputter.write("Now create dual of this primal problem.")
        problem = self.problem
        if problem.get_is_max():
            print("Converting to minimization problem.")
            self.outputter.write("Primal problem must be of type minimization, convert primal to minimization problem.")
            problem = self.invert()

            # raise ValueError("Cannot create dual LPP from maximization problem. "
            #                  "Primal needs to be of type Minimization.")

        simple, non_simple, _ = problem.get_simple_constraints()
        free_variables = problem.get_free_variables()
        table_form = np.array(problem.get_table_form())
        transposed_form = table_form.T

        new_vars = [sympy.symbols(f"p{i}") for i in range(1, len(non_simple) + 1)]
        new_consts = []
        variables = problem.get_variables()
        for i in range(len(variables)):
            variable = variables[i]
            lhs = transposed_form[i][:-1].dot(new_vars)
            mode = equation.EEQ
            if variable not in free_variables:
                for const in simple:
                    if variable in const.get_vars():
                        mode = equation.invert_type(const.get_type())
                        break

            exp = SymEquation(Relational(lhs, transposed_form[i][-1], mode))
            new_consts.append(exp)

        for i in range(len(non_simple)):
            # Trust the order of non_simple (i may not be aligned with Ai
            const = non_simple[i]
            if const.get_type() != equation.EEQ:
                exp = SymEquation(Relational(new_vars[i], 0, const.get_type()))
                new_consts.append(exp)

        # Create new objective: Bt * X
        new_objective = SymEquation(transposed_form[-1].dot(new_vars + [1]))
        self.problem = problem.__class__(new_objective, new_consts, True, problem.outputter)
        return self.problem
