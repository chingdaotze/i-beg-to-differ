from abc import ABC, abstractmethod
from typing import List
from functools import cached_property

from pandas import DataFrame

from ..base import Base
from ..compare_sets.compare_set.compare.field_pair import FieldPair


class CompareEngine(
    Base,
    ABC,
):
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
        pk_fields: List[FieldPair] | None = None,
        dt_fields: List[FieldPair] | None = None,
    ):

        Base.__init__(
            self=self,
        )

        self.pk_fields = pk_fields
        self.dt_fields = dt_fields

    @cached_property
    @abstractmethod
    def src_df(
        self,
    ) -> DataFrame:
        """
        Source DataFrame for comparisons.

        :return:
        """

    @cached_property
    @abstractmethod
    def tgt_df(
        self,
    ) -> DataFrame:
        """
        Target DataFrame for comparisons.

        :return:
        """

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
