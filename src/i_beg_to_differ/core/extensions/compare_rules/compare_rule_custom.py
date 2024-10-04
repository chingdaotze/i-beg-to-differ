from pathlib import Path
from typing import (
    Dict,
    Self,
)
from zipfile import ZipFile

from pandas import Series

from ...compare_sets.compare_set.compare.field_pair.compare_rule import (
    CompareRule,
)
from ...wildcards_sets import WildcardSets
from ...base import log_exception


class CompareRuleCustom(
    CompareRule,
):

    file_name: str
    _wildcard_sets: WildcardSets | None

    extension_name = 'Custom Python Script'

    def __init__(
        self,
        file_name: str,
        wildcard_sets: WildcardSets | None = None,
    ):

        CompareRule.__init__(
            self=self,
        )

        self.file_name = file_name
        self._wildcard_sets = wildcard_sets

    def __str__(
        self,
    ) -> str:

        return f'{self.extension_name}: {self.file_name}'

    def compare(
        self,
        source_field: Series,
        target_field: Series,
    ) -> Series:
        """
        Compares values between source and target fields, using strict equality.

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

        return CompareRuleCustom(
            file_name=instance_data['parameters']['file_name'],
            wildcard_sets=wildcard_sets,
        )

    @log_exception
    def serialize(
        self,
        ib2d_file: ZipFile,
    ) -> Dict:

        return {
            'extension_id': self.extension_id,
            'parameters': {
                'file_name': self.file_name,
            },
        }
