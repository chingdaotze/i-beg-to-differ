from pathlib import Path
from typing import List

from ..ib2d_file_element import IB2DFileElement


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
