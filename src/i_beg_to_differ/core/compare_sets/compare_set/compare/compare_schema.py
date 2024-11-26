from abc import ABC

from pandas import DataFrame

from .compare_base import (
    CompareBase,
    AUTO_MATCH,
)
from .compare_values import CompareValues
from i_beg_to_differ.extensions.data_sources.data_source_dataframe import (
    DataSourceDataFrame,
)
from ....data_sources import DataSources
from .field_reference_pair import FieldReferencePairPrimaryKey
from .data_source_reference import DataSourceReference


class CompareSchema(
    CompareBase,
    ABC,
):

    @property
    def schema_compare(
        self,
    ) -> DataFrame:

        source_types = DataSourceDataFrame(
            data=self.source_data_source.data_types,
        )

        target_types = DataSourceDataFrame(
            data=self.target_data_source.data_types,
        )

        data_sources = DataSources(
            data_sources={
                'source': source_types,
                'target': target_types,
            }
        )

        source_data_source_ref = DataSourceReference(
            data_source_name='source',
        )

        target_data_source_ref = DataSourceReference(
            data_source_name='target',
        )

        compare_values = CompareValues(
            source_data_source_ref=source_data_source_ref,
            target_data_source_ref=target_data_source_ref,
            data_sources=data_sources,
            pk_fields=[
                FieldReferencePairPrimaryKey(
                    source_field_name='column_name',
                    target_field_name='column_name',
                )
            ],
            dt_fields=AUTO_MATCH,
        )

        return compare_values.values_comparison
