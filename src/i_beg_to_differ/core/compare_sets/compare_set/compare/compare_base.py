from typing import (
    Final,
    List,
)
from abc import ABC

from pandas import DataFrame

from ....base import (
    Base,
)
from .data_source_reference import DataSourceReference
from ....data_sources import DataSources
from .field_reference_pair import (
    FieldReferencePairPrimaryKey,
    FieldReferencePairData,
)
from ....wildcards_sets import WildcardSets
from ....data_sources.data_source import DataSource


AUTO_MATCH: Final[str] = 'auto_match'


class CompareBase(
    Base,
    ABC,
):
    """
    Base comparison class. Provides methods and structure for data access.
    """

    _source_data_source_ref: DataSourceReference
    _target_data_source_ref: DataSourceReference
    data_sources: DataSources
    _pk_fields: List[FieldReferencePairPrimaryKey]
    _dt_fields: List[FieldReferencePairData] | AUTO_MATCH
    _wildcard_sets: WildcardSets

    def __init__(
        self,
        source_data_source_ref: DataSourceReference,
        target_data_source_ref: DataSourceReference,
        data_sources: DataSources,
        pk_fields: List[FieldReferencePairPrimaryKey] | None = None,
        dt_fields: List[FieldReferencePairData] | AUTO_MATCH | None = None,
        wildcard_sets: WildcardSets | None = None,
    ):

        Base.__init__(
            self=self,
        )

        self.pk_fields = pk_fields
        self.dt_fields = dt_fields

        self._source_data_source_ref = source_data_source_ref
        self._target_data_source_ref = target_data_source_ref
        self.data_sources = data_sources

        self._wildcard_sets = wildcard_sets

    def __str__(
        self,
    ) -> str:

        return str(
            id(
                self,
            ),
        )

    @property
    def source_data_source(
        self,
    ) -> DataSource:

        return self.data_sources[self.source_data_source_ref]

    @property
    def target_data_source(
        self,
    ) -> DataSource:

        return self.data_sources[self.target_data_source_ref]

    @property
    def pk_fields(
        self,
    ) -> List[FieldReferencePairPrimaryKey]:
        """
        Primary key field pairs.
        """

        return self._pk_fields

    @pk_fields.setter
    def pk_fields(
        self,
        value: List[FieldReferencePairPrimaryKey] | None,
    ) -> None:
        """
        Primary key field pairs.
        """

        if value is None:
            self._pk_fields = []

        else:
            self._pk_fields = value

    @property
    def auto_match_dt_fields(
        self,
    ) -> List[FieldReferencePairData]:
        """
        Matching list of field pairs between the source and target data sources,
        using column names to match.
        """

        source_columns = self.source_data_source.columns
        target_columns = self.target_data_source.columns

        matching_columns = [
            column for column in source_columns if column in target_columns
        ]

        field_pairs = [
            field_pair
            for field in matching_columns
            if (
                field_pair := FieldReferencePairData(
                    source_field_name=field,
                    target_field_name=field,
                    wildcard_sets=self._wildcard_sets,
                )
            )
            not in self.pk_fields
        ]

        return field_pairs

    @property
    def dt_fields(
        self,
    ) -> List[FieldReferencePairData]:
        """
        Data field pairs.

        #. If data fields are provided, those will be used.
        #. If data fields are set to ``AUTO_MATCH``, those will be matched, less any primary keys.
        """

        if self._dt_fields == AUTO_MATCH:
            dt_fields = self.auto_match_dt_fields

        else:
            dt_fields = self._dt_fields

        return dt_fields

    @dt_fields.setter
    def dt_fields(
        self,
        value: List[FieldReferencePairData] | AUTO_MATCH | None = None,
    ) -> None:
        """
        Data field pairs.
        """

        if value is None:
            self._dt_fields = []

        else:
            self._dt_fields = value

    @property
    def fields(
        self,
    ) -> List[FieldReferencePairPrimaryKey | FieldReferencePairData]:
        """
        All fields, including both primary key and data fields.
        """

        return self.pk_fields + self.dt_fields

    @property
    def source_data_source_ref(
        self,
    ) -> DataSourceReference:
        """
        Pointer to the source data source.
        """

        return self._source_data_source_ref

    @source_data_source_ref.setter
    def source_data_source_ref(
        self,
        value: DataSourceReference,
    ) -> None:
        """
        Pointer to the source data source. Synchronizes source data source across field pairs.
        """

        self._source_data_source_ref = value

        for field in self.fields:
            field.source_data_source_ref = self._source_data_source_ref

    @property
    def target_data_source_ref(
        self,
    ) -> DataSourceReference:
        """
        Pointer to the target data source.
        """

        return self._target_data_source_ref

    @target_data_source_ref.setter
    def target_data_source_ref(
        self,
        value: DataSourceReference,
    ) -> None:
        """
        Pointer to the target data source. Synchronizes target data source across field pairs.
        """

        self._target_data_source_ref = value

        for field in self.fields:
            field.target_data_source_ref = self._target_data_source_ref

    @property
    def source_table(
        self,
    ) -> DataFrame:
        """
        Source table. Combines multiple fields into single table and adds primary key.
        """

        futures = {
            field_pair: self.pool.apply_async(
                func=self.source_data_source.calculate_field,
                kwds={
                    'field_reference': field_pair.source_field_ref,
                },
            )
            for field_pair in self.fields
        }

        data = {field_pair: future.get() for field_pair, future in futures.items()}

        dataframe = DataFrame(
            data=data,
        )

        if self.pk_fields:
            dataframe.set_index(
                keys=[field_pair for field_pair in self.pk_fields],
                inplace=True,
            )

        return dataframe

    @property
    def source_table_deduplicated(
        self,
    ) -> DataFrame:

        deduplicated_table = self.source_table[
            ~self.source_table.index.duplicated(
                keep=False,
            )
        ]

        return deduplicated_table

    @property
    def target_table(
        self,
    ) -> DataFrame:
        """
        Target table. Combines multiple fields into single table and adds primary key.
        """

        futures = {
            field_pair: self.pool.apply_async(
                func=self.target_data_source.calculate_field,
                kwds={
                    'field_reference': field_pair.target_field_ref,
                },
            )
            for field_pair in self.fields
        }

        data = {field_pair: future.get() for field_pair, future in futures.items()}

        dataframe = DataFrame(
            data=data,
        )

        if self.pk_fields:
            dataframe.set_index(
                keys=[field_pair for field_pair in self.pk_fields],
                inplace=True,
            )

        return dataframe

    @property
    def target_table_deduplicated(
        self,
    ) -> DataFrame:

        deduplicated_table = self.target_table[
            ~self.target_table.index.duplicated(
                keep=False,
            )
        ]

        return deduplicated_table

    @property
    def merged_table_deduplicated(
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
            for field_pair in self.fields
        }

        # Build DataFrame
        data = {}

        for field_pair in self.fields:
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
