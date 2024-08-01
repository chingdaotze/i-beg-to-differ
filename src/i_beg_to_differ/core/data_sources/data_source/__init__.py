from abc import (
    ABC,
    abstractmethod,
)
from typing import Dict
from pathlib import Path
from functools import cached_property

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

    __wildcard_sets: WildcardSets | None
    """
    Attribute, used to initialize Fields on-demand.
    """

    def __init__(
        self,
        module_name: str,
        working_dir_path: Path,
    ):

        IB2DFileElement.__init__(
            self=self,
            module_name=module_name,
            working_dir_path=working_dir_path,
        )

    @cached_property
    def data(
        self,
    ) -> DataFrame:
        """
        Cached copy of the data source, for quicker local processing.
        """

        return self.load()

    @abstractmethod
    def load(
        self,
    ) -> DataFrame:
        """
        Loads data to a dataframe. Must be multiprocess-safe.

        :return: Dataframe of loaded data.
        """

    @abstractmethod
    @property
    def native_types(
        self,
    ) -> Dict[str, str]:
        """
        Dictionary of native types. Keys are column names.

        :return: Dictionary of native types.
        """

    @abstractmethod
    @property
    def py_types(
        self,
    ) -> Dict[str, str]:
        """
        Dictionary of python types. Keys are column names.

        :return: Dictionary of python types.
        """

    def __getitem__(
        self,
        name: str,
    ) -> Field:

        if name not in self.fields:

            self.fields[name] = Field(
                working_dir_path=self.working_dir_path,
                name=name,
                data_source=self,
                wildcard_sets=self.__wildcard_sets,
            )

        return self.fields[name]
