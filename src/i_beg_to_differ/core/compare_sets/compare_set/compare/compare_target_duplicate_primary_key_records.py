from typing import List

from pandas import DataFrame

from .compare_base import (
    CompareBase,
    AUTO_MATCH,
)
from .data_source_reference import DataSourceReference
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
        pk_fields: List[FieldReferencePairPrimaryKey] | None = None,
        dt_fields: List[FieldReferencePairData] | AUTO_MATCH | None = None,
        wildcard_sets: WildcardSets | None = None,
    ):

        CompareBase.__init__(
            self=self,
            source_data_source_ref=source_data_source_ref,
            target_data_source_ref=target_data_source_ref,
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
