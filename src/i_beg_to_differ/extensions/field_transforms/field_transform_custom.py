from pathlib import Path
from typing import (
    Dict,
    Self,
)
from zipfile import ZipFile
from copy import copy

from pandas import Series

from i_beg_to_differ.core.data_sources.data_source.field.field_transforms.field_transform import (
    FieldTransform,
)
from i_beg_to_differ.core.extensions.extension import CustomPythonExtension
from i_beg_to_differ.core.wildcards_sets import WildcardSets
from i_beg_to_differ.core.base import log_exception


class FieldTransformCustom(
    FieldTransform,
    CustomPythonExtension,
):

    extension_name = 'Custom Python Transform Script'

    def __init__(
        self,
        working_dir_path: Path,
        py_file_name: str | Path | None,
        wildcard_sets: WildcardSets | None = None,
    ):

        FieldTransform.__init__(
            self=self,
        )

        CustomPythonExtension.__init__(
            self=self,
            working_dir_path=working_dir_path,
            extension_func=self.transform,
            py_file_name=py_file_name,
            wildcard_sets=wildcard_sets,
        )

    def __str__(
        self,
    ) -> str:

        return f'{self.extension_name}: {self.py_file_name}'

    def transform(
        self,
        values: Series,
    ) -> Series:
        """
        Transforms values in a single Field.

        :param values: Values to transform.
        :return: Transformed values.
        """

        extension_func = self.get_extension_func()

        return extension_func(
            values=values,
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

        field_transform = FieldTransformCustom(
            working_dir_path=working_dir_path,
            py_file_name=instance_data["parameters"]["py_file_name"],
            wildcard_sets=wildcard_sets,
        )

        field_transform.inflate_py_file(
            ib2d_file=ib2d_file,
        )

        return field_transform

    @log_exception
    def serialize(
        self,
        ib2d_file: ZipFile,
    ) -> Dict:

        self.deflate_py_file(
            ib2d_file=ib2d_file,
        )

        return {
            "extension_id": self.get_extension_id(),
            "parameters": {
                "py_file_name": self.py_file_name,
            },
        }
