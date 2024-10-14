from pathlib import Path
from typing import (
    Dict,
    Self,
)
from zipfile import ZipFile
from copy import copy

from pandas import Series

from ...compare_sets.compare_set.compare.field_pair.compare_rule import (
    CompareRule,
)
from ..custom_python_extension import CustomPythonExtension
from ...wildcards_sets import WildcardSets
from ...base import log_exception


class CompareRuleCustom(
    CompareRule,
    CustomPythonExtension,
):

    extension_name = 'Custom Python Compare Script'

    def __init__(
        self,
        working_dir_path: Path,
        py_file_name: str | Path | None,
        wildcard_sets: WildcardSets | None = None,
    ):

        CompareRule.__init__(
            self=self,
        )

        CustomPythonExtension.__init__(
            self=self,
            working_dir_path=working_dir_path,
            extension_func=self.compare,
            py_file_name=py_file_name,
            wildcard_sets=wildcard_sets,
        )

    def __str__(
        self,
    ) -> str:

        return f'{self.extension_name}: {self.py_file_name}'

    def compare(
        self,
        source_field: Series,
        target_field: Series,
    ) -> Series:
        """
        Compares values between source and target fields, using custom Python code.
        The return value should be a Series of booleans, where True indicates a match
        and False indicates a mismatch.

        :param source_field: Source field to compare.
        :param target_field: Target field to compare.
        :return: Series of booleans, where True indicates a match.
        """

        extension_func = self.get_extension_func()

        return extension_func(
            source_field=source_field,
            target_field=target_field,
            wildcards=(
                copy(self.wildcard_sets.active_wildcard_set.replacement_values)
                if isinstance(self.wildcard_sets, WildcardSets)
                else {}
            ),
        )

    @classmethod
    @log_exception
    def deserialize(
        cls,
        instance_data: Dict,
        working_dir_path: Path,
        ib2d_file: ZipFile,
        wildcard_sets: WildcardSets | None = None,
    ) -> Self:

        compare_rule = CompareRuleCustom(
            working_dir_path=working_dir_path,
            py_file_name=instance_data['parameters']['py_file_name'],
            wildcard_sets=wildcard_sets,
        )

        compare_rule.inflate_py_file(
            ib2d_file=ib2d_file,
        )

        return compare_rule

    @log_exception
    def serialize(
        self,
        ib2d_file: ZipFile,
    ) -> Dict:

        self.deflate_py_file(
            ib2d_file=ib2d_file,
        )

        return {
            'extension_id': self.extension_id,
            'parameters': {
                'py_file_name': self.py_file_name,
            },
        }
