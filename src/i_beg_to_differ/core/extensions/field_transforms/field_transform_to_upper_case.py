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


class FieldTransformToUpperCase(
    FieldTransform,
):

    def __init__(
        self,
        working_dir_path: Path,
    ):

        FieldTransform.__init__(
            self=self,
            working_dir_path=working_dir_path,
            extension_id='bdcb04a0-cf74-47c4-9cdc-59b78c8b9034',
            extension_name='Convert to upper case',
        )

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

        # TODO: Implement transform.

        pass

    @classmethod
    def deserialize(
        cls,
        instance_data: Dict,
        working_dir_path: Path,
        ib2d_file: ZipFile,
        wildcard_sets: WildcardSets | None = None,
    ) -> Self:

        return FieldTransformToUpperCase(
            working_dir_path=working_dir_path,
        )

    def serialize(
        self,
        ib2d_file: ZipFile,
    ) -> Dict:

        return {
            'extension_id': str(self),
            'parameters': None,
        }
