from abc import (
    ABC,
    abstractmethod,
)
from pathlib import Path

from pandas import (
    DataFrame,
    Series,
)

from ......ib2d_file.ib2d_file_element import IB2DFileElement
from ......extensions.extension import Extension


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
        working_dir_path: Path,
    ):

        IB2DFileElement.__init__(
            self=self,
            working_dir_path=working_dir_path,
        )

    @abstractmethod
    def transform(
        self,
        raw_table: DataFrame,
        transformed_table: DataFrame,
        field: Series,
    ) -> Series:
        """
        Transforms values in a single Field.

        :param raw_table: Read-only copy of the original table.
        :param transformed_table: Read-only copy of the transformed table.
        :param field: Values to transform.
        :return: Transformed values.
        """
