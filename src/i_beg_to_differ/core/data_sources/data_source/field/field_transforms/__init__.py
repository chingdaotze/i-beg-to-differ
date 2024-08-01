from typing import (
    List,
    Dict,
    Self,
)
from pathlib import Path

from zipfile import ZipFile
from pandas import (
    Series,
    DataFrame,
)

from .....ib2d_file.ib2d_file_element import IB2DFileElement
from .....base import log_exception
from .....wildcards_sets import WildcardSets
from .field_transform import FieldTransform


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

        return ' | '.join(
            [str(transform) for transform in self.transforms],
        )

    def __iter__(
        self,
    ) -> Self:

        return self

    def __next__(
        self,
    ) -> FieldTransform:

        for transform in self.transforms:
            yield transform

    @classmethod
    @log_exception
    def deserialize(
        cls,
        instance_data: Dict,
        working_dir_path: Path,
        ib2d_file: ZipFile,
        wildcard_sets: WildcardSets | None = None,
    ) -> Self:

        return FieldTransforms(
            working_dir_path=working_dir_path,
            transforms=[
                FieldTransform.deserialize(
                    instance_data=field_transform_data,
                    working_dir_path=working_dir_path,
                    ib2d_file=ib2d_file,
                    wildcard_sets=wildcard_sets,
                )
                for field_transform_data in instance_data["transforms"]
            ],
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
