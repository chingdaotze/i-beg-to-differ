from pathlib import Path
from typing import (
    Dict,
    Self,
)
from zipfile import ZipFile

from pandas import read_csv

from ...data_sources.data_source import DataSource
from ...base import log_exception
from ...wildcards_sets.wildcard_field import WildcardField
from ...wildcards_sets import WildcardSets


class DataSourceCsv(
    DataSource,
):

    path: WildcardField
    """
    Path to the ``*.csv`` file.
    """

    extension_name = '*.csv File'

    def __init__(
        self,
        working_dir_path: Path,
        path: str,
        description: str | None = None,
        wildcard_sets: WildcardSets | None = None,
    ):

        DataSource.__init__(
            self=self,
            working_dir_path=working_dir_path,
            description=description,
        )

        self.path = WildcardField(
            base_value=path,
            wildcard_sets=wildcard_sets,
        )

    def __str__(
        self,
    ) -> str:

        return f'{self.extension_name}: "{self.path.base_value}"'

    def load(
        self,
    ) -> Self:

        self.cache = read_csv(
            filepath_or_buffer=str(self.path),
            engine='pyarrow',
            dtype_backend='pyarrow',
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
            working_dir_path=working_dir_path,
            path=instance_data['parameters']['path'],
            wildcard_sets=wildcard_sets,
        )

    @log_exception
    def serialize(
        self,
        ib2d_file: ZipFile,
    ) -> Dict:

        instance_data = DataSource.serialize(
            self=self,
            ib2d_file=ib2d_file,
        )

        instance_data['parameters'] = {
            'path': self.path.base_value,
        }

        return {
            'extension_id': str(self),
            'parameters': {
                'path': self.path.base_value,
            },
        }

    @property
    def native_types(
        self,
    ) -> Dict[str, str]:

        return {column: str.__name__ for column in self.cache}
