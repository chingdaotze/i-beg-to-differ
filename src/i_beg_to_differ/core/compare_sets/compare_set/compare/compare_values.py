from typing import List

from pandas import DataFrame

from .compare_values_unmasked import CompareValuesUnmasked
from .compare_base import AUTO_MATCH
from ....data_sources import DataSources
from .data_source_reference import DataSourceReference
from .field_reference_pair import (
    FieldReferencePairPrimaryKey,
    FieldReferencePairData,
)
from ....wildcards_sets import WildcardSets


class CompareValues(
    CompareValuesUnmasked,
):

    def __init__(
        self,
        source_data_source_ref: DataSourceReference,
        target_data_source_ref: DataSourceReference,
        data_sources: DataSources,
        pk_fields: List[FieldReferencePairPrimaryKey] | None = None,
        dt_fields: List[FieldReferencePairData] | AUTO_MATCH | None = None,
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
    def values_comparison(
        self,
    ) -> DataFrame:

        values_comparison = self.values_comparison_unmasked.copy(
            deep=True,
        )

        values_comparison = self.apply_mask(
            dataframe=values_comparison,
        )

        return values_comparison
