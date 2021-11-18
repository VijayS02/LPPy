EQ = "="
LEQ = "<="
GEQ = ">="
NEQ = "!="
GE = ">"
LE = "<"
EEQ = "=="


class Equation:
    def get_array_form(self, mask):
        # Note that this only gets the array form of the LHS of the equation.
        raise NotImplementedError

    def get_type(self):
        raise NotImplementedError

    def get_lhs(self):
        raise NotImplementedError

    def get_rhs(self):
        raise NotImplementedError

    def substitute(self, old_vars, new_vars):
        raise NotImplementedError

    def __str__(self):
        raise NotImplementedError

    def get_vars(self):
        raise NotImplementedError

    def set_type(self, mode):
        raise NotImplementedError

    def add_slack_variable(self, variables):
        raise NotImplementedError

    def __neg__(self):
        raise NotImplementedError
