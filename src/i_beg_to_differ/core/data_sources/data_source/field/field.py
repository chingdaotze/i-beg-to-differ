from typing import (
    Dict,
    List,
    TYPE_CHECKING,
)

from pandas import Series

from ....base import Base
from ....wildcards_sets.wildcard_field import WildcardField
from ....wildcards_sets import WildcardSets
from .field_transforms import FieldTransforms
from .field_transforms.field_transform import FieldTransform

if TYPE_CHECKING:
    from ...data_source import DataSource


class Field(
    Base,
):
    """
    Abstraction layer over the data. Primarily responsible for
    managing transforms over the base data layer.
    """

    name: WildcardField
    """
    Name of this field.
    """

    data_source: 'DataSource'
    """
    Base data layer.
    """

    transforms: Dict[FieldTransforms, Series | None]
    """
    Dictionary of transformations that apply to this field, and corresponding values.
    """

    def __init__(
        self,
        name: str,
        data_source: 'DataSource',
        wildcard_sets: WildcardSets | None = None,
    ):

        Base.__init__(
            self=self,
        )

        self.name = WildcardField(
            base_value=name,
            wildcard_sets=wildcard_sets,
        )
        self.data_source = data_source
        self.transforms = self.manager.dict()

    def __str__(
        self,
    ) -> str:

        return str(self.name)

    def __getitem__(
        self,
        __field_transforms: FieldTransforms,
    ) -> Series:

        if __field_transforms not in self.transforms:
            self.append(
                __field_transforms,
            )

        values = self.transforms[__field_transforms]

        if values is None:
            values = __field_transforms.apply(
                values=self.transforms[FieldTransforms()],
            )

            self.transforms[__field_transforms] = values

        return values

    def init_transform(
        self,
        field_transform: FieldTransform,
    ) -> None:
        """
        Initializes a single field transform.

        :param field_transform: Field transform to initialize.
        :return:
        """

    def init_transforms(
        self,
        field_transforms: List[FieldTransform],
    ) -> None:
        """
        Initializes a list of field transforms in parallel.

        :param field_transforms: List of field transforms to initialize.
        :return:
        """

        pass

    def append(
        self,
        __field_transforms: FieldTransforms | List[FieldTransform],
    ) -> None:
        """
        Add field transforms to the collection of field transforms for this field.

        :param __field_transforms: Transforms to add.
        :return:
        """

        if isinstance(__field_transforms, list):
            __field_transforms = FieldTransforms(
                transforms=__field_transforms,
            )

        self.transforms[__field_transforms] = None

    def remove(
        self,
        __field_transforms: FieldTransforms | List[FieldTransform],
    ) -> None:
        """
        Delete field transforms from the collection of field transforms for this field.

        :param __field_transforms: Transforms to delete.
        :return:
        """

        if isinstance(__field_transforms, list):
            __field_transforms = FieldTransforms(
                transforms=__field_transforms,
            )

        del self.transforms[__field_transforms]

    @property
    def native_type(
        self,
    ) -> str:
        """
        Native data type for this field.

        :return: Native data type.
        """

        return self.data_source.native_types[str(self.name)]

    @property
    def py_type(
        self,
    ) -> str:
        """
        Python data type for this field.

        :return: Python data type.
        """

        return self.data_source.py_types[str(self.name)]
