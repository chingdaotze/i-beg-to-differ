from typing import (
    Dict,
    ClassVar,
    Union,
    Self,
)
from pathlib import Path
from zipfile import ZipFile

from ..ib2d_file.ib2d_file_element import IB2DFileElement
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

    def __getitem__(
        self,
        data_source_: str | DataSource,
    ) -> DataSource:

        if isinstance(data_source_, DataSource):
            data_source_ = str(
                data_source_,
            )

        return self.data_sources[data_source_]

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

    @classmethod
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

    def serialize(
        self,
        ib2d_file: ZipFile,
    ) -> Dict:

        # TODO: Serialize

        data = {}

        for data_source in self.data_sources.values():
            data[data_source.id]
