from typing import (
    List,
    ClassVar,
    Dict,
    Self,
)
from pathlib import Path

from zipfile import ZipFile
from pandas import Series

from .....ib2d_file.ib2d_file_element import IB2DFileElement
from .field_transform import FieldTransform
from .....extensions.field_transforms import FieldTransformExtensions
from .....base import log_exception
from .....wildcards_sets import WildcardSets


class FieldTransforms(
    IB2DFileElement,
):
    """
    Sequence of field transforms.
    """

    transforms: List[FieldTransform]
    """
    List of transforms.
    """

    transform_extensions: ClassVar[FieldTransformExtensions] = (
        FieldTransformExtensions()
    )
    """
    All field transform extensions for this package.
    """

    def __init__(
        self,
        working_dir_path: Path,
        transforms: List[FieldTransform] | None = None,
    ):
        IB2DFileElement.__init__(
            self=self,
            module_name=__name__,
            working_dir_path=working_dir_path,
        )

        if transforms is None:
            self.transforms = []

        else:
            self.transforms = transforms

    def __str__(
        self,
    ) -> str:

        if self.transforms:
            return ' | '.join(
                [str(transform) for transform in self.transforms],
            )
        else:
            return 'None'

    def __getitem__(
        self,
        index: int,
    ) -> FieldTransform:

        return self.transforms[index]

    def __setitem__(
        self,
        index: int,
        transform: FieldTransform,
    ) -> None:

        self.transforms[index] = transform

    def __iter__(
        self,
    ) -> Self:

        return self

    def __next__(
        self,
    ) -> FieldTransform:

        for transform in self.transforms:
            yield transform

    def append(
        self,
        transform: FieldTransform,
    ) -> None:
        """
        Add field transform to the collection of field transforms.

        :param transform: Field transform to add.
        :return:
        """

        self.transforms.append(
            transform,
        )

    def remove(
        self,
        transform: FieldTransform,
    ) -> None:
        """
        Delete field transform from the collection of field transforms.

        :param transform: Field transform to delete.
        :return:
        """

        self.transforms.remove(
            transform,
        )

    @classmethod
    @log_exception
    def deserialize(
        cls,
        instance_data: Dict,
        working_dir_path: Path,
        ib2d_file: ZipFile,
        wildcard_sets: WildcardSets | None = None,
    ) -> Self:

        transforms = []

        for transform_data in instance_data:
            extension_id = transform_data['extension_id']
            field_transform_ = cls.transform_extensions[extension_id]

            transforms.append(
                field_transform_.deserialize(
                    instance_data=transform_data,
                    working_dir_path=working_dir_path,
                    ib2d_file=ib2d_file,
                    wildcard_sets=wildcard_sets,
                ),
            )

        return FieldTransforms(
            working_dir_path=working_dir_path,
            transforms=transforms,
        )

    @log_exception
    def serialize(
        self,
        ib2d_file: ZipFile,
    ) -> Dict:

        return {
            "transforms": [
                instance.serialize(
                    ib2d_file=ib2d_file,
                )
                for instance in self.transforms
            ],
        }

    def apply(
        self,
        values: Series,
    ) -> Series:

        for transform in self:

            values = transform.transform(
                values=values,
            )

        return values
