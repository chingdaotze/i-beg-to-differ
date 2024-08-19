from pathlib import Path
from typing import (
    Dict,
    Self,
)
from zipfile import ZipFile

from pandas import (
    DataFrame,
    read_excel,
)

from ...data_sources.data_source import DataSource
from ...base import log_exception
from ...wildcards_sets.wildcard_field import WildcardField
from ...wildcards_sets import WildcardSets


class DataSourceExcel(
    DataSource,
):

    path: WildcardField
    """
    Path to the ``*.xlsx`` file.
    """

    sheet: WildcardField
    """
    Name of the worksheet within the ``*.xlsx`` file.
    """

    extension_name = '*.xlsx File'

    def __init__(
        self,
        working_dir_path: Path,
        path: str,
        sheet: str,
        description: str | None = None,
        wildcard_sets: WildcardSets | None = None,
    ):

        DataSource.__init__(
            self=self,
            module_name=__name__,
            working_dir_path=working_dir_path,
            description=description,
        )

        self.path = WildcardField(
            base_value=path,
            wildcard_sets=wildcard_sets,
        )

        self.sheet = WildcardField(
            base_value=sheet,
            wildcard_sets=wildcard_sets,
        )

    def __str__(
        self,
    ) -> str:

        return f'{self.extension_name}: \'[{self.path.base_value}]{self.sheet.base_value}\''

    def load(
        self,
    ) -> DataFrame:

        data_frame = read_excel(
            io=str(self.path),
            sheet_name=str(self.sheet),
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

        return DataSourceExcel(
            working_dir_path=working_dir_path,
            path=instance_data['parameters']['path'],
            sheet=instance_data['parameters']['sheet'],
            wildcard_sets=wildcard_sets,
        )

    @log_exception
    def serialize(
        self,
        ib2d_file: ZipFile,
    ) -> Dict:

        return {
            'extension_id': str(self),
            'parameters': {
                'path': self.path.base_value,
                'sheet': self.sheet.base_value,
            },
        }

    def py_types(
        self,
    ) -> Dict[str, str]:
        # TODO: Implement py_types

        return {}

    def native_types(
        self,
    ) -> Dict[str, str]:
        # TODO: Implement native_types

        return {}
