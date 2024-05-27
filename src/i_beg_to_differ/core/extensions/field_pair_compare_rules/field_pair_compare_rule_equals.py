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


class FieldCompareRuleEquals(
    FieldPairCompareRule,
):

    def __init__(
        self,
        working_dir_path: Path,
        linkage: FieldPairCompareRuleLinkage,
    ):

        FieldPairCompareRule.__init__(
            self=self,
            working_dir_path=working_dir_path,
            extension_id='eeb407c8-de62-42ad-ab32-3532cd428f6a',
            extension_name='Equals',
            linkage=linkage,
        )

    def compare(
        self,
        raw_table: DataFrame,
        transformed_table: DataFrame,
        source_field: Series,
        target_field: Series,
    ) -> Series[bool]:
        """
        Compares values between source and target fields, using strict equality.

        :param raw_table: Read-only copy of the original table.
        :param transformed_table: Read-only copy of the transformed table.
        :param source_field: Source field to compare.
        :param target_field: Target field to compare.
        :return: Series of booleans, where True indicates a match.
        """

        # TODO: Implement compare

        pass

    @classmethod
    def deserialize(
        cls,
        instance_data: Dict,
        working_dir_path: Path,
        ib2d_file: ZipFile,
        wildcard_sets: WildcardSets | None = None,
    ) -> Self:

        return FieldCompareRuleEquals(
            working_dir_path=working_dir_path,
            linkage=FieldPairCompareRuleLinkage(
                instance_data['parameters']['linkage'],
            ),
        )

    def serialize(
        self,
        ib2d_file: ZipFile,
    ) -> Dict:

        return {
            'extension_id': str(self),
            'parameters': None,
            'linkage': str(self.linkage),
        }