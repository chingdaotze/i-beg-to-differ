from pathlib import Path

from pandas import (
    DataFrame,
    Series,
)

from . import CompareRule
from ...wildcards_sets import WildcardSets


class CompareRuleAbsoluteTolerance(
    CompareRule,
):

    tolerance: float
    """
    Absolute tolerance.
    """

    def __init__(
        self,
        working_dir_path: Path,
        tolerance: float,
        wildcards: WildcardSets | None = None,
    ):

        CompareRule.__init__(
            self=self,
            working_dir_path=working_dir_path,
            name="Equals",
            wildcards=wildcards,
        )

        self.tolerance = tolerance

    def compare(
        self,
        raw_table: DataFrame,
        transformed_table: DataFrame,
        source_field: Series,
        target_field: Series,
    ) -> Series[bool]:
        """
        Compares values between source and target fields, using strict equality.

        :param raw_table: Read-only copy of the original table.
        :param transformed_table: Read-only copy of the transformed table.
        :param source_field: Source field to compare.
        :param target_field: Target field to compare.
        :return: Series of booleans, where True indicates a match.
        """

        # TODO: Implement compare

        pass
