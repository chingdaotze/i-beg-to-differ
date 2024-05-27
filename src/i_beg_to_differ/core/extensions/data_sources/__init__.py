from .. import Extensions
from ...compare_sets.compare_set.compare.table.data_source import DataSource


class DataSources[DataSource](
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
        )

        # TODO: Load all extensions
