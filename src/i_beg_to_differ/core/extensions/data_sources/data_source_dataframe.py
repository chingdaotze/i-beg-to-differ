from pathlib import Path
from typing import (
    Dict,
    Self,
)
from zipfile import ZipFile

from pandas import DataFrame

from ...data_sources.data_source import DataSource
from ...base import log_exception
from ...wildcards_sets import WildcardSets


class DataSourceDataFrame(
    DataSource,
):
    """
    DataFrame data source.
    """

    data: DataFrame
    """
    DataFrame.
    """

    extension_name = 'DataFrame'

    def __init__(
        self,
        data: DataFrame,
        description: str | None = None,
    ):

        DataSource.__init__(
            self=self,
            description=description,
        )

        self.data = data

    def __str__(
        self,
    ) -> str:

        return f'{self.extension_name}: {id(self)}'

    def load(
        self,
    ) -> Self:
        self.cache = self.data

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

        return DataSourceDataFrame(
            data=DataFrame(
                data=instance_data['parameters']['data'],
            ),
        )

    @log_exception
    def serialize(
        self,
        ib2d_file: ZipFile,
    ) -> Dict:

        return {
            'extension_id': str(self),
            'parameters': {
                'data': self.data.to_dict(),
            },
        }

    @property
    def native_types(
        self,
    ) -> Dict[str, str]:

        return {column: str.__name__ for column in self.cache}
