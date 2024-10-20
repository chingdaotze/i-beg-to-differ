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
from i_beg_to_differ.core.wildcards_sets.wildcard_field import WildcardField
from i_beg_to_differ.core.wildcards_sets import WildcardSets
from i_beg_to_differ.core.base import log_exception


class FieldTransformReplaceNullWithNumber(
    FieldTransform,
):
    _replacement_value: WildcardField | float

    extension_name = "Replace Null with Number"

    def __init__(
        self,
        replacement_value: float | str = 0.0,
        wildcard_sets: WildcardSets | None = None,
    ):

        FieldTransform.__init__(
            self=self,
        )

        if isinstance(replacement_value, str):
            self._replacement_value = WildcardField(
                base_value=replacement_value,
                wildcard_sets=wildcard_sets,
            )

        else:
            self._replacement_value = replacement_value

    def __str__(
        self,
    ) -> str:

        return self.extension_name

    @property
    @log_exception
    def replacement_value(
        self,
    ) -> float:
        """
        Absolute tolerance.

        :return: Absolute tolerance.
        """

        if isinstance(self._replacement_value, WildcardField):
            return float(
                str(
                    self._replacement_value,
                )
            )

        else:
            return self._replacement_value

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
    @log_exception
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

    @log_exception
    def serialize(
        self,
        ib2d_file: ZipFile,
    ) -> Dict:

        if isinstance(self._replacement_value, WildcardField):
            replacement_value = self._replacement_value.base_value

        else:
            replacement_value = self._replacement_value

        return {
            'extension_id': self.get_extension_id(),
            'parameters': {
                'replacement_value': replacement_value,
            },
        }
