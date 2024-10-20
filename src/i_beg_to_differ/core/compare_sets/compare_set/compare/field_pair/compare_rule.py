from abc import (
    ABC,
    abstractmethod,
)
from typing import Dict

from pandas import Series

from .....ib2d_file.ib2d_file_element import IB2DFileElement
from .....extensions.extension import DataTypeExtension


class CompareRule(
    IB2DFileElement,
    DataTypeExtension,
    ABC,
):
    """
    Base field pair compare rule class.
    """

    parameters: Dict
    """
    Compare rule parameters.
    """

    def __init__(
        self,
    ):
        IB2DFileElement.__init__(
            self=self,
        )

    def convert_compare(
        self,
        source_field: Series,
        target_field: Series,
    ) -> Series:
        """
        Converts data into appropriate types first, then executes the compare function.

        :param source_field:
        :param target_field:
        :return:
        """

        source_field, target_field = self.cast_data_type(
            source=source_field,
            target=target_field,
        )

        return self.compare(
            source_field=source_field,
            target_field=target_field,
        )

    @abstractmethod
    def compare(
        self,
        source_field: Series,
        target_field: Series,
    ) -> Series:
        """
        Compares values between source and target fields.

        :param source_field: Source field to compare.
        :param target_field: Target field to compare.
        :return: Series of booleans, where True indicates a match.
        """
