from enum import StrEnum
from pathlib import Path
from typing import (
    Dict,
    Self,
)
from zipfile import ZipFile

from pandas import Series

from i_beg_to_differ.core.compare_sets.compare_set.compare.field_reference_pair.compare_rule import (
    CompareRule,
)
from i_beg_to_differ.core.input_fields.wildcard_input_fields import WildcardInputField
from i_beg_to_differ.core.input_fields.input_field_options import (
    StaticInputFieldOptions,
)
from i_beg_to_differ.core.extensions.extension import DataType
from i_beg_to_differ.core.wildcards_sets import WildcardSets
from i_beg_to_differ.core.base import log_exception


class DiffMode(
    StrEnum,
):
    PERCENT = 'percent'
    SUBTRACTION = 'subtraction'


class NumericMode(
    StrEnum,
):
    ABSOLUTE = 'absolute'
    REAL = 'real'


class CompareRuleNumericTolerance(
    CompareRule,
):

    _tolerance: WildcardInputField
    _numeric_mode: WildcardInputField
    _diff_mode: WildcardInputField

    extension_name = 'Numeric Tolerance'
    data_type = DataType.NUMERIC

    def __init__(
        self,
        tolerance: float | str = 0.0,
        diff_mode: str | DiffMode = DiffMode.SUBTRACTION,
        numeric_mode: str | NumericMode = NumericMode.REAL,
        wildcard_sets: WildcardSets | None = None,
    ):

        CompareRule.__init__(
            self=self,
        )

        self._tolerance = WildcardInputField(
            base_value=str(tolerance),
            title='Tolerance',
            wildcard_sets=wildcard_sets,
        )

        self._diff_mode = WildcardInputField(
            base_value=diff_mode,
            title='Difference Mode: ',
            wildcard_sets=wildcard_sets,
            options=StaticInputFieldOptions(
                options=list(
                    DiffMode,
                ),
            ),
        )

        self._numeric_mode = WildcardInputField(
            base_value=numeric_mode,
            title='Numeric Mode: ',
            wildcard_sets=wildcard_sets,
            options=StaticInputFieldOptions(
                options=list(
                    NumericMode,
                ),
            ),
        )

    def __str__(
        self,
    ) -> str:

        return (
            f'{self.extension_name}: '
            f'{self.tolerance} | '
            f'{self.diff_mode} | '
            f'{self.numeric_mode}'
        )

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

    @property
    @log_exception
    def diff_mode(
        self,
    ) -> DiffMode:
        """
        Difference mode that informs how differences between the source and target are calculated.

        :return: Difference mode.
        """

        return DiffMode(
            str(
                self._diff_mode,
            ),
        )

    @property
    @log_exception
    def numeric_mode(
        self,
    ) -> NumericMode:
        """
        Numeric mode that informs how differences between the source and target are interpreted.

        :return: Numeric mode.
        """

        return NumericMode(
            str(
                self._numeric_mode,
            ),
        )

    def compare(
        self,
        source_field: Series,
        target_field: Series,
    ) -> Series:
        """
        Compares values between source and target fields, using a numeric tolerance.

        :param source_field: Source field to compare.
        :param target_field: Target field to compare.
        :return: Series of booleans, where True indicates a match.
        """

        # Diff mode
        if self.diff_mode == DiffMode.SUBTRACTION:
            diff = source_field - target_field

        elif self.diff_mode == DiffMode.PERCENT:
            diff = (source_field / target_field) - 1.0

        else:
            raise NotImplementedError(
                f'{self.diff_mode} is not a recognized diff mode for diffing!',
            )

        # Numeric mode
        if self.numeric_mode == NumericMode.REAL:
            pass

        elif self.numeric_mode == NumericMode.ABSOLUTE:
            diff = abs(
                diff,
            )

        else:
            raise NotImplementedError(
                f'{self.numeric_mode} is not a recognized numeric mode for diffing!',
            )

        # Do compare
        result = diff <= self.tolerance

        return result

    @classmethod
    @log_exception
    def deserialize(
        cls,
        instance_data: Dict,
        working_dir_path: Path,
        ib2d_file: ZipFile,
        wildcard_sets: WildcardSets | None = None,
    ) -> Self:

        return CompareRuleNumericTolerance(
            tolerance=instance_data['parameters']['tolerance'],
            diff_mode=instance_data['parameters']['diff_mode'],
            numeric_mode=instance_data['parameters']['numeric_mode'],
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
                'tolerance': self._tolerance.base_value,
                'diff_mode': self._diff_mode.base_value,
                'numeric_mode': self._numeric_mode.base_value,
            },
        }
