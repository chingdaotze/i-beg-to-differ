from typing import List
from functools import cached_property

from pandas import DataFrame

from ..base import Base
from ..data_sources import DataSources
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

    pk_fields: List[FieldPair]
    """
    Primary key field pairs.
    """

    dt_fields: List[FieldPair]
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

        self.data_sources = data_sources
        self.source = source
        self.target = target
        self.pk_fields = pk_fields
        self.dt_fields = dt_fields

    def __str__(
        self,
    ) -> str:

        return f'Compare Engine: {id(self)}'

    @cached_property
    def src_df(
        self,
    ) -> DataFrame:
        """
        Source DataFrame for comparisons.

        :return:
        """

        # TODO: Init cache

    @cached_property
    def tgt_df(
        self,
    ) -> DataFrame:
        """
        Target DataFrame for comparisons.

        :return:
        """

        # TODO: Init cache

    @property
    def fields(
        self,
    ) -> List[FieldPair]:

        return self.pk_fields + self.dt_fields

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
