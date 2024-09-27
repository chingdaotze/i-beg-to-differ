from pathlib import Path
from typing import (
    Dict,
    Self,
    ClassVar,
)
from zipfile import ZipFile

from .....ib2d_file.ib2d_file_element import IB2DFileElement
from .field_pair import FieldPair
from .....base import log_exception
from .....data_sources.data_source.field.field_transforms import FieldTransforms
from .compare_rule import CompareRule
from .....extensions.compare_rules.compare_rule_equals import (
    CompareRuleEquals,
)
from .....wildcards_sets import WildcardSets
from .....extensions.compare_rules import CompareRuleExtensions
from .....wildcards_sets.wildcard_field import WildcardField


class FieldPairData(
    FieldPair,
    IB2DFileElement,
):
    """
    Pair of data fields for comparison. Also links a comparison rule to
    the field pair.
    """

    compare_rule: CompareRule
    """
    Comparison rule used to compare the source and target fields.
    """

    _compare_rule_extensions: ClassVar[CompareRuleExtensions] = CompareRuleExtensions()

    def __init__(
        self,
        source_field: str | WildcardField,
        target_field: str | WildcardField,
        source_transforms: FieldTransforms | None = None,
        target_transforms: FieldTransforms | None = None,
        compare_rule: CompareRule | None = None,
        wildcard_sets: WildcardSets | None = None,
    ):

        FieldPair.__init__(
            self=self,
            source_field=source_field,
            target_field=target_field,
            source_transforms=source_transforms,
            target_transforms=target_transforms,
            wildcard_sets=wildcard_sets,
        )

        IB2DFileElement.__init__(
            self=self,
        )

        if compare_rule is None:
            self.compare_rule = CompareRuleEquals()

        else:
            self.compare_rule = compare_rule

    @classmethod
    @log_exception
    def deserialize(
        cls,
        instance_data: Dict,
        working_dir_path: Path,
        ib2d_file: ZipFile,
        wildcard_sets: WildcardSets | None = None,
    ) -> Self:

        source_field = instance_data['source']['name']
        source_transforms = FieldTransforms.deserialize(
            instance_data=instance_data['source']['transforms'],
            working_dir_path=working_dir_path,
            ib2d_file=ib2d_file,
            wildcard_sets=wildcard_sets,
        )

        target_field = instance_data['target']['name']
        target_transforms = FieldTransforms.deserialize(
            instance_data=instance_data['target']['transforms'],
            working_dir_path=working_dir_path,
            ib2d_file=ib2d_file,
            wildcard_sets=wildcard_sets,
        )

        compare_rule = cls._compare_rule_extensions[
            instance_data['compare_rule']['extension_id']
        ]

        compare_rule = compare_rule.deserialize(
            instance_data=instance_data['compare_rule'],
            working_dir_path=working_dir_path,
            ib2d_file=ib2d_file,
            wildcard_sets=wildcard_sets,
        )

        instance = FieldPairData(
            source_field=source_field,
            source_transforms=source_transforms,
            target_field=target_field,
            target_transforms=target_transforms,
            compare_rule=compare_rule,
        )

        return instance

    @log_exception
    def serialize(
        self,
        ib2d_file: ZipFile,
    ) -> Dict:

        instance_data = {
            'source': {
                'name': self.source_field.base_value,
            }
            | self.source_transforms.serialize(
                ib2d_file=ib2d_file,
            ),
            'target': {
                'name': self.target_field.base_value,
            }
            | self.target_transforms.serialize(
                ib2d_file=ib2d_file,
            ),
            'compare_rule': self.compare_rule.serialize(
                ib2d_file=ib2d_file,
            ),
        }

        return instance_data
