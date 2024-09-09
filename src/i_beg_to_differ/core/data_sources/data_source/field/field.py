from typing import (
    Dict,
    List,
    TYPE_CHECKING,
)

from pandas import Series

from ....base import Base, log_exception
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

    field_transforms: Dict[FieldTransforms, Series | None]
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
        self.field_transforms = self.manager.dict()

    def __str__(
        self,
    ) -> str:

        return str(
            self.name,
        )

    def __getitem__(
        self,
        __field_transforms: FieldTransforms | List[FieldTransform] | None,
    ) -> Series:

        field_transforms = self.__convert_field_transforms(
            field_transforms=__field_transforms,
        )

        self.init_field_transforms(
            field_transforms=field_transforms,
        )

        values = self.field_transforms[field_transforms]

        return values

    @staticmethod
    def __convert_field_transforms(
        field_transforms: FieldTransforms | List[FieldTransform] | None,
    ) -> FieldTransforms:

        if field_transforms is None:
            field_transforms = FieldTransforms()

        elif isinstance(field_transforms, list):
            field_transforms = FieldTransforms(
                transforms=field_transforms,
            )

        return field_transforms

    def init_field_transforms(
        self,
        field_transforms: FieldTransforms | List[FieldTransform] | None,
    ) -> None:
        """
        Initializes a sequence of field transforms.

        :param field_transforms: Field transforms to initialize.
        :return:
        """

        field_transforms = self.__convert_field_transforms(
            field_transforms=field_transforms,
        )

        self.append(
            field_transforms,
        )

        values = self.field_transforms[field_transforms]

        if values is None:
            values = field_transforms.apply(
                values=self.data_source.cache[str(self.name)],
            )

            self.field_transforms[field_transforms] = values

    @log_exception
    def append(
        self,
        field_transforms: FieldTransforms | List[FieldTransform] | None,
    ) -> None:
        """
        Add field transforms to the collection of field transforms for this field.
        Field transform will not be calculated.

        :param field_transforms: Transforms to add.
        :return:
        """

        field_transforms = self.__convert_field_transforms(
            field_transforms=field_transforms,
        )

        if field_transforms not in self.field_transforms:
            self.field_transforms[field_transforms] = None

    @log_exception
    def remove(
        self,
        __field_transforms: FieldTransforms | List[FieldTransform] | None,
    ) -> None:
        """
        Delete field transforms from the collection of field transforms for this field.

        :param __field_transforms: Transforms to delete.
        :return:
        """

        field_transforms = self.__convert_field_transforms(
            field_transforms=__field_transforms,
        )

        del self.field_transforms[field_transforms]

    @property
    @log_exception
    def native_type(
        self,
    ) -> str:
        """
        Native data type for this field.

        :return: Native data type.
        """

        return self.data_source.native_types[str(self.name)]

    @property
    @log_exception
    def py_type(
        self,
    ) -> str:
        """
        Python data type for this field.

        :return: Python data type.
        """

        return self.data_source.py_types[str(self.name)]
