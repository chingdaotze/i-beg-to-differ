from pathlib import Path
from typing import (
    Dict,
    Self,
)
from zipfile import ZipFile

from .ib2d_file.ib2d_file_element import IB2DFileElement


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
        IB2DFileElement.__init__(
            self=self,
            working_dir_path=working_dir_path,
        )

        if wildcards is None:
            self.wildcards = {}

        else:
            self.wildcards = wildcards

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
        ib2d_file: ZipFile,
    ) -> Self:

        instance = Wildcards(
            working_dir_path=working_dir_path,
            wildcards=instance_data,
        )

        return instance

    def serialize(
        self,
        ib2d_file: ZipFile,
    ) -> Dict:

        return self.wildcards
