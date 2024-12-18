from pathlib import Path
from typing import (
    Dict,
    Self,
)
from zipfile import ZipFile

from pandas import DataFrame

from i_beg_to_differ.core.data_sources.data_source import DataSource
from i_beg_to_differ.core.base import log_exception
from i_beg_to_differ.core.wildcards_sets import WildcardSets


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

    name: str

    def __init__(
        self,
        name: str,
        data: DataFrame | None = None,
        description: str | None = None,
    ):

        DataSource.__init__(
            self=self,
            description=description,
        )

        self.name = name

        if data is None:
            data = DataFrame()

        self.data = data

    def __str__(
        self,
    ) -> str:

        return self.name

    def load(
        self,
    ) -> DataFrame:
        return self.data

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
            'extension_id': self.get_extension_id(),
            'description': self.description.value,
            'parameters': {
                'data': self.data.to_dict(),
            },
        }

    @property
    def native_types(
        self,
    ) -> Dict[str, str]:

        return {column: str.__name__ for column in self.cache}
