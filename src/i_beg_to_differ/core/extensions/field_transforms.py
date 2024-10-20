from ..data_sources.data_source.field.field_transforms.field_transform import (
    FieldTransform,
)
from . import Extensions
from i_beg_to_differ.extensions import field_transforms


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
            namespace_package=field_transforms,
        )
