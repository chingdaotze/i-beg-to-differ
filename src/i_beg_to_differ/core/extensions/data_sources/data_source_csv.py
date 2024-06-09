from pathlib import Path
from typing import (
    Dict,
    Self,
)
from zipfile import ZipFile

from pandas import (
    DataFrame,
    read_csv,
)

from ...compare_sets.compare_set.compare.table.data_source import DataSource
from ...base import (
    log_exception,
    log_runtime,
)
from ...wildcards_sets.wildcard_field import WildcardField
from ...wildcards_sets import WildcardSets


class DataSourceCsv(
    DataSource,
):

    path: WildcardField
    """
    Path to the ``*.csv`` file.
    """

    extension_id = 'ba6cb274-e274-475a-bed3-6b7cb6f48247'
    extension_name = '*.csv file'

    def __init__(
        self,
        working_dir_path: Path,
        path: str,
        wildcard_sets: WildcardSets | None = None,
    ):

        DataSource.__init__(
            self=self,
            module_name=__name__,
            working_dir_path=working_dir_path,
        )

        self.path = WildcardField(
            base_value=path,
            wildcard_sets=wildcard_sets,
        )

    def __str__(
        self,
    ):

        return f'{self.extension_name}: \'{self.path.base_value}\''

    @log_exception
    @log_runtime
    def load(
        self,
    ) -> DataFrame:

        data_frame = read_csv(
            filepath_or_buffer=str(self.path),
            engine='pyarrow',
            dtype_backend='pyarrow',
        )

        return data_frame

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
