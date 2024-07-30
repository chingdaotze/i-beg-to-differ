from .. import Extensions


class FieldTransforms[FieldTransform](
    Extensions,
):
    """
    Contains and manages all FieldTransform types for this package.
    """

    def __init__(
        self,
    ):
        Extensions.__init__(
            self=self,
            path=__path__,
            name=__name__,
        )
