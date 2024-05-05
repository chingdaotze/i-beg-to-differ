from pathlib import Path
from typing import (
    TYPE_CHECKING,
    Dict,
    Self,
)

from ....ib2d_file.ib2d_file_element import IB2DFileElement
from ....wildcards import Wildcards

if TYPE_CHECKING:
    from ....ib2d_file import IB2DFile


class Field(
    IB2DFileElement,
):
    """
    Field object.
    """

    name: str
    py_type: str
    native_type: str

    def __init__(
        self,
        working_dir_path: Path,
        wildcards: Wildcards | None = None,
    ):

        IB2DFileElement.__init__(
            self=self,
            working_dir_path=working_dir_path,
            wildcards=wildcards,
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
