from typing import (
    Dict,
    ClassVar,
    List,
    Union,
    Self,
)
from pathlib import Path
from zipfile import ZipFile

from ..ib2d_file.ib2d_file_element import IB2DFileElement
from ..base import (
    log_exception,
    log_runtime,
)
from ..extensions.data_sources import DataSourceExtensions
from .data_source import DataSource
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
        working_dir_path: Path,
        data_sources: Dict[str, DataSource],
    ):

        IB2DFileElement.__init__(
            self=self,
            working_dir_path=working_dir_path,
        )

        self.data_sources = data_sources

    def __str__(
        self,
    ) -> str:

        return 'Data Sources'

    @log_exception
    def __getitem__(
        self,
        data_source_: str | DataSource,
    ) -> DataSource:

        if isinstance(data_source_, DataSource):
            data_source_ = str(
                data_source_,
            )

        return self.data_sources[data_source_]

    @log_exception
    def append(
        self,
        data_source_: DataSource,
    ) -> None:
        """
        Add data source to the collection of data sources.

        :param data_source_: Data source to add.
        :return:
        """

        self.data_sources[str(data_source_)] = data_source_

    @log_exception
    def remove(
        self,
        data_source_: DataSource,
    ) -> None:
        """
        Delete data source from the collection of data sources.

        :param data_source_: Transforms to delete.
        :return:
        """

        del self.data_sources[str(data_source_)]

    @log_exception
    @log_runtime
    def init_caches(
        self,
        data_sources: List[str | DataSource],
        force_reload: bool = False,
    ) -> None:
        """
        Prepares specified caches for reading. Uses multiprocessing, so can be more performant than lazy loading.
        If a cache has not been loaded yet, loads the cache.
        If a cache has already been loaded, the cached copy will continue to be used.
        Optionally, can force a reload of all specified caches.

        :param data_sources: List of data sources to init.
        :param force_reload: Set to ``True`` to force a cache reload.
        :return:
        """

        futures = []

        for data_source_ in data_sources:
            data_source_ = self[data_source_]

            if data_source_.empty or force_reload:
                futures.append(
                    self.pool.apply_async(
                        func=data_source_.load,
                    ),
                )

            else:
                self.log_info(
                    msg=f'Using cached data for data source: {str(data_source_)} ...',
                )

        for future in futures:
            self.append(
                future.get(),
            )

    @classmethod
    @log_exception
    def deserialize(
        cls,
        instance_data: Dict,
        working_dir_path: Path,
        ib2d_file: ZipFile,
        wildcard_sets: Union['WildcardSets', None] = None,
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
            working_dir_path=working_dir_path,
            data_sources=data_sources,
        )

    @log_exception
    def serialize(
        self,
        ib2d_file: ZipFile,
    ) -> Dict:

        # TODO: Serialize

        data = {}

        for data_source in self.data_sources.values():
            data[data_source.id]
