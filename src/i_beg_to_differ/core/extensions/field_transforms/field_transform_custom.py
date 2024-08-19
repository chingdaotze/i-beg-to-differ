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

from ...data_sources.data_source.field.field_transforms.field_transform import (
    FieldTransform,
)
from ...wildcards_sets import WildcardSets
from ...base import (
    log_exception,
    log_runtime,
)


class FieldTransformCustom(
    FieldTransform,
):

    file_name: str
    _wildcard_sets: WildcardSets | None

    extension_name = 'Custom Python Script'

    def __init__(
        self,
        working_dir_path: Path,
        file_name: str,
        wildcard_sets: WildcardSets | None = None,
    ):

        FieldTransform.__init__(
            self=self,
            module_name=__name__,
            working_dir_path=working_dir_path,
        )

        self.file_name = file_name
        self._wildcard_sets = wildcard_sets

    def __str__(
        self,
    ) -> str:

        return f'{self.extension_name}: {self.file_name}'

    @log_exception
    @log_runtime
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
    @log_exception
    def deserialize(
        cls,
        instance_data: Dict,
        working_dir_path: Path,
        ib2d_file: ZipFile,
        wildcard_sets: WildcardSets | None = None,
    ) -> Self:

        return FieldTransformCustom(
            working_dir_path=working_dir_path,
            file_name=instance_data["parameters"]["file_name"],
            wildcard_sets=wildcard_sets,
        )

    @log_exception
    def serialize(
        self,
        ib2d_file: ZipFile,
    ) -> Dict:

        return {
            "extension_id": str(self),
            "parameters": {
                "file_name": self.file_name,
            },
        }
