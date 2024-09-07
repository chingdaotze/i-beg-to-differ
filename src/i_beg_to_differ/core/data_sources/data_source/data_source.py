from abc import (
    ABC,
    abstractmethod,
)
from typing import (
    Dict,
    Self,
)

from pandas import DataFrame

from .field import Field
from ...ib2d_file.ib2d_file_element import IB2DFileElement
from ...extensions.extension import Extension
from ...wildcards_sets import WildcardSets


class DataSource(
    IB2DFileElement,
    Extension,
    ABC,
):
    """
    Abstract data source that functions as cached data storage. Primarily responsible for:
        #. Loading data into a DataFrame.
        #. Managing Fields, which serve as an abstraction layer over the data.

    This class must be pickleable.
    """

    fields: Dict[str, Field]
    """
    Collection of Fields, specific to this data source.
    """

    description: str | None
    """
    Human-readable description of this data source.
    """

    _wildcard_sets: WildcardSets | None
    """
    Attribute, used to initialize Fields on-demand.
    """

    _data: DataFrame | None
    """
    Cached copy of the data.
    """

    def __init__(
        self,
        description: str | None = None,
        wildcard_sets: WildcardSets | None = None,
    ):

        IB2DFileElement.__init__(
            self=self,
        )

        self.description = description
        self.fields = {}
        self._wildcard_sets = wildcard_sets
        self._data = None

    def __getitem__(
        self,
        name: str,
    ) -> Field:

        if name not in self.fields:

            self.fields[name] = Field(
                name=name,
                data_source=self,
                wildcard_sets=self._wildcard_sets,
            )

        return self.fields[name]

    @property
    def cache(
        self,
    ) -> DataFrame:
        """
        Cached copy of the data source, for quicker local processing.
        """

        if self.empty:
            self.load()

        return self._data

    @cache.setter
    def cache(
        self,
        value: DataFrame,
    ) -> None:

        self._data = value

    @property
    def empty(
        self,
    ) -> bool:
        """
        Boolean flag that indicates whether the cache is empty.
        ``True`` if the cache is empty, otherwise ``False``.
        """

        if self._data is None:
            return True

        else:
            return False

    def clear(
        self,
    ) -> None:
        """
        Clears the cache.

        :return:
        """

        self._data = None

    @abstractmethod
    def load(
        self,
    ) -> Self:
        """
        Reads data from a data source and sets the cache attribute. Must be multiprocess-safe.

        :return: Instance where cache has been loaded.
        """

    @property
    @abstractmethod
    def native_types(
        self,
    ) -> Dict[str, str]:
        """
        Dictionary of native types. Keys are column names.

        :return: Dictionary of native types.
        """

    @property
    def py_types(
        self,
    ) -> Dict[str, str]:
        """
        Dictionary of python types. Keys are column names.

        :return: Dictionary of python types.
        """

        return {
            str(column): dtype.type.__name__
            for column, dtype in self.cache.dtypes.items()
        }
