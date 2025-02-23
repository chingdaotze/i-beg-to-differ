"""
Contains definition of the DataSourceExtensions class.
"""

from i_beg_to_differ.extensions import data_sources
from . import Extensions


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
