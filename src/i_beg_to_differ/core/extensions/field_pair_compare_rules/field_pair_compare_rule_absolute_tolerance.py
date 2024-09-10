from pathlib import Path
from typing import (
    Dict,
    Self,
)
from zipfile import ZipFile

from pandas import Series

from ...compare_sets.compare_set.compare.field_pair.field_pair_compare_rule import (
    FieldPairCompareRule,
)
from ...wildcards_sets.wildcard_field import WildcardField
from ...wildcards_sets import WildcardSets
from ...base import (
    log_exception,
    log_runtime,
)


class FieldCompareRuleAbsoluteTolerance(
    FieldPairCompareRule,
):

    _tolerance: WildcardField

    extension_name = 'Absolute Tolerance'

    def __init__(
        self,
        tolerance: float | str = 0.0,
        wildcard_sets: WildcardSets | None = None,
    ):

        FieldPairCompareRule.__init__(
            self=self,
        )

        self._tolerance = WildcardField(
            base_value=str(tolerance),
            wildcard_sets=wildcard_sets,
        )

    def __str__(
        self,
    ) -> str:

        return f'{self.extension_name}: {self.tolerance}'

    @property
    @log_exception
    def tolerance(
        self,
    ) -> float:
        """
        Absolute tolerance.

        :return: Absolute tolerance.
        """

        return float(
            self._tolerance,
        )

    @log_exception
    @log_runtime
    def compare(
        self,
        source_field: Series,
        target_field: Series,
    ) -> Series:
        """
        Compares values between source and target fields, using strict equality.

        :param source_field: Source field to compare.
        :param target_field: Target field to compare.
        :return: Series of booleans, where True indicates a match.
        """

        # TODO: Implement compare

        pass

    @classmethod
    @log_exception
    def deserialize(
        cls,
        instance_data: Dict,
        working_dir_path: Path,
        ib2d_file: ZipFile,
        wildcard_sets: WildcardSets | None = None,
    ) -> Self:

        return FieldCompareRuleAbsoluteTolerance(
            tolerance=instance_data['parameters']['tolerance'],
            wildcard_sets=wildcard_sets,
        )

    @log_exception
    def serialize(
        self,
        ib2d_file: ZipFile,
    ) -> Dict:

        return {
            'extension_id': self,
            'parameters': {
                'tolerance': self._tolerance.base_value,
            },
        }
