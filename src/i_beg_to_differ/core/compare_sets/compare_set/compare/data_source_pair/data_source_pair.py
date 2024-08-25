from pathlib import Path
from typing import (
    Dict,
    Self,
)
from zipfile import ZipFile
from functools import cached_property

from pandas import DataFrame

from .....ib2d_file.ib2d_file_element import IB2DFileElement
from .....data_sources.data_source import DataSource
from .....data_sources import DataSources
from .....base import log_exception
from .....wildcards_sets import WildcardSets


class DataSourcePair(
    IB2DFileElement,
):
    source: DataSource
    """
    Source data source object.
    """

    target: DataSource
    """
    Target data source object.
    """

    _data_sources: DataSources
    """
    All data sources.
    """

    def __init__(
        self,
        working_dir_path: Path,
        source: DataSource,
        target: DataSource,
        data_sources: DataSources,
    ):
        IB2DFileElement.__init__(
            self=self,
            working_dir_path=working_dir_path,
        )

        self.source = source
        self.target = target
        self._data_sources = data_sources

    def __str__(
        self,
    ) -> str:

        return f'{self.source} | {self.target}'

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
        source = data_sources[source_data_source_id]

        target_data_source_id = instance_data['target']
        target = data_sources[target_data_source_id]

        return DataSourcePair(
            working_dir_path=working_dir_path,
            source=source,
            target=target,
            data_sources=data_sources,
        )

    @log_exception
    def serialize(
        self,
        ib2d_file: ZipFile,
    ) -> Dict:

        return {
            'source': self.source.serialize(
                ib2d_file=ib2d_file,
            ),
            'target': self.source.serialize(
                ib2d_file=ib2d_file,
            ),
        }

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

    @cached_property
    def schema_comparison(
        self,
    ) -> DataFrame:

        source_native_types = self.source.native_types
        source_py_types = self.source.py_types

        target_native_types = self.target.native_types
        target_py_types = self.target.py_types

        pass
