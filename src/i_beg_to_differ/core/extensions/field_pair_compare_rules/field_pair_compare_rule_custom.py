from pathlib import Path
from typing import (
    Dict,
    Self,
)
from zipfile import ZipFile

from pandas import (
    DataFrame,
    Series,
)

from ...compare_sets.compare_set.compare.field_pair.field_pair_compare_rule import (
    FieldPairCompareRule,
    FieldPairCompareRuleLinkage,
)
from ...wildcards_sets import WildcardSets


class FieldCompareRuleCustom(
    FieldPairCompareRule,
):

    _file_name: str
    _wildcard_sets: WildcardSets | None

    extension_id = '5e932dfc-9d46-485b-8697-b02d850ddad2'
    extension_name = 'Custom'

    def __init__(
        self,
        working_dir_path: Path,
        linkage: FieldPairCompareRuleLinkage,
        file_name: str,
        wildcard_sets: WildcardSets | None = None,
    ):

        FieldPairCompareRule.__init__(
            self=self,
            working_dir_path=working_dir_path,
            linkage=linkage,
        )

        self._file_name = file_name
        self._wildcard_sets = wildcard_sets

    def compare(
        self,
        raw_table: DataFrame,
        transformed_table: DataFrame,
        source_field: Series,
        target_field: Series,
    ) -> Series:
        """
        Compares values between source and target fields, using strict equality.

        :param raw_table: Read-only copy of the original table.
        :param transformed_table: Read-only copy of the transformed table.
        :param source_field: Source field to compare.
        :param target_field: Target field to compare.
        :return: Series of booleans, where True indicates a match.
        """

        # TODO: Load custom file, pass in current active wildcard set.

        pass

    @classmethod
    def deserialize(
        cls,
        instance_data: Dict,
        working_dir_path: Path,
        ib2d_file: ZipFile,
        wildcard_sets: WildcardSets | None = None,
    ) -> Self:

        return FieldCompareRuleCustom(
            working_dir_path=working_dir_path,
            linkage=FieldPairCompareRuleLinkage(
                instance_data['parameters']['linkage'],
            ),
            wildcard_sets=wildcard_sets,
        )

    def serialize(
        self,
        ib2d_file: ZipFile,
    ) -> Dict:

        return {
            'extension_id': str(self),
            'parameters': {
                'file_name': self._file_name,
            },
            'linkage': str(self.linkage),
        }
