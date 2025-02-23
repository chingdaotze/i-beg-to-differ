"""
Contains definition of the FieldTransformReplaceNullWithNumber class.
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
from i_beg_to_differ.core.extensions.ui import WildcardInputField
from i_beg_to_differ.core.wildcards_sets import WildcardSets


class FieldTransformReplaceNullWithNumber(
    FieldTransform,
):
    """
    Field transform that replaces NULL in a column with a number.
    """

    _replacement_value: WildcardInputField

    extension_name = "Replace Null with Number"

    def __init__(
        self,
        replacement_value: float | str = 0.0,
        wildcard_sets: WildcardSets | None = None,
    ):

        FieldTransform.__init__(
            self=self,
        )

        self._replacement_value = WildcardInputField(
            base_value=str(
                replacement_value,
            ),
            wildcard_sets=wildcard_sets,
            title='Replacement Value',
        )

    def __str__(
        self,
    ) -> str:

        return f'{self.extension_name}: {self._replacement_value.base_value}'

    @property
    def replacement_value(
        self,
    ) -> float:
        """
        Absolute tolerance.

        :return: Absolute tolerance.
        """

        return float(
            str(
                self._replacement_value,
            )
        )

    def transform(
        self,
        values: Series,
    ) -> Series:
        """
        Transforms values in a single Field.

        :param values: Values to transform.
        :return: Transformed values.
        """

        values = values.fillna(
            value=self.replacement_value,
        )

        return values

    @classmethod
    def deserialize(
        cls,
        instance_data: Dict,
        working_dir_path: Path,
        ib2d_file: ZipFile,
        wildcard_sets: WildcardSets | None = None,
    ) -> Self:

        return FieldTransformReplaceNullWithNumber(
            replacement_value=instance_data['parameters']['replacement_value'],
            wildcard_sets=wildcard_sets,
        )

    def serialize(
        self,
        ib2d_file: ZipFile,
    ) -> Dict:

        return {
            'extension_id': self.get_extension_id(),
            'parameters': {
                'replacement_value': self._replacement_value.base_value,
            },
        }
