"""
Contains definition of the FieldTransformExtensions class.
"""

from i_beg_to_differ.extensions import field_transforms
from . import Extensions


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
