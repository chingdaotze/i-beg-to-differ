from abc import (
    ABC,
    abstractmethod,
)
from pathlib import Path

from pandas import Series

from .....ib2d_file.ib2d_file_element import IB2DFileElement
from .....extensions.extension import Extension


class FieldTransform(
    IB2DFileElement,
    Extension,
    ABC,
):
    """
    Base Field transform class.
    """

    def __init__(
        self,
        module_name: str,
        working_dir_path: Path,
    ):

        IB2DFileElement.__init__(
            self=self,
            module_name=module_name,
            working_dir_path=working_dir_path,
        )

    @abstractmethod
    def transform(
        self,
        values: Series,
    ) -> Series:
        """
        Transforms values in a single Field.

        :param values: Values to transform.
        :return: Transformed values.
        """
