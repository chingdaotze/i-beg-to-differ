from .. import Extensions
from ...compare_sets.compare_set.compare.field_pair.field.field_transform import (
    FieldTransform,
)


class FieldTransforms[FieldTransform](
    Extensions,
):
    """
    Contains and manages all DataSource types for this package.
    """

    def __init__(
        self,
    ):
        Extensions.__init__(
            self=self,
        )

        # TODO: Load all extensions
