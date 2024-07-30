from abc import (
    ABC,
    abstractmethod,
)
from typing import List
from pathlib import Path
from functools import cached_property

from pandas import DataFrame

from .field import Field
from ...ib2d_file.ib2d_file_element import IB2DFileElement
from ...extensions.extension import Extension
from ...wildcards_sets import WildcardSets
from .field.field_transform import FieldTransform


class DataSource(
    IB2DFileElement,
    Extension,
    ABC,
):
    """
    Abstract filtered data source.
    """

    __fields: List[Field]
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
        wildcard_sets: WildcardSets | None = None,
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

    def get_field(
        self,
        name: str,
        transforms: List[FieldTransform] | None = None,
    ) -> Field:

        instance = Field(
            working_dir_path=self.working_dir_path,
            name=name,
            data_source=self,
            transforms=transforms,
            wildcard_sets=self.__wildcard_sets,
        )

        if instance not in self.__fields:

            self.__fields.append(
                instance,
            )

        instance = [field_ for field_ in self.__fields if field_ == instance][0]

        return instance
