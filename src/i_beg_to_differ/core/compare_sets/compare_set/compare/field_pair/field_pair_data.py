from pathlib import Path
from typing import (
    Dict,
    Self,
    ClassVar,
)
from zipfile import ZipFile

from .field_pair import FieldPair
from .....ib2d_file.ib2d_file_element import IB2DFileElement
from .field_pointer import FieldPointer
from .....base import log_exception
from .....data_sources.data_source.field.field_transforms import FieldTransforms
from .compare_rule import CompareRule
from .....wildcards_sets import WildcardSets
from .....extensions.compare_rules import CompareRuleExtensions


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
        source_field_pointer: FieldPointer | str,
        target_field_pointer: FieldPointer | str,
        wildcard_sets: WildcardSets | None = None,
        compare_rule: CompareRule | None = None,
    ):

        FieldPair.__init__(
            self=self,
            source_field_pointer=source_field_pointer,
            target_field_pointer=target_field_pointer,
            wildcard_sets=wildcard_sets,
        )

        IB2DFileElement.__init__(
            self=self,
        )

        if compare_rule is None:
            self.compare_rule = self._compare_rule_extensions['compare_rule_equals']()

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
        # Source
        source_field_name = instance_data['source']['name']

        source_transforms = FieldTransforms.deserialize(
            instance_data=instance_data['source']['transforms'],
            working_dir_path=working_dir_path,
            ib2d_file=ib2d_file,
            wildcard_sets=wildcard_sets,
        )

        source_field_pointer = FieldPointer(
            field_name=source_field_name,
            transforms=source_transforms,
            wildcard_sets=wildcard_sets,
        )

        # Target
        target_field_name = instance_data['target']['name']

        target_transforms = FieldTransforms.deserialize(
            instance_data=instance_data['target']['transforms'],
            working_dir_path=working_dir_path,
            ib2d_file=ib2d_file,
            wildcard_sets=wildcard_sets,
        )

        target_field_pointer = FieldPointer(
            field_name=target_field_name,
            transforms=target_transforms,
            wildcard_sets=wildcard_sets,
        )

        # Compare rule
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
            source_field_pointer=source_field_pointer,
            target_field_pointer=target_field_pointer,
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
                'name': self.source_field_pointer.field_name.base_value,
            }
            | self.source_field_pointer.transforms.serialize(
                ib2d_file=ib2d_file,
            ),
            'target': {
                'name': self.target_field_pointer.field_name.base_value,
            }
            | self.target_field_pointer.transforms.serialize(
                ib2d_file=ib2d_file,
            ),
            'compare_rule': self.compare_rule.serialize(
                ib2d_file=ib2d_file,
            ),
        }

        return instance_data
