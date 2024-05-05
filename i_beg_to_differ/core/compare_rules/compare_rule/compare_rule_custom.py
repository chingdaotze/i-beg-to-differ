from pathlib import Path
from typing import Callable

from pandas import (
    DataFrame,
    Series,
)

from . import CompareRule
from ...wildcards import Wildcards


class CompareRuleCustom(
    CompareRule,
):

    def __init__(
        self,
        working_dir_path: Path,
        name: str,
        compare_func: Callable[
            [
                DataFrame,
                DataFrame,
                Series,
                Series,
            ],
            Series[bool],
        ],
        wildcards: Wildcards | None = None,
    ):

        CompareRule.__init__(
            self=self,
            working_dir_path=working_dir_path,
            name=name,
            wildcards=wildcards,
        )

        self.compare = compare_func

    def compare(
        self,
        raw_table: DataFrame,
        transformed_table: DataFrame,
        source_field: Series,
        target_field: Series,
    ) -> Series[bool]:
        """
        Placeholder compare function, to be overridden on class init.

        :param raw_table: Read-only copy of the original table.
        :param transformed_table: Read-only copy of the transformed table.
        :param source_field: Source field to compare.
        :param target_field: Target field to compare.
        :return: Series of booleans, where True indicates a match.
        """
