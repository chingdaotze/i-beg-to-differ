from pathlib import Path
from typing import (
    Dict,
    Self,
)
from zipfile import ZipFile

from pandas import Series

from i_beg_to_differ.core.compare_sets.compare_set.compare.field_reference_pair.compare_rule import (
    CompareRule,
)
from i_beg_to_differ.core.base import log_exception
from i_beg_to_differ.core.wildcards_sets import WildcardSets


class CompareRuleEquals(
    CompareRule,
):

    extension_name = 'Equals'

    def __init__(
        self,
    ):

        CompareRule.__init__(
            self=self,
        )

    def __str__(
        self,
    ) -> str:

        return self.extension_name

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

        result = source_field == target_field

        return result

    @classmethod
    @log_exception
    def deserialize(
        cls,
        instance_data: Dict,
        working_dir_path: Path,
        ib2d_file: ZipFile,
        wildcard_sets: WildcardSets | None = None,
    ) -> Self:

        return CompareRuleEquals()

    @log_exception
    def serialize(
        self,
        ib2d_file: ZipFile,
    ) -> Dict:

        return {
            'extension_id': self.get_extension_id(),
            'parameters': None,
        }
