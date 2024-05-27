from pathlib import Path
from typing import (
    Dict,
    Self,
)
from zipfile import ZipFile

from pandas import DataFrame

from ...compare_sets.compare_set.compare.table.data_source import DataSource
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

    def __init__(
        self,
        working_dir_path: Path,
        path: str,
        sheet: str,
        wildcard_sets: WildcardSets | None = None,
    ):

        DataSource.__init__(
            self=self,
            working_dir_path=working_dir_path,
            extension_id='44054bc8-978d-4f9a-b3d9-9e539fde5651',
            extension_name='*.xlsx file',
        )

        self.path = WildcardField(
            base_value=path,
            wildcard_sets=wildcard_sets,
        )

        self.sheet = WildcardField(
            base_value=sheet,
            wildcard_sets=wildcard_sets,
        )

    def __repr__(
        self,
    ):

        return f'{self.extension_name}: \'[{self.path.base_value}]{self.sheet.base_value}\''

    def load(
        self,
    ) -> DataFrame:

        # TODO: Load csv
        pass

    @classmethod
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
