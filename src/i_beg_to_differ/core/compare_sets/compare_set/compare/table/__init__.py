from pandas import DataFrame

from .data_source import DataSource


class Table:
    """
    Table object.
    """

    data_source: DataSource
    data: DataFrame

    def __init__(
        self,
        data_source: DataSource,
    ):

        self.data_source = data_source

    # TODO: Implement compare methods
