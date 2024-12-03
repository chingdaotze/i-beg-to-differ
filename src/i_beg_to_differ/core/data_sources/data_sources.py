from typing import (
    Dict,
    ClassVar,
    List,
    Self,
)
from pathlib import Path
from zipfile import ZipFile

from ..ib2d_file.ib2d_file_element import IB2DFileElement
from ..base import log_exception
from .data_source import DataSource
from ..extensions.data_sources import DataSourceExtensions
from ..compare_sets.compare_set.compare.data_source_reference import DataSourceReference
from ..wildcards_sets import WildcardSets


class DataSources(
    IB2DFileElement,
):
    """
    Collection of data sources.
    """

    data_sources: Dict[str, DataSource]
    """
    Collection of data sources.
    """

    data_source_extensions: ClassVar[DataSourceExtensions] = DataSourceExtensions()
    """
    All data source extensions for this package.
    """

    def __init__(
        self,
        data_sources: Dict[str, DataSource] | None = None,
    ):

        IB2DFileElement.__init__(
            self=self,
        )

        if data_sources is None:
            data_sources = {}

        self.data_sources = {}

        for key, data_source in data_sources.items():
            self.data_sources[key] = data_source

    def __str__(
        self,
    ) -> str:

        return 'Data Sources'

    @log_exception
    def __getitem__(
        self,
        data_source: str | DataSource | DataSourceReference,
    ) -> DataSource:

        if isinstance(data_source, DataSourceReference):
            key = data_source.data_source_name.base_value

        else:
            key = str(
                data_source,
            )

        return self.data_sources[key]

    @log_exception
    def append(
        self,
        data_source: DataSource,
    ) -> None:
        """
        Add data source to the collection of data sources.

        :param data_source: Data source to add.
        :return:
        """

        self.data_sources[str(data_source)] = data_source

    @log_exception
    def remove(
        self,
        data_source: DataSource | DataSourceReference,
    ) -> None:
        """
        Delete data source from the collection of data sources.

        :param data_source: Transforms to delete.
        :return:
        """

        del self.data_sources[str(data_source)]

    def list_data_sources(
        self,
    ) -> List[str]:

        return list(
            self.data_sources.keys(),
        )

    @classmethod
    @log_exception
    def deserialize(
        cls,
        instance_data: Dict,
        working_dir_path: Path,
        ib2d_file: ZipFile,
        wildcard_sets: WildcardSets | None = None,
    ) -> Self:

        data_sources = {}

        for name, data_source_instance_data in instance_data.items():
            extension_id = data_source_instance_data['extension_id']
            data_source_ = cls.data_source_extensions[extension_id]

            data_sources[name] = data_source_.deserialize(
                instance_data=data_source_instance_data,
                working_dir_path=working_dir_path,
                ib2d_file=ib2d_file,
                wildcard_sets=wildcard_sets,
            )

        return DataSources(
            data_sources=data_sources,
        )

    @log_exception
    def serialize(
        self,
        ib2d_file: ZipFile,
    ) -> Dict:

        return {
            extension_id: instance.serialize(
                ib2d_file=ib2d_file,
            )
            for extension_id, instance in self.data_sources.items()
        }
