from ...data_sources.data_source import DataSource
from .. import Extensions


class DataSourceExtensions[DataSource](
    Extensions,
):
    """
    Contains and manages all DataSource types for this package.
    """

    def __init__(
        self,
    ):
        Extensions.__init__(
            self=self,
            path=__path__,
            name=__name__,
        )
