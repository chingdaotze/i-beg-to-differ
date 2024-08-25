from pathlib import Path
from typing import (
    List,
    Dict,
    Self,
)
from zipfile import ZipFile
from functools import cached_property

from pandas import DataFrame

from ....ib2d_file.ib2d_file_element import IB2DFileElement
from .data_source_pair import DataSourcePair
from .field_pair import FieldPair
from ....base import log_exception
from ....data_sources import DataSources
from ....wildcards_sets import WildcardSets


class Compare(
    IB2DFileElement,
):
    """
    Compare object.
    """

    description: str | None
    """
    Human-readable description.
    """

    data_sources: DataSourcePair
    """
    Data source pair.
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
        working_dir_path: Path,
        data_sources: DataSourcePair,
        pk_fields: List[FieldPair] | None = None,
        dt_fields: List[FieldPair] | None = None,
        description: str | None = None,
    ):
        IB2DFileElement.__init__(
            self=self,
            working_dir_path=working_dir_path,
        )

        self.description = description
        self.data_sources = data_sources
        self.pk_fields = pk_fields
        self.dt_fields = dt_fields

    def __str__(
        self,
    ) -> str:
        # TODO: Implement hash to make this unique

        return str(
            self.data_sources,
        )

    @property
    def fields(
        self,
    ) -> List[FieldPair]:

        return self.pk_fields + self.dt_fields

    @classmethod
    @log_exception
    def deserialize(
        cls,
        instance_data: Dict,
        working_dir_path: Path,
        ib2d_file: ZipFile,
        data_sources: DataSources,
        wildcard_sets: WildcardSets | None = None,
    ) -> Self:

        data_sources = DataSourcePair.deserialize(
            instance_data=instance_data,
            working_dir_path=working_dir_path,
            ib2d_file=ib2d_file,
            data_sources=data_sources,
            wildcard_sets=wildcard_sets,
        )

        pk_fields = [
            FieldPair.deserialize(
                instance_data=pk_field_data,
                working_dir_path=working_dir_path,
                ib2d_file=ib2d_file,
                source_data_source=data_sources.source,
                target_data_source=data_sources.target,
                wildcard_sets=wildcard_sets,
            )
            for pk_field_data in instance_data['pk_fields']
        ]

        dt_fields = [
            FieldPair.deserialize(
                instance_data=dt_field_data,
                working_dir_path=working_dir_path,
                ib2d_file=ib2d_file,
                source_data_source=data_sources.source,
                target_data_source=data_sources.target,
                wildcard_sets=wildcard_sets,
            )
            for dt_field_data in instance_data['dt_fields']
        ]

        return Compare(
            working_dir_path=working_dir_path,
            data_sources=data_sources,
            pk_fields=pk_fields,
            dt_fields=dt_fields,
            description=instance_data['description'],
        )

    @log_exception
    def serialize(
        self,
        ib2d_file: ZipFile,
    ) -> Dict:

        return {
            'description': self.description,
            'source': self.data_sources.source.serialize(
                ib2d_file=ib2d_file,
            ),
            'target': self.data_sources.target.serialize(
                ib2d_file=ib2d_file,
            ),
            'pk_fields': [
                instance.serialize(
                    ib2d_file=ib2d_file,
                )
                for instance in self.pk_fields
            ],
            'dt_fields': [
                instance.serialize(
                    ib2d_file=ib2d_file,
                )
                for instance in self.dt_fields
            ],
        }

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
    def duplicate_primary_key_records(
        self,
    ) -> DataFrame:

        pass
