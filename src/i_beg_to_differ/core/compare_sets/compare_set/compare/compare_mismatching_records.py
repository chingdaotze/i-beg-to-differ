from typing import List

from pandas import (
    DataFrame,
    Series,
)

from .compare_values_unmasked import CompareValuesUnmasked
from .compare_base import AUTO_MATCH
from .data_source_reference import DataSourceReference
from .field_reference_pair import (
    FieldReferencePairPrimaryKey,
    FieldReferencePairData,
)
from ....wildcards_sets import WildcardSets


class CompareMismatchingRecords(
    CompareValuesUnmasked,
):

    def __init__(
        self,
        source_data_source_ref: DataSourceReference,
        target_data_source_ref: DataSourceReference,
        pk_fields: List[FieldReferencePairPrimaryKey] | None = None,
        dt_fields: List[FieldReferencePairData] | AUTO_MATCH | None = None,
        wildcard_sets: WildcardSets | None = None,
    ):

        CompareValuesUnmasked.__init__(
            self=self,
            source_data_source_ref=source_data_source_ref,
            target_data_source_ref=target_data_source_ref,
            pk_fields=pk_fields,
            dt_fields=dt_fields,
            wildcard_sets=wildcard_sets,
        )

    @property
    def mismatching_records(
        self,
    ) -> DataFrame:

        mismatching_records = self.values_comparison_unmasked.copy(
            deep=True,
        )

        keep_rows = Series(
            data=False,
            index=mismatching_records.index,
        )

        for field_pair in self.dt_fields:
            diff_values = mismatching_records[field_pair]['diff']
            keep_rows = keep_rows | ~diff_values

        mismatching_records = mismatching_records[keep_rows]

        for field_pair in self.dt_fields:
            mismatching_records[field_pair]['diff'] = mismatching_records[field_pair][
                'diff'
            ].replace(
                to_replace={
                    True: '',
                    False: '*',
                },
            )

        return mismatching_records
