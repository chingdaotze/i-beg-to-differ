from typing import Dict

from ..base import Base

from .data_source import DataSource


class DataSources(
    Base,
):
    """
    Collection of data sources.
    """

    data_sources: Dict[str, DataSource]

    def __init__(
        self,
    ):

        Base.__init__(
            self=self,
            module_name=__name__,
        )

        self.data_sources = {}

    def __str__(
        self,
    ) -> str:

        return 'Data Sources'

    def __getitem__(
        self,
        __data_source: str | DataSource,
    ) -> DataSource:

        if isinstance(__data_source, DataSource):
            __data_source = str(
                __data_source,
            )

        return self.data_sources[__data_source]

    def append(
        self,
        __data_source: DataSource,
    ) -> None:
        """
        Add data source to the collection of data sources.

        :param __data_source: Data source to add.
        :return:
        """

        self.data_sources[str(__data_source)] = __data_source

    def remove(
        self,
        __data_source: DataSource,
    ) -> None:
        """
        Delete data source from the collection of data sources.

        :param __data_source: Transforms to delete.
        :return:
        """

        del self.data_sources[str(__data_source)]
