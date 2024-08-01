from pathlib import Path
from typing import (
    Dict,
    List,
    Self,
    TYPE_CHECKING,
)
from zipfile import ZipFile
from functools import cached_property

from pandas import Series

from ....ib2d_file.ib2d_file_element import IB2DFileElement
from ....base import log_exception
from ....wildcards_sets.wildcard_field import WildcardField
from ....wildcards_sets import WildcardSets
from .field_transforms import FieldTransforms
from .field_transforms.field_transform import FieldTransform

if TYPE_CHECKING:
    from ...data_source import DataSource


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

    data_source: 'DataSource'
    """
    Parent data source.
    """

    transforms: Dict[FieldTransforms, Series | None]
    """
    Dictionary of transformations that apply to this field, and corresponding values.
    """

    def __init__(
        self,
        working_dir_path: Path,
        name: str,
        data_source: DataSource,
        transforms: List[FieldTransforms] | None = None,
        wildcard_sets: WildcardSets | None = None,
    ):

        IB2DFileElement.__init__(
            self=self,
            module_name=__name__,
            working_dir_path=working_dir_path,
        )

        self.name = WildcardField(
            base_value=name,
            wildcard_sets=wildcard_sets,
        )

        self.data_source = data_source

        self.transforms = {
            FieldTransforms(
                working_dir_path=self.working_dir_path,
            ): None,
        }

        if transforms is not None:
            self.transforms |= dict.fromkeys(
                transforms,
            )

    def __str__(
        self,
    ) -> str:

        return f'{str(self.name)} >> {str(self.transforms)}'

    def __getitem__(
        self,
        transforms: FieldTransforms,
    ) -> Series:

        if transforms not in self.transforms:
            self.append(
                transforms=transforms,
            )

        values = self.transforms[transforms]

        if values is None:
            values = transforms.apply(
                values=self.transforms[
                    FieldTransforms(
                        working_dir_path=self.working_dir_path,
                    )
                ]
            )

            self.transforms[transforms] = values

        return values

    def append(
        self,
        transforms: FieldTransforms | List[FieldTransform],
    ) -> None:
        """
        Add transforms to the collection of transforms for this field.

        :param transforms: Transforms to add.
        :return:
        """

        if isinstance(transforms, list):
            transforms = FieldTransforms(
                working_dir_path=self.working_dir_path,
                transforms=transforms,
            )

        self.transforms[transforms] = None

    def remove(
        self,
        transforms: FieldTransforms | List[FieldTransforms],
    ) -> None:
        """
        Delete transforms from the collection of transforms for this field.

        :param transforms: Transforms to delete.
        :return:
        """

        if isinstance(transforms, list):
            transforms = FieldTransforms(
                working_dir_path=self.working_dir_path,
                transforms=transforms,
            )

        del self.transforms[transforms]

    @classmethod
    @log_exception
    def deserialize(
        cls,
        instance_data: Dict,
        working_dir_path: Path,
        ib2d_file: ZipFile,
        data_source: 'DataSource',
        wildcard_sets: WildcardSets | None = None,
    ) -> Self:

        return Field(
            working_dir_path=working_dir_path,
            name=instance_data["name"],
            data_source=data_source,
            transforms=FieldTransforms.deserialize(
                instance_data=instance_data["transforms"],
                working_dir_path=working_dir_path,
                ib2d_file=ib2d_file,
                wildcard_sets=wildcard_sets,
            ),
        )

    @log_exception
    def serialize(
        self,
        ib2d_file: ZipFile,
    ) -> Dict:

        return {
            "name": self.name.base_value,
            "transforms": [
                transform.serialize(
                    ib2d_file=ib2d_file,
                )
                for transform in self.transforms.keys()
            ],
        }

    @cached_property
    def native_type(
        self,
    ) -> str:
        """
        Native data type for this field.

        :return: Native data type.
        """

        return self.data_source.native_types[str(self.name)]

    @cached_property
    def py_type(
        self,
    ) -> str:
        """
        Python data type for this field.

        :return: Python data type.
        """

        return self.data_source.py_types[str(self.name)]
