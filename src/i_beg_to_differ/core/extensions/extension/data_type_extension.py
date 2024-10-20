from enum import StrEnum
from abc import ABC
from typing import (
    ClassVar,
    List,
    Callable,
    Tuple,
)

from pandas import (
    Series,
    to_numeric,
    to_datetime,
    to_timedelta,
)
from pandas.api.types import (
    is_string_dtype,
    is_bool_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_datetime64_dtype,
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
    ABC,
):
    """
    Abstract class for an extension that has data type requirements.
    """

    data_type: ClassVar[DataType | List[DataType]] = DataType.ANY
    """
    Determines applicable data types for this extension. Override this to hint
    data type conversion whenever this extension is used.
    """

    EQUIVALENT_DTYPE_CHECKS: ClassVar[List[Callable[[Series], bool]]] = [
        is_string_dtype,
        is_bool_dtype,
        is_datetime64_any_dtype,
        is_numeric_dtype,
        is_datetime64_dtype,
    ]

    def __init__(
        self,
    ):

        Extension.__init__(
            self=self,
        )

    def cast_data_type(
        self,
        values: Series,
    ) -> Series:
        """
        Casts data to appropriate type given extension requirements.
        Tries not to cast data unless necessary.

        :param values: Values to convert.
        :return: Converted values.
        """

        match self.data_type:
            case DataType.ANY:
                pass

                return values

            case DataType.STRING:
                values = values.astype(
                    dtype=str,
                )

                return values

            case DataType.NUMERIC:
                values = to_numeric(
                    arg=values,
                )

                return values

            case DataType.DATE_TIME:
                values = to_datetime(
                    arg=values,
                )

                return values

            case DataType.TIME_DELTA:
                values = to_timedelta(
                    arg=values,
                )

                return values

            case _:
                raise NotImplementedError(
                    f'Unhandled data type conversion: {self.data_type} !'
                )

    def cast_source_target_data_type(
        self,
        source: Series,
        target: Series,
    ) -> Tuple[Series, Series]:
        """
        Casts source and target data to appropriate types given extension requirements.
        Tries not to cast data unless necessary.

        :param source: Source data to convert.
        :param target: Target data to convert.
        :return: Converted source and target data.
        """

        match self.data_type:
            case DataType.ANY:
                if any(
                    [
                        equivalence_check(source) & equivalence_check(target)
                        for equivalence_check in self.EQUIVALENT_DTYPE_CHECKS
                    ]
                ):
                    pass

                else:
                    source = source.astype(
                        dtype=str,
                    )

                    target = target.astype(
                        dtype=str,
                    )

                return source, target

            case DataType.STRING:
                source = source.astype(
                    dtype=str,
                )

                target = target.astype(
                    dtype=str,
                )

                return source, target

            case DataType.NUMERIC:
                source = to_numeric(
                    arg=source,
                )

                target = to_numeric(
                    arg=target,
                )

                return source, target

            case DataType.DATE_TIME:
                source = to_datetime(
                    arg=source,
                )

                target = to_datetime(
                    arg=target,
                )

                return source, target

            case DataType.TIME_DELTA:
                source = to_timedelta(
                    arg=source,
                )

                target = to_timedelta(
                    arg=target,
                )

                return source, target

            case _:
                raise NotImplementedError(
                    f'Unhandled data type conversion: {self.data_type} !'
                )
