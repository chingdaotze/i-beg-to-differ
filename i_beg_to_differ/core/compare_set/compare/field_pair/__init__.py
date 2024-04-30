from pathlib import Path
from typing import (
    TYPE_CHECKING,
    List,
    Dict,
    Self,
)

from ....ib2d_file_element import IB2DFileElement
from .field import Field

if TYPE_CHECKING:
    from ....ib2d_file import IB2DFile


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

        # TODO: Deserialize object

        pass
