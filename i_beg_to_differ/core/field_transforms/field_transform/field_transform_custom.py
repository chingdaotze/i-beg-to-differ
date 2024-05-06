from pathlib import Path
from typing import Callable

from pandas import (
    DataFrame,
    Series,
)

from . import FieldTransform
from ...wildcards import Wildcards


class FieldTransformCustom(
    FieldTransform,
):

    def __init__(
        self,
        working_dir_path: Path,
        name: str,
        transform_func: Callable[
            [
                DataFrame,
                DataFrame,
                Series,
            ],
            Series,
        ],
        wildcards: Wildcards | None = None,
    ):

        FieldTransform.__init__(
            self=self,
            working_dir_path=working_dir_path,
            name=name,
            wildcards=wildcards,
        )

        self.transform = transform_func

    def transform(
        self,
        raw_table: DataFrame,
        transformed_table: DataFrame,
        field: Series,
    ) -> Series:
        """
        Placeholder transform function, to be overridden on class init.

        :param raw_table: Read-only copy of the original table.
        :param transformed_table: Read-only copy of the transformed table.
        :param field: Values to transform.
        :return: Transformed values.
        """