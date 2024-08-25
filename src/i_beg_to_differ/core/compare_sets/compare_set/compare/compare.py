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
from ....base import (
    log_exception,
    log_runtime,
)
from ....data_sources.data_source import DataSource
from ....data_sources import DataSources
from .field_pair import FieldPair
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

    source: DataSource
    """
    Source table object.
    """

    target: DataSource
    """
    Target table object.
    """

    pk_fields: List[FieldPair]
    """
    Primary key field pairs.
    """

    dt_fields: List[FieldPair]
    """
    Data field pairs.
    """

    fields: List[FieldPair]
    """
    All field pairs.
    """

    _data_sources: DataSources
    """
    All data sources.
    """

    def __init__(
        self,
        working_dir_path: Path,
        data_sources: DataSources,
        source: DataSource,
        target: DataSource,
        pk_fields: List[FieldPair] | None = None,
        dt_fields: List[FieldPair] | None = None,
        description: str | None = None,
    ):
        IB2DFileElement.__init__(
            self=self,
            working_dir_path=working_dir_path,
        )

        self.description = description

        self._data_sources = data_sources
        self.source = source
        self.target = target

        self.pk_fields = pk_fields
        self.dt_fields = dt_fields

    def __str__(
        self,
    ) -> str:

        return f'{self.source} | {self.target}'

    def init_caches(
        self,
    ) -> None:
        """
        Prepares the source and target caches for reading.

        :return:
        """

        self._data_sources.init_caches(
            data_sources=[
                self.source,
                self.target,
            ]
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

        source_data_source_id = instance_data['source']
        source_data_source = data_sources[source_data_source_id]

        target_data_source_id = instance_data['target']
        target_data_source = data_sources[target_data_source_id]

        pk_fields = [
            FieldPair.deserialize(
                instance_data=pk_field_data,
                working_dir_path=working_dir_path,
                ib2d_file=ib2d_file,
                source_data_source=source_data_source,
                target_data_source=target_data_source,
                wildcard_sets=wildcard_sets,
            )
            for pk_field_data in instance_data['pk_fields']
        ]

        dt_fields = [
            FieldPair.deserialize(
                instance_data=dt_field_data,
                working_dir_path=working_dir_path,
                ib2d_file=ib2d_file,
                source_data_source=source_data_source,
                target_data_source=target_data_source,
                wildcard_sets=wildcard_sets,
            )
            for dt_field_data in instance_data['dt_fields']
        ]

        return Compare(
            working_dir_path=working_dir_path,
            data_sources=data_sources,
            source=source_data_source,
            target=target_data_source,
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
            'source': self.source.serialize(
                ib2d_file=ib2d_file,
            ),
            'target': self.source.serialize(
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
    def schema_comparison(
        self,
    ) -> DataFrame:

        source_native_types = self.source.native_types
        source_py_types = self.source.py_types

        target_native_types = self.target.native_types
        target_py_types = self.target.py_types

        pass

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
