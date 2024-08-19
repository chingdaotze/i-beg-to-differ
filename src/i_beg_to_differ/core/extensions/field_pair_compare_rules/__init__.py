from ...compare_sets.compare_set.compare.field_pair.field_pair_compare_rule import (
    FieldPairCompareRule,
)
from .. import Extensions


class FieldPairCompareRuleExtensions[FieldPairCompareRule](
    Extensions,
):
    """
    Contains and manages all FieldPairCompareRule types for this package.
    """

    def __init__(
        self,
    ):
        Extensions.__init__(
            self=self,
            path=__path__,
            name=__name__,
        )
