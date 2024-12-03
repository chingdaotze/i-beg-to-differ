from pathlib import Path
from typing import (
    Dict,
    Self,
)
from zipfile import ZipFile

from pandas import (
    read_csv,
    DataFrame,
)

from i_beg_to_differ.core.data_sources.data_source import DataSource
from i_beg_to_differ.core.extensions.ui import WildcardFilePathInputField
from i_beg_to_differ.core.base import log_exception
from i_beg_to_differ.core.wildcards_sets import WildcardSets


class DataSourceCsv(
    DataSource,
):
    """
    *.csv file Data Source.
    """

    path: WildcardFilePathInputField
    """
    Path to the ``*.csv`` file.
    """

    extension_name = '*.csv File'

    def __init__(
        self,
        path: str,
        description: str | None = None,
        wildcard_sets: WildcardSets | None = None,
    ):

        DataSource.__init__(
            self=self,
            description=description,
        )

        self.path = WildcardFilePathInputField(
            path=path,
            file_dialog_caption='Open *.csv File',
            file_dialog_filter='Comma-Separated Value Files (*.csv)',
            wildcard_sets=wildcard_sets,
            title='File Path',
        )

    def __str__(
        self,
    ) -> str:

        return f'{self.extension_name}: \'{self.path.base_value}\''

    def load(
        self,
    ) -> DataFrame:
        path = str(
            self.path,
        )

        self.log_info(
            msg=f'Loading *.csv file: {path} ...',
        )

        return read_csv(
            filepath_or_buffer=path,
            engine='pyarrow',
        )

    @classmethod
    @log_exception
    def deserialize(
        cls,
        instance_data: Dict,
        working_dir_path: Path,
        ib2d_file: ZipFile,
        wildcard_sets: WildcardSets | None = None,
    ) -> Self:

        return DataSourceCsv(
            path=instance_data['parameters']['path'],
            wildcard_sets=wildcard_sets,
        )

    @log_exception
    def serialize(
        self,
        ib2d_file: ZipFile,
    ) -> Dict:

        return {
            'extension_id': self.get_extension_id(),
            'description': self.description.value,
            'parameters': {
                'path': self.path.base_value,
            },
        }

    @property
    def native_types(
        self,
    ) -> Dict[str, str]:

        return {column: str.__name__ for column in self.cache}
