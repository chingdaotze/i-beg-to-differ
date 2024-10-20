from abc import (
    ABC,
    abstractmethod,
)

from pandas import Series

from .....ib2d_file.ib2d_file_element import IB2DFileElement
from .....extensions.extension import DataTypeExtension


class FieldTransform(
    IB2DFileElement,
    DataTypeExtension,
    ABC,
):
    """
    Base Field transform class.
    """

    def __init__(
        self,
    ):

        IB2DFileElement.__init__(
            self=self,
        )

    def convert_transform(
        self,
        values: Series,
    ) -> Series:
        """
        Converts data into appropriate types first, then executes the transform function.

        :param values: Values to transform.
        :return: Transformed values.
        """

        values = self.cast_data_type(
            values=values,
        )

        return self.transform(
            values=values,
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
