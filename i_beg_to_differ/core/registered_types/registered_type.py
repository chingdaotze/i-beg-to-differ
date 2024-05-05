class RegisteredType:
    """
    Base class for a registered type.
    """

    name: str

    def __init__(
        self,
        name: str,
    ):

        self.name = name
