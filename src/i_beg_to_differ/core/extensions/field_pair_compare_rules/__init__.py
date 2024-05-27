from .. import Extensions
from ...compare_sets.compare_set.compare.field_pair.field_pair_compare_rule import (
    FieldPairCompareRule,
)


class FieldPairCompareRules[FieldPairCompareRule](
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
