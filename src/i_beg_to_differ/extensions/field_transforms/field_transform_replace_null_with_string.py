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
from i_beg_to_differ.core.base import log_exception


class FieldTransformReplaceNullWithString(
    FieldTransform,
):

    replacement_value: WildcardInputField
    """
    Replacement value for null value.
    """

    extension_name = 'Replace Null with String'

    def __init__(
        self,
        replacement_value: str = '',
        wildcard_sets: WildcardSets | None = None,
    ):

        FieldTransform.__init__(
            self=self,
        )

        self.replacement_value = WildcardInputField(
            base_value=replacement_value,
            wildcard_sets=wildcard_sets,
            title='Replacement Value',
        )

    def __str__(
        self,
    ) -> str:

        return f'{self.extension_name}: {self.replacement_value.base_value}'

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
            value=str(
                self.replacement_value,
            ),
        )

        return values

    @classmethod
    @log_exception
    def deserialize(
        cls,
        instance_data: Dict,
        working_dir_path: Path,
        ib2d_file: ZipFile,
        wildcard_sets: WildcardSets | None = None,
    ) -> Self:

        return FieldTransformReplaceNullWithString(
            replacement_value=instance_data['parameters']['replacement_value'],
            wildcard_sets=wildcard_sets,
        )

    @log_exception
    def serialize(
        self,
        ib2d_file: ZipFile,
    ) -> Dict:

        return {
            'extension_id': self.get_extension_id(),
            'parameters': {
                'replacement_value': self.replacement_value.base_value,
            },
        }
