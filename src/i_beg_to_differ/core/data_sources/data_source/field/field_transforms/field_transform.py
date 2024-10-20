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
