from typing import List

from pandas import DataFrame

from .compare_base import (
    CompareBase,
    AUTO_MATCH,
)
from .data_source_reference import DataSourceReference
from ....data_sources import DataSources
from .field_reference_pair import (
    FieldReferencePairPrimaryKey,
    FieldReferencePairData,
)
from ....wildcards_sets import WildcardSets


class CompareTargetOnlyRecords(
    CompareBase,
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

        CompareBase.__init__(
            self=self,
            source_data_source_ref=source_data_source_ref,
            target_data_source_ref=target_data_source_ref,
            data_sources=data_sources,
            pk_fields=pk_fields,
            dt_fields=dt_fields,
            wildcard_sets=wildcard_sets,
        )

    @property
    def target_only_records(
        self,
    ) -> DataFrame:

        inner_index = self.source_table_deduplicated.index.join(
            other=self.target_table_deduplicated.index,
            how='inner',
        )

        target_only_records = self.target_table_deduplicated.loc[
            ~self.target_table_deduplicated.index.isin(
                values=inner_index.values,
            )
        ]

        return target_only_records
