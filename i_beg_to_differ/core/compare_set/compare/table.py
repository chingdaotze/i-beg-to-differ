from pathlib import Path


from ...ib2d_file.ib2d_file_element import IB2DFileElement
from ...wildcards import Wildcards
from ...data_sources import DataSources
from ...data_sources.data_source import DataSource


class Table(
    IB2DFileElement,
):
    """
    Table object.
    """

    data_source: DataSource

    def __init__(
        self,
        working_dir_path: Path,
        data_source: DataSource,
        wildcards: Wildcards | None = None,
    ):

        IB2DFileElement.__init__(
            self=self,
            working_dir_path=working_dir_path,
            wildcards=wildcards,
        )

        self.data_source = data_source
