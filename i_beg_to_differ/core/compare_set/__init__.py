from pathlib import Path
from typing import (
    List,
    Dict,
    TYPE_CHECKING,
    Self,
)

from ..ib2d_file_element import IB2DFileElement
from .compare import Compare

if TYPE_CHECKING:
    from ..ib2d_file import IB2DFile


class CompareSet(
    IB2DFileElement,
):
    """
    Compare set object. Contains a collection of compares.
    """

    def __init__(
        self,
        working_dir_path: Path,
        compares: List | None = None,
    ):
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
        compares = [
            Compare.deserialize(
                instance_data=compare_instance_data,
                working_dir_path=working_dir_path,
                ib2d_file=ib2d_file,
            )
            for compare_instance_data in instance_data['compare_set']
        ]

        instance = CompareSet(
            working_dir_path=working_dir_path,
            compares=compares,
        )

        return instance
