from ..registered_types import RegisteredTypes
from .field_transform import FieldTransform


class FieldTransforms[FieldTransform](
    RegisteredTypes,
):
    """
    Contains and manages all FieldTransform types for this package.
    """

    def __init__(
        self,
    ):
        RegisteredTypes.__init__(
            self=self,
        )
