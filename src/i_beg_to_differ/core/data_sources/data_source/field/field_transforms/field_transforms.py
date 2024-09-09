from typing import (
    List,
    ClassVar,
    Dict,
    Self,
    Iterator,
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
        transforms: List[FieldTransform] | None = None,
    ):
        IB2DFileElement.__init__(
            self=self,
        )

        if transforms is None:
            self.transforms = []

        else:
            self.transforms = transforms

    def __str__(
        self,
    ) -> str:

        if self.transforms:
            return ' >> '.join(
                [str(transform) for transform in self.transforms],
            )
        else:
            return 'None'

    def __bool__(
        self,
    ) -> bool:
        if self.transforms:
            return True

        else:
            return False

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
    ) -> Iterator:

        return iter(
            self.transforms,
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

    @log_exception
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

    @log_exception
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

    @log_exception
    def apply(
        self,
        values: Series,
    ) -> Series:

        for transform in self:

            values = transform.transform(
                values=values,
            )

        return values
