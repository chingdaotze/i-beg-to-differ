from typing import (
    List,
    Dict,
)
from functools import cached_property

from pandas import DataFrame

from ..base import (
    Base,
    log_exception,
)
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

    @log_exception
    def init_field_transforms(
        self,
    ) -> None:
        """
        Calculates field transformations in parallel, if they do not already exist.

        :return:
        """

        # TODO: Remove duplicate field / transform combinations, and skip ones that already exist
        # TODO: Pass list of these combinations to init

        # TODO: Each field initializes all the transforms expected within itself. The initialize routine sets values in the shared dictionary
        # TODO: Fields within a data source are processed in parallel
        # TODO: Both data sources are processed at the same time

        # TODO: Retrieve transformed fields to construct DataFrame? Or perhaps this isn't necessary and we can skip this whole cache thing... might save on RAM
        # TODO: Final data type conversion for compare should be performed outside the scope of this

        source_data_source = self.data_sources[self.source]
        target_data_source = self.data_sources[self.target]

        futures = []

        for field_pair in self.fields:
            source_field = source_data_source[str(field_pair.source_field)]

            source_field.append(
                field_pair.source_transforms,
            )

            source_field_transformed = source_field.field_transforms[
                field_pair.source_transforms
            ]

            if source_field_transformed is None:
                futures.append(
                    self.pool.apply_async(
                        func=source_field.init_field_transforms,
                        kwds={
                            'field_transforms': field_pair.source_transforms,
                        },
                    ),
                )

            target_field = target_data_source[str(field_pair.target_field)]

            target_field.append(
                field_pair.target_transforms,
            )

            target_field_transformed = target_field.field_transforms[
                field_pair.target_transforms
            ]

            if target_field_transformed is None:
                futures.append(
                    self.pool.apply_async(
                        func=target_field.init_field_transforms,
                        kwds={
                            'field_transforms': field_pair.target_transforms,
                        },
                    ),
                )

        for future in futures:
            future.get()

        pass

    # TODO: Implement compare methods
    @cached_property
    def values_comparison(
        self,
    ) -> DataFrame:

        self.init_field_transforms()

    @cached_property
    def source_only_records(
        self,
    ) -> DataFrame:

        self.init_field_transforms()

    @cached_property
    def target_only_records(
        self,
    ) -> DataFrame:

        self.init_field_transforms()

    @cached_property
    def source_duplicate_primary_key_records(
        self,
    ) -> DataFrame:

        self.init_field_transforms()

    @cached_property
    def target_duplicate_primary_key_records(
        self,
    ) -> DataFrame:

        self.init_field_transforms()
