from ..data_sources.data_source import DataSource
from . import Extensions
from i_beg_to_differ.extensions import data_sources


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
            namespace_package=data_sources,
        )
