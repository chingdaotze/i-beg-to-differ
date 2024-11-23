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


class CompareValuesUnmasked(
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
    def values_comparison_unmasked(
        self,
    ) -> DataFrame:
        """
        Combined DataFrame, without duplicates.
        """

        # Get intersection
        source_table = self.source_table_deduplicated
        target_table = self.target_table_deduplicated

        intersection = source_table.index.intersection(
            other=target_table.index,
        )

        source_table = source_table.loc[intersection]
        target_table = target_table.loc[intersection]

        # Compute compares
        futures = {
            (field_pair, 'diff'): self.pool.apply_async(
                func=field_pair.compare_rule.convert_compare,
                kwds={
                    'source_field': source_table[field_pair],
                    'target_field': target_table[field_pair],
                },
            )
            for field_pair in self.dt_fields
        }

        # Build DataFrame
        data = {}

        for field_pair in self.dt_fields:
            data[(field_pair, 'source')] = source_table[field_pair]
            data[(field_pair, 'target')] = target_table[field_pair]
            data[(field_pair, 'diff')] = futures[(field_pair, 'diff')].get()

        dataframe = DataFrame(
            data=data,
            index=[
                'field_pair',
                'source_or_target',
            ],
        )

        return dataframe

    @property
    def values_comparison(
        self,
    ) -> DataFrame:

        values_comparison = self.values_comparison_unmasked.copy(
            deep=True,
        )

        for field_pair in self.dt_fields:
            values_comparison[field_pair]['diff'] = values_comparison[field_pair][
                'diff'
            ].replace(
                to_replace={
                    True: '',
                    False: '*',
                },
            )

        return values_comparison
