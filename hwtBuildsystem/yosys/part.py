

class LatticePart():
    """
    Lattice FPGA model name specification eg. 'Lattice', 'iCE40', 'up5k', 'sg48'
    """

    def __init__(self, family, model, package):
        self.family = family
        self.model = model
        self.package = package

    def as_tuple(self):
        return (
            self.family,
            self.model,
            self.package,
        )

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.as_tuple() == other.as_tuple()

    def __hash__(self):
        return hash(self.as_tuple())

    def __repr__(self):
        return f"<{self.__class__.__name__:s} {self.family:s} {self.model:s} {self.package}>"
