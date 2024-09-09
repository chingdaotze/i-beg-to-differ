from typing import (
    List,
    Dict,
)
from functools import cached_property

from pandas import (
    DataFrame,
    concat,
)

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

        # TODO: Final data type conversion for compare rule should be performed outside the scope of this

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

    @cached_property
    def source_dataframe(
        self,
    ) -> DataFrame:
        """
        DataFrame containing transformed source fields.
        """

        self.init_field_transforms()

        dataframe = concat(
            objs=[
                self.data_sources[self.source][str(field_pair.source_field)][
                    field_pair.source_transforms
                ]
                for field_pair in self.fields
            ],
            axis=1,
        )

        if self.pk_fields:
            dataframe.set_index(
                keys=[str(field_pair.source_field) for field_pair in self.pk_fields],
                inplace=True,
            )

        return dataframe

    @cached_property
    def target_dataframe(
        self,
    ) -> DataFrame:
        """
        DataFrame containing transformed target fields.
        """

        self.init_field_transforms()

        dataframe = concat(
            objs=[
                self.data_sources[self.target][str(field_pair.target_field)][
                    field_pair.target_transforms
                ]
                for field_pair in self.fields
            ],
            axis=1,
        )

        if self.pk_fields:
            dataframe.set_index(
                keys=[str(field_pair.target_field) for field_pair in self.pk_fields],
                inplace=True,
            )

        return dataframe

    # TODO: Implement compare methods
    @cached_property
    def values_comparison(
        self,
    ) -> DataFrame:

        source = self.source_dataframe
        target = self.target_dataframe

        pass

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
