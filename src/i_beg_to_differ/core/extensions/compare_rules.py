from ..compare_sets.compare_set.compare.field_pair.compare_rule import (
    CompareRule,
)
from . import Extensions
from i_beg_to_differ.extensions import compare_rules


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
            namespace_package=compare_rules,
        )
