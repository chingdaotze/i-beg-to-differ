from typing import (
    List,
    Dict,
)
from functools import cached_property

from pandas import DataFrame

from ..base import Base
from ..data_sources import DataSources
from .compare_engine_field_pair import CompareEngineFieldPair
from ..compare_sets.compare_set.compare.field_pair import FieldPair


class CompareEngine(
    Base,
):
    """
    Object that contains diffing logic.
    """

    data_sources: DataSources
    """
    Global data sources.
    """

    source: str
    """
    Pointer to source data source.
    """

    target: str
    """
    Pointer to target data source.
    """

    pk_fields: List[CompareEngineFieldPair]
    """
    Primary key field pairs.
    """

    dt_fields: List[CompareEngineFieldPair]
    """
    Data field pairs.
    """

    _source_dataframe: DataFrame | None
    """
    DataFrame containing transformed source fields.
    """

    _target_dataframe: DataFrame | None
    """
    DataFrame containing transformed target fields.
    """

    def __init__(
        self,
        data_sources: DataSources,
        source: str,
        target: str,
        pk_fields: List[FieldPair] | None = None,
        dt_fields: List[FieldPair] | None = None,
    ):

        Base.__init__(
            self=self,
        )

        def field_pair_list_to_compare_engine_field_pair_list(
            field_pairs: List[FieldPair] | None,
            source_field_counts: Dict[str, int],
            target_field_counts: Dict[str, int],
        ) -> List[CompareEngineFieldPair]:

            compare_engine_field_pairs = []

            if field_pairs is not None:
                for field_pair in field_pairs:
                    source_field = str(field_pair.source_field)

                    if source_field not in source_field_counts:
                        source_field_counts[source_field] = 0

                    source_field_counts[source_field] += 1

                    target_field = str(field_pair.target_field)

                    if target_field not in target_field_counts:
                        target_field_counts[target_field] = 0

                    target_field_counts[target_field] += 1

                    compare_engine_field_pairs.append(
                        CompareEngineFieldPair(
                            field_pair=field_pair,
                            source_field_index=source_field_counts[source_field],
                            target_field_index=target_field_counts[target_field],
                        )
                    )

            return compare_engine_field_pairs

        self.data_sources = data_sources
        self.source = source
        self.target = target

        _source_field_counts = {}
        _target_field_counts = {}

        self.pk_fields = field_pair_list_to_compare_engine_field_pair_list(
            field_pairs=pk_fields,
            source_field_counts=_source_field_counts,
            target_field_counts=_target_field_counts,
        )

        self.dt_fields = field_pair_list_to_compare_engine_field_pair_list(
            field_pairs=dt_fields,
            source_field_counts=_source_field_counts,
            target_field_counts=_target_field_counts,
        )

        self._source_dataframe = None
        self._target_dataframe = None

    def __str__(
        self,
    ) -> str:

        return f'Compare Engine: {id(self)}'

    @cached_property
    def fields(
        self,
    ) -> List[FieldPair]:
        """
        All fields, including both primary key and data fields.

        :return:
        """

        return self.pk_fields + self.dt_fields

    @cached_property
    def cache(
        self,
    ) -> DataFrame:
        """
        DataFrame for comparisons. Calculates field transformations in parallel.

        :return:
        """

        # TODO: Construct an intermediate dataframe by assigning transformed fields to fully-qualified keys
        # TODO: Perform data type conversions as transforms are applied - this should happen in the field pair
        # TODO: Perform final data type conversion for compare rule

        pass

    # TODO: Implement compare methods
    @cached_property
    def values_comparison(
        self,
    ) -> DataFrame:

        cache = self.cache

    @cached_property
    def source_only_records(
        self,
    ) -> DataFrame:

        pass

    @cached_property
    def target_only_records(
        self,
    ) -> DataFrame:

        pass

    @cached_property
    def source_duplicate_primary_key_records(
        self,
    ) -> DataFrame:

        pass

    @cached_property
    def target_duplicate_primary_key_records(
        self,
    ) -> DataFrame:
        pass
