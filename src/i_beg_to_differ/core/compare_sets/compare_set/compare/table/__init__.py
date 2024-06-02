from pandas import DataFrame

from .data_source import DataSource


class Table:
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

        self.data_source = data_source

    def __str__(
        self,
    ) -> str:

        return str(
            self.data_source,
        )

    def __repr__(
        self,
    ) -> str:

        return str(
            self,
        )

    def load(
        self,
    ) -> None:

        self.data = self.data_source.load()

    # TODO: Implement compare methods
