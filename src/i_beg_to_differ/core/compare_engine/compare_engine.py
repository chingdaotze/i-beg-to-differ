from typing import (
    List,
    ClassVar,
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

    _SOURCE_PREFIX: ClassVar[str] = 'src'
    """
    Prefix to assign to source fields.
    """

    _TARGET_PREFIX: ClassVar[str] = 'tgt'
    """
    Prefix to assign to target fields.
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

        self.data_sources = data_sources
        self.source = source
        self.target = target

        if pk_fields is None:
            self.pk_fields = []

        else:
            self.pk_fields = [
                CompareEngineFieldPair(
                    field_pair=field_pair,
                )
                for field_pair in pk_fields
            ]

        if dt_fields is None:
            self.dt_fields = []

        else:
            self.dt_fields = [
                CompareEngineFieldPair(
                    field_pair=field_pair,
                )
                for field_pair in dt_fields
            ]

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
        # TODO: Perform data type promotion

    # TODO: Implement compare methods
    @cached_property
    def values_comparison(
        self,
    ) -> DataFrame:

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
