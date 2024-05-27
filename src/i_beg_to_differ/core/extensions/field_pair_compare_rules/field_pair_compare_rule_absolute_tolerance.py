from pathlib import Path
from typing import (
    Dict,
    Self,
)
from zipfile import ZipFile

from pandas import (
    DataFrame,
    Series,
)

from ...compare_sets.compare_set.compare.field_pair.field_pair_compare_rule import (
    FieldPairCompareRule,
    FieldPairCompareRuleLinkage,
)
from ...wildcards_sets import WildcardSets
from ...wildcards_sets.wildcard_field import WildcardField


class FieldCompareRuleAbsoluteTolerance(
    FieldPairCompareRule,
):

    _tolerance: WildcardField

    def __init__(
        self,
        working_dir_path: Path,
        linkage: FieldPairCompareRuleLinkage,
        tolerance: float | str = 0.0,
        wildcard_sets: WildcardSets | None = None,
    ):

        FieldPairCompareRule.__init__(
            self=self,
            working_dir_path=working_dir_path,
            extension_id='ec4928d1-a745-49d0-a0db-efaf2ecc3262',
            extension_name='Absolute Tolerance',
            linkage=linkage,
        )

        self._tolerance = WildcardField(
            base_value=str(tolerance),
            wildcard_sets=wildcard_sets,
        )

    @property
    def tolerance(
        self,
    ) -> float:
        """
        Absolute tolerance.

        :return: Absolute tolerance.
        """

        return float(
            self._tolerance.value,
        )

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

    @classmethod
    def deserialize(
        cls,
        instance_data: Dict,
        working_dir_path: Path,
        ib2d_file: ZipFile,
        wildcard_sets: WildcardSets | None = None,
    ) -> Self:

        return FieldCompareRuleAbsoluteTolerance(
            working_dir_path=working_dir_path,
            linkage=FieldPairCompareRuleLinkage(
                instance_data['parameters']['linkage'],
            ),
            tolerance=instance_data['parameters']['tolerance'],
            wildcard_sets=wildcard_sets,
        )

    def serialize(
        self,
        ib2d_file: ZipFile,
    ) -> Dict:

        return {
            'extension_id': str(self),
            'parameters': {
                'tolerance': self._tolerance.base_value,
            },
            'linkage': str(self.linkage),
        }
