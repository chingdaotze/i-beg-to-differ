from typing import ClassVar

from .field_reference_pair import FieldReferencePair
from .....data_sources.data_source.field.field_transforms import FieldTransforms
from .....wildcards_sets import WildcardSets
from .compare_rule import CompareRule
from .....extensions.compare_rules import CompareRuleExtensions


class FieldReferencePairData(
    FieldReferencePair,
):
    """
    Pair of primary key references for aligning data fields.
    """

    _compare_rule_extensions: ClassVar[CompareRuleExtensions] = CompareRuleExtensions()

    def __init__(
        self,
        source_field_name: str,
        target_field_name: str,
        source_field_transforms: FieldTransforms | None = None,
        target_field_transforms: FieldTransforms | None = None,
        wildcard_sets: WildcardSets | None = None,
        compare_rule: CompareRule | None = None,
    ):

        FieldReferencePair.__init__(
            self=self,
            source_field_name=source_field_name,
            target_field_name=target_field_name,
            source_field_transforms=source_field_transforms,
            target_field_transforms=target_field_transforms,
            wildcard_sets=wildcard_sets,
        )

        if compare_rule is None:
            self.compare_rule = self._compare_rule_extensions['compare_rule_equals']()

        else:
            self.compare_rule = compare_rule
