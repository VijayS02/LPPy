from Abstract.equation import Equation


class OutputHandler:
    def write_eq(self, constraint: Equation):
        raise NotImplementedError

    def write(self, output):
        raise NotImplementedError

    def write_tableau(self, table, variables, basic=None, pivot=None):
        raise NotImplementedError
