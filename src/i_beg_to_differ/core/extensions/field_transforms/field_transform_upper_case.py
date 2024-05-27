from pathlib import Path

from pandas import (
    DataFrame,
    Series,
)

from . import FieldTransform
from ...wildcards_sets import WildcardSets


class FieldTransformLowerCase(
    FieldTransform,
):

    def __init__(
        self,
        working_dir_path: Path,
        wildcards: WildcardSets | None = None,
    ):

        FieldTransform.__init__(
            self=self,
            working_dir_path=working_dir_path,
            name="Upper Case",
            wildcards=wildcards,
        )

    def transform(
        self,
        raw_table: DataFrame,
        transformed_table: DataFrame,
        field: Series,
    ) -> Series:
        """
        Transforms values in the field to upper case.

        :param raw_table: Read-only copy of the original table.
        :param transformed_table: Read-only copy of the transformed table.
        :param field: Values to transform.
        :return: Transformed values.
        """

        return field.str.upper()
