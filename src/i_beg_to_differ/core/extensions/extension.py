class Extension:
    """
    Base class for an IB2D extension.
    """

    extension_id: str
    """
    Unique identifier for this extension.
    """

    def __init__(
        self,
        extension_id: str,
    ):

        self.extension_id = extension_id
