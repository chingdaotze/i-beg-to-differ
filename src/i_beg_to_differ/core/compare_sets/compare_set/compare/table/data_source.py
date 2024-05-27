from abc import (
    ABC,
    abstractmethod,
)
from pathlib import Path

from pandas import DataFrame

from .....ib2d_file.ib2d_file_element import IB2DFileElement
from .....extensions.extension import Extension


class DataSource(
    IB2DFileElement,
    Extension,
    ABC,
):
    """
    Abstract data source.
    """

    def __init__(
        self,
        working_dir_path: Path,
        extension_id: str,
        extension_name: str,
    ):

        IB2DFileElement.__init__(
            self=self,
            working_dir_path=working_dir_path,
        )

        Extension.__init__(
            self=self,
            extension_id=extension_id,
            extension_name=extension_name,
        )

    @abstractmethod
    def load(
        self,
    ) -> DataFrame:
        """
        Loads data to a dataframe. Must be multiprocess-safe.

        :return: Dataframe of loaded data.
        """
