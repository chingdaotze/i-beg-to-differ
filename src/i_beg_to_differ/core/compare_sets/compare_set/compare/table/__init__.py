from typing import (
    List,
    Self,
)

from pandas import DataFrame

from .....base import (
    Base,
    log_exception,
    log_runtime,
)
from .....data_sources.data_source import DataSource


class Table(
    Base,
):
    """
    Transformed raw data source.
    """

    data_source: DataSource
    """
    Data source object.
    """

    data: DataFrame | None
    """
    Data source data as a DataFrame.
    """

    transforms: List[Transform]

    def __init__(
        self,
        data_source: DataSource,
    ):
        Base.__init__(
            self=self,
            module_name=__name__,
        )

        self.data_source = data_source
        self.data = None

    def __str__(
        self,
    ) -> str:

        return str(
            self.data_source,
        )

    def __eq__(
        self,
        other: Self,
    ) -> bool:

        if (
            self.data_source == other.data_source
            and self.transforms == other.transforms
        ):
            return True

        else:
            return False

    def __ne__(
        self,
        other: Self,
    ) -> bool:

        if self == other:
            return False
        else:
            return True

    @log_exception
    @log_runtime
    def load(
        self,
    ) -> None:

        self.data = self.data_source.load()
