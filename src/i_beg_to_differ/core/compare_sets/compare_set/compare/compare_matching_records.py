from typing import List

from pandas import (
    DataFrame,
    Series,
)

from .compare_values_unmasked import CompareValuesUnmasked
from .data_source_reference import DataSourceReference
from ....data_sources import DataSources
from .field_reference_pair import (
    FieldReferencePairPrimaryKey,
    FieldReferencePairData,
)
from ....wildcards_sets import WildcardSets


class CompareMatchingRecords(
    CompareValuesUnmasked,
):

    def __init__(
        self,
        source_data_source_ref: DataSourceReference,
        target_data_source_ref: DataSourceReference,
        data_sources: DataSources,
        pk_fields: List[FieldReferencePairPrimaryKey] | None = None,
        dt_fields: List[FieldReferencePairData] | None = None,
        wildcard_sets: WildcardSets | None = None,
    ):

        CompareValuesUnmasked.__init__(
            self=self,
            source_data_source_ref=source_data_source_ref,
            target_data_source_ref=target_data_source_ref,
            data_sources=data_sources,
            pk_fields=pk_fields,
            dt_fields=dt_fields,
            wildcard_sets=wildcard_sets,
        )

    @property
    def matching_records(
        self,
    ) -> DataFrame:

        matching_records = self.values_comparison_unmasked.copy(
            deep=True,
        )

        keep_rows = Series(
            data=True,
            index=matching_records.index,
        )

        for field_pair in self.dt_fields:
            diff_values = matching_records[field_pair]['diff']
            keep_rows = keep_rows & diff_values

        matching_records = matching_records[keep_rows]

        matching_records = self.apply_mask(
            dataframe=matching_records,
        )

        return matching_records
