from pandas import DataFrame

from .....base import (
    Base,
    log_exception,
    log_runtime,
)
from .data_source import DataSource


class Table(
    Base,
):
    """
    Table object.
    """

    data_source: DataSource
    """
    Data source object.
    """

    data: DataFrame
    """
    Data source data as a DataFrame.
    """

    def __init__(
        self,
        data_source: DataSource,
    ):
        Base.__init__(
            self=self,
            module_name=__name__,
        )

        self.data_source = data_source

    def __str__(
        self,
    ) -> str:

        return str(
            self.data_source,
        )

    @log_exception
    @log_runtime
    def load(
        self,
    ) -> None:

        self.data = self.data_source.load()

    # TODO: Implement compare methods
