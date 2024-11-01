from pathlib import Path
from typing import (
    Dict,
    Self,
)
from zipfile import ZipFile

from pandas import read_csv

from i_beg_to_differ.core.data_sources.data_source import DataSource
from i_beg_to_differ.core.extensions.input_fields import PathInputField
from i_beg_to_differ.core.base import log_exception
from i_beg_to_differ.core.wildcards_sets import WildcardSets


class DataSourceCsv(
    DataSource,
):
    """
    *.csv file Data Source.
    """

    path: PathInputField
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

        self.path = PathInputField(
            label='*.csv File Path: ',
            path=path,
            wildcard_sets=wildcard_sets,
        )

    def __str__(
        self,
    ) -> str:

        return f'{self.extension_name}: \'{self.path.base_value}\''

    def load(
        self,
    ) -> Self:
        path = str(
            self.path,
        )

        self.log_info(
            msg=f'Loading *.csv file: {path} ...',
        )

        self.cache = read_csv(
            filepath_or_buffer=path,
            engine='pyarrow',
        )

        return self

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
