class Converter:
    def convert_to_canonical(self):
        raise NotImplementedError

    def convert_to_standard(self):
        raise NotImplementedError

    def generate_tableau(self, tableauClass):
        raise NotImplementedError

    def generate_dual(self):
        raise NotImplementedError
