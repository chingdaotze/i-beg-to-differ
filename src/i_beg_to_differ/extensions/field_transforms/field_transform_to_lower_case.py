"""
Contains definition of the FieldTransformToLowerCase class.
"""

from pathlib import Path
from typing import (
    Dict,
    Self,
)
from zipfile import ZipFile

from pandas import Series

from i_beg_to_differ.core.data_sources.data_source.field.field_transforms.field_transform import (
    FieldTransform,
)
from i_beg_to_differ.core.extensions.extension import DataType
from i_beg_to_differ.core.wildcards_sets import WildcardSets


class FieldTransformToLowerCase(
    FieldTransform,
):
    """
    Field transform that normalizes string to lower case.
    """

    extension_name = "Convert to Lower Case"
    data_type = DataType.STRING

    def __init__(
        self,
    ):

        FieldTransform.__init__(
            self=self,
        )

    def __str__(
        self,
    ) -> str:

        return self.extension_name

    def transform(
        self,
        values: Series,
    ) -> Series:
        """
        Transforms string values to lower case.

        :param values: Values to transform.
        :return: Transformed values.
        """

        values = values.str.lower()

        return values

    @classmethod
    def deserialize(
        cls,
        instance_data: Dict,
        working_dir_path: Path,
        ib2d_file: ZipFile,
        wildcard_sets: WildcardSets | None = None,
    ) -> Self:

        return FieldTransformToLowerCase()

    def serialize(
        self,
        ib2d_file: ZipFile,
    ) -> Dict:

        return {
            "extension_id": self.get_extension_id(),
            "parameters": None,
        }
