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
from ...base import (
    log_exception,
    log_runtime,
)


class FieldCompareRuleCustom(
    FieldPairCompareRule,
):

    file_name: str
    _wildcard_sets: WildcardSets | None

    extension_name = 'Custom Python Script'

    def __init__(
        self,
        linkage: FieldPairCompareRuleLinkage,
        file_name: str,
        wildcard_sets: WildcardSets | None = None,
    ):

        FieldPairCompareRule.__init__(
            self=self,
            linkage=linkage,
        )

        self.file_name = file_name
        self._wildcard_sets = wildcard_sets

    def __str__(
        self,
    ) -> str:

        return f'{self.extension_name}: {self.file_name}'

    @log_exception
    @log_runtime
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
    @log_exception
    def deserialize(
        cls,
        instance_data: Dict,
        working_dir_path: Path,
        ib2d_file: ZipFile,
        wildcard_sets: WildcardSets | None = None,
    ) -> Self:

        return FieldCompareRuleCustom(
            linkage=FieldPairCompareRuleLinkage(
                instance_data['parameters']['linkage'],
            ),
            file_name=instance_data['parameters']['file_name'],
            wildcard_sets=wildcard_sets,
        )

    @log_exception
    def serialize(
        self,
        ib2d_file: ZipFile,
    ) -> Dict:

        return {
            'extension_id': self,
            'parameters': {
                'file_name': self.file_name,
            },
            'linkage': str(self.linkage),
        }
