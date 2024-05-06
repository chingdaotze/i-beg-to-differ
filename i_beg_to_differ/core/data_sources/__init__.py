from ..registered_types import RegisteredTypes
from .data_source import DataSource


class DataSources[DataSource](
    RegisteredTypes,
):
    """
    Contains and manages all DataSource types for this package.
    """

    def __init__(
        self,
    ):
        RegisteredTypes.__init__(
            self=self,
        )