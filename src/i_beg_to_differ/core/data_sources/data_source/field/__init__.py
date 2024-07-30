from pathlib import Path
from typing import (
    List,
    Dict,
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
from .field_transform import FieldTransform

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

    transforms: List[FieldTransform] | None
    """
    List of transformations to apply to this field.
    """

    def __init__(
        self,
        working_dir_path: Path,
        name: str,
        data_source: DataSource,
        transforms: List[FieldTransform] | None = None,
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
        self.transforms = transforms

    def __str__(
        self,
    ) -> str:

        return (
            str(self.name)
            + ' >> '
            + ' | '.join(
                [str(transform) for transform in self.transforms],
            )
        )

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
            "name": self.name.base_value,
            "transforms": [
                instance.serialize(
                    ib2d_file=ib2d_file,
                )
                for instance in self.transforms
            ],
        }

    @cached_property
    def native_type(
        self,
    ) -> str:

        # TODO: Get native type from data frame
        ...

    @cached_property
    def py_type(
        self,
    ) -> str:

        # TODO: Get Python type from data frame
        ...

    @cached_property
    def value(
        self,
    ) -> Series:

        # TODO: Get series from data frame and apply transformations
        ...
