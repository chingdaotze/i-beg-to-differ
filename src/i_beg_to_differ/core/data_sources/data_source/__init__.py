from abc import (
    ABC,
    abstractmethod,
)
from typing import Dict
from pathlib import Path

from pandas import DataFrame

from .field.field_transforms import FieldTransforms
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
    Abstract filtered data source.
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
        working_dir_path: Path,
        description: str | None = None,
        wildcard_sets: WildcardSets | None = None,
    ):

        IB2DFileElement.__init__(
            self=self,
            working_dir_path=working_dir_path,
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
                working_dir_path=self.working_dir_path,
                name=name,
                data_source=self,
                wildcard_sets=self._wildcard_sets,
            )

        return self.fields[name]

    @property
    def data(
        self,
    ) -> DataFrame:
        """
        Cached copy of the data source, for quicker local processing.
        """

        if self._data is None:
            self._data = self.load()

        return self._data

    @data.setter
    def data(
        self,
        value: DataFrame,
    ) -> None:

        self._data = value

    @abstractmethod
    def load(
        self,
    ) -> DataFrame:
        """
        Loads data to a dataframe. Must be multiprocess-safe.

        :return: Dataframe of loaded data.
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
    @abstractmethod
    def py_types(
        self,
    ) -> Dict[str, str]:
        """
        Dictionary of python types. Keys are column names.

        :return: Dictionary of python types.
        """
