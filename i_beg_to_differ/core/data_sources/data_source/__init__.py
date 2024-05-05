from abc import (
    ABC,
    abstractmethod,
)
from pathlib import Path
from typing import (
    TYPE_CHECKING,
    Dict,
    Self,
)

from pandas import DataFrame

from ...ib2d_file.ib2d_file_element import IB2DFileElement
from ...registered_types.registered_type import RegisteredType

if TYPE_CHECKING:
    from ...ib2d_file import IB2DFile


class DataSource(
    IB2DFileElement,
    RegisteredType,
    ABC,
):
    """
    Abstract data source.
    """

    def __init__(
        self,
        working_dir_path: Path,
        name: str,
    ):
        self.name = name

        IB2DFileElement.__init__(
            self=self,
            working_dir_path=working_dir_path,
        )

        RegisteredType.__init__(
            self=self,
            name=name,
        )

    @abstractmethod
    def load(
        self,
    ) -> DataFrame:
        """
        Loads data to a dataframe. Must be multiprocess-safe.

        :return: Dataframe of loaded data.
        """

    @classmethod
    def deserialize(
        cls,
        instance_data: Dict,
        working_dir_path: Path,
        ib2d_file: 'IB2DFile',
    ) -> Self:

        # TODO: Deserialize object

        pass
