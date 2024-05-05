from pathlib import Path
from abc import abstractmethod

from pandas import (
    DataFrame,
    Series,
)

from ...ib2d_file.ib2d_file_element import IB2DFileElement
from ...registered_types.registered_type import RegisteredType
from ...wildcards import Wildcards


class FieldTransform(
    IB2DFileElement,
    RegisteredType,
):
    """
    Base Field transform class.
    """

    def __init__(
        self,
        working_dir_path: Path,
        name: str,
        wildcards: Wildcards | None = None,
    ):

        IB2DFileElement.__init__(
            self=self,
            working_dir_path=working_dir_path,
            wildcards=wildcards,
        )

        RegisteredType.__init__(
            self=self,
            name=name,
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
