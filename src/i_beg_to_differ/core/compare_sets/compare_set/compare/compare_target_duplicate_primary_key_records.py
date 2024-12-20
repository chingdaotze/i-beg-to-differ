from typing import List

from pandas import DataFrame

from .compare_base import CompareBase
from .data_source_reference import DataSourceReference
from ....data_sources import DataSources
from .field_reference_pair import (
    FieldReferencePairPrimaryKey,
    FieldReferencePairData,
)
from ....wildcards_sets import WildcardSets


class CompareTargetDuplicatePrimaryKeyRecords(
    CompareBase,
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
    def target_duplicate_primary_key_records(
        self,
    ) -> DataFrame:

        duplicated_dataframe = self.target_table[
            self.target_table.index.duplicated(
                keep=False,
            )
        ]

        return duplicated_dataframe
