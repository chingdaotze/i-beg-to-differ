from pathlib import Path
from typing import (
    List,
    Dict,
    Self,
)
from zipfile import ZipFile

from ......ib2d_file.ib2d_file_element import IB2DFileElement
from ......wildcards_sets.wildcard_field import WildcardField
from ......wildcards_sets import WildcardSets
from .field_transform import FieldTransform


class Field(
    IB2DFileElement,
):
    """
    Field object.
    """

    name: WildcardField
    """
    Name of this field.
    """

    py_type: str | None
    """
    Python data type.
    """

    native_type: str | None
    """
    Original data type.
    """

    transforms: List[FieldTransform] | None
    """
    List of transformations to apply to this field.
    """

    def __init__(
        self,
        working_dir_path: Path,
        name: str,
        transforms: List[FieldTransform] | None = None,
        wildcard_sets: WildcardSets | None = None,
    ):

        IB2DFileElement.__init__(
            self=self,
            working_dir_path=working_dir_path,
        )

        self.name = WildcardField(
            base_value=name,
            wildcard_sets=wildcard_sets,
        )

        self.transforms = transforms

        self.py_type = None
        self.native_type = None

    @classmethod
    def deserialize(
        cls,
        instance_data: Dict,
        working_dir_path: Path,
        ib2d_file: ZipFile,
        wildcard_sets: WildcardSets | None = None,
    ) -> Self:

        return Field(
            working_dir_path=working_dir_path,
            name=instance_data['name'],
            transforms=[
                FieldTransform.deserialize(
                    instance_data=field_transform_data,
                    working_dir_path=working_dir_path,
                    ib2d_file=ib2d_file,
                    wildcard_sets=wildcard_sets,
                )
                for field_transform_data in instance_data['transforms']
            ],
        )

    def serialize(
        self,
        ib2d_file: ZipFile,
    ) -> Dict:

        return {
            'name': self.name.base_value,
            'transforms': [
                instance.serialize(
                    ib2d_file=ib2d_file,
                )
                for instance in self.transforms
            ],
        }
