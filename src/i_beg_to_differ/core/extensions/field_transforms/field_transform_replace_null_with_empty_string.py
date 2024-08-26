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


class FieldTransformReplaceNullWithEmptyString(
    FieldTransform,
):

    extension_name = 'Replace Null with Empty String'

    def __init__(
        self,
    ):

        FieldTransform.__init__(
            self=self,
        )

    def __str__(
        self,
    ) -> str:

        return self.extension_name

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

        # TODO: Implement transform.

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

        return FieldTransformReplaceNullWithEmptyString()

    @log_exception
    def serialize(
        self,
        ib2d_file: ZipFile,
    ) -> Dict:

        return {
            "extension_id": str(self),
            "parameters": None,
        }
