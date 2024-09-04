from enum import StrEnum
from typing import (
    ClassVar,
    List,
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
