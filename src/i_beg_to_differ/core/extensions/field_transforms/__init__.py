from ...data_sources.data_source.field.field_transforms.field_transform import (
    FieldTransform,
)
from .. import Extensions


class FieldTransformExtensions[FieldTransform](
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
