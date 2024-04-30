from abc import ABC
from pathlib import Path
from typing import (
    TYPE_CHECKING,
    Dict,
    Self,
)

from ..ib2d_file_element import IB2DFileElement

if TYPE_CHECKING:
    from ..ib2d_file import IB2DFile


class DataSource(
    IB2DFileElement,
    ABC,
):
    """
    Abstract data source.
    """

    type_id: str
    """
    Unique identifier for this DataSource.
    """

    def __init__(
        self,
        working_dir_path: Path,
        type_id: str,
    ):
        self.type_id = type_id

        IB2DFileElement.__init__(
            self=self,
            working_dir_path=working_dir_path,
        )

    @classmethod
    def deserialize(
        cls,
        instance_data: Dict,
        working_dir_path: Path,
        ib2d_file: 'IB2DFile',
    ) -> Self:

        # TODO: Deserialize object

        pass
