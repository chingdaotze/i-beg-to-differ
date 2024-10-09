from enum import StrEnum
from typing import (
    ClassVar,
    List,
)

from pandas import (
    Series,
    to_numeric,
    to_datetime,
    to_timedelta,
)

from .extension import Extension


class DataType(
    StrEnum,
):
    """
    Determines applicable data types for a given extension.
    """

    ANY = 'Any'  # convert_dtypes
    STRING = 'String'  # astype(str)
    NUMERIC = 'Numeric'  # to_numeric
    DATE_TIME = 'DateTime'  # to_datetime
    TIME_DELTA = 'TimeDelta'  # to_timedelta


class DataTypeExtension(
    Extension,
):

    data_type: ClassVar[DataType | List[DataType]] = DataType.ANY
    """
    Determines applicable data types for this extension. Override this to hint
    data type conversion whenever this extension is used.
    """

    def __init__(
        self,
    ):

        Extension.__init__(
            self=self,
        )

    def cast_data_type(
        self,
        data: Series,
    ) -> Series:

        match self.data_type:
            case DataType.ANY | DataType.STRING:
                return data.astype(
                    dtype=str,
                )

            case DataType.NUMERIC:
                return to_numeric(
                    arg=data,
                )

            case DataType.DATE_TIME:
                return to_datetime(
                    arg=data,
                )

            case DataType.TIME_DELTA:
                return to_timedelta(
                    arg=data,
                )

            case _:
                raise NotImplementedError(
                    f'Unhandled data type conversion: {self.data_type} !'
                )
