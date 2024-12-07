from pathlib import Path
from typing import (
    ClassVar,
    Dict,
    Union,
    Self,
)
from zipfile import ZipFile

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

    compare_rule_extensions: ClassVar[CompareRuleExtensions] = CompareRuleExtensions()

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
            self.compare_rule = self.compare_rule_extensions['compare_rule_equals']()

        else:
            self.compare_rule = compare_rule

    @classmethod
    def deserialize(
        cls,
        instance_data: Dict,
        working_dir_path: Path,
        ib2d_file: ZipFile,
        wildcard_sets: Union['WildcardSets', None] = None,
    ) -> Self:

        return FieldReferencePairData(
            source_field_name=instance_data['source']['name'],
            target_field_name=instance_data['target']['name'],
            source_field_transforms=FieldTransforms.deserialize(
                instance_data=instance_data['source']['transforms'],
                working_dir_path=working_dir_path,
                ib2d_file=ib2d_file,
                wildcard_sets=wildcard_sets,
            ),
            target_field_transforms=FieldTransforms.deserialize(
                instance_data=instance_data['target']['transforms'],
                working_dir_path=working_dir_path,
                ib2d_file=ib2d_file,
                wildcard_sets=wildcard_sets,
            ),
            wildcard_sets=wildcard_sets,
            compare_rule=cls.compare_rule_extensions[
                instance_data['compare_rule']['extension_id']
            ].deserialize(
                instance_data=instance_data['compare_rule'],
                working_dir_path=working_dir_path,
                ib2d_file=ib2d_file,
                wildcard_sets=wildcard_sets,
            ),
        )

    def serialize(
        self,
        ib2d_file: ZipFile,
    ) -> Dict:

        return {
            'source': {
                'name': self.source_field_ref.field_name.base_value,
            }
            | self.source_field_ref.transforms.serialize(
                ib2d_file=ib2d_file,
            ),
            'target': {
                'name': self.target_field_ref.field_name.base_value,
            }
            | self.target_field_ref.transforms.serialize(
                ib2d_file=ib2d_file,
            ),
            'compare_rule': self.compare_rule.serialize(
                ib2d_file=ib2d_file,
            ),
        }
