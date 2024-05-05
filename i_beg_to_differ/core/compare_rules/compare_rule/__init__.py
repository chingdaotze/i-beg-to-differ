from pathlib import Path
from abc import abstractmethod

from pandas import (
    DataFrame,
    Series,
)

from ...ib2d_file.ib2d_file_element import IB2DFileElement
from ...registered_types.registered_type import RegisteredType
from ...wildcards import Wildcards


class CompareRule(
    IB2DFileElement,
    RegisteredType,
):
    """
    Base compare rule class.
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
    def compare(
        self,
        raw_table: DataFrame,
        transformed_table: DataFrame,
        source_field: Series,
        target_field: Series,
    ) -> Series[bool]:
        """
        Compares values between source and target fields.

        :param raw_table: Read-only copy of the original table.
        :param transformed_table: Read-only copy of the transformed table.
        :param source_field: Source field to compare.
        :param target_field: Target field to compare.
        :return: Series of booleans, where True indicates a match.
        """
