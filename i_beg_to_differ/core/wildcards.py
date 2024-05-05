from pathlib import Path
from typing import (
    TYPE_CHECKING,
    Dict,
    Self,
)

from i_beg_to_differ.core.ib2d_file.ib2d_file_element import IB2DFileElement

if TYPE_CHECKING:
    from .ib2d_file import IB2DFile


class Wildcards(
    IB2DFileElement,
):
    """
    Collection of wildcards, used to replace values.
    """

    wildcards: Dict[str, str]
    """
    Collection of wildcards.
    """

    _MAX_REPLACEMENT_DEPTH = 1000

    def __init__(
        self,
        working_dir_path: Path,
        wildcards: Dict[str, str] | None = None,
    ):

        if wildcards is None:
            self.wildcards = {}

        else:
            self.wildcards = wildcards

        IB2DFileElement.__init__(
            self=self,
            working_dir_path=working_dir_path,
        )

    def replace_wildcards(
        self,
        string,
    ) -> str:

        # TODO: Implement wildcard replacement

        pass

    @classmethod
    def deserialize(
        cls,
        instance_data: Dict,
        working_dir_path: Path,
        ib2d_file: 'IB2DFile',
    ) -> Self:

        instance = Wildcards(
            working_dir_path=working_dir_path,
            wildcards=instance_data,
        )

        return instance

    def serialize(
        self,
        ib2d_file: 'IB2DFile',
    ) -> Dict:

        return self.wildcards
