from typing import (
    Final,
    List,
)
from abc import ABC

from ..base import (
    Base,
)
from ..compare_sets.compare_set.compare.data_source_pair import DataSourcePair
from ..compare_sets.compare_set.compare.field_pair import (
    FieldPairPrimaryKey,
    FieldPairData,
)


AUTO_MATCH: Final[str] = 'auto_match'


class CompareBase(
    Base,
    ABC,
):

    data_source_pair: DataSourcePair
    """
    Pointer to source and target data sources.
    """

    _pk_fields: List[FieldPairPrimaryKey]
    _dt_fields: List[FieldPairData] | AUTO_MATCH

    def __init__(
        self,
        data_source_pair: DataSourcePair,
        pk_fields: List[FieldPairPrimaryKey] | None = None,
        dt_fields: List[FieldPairData] | AUTO_MATCH | None = None,
    ):

        Base.__init__(
            self=self,
        )

        self.data_source_pair = data_source_pair
        self._pk_fields = pk_fields
        self._dt_fields = dt_fields

    @property
    def pk_fields(
        self,
    ) -> List[FieldPairPrimaryKey]:
        """
        Primary key field pairs.
        """

        return self._pk_fields

    @pk_fields.setter
    def pk_fields(
        self,
        value: List[FieldPairPrimaryKey] | None,
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
    ) -> List[FieldPairData]:
        """
        Matching list of field pairs between the source and target data sources,
        using column names to match.
        """

        source_columns = self.data_source_pair.source_data_source.columns
        target_columns = self.data_source_pair.target_data_source.columns

        matching_columns = [
            column for column in source_columns if column in target_columns
        ]

        field_pairs = [
            field_pair
            for field in matching_columns
            if (
                field_pair := FieldPairData(
                    source_field_pointer=field,
                    target_field_pointer=field,
                )
            )
            not in self.pk_fields
        ]

        return field_pairs

    @property
    def dt_fields(
        self,
    ) -> List[FieldPairData]:
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
        value: List[FieldPairData] | AUTO_MATCH | None = None,
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
    ) -> List[FieldPairPrimaryKey | FieldPairData]:
        """
        All fields, including both primary key and data fields.
        """

        return self.pk_fields + self.dt_fields
