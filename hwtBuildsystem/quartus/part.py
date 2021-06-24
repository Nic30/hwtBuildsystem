

class IntelPart():
    """
    Intel/Altera FPGA model name specification
    """

    def __init__(self, family:str, device:str):
        self.family = family
        self.device = device

    def as_tuple(self):
        return (
            self.family,
            self.device,
        )

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.as_tuple() == other.as_tuple()

    def __hash__(self):
        return hash(self.as_tuple())

    def __repr__(self):
        return f"<{self.__class__.__name__:s} {self.family:s} {self.device}>"
