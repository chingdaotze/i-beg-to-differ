from pathlib import Path

from pandas import (
    DataFrame,
    Series,
)

from . import FieldTransform
from ...wildcards import Wildcards


class FieldTransformLowerCase(
    FieldTransform,
):

    def __init__(
        self,
        working_dir_path: Path,
        wildcards: Wildcards | None = None,
    ):

        FieldTransform.__init__(
            self=self,
            working_dir_path=working_dir_path,
            name="Lower Case",
            wildcards=wildcards,
        )

    def transform(
        self,
        raw_table: DataFrame,
        transformed_table: DataFrame,
        field: Series,
    ) -> Series:
        """
        Transforms values in the field to lower case.

        :param raw_table: Read-only copy of the original table.
        :param transformed_table: Read-only copy of the transformed table.
        :param field: Values to transform.
        :return: Transformed values.
        """

        return field.str.lower()
