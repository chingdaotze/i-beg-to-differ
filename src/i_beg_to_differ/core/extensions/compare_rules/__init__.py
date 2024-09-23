from ...compare_sets.compare_set.compare.field_pair.compare_rule import (
    CompareRule,
)
from .. import Extensions


class CompareRuleExtensions[CompareRule](
    Extensions,
):
    """
    Contains and manages all CompareRule types for this package.
    """

    def __init__(
        self,
    ):
        Extensions.__init__(
            self=self,
            path=__path__,
            name=__name__,
        )
