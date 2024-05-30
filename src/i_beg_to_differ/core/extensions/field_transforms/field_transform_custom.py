from pathlib import Path
from typing import (
    Dict,
    Self,
)
from zipfile import ZipFile

from pandas import (
    DataFrame,
    Series,
)

from ...compare_sets.compare_set.compare.field_pair.field.field_transform import (
    FieldTransform,
)
from ...wildcards_sets import WildcardSets


class FieldTransformCustom(
    FieldTransform,
):

    _file_name: str
    _wildcard_sets: WildcardSets | None

    extension_id = '6b8d572d-49bb-4d15-b612-98ab2f81cb5a'
    extension_name = 'Custom'

    def __init__(
        self,
        working_dir_path: Path,
        file_name: str,
        wildcard_sets: WildcardSets | None = None,
    ):

        FieldTransform.__init__(
            self=self,
            working_dir_path=working_dir_path,
        )

        self._file_name = file_name
        self._wildcard_sets = wildcard_sets

    def transform(
        self,
        raw_table: DataFrame,
        transformed_table: DataFrame,
        field: Series,
    ) -> Series:
        """
        Transforms values in a single Field.

        :param raw_table: Read-only copy of the original table.
        :param transformed_table: Read-only copy of the transformed table.
        :param field: Values to transform.
        :return: Transformed values.
        """

        # TODO: Load custom file, pass in current active wildcard set.

        pass

    @classmethod
    def deserialize(
        cls,
        instance_data: Dict,
        working_dir_path: Path,
        ib2d_file: ZipFile,
        wildcard_sets: WildcardSets | None = None,
    ) -> Self:

        return FieldTransformCustom(
            working_dir_path=working_dir_path,
            file_name=instance_data['parameters']['file_name'],
            wildcard_sets=wildcard_sets,
        )

    def serialize(
        self,
        ib2d_file: ZipFile,
    ) -> Dict:

        return {
            'extension_id': str(self),
            'parameters': {
                'file_name': self._file_name,
            },
        }
