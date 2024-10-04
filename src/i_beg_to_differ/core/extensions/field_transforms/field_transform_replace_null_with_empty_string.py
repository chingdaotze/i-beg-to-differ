from pathlib import Path
from typing import (
    Dict,
    Self,
)
from zipfile import ZipFile

from pandas import Series

from ...data_sources.data_source.field.field_transforms.field_transform import (
    FieldTransform,
)
from ...wildcards_sets import WildcardSets
from ...base import log_exception

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

    def transform(
        self,
        values: Series,
    ) -> Series:
        """
        Transforms values in a single Field.

        :param values: Values to transform.
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
            "extension_id": self.extension_id,
            "parameters": None,
        }
