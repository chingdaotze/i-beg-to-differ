from pathlib import Path
from typing import (
    List,
    Dict,
    Self,
)
from zipfile import ZipFile

from ....ib2d_file.ib2d_file_element import IB2DFileElement
from .field import Field
from ....wildcards import Wildcards


class FieldPair(
    IB2DFileElement,
):
    """
    Pair of Fields for comparison.
    """

    source: Field
    target: Field

    comparison_rules: List[ComparisonRule]

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
        ib2d_file: ZipFile,
    ) -> Self:

        # TODO: Deserialize object

        pass