from pandas import Series

from .....base import (
    Base,
)
from .....wildcards_sets.wildcard_field import WildcardField
from .....data_sources.data_source.field.field_transforms import FieldTransforms
from ..data_source_reference import DataSourceReference
from .....wildcards_sets import WildcardSets


class FieldReference(
    Base,
):
    """
    Pointer to a Field within a Data Source.
    """

    field_name: WildcardField
    """
    Name of a field within a Data Source.
    """

    transforms: FieldTransforms
    """
    List of transforms applied to this field.
    """

    data_source_ref: DataSourceReference | None
    """
    Reference to a data source.
    """

    def __init__(
        self,
        field_name: str,
        transforms: FieldTransforms | None = None,
        data_source_ref: DataSourceReference | None = None,
        wildcard_sets: WildcardSets | None = None,
    ):

        Base.__init__(
            self=self,
        )

        self.data_source_ref = data_source_ref

        self.field_name = WildcardField(
            base_value=field_name,
            wildcard_sets=wildcard_sets,
        )

        if transforms is None:
            self.transforms = FieldTransforms()

        else:
            self.transforms = transforms

    def __str__(
        self,
    ) -> str:

        field_ref = str(
            self.field_name,
        )

        if self.transforms:
            field_ref += f' >> {self.transforms}'

        return field_ref

    @property
    def field_value(
        self,
    ) -> Series:

        assert self.data_source_ref is not None

        return self.data_source_ref.data_source[
            str(
                self.field_name,
            )
        ][self.transforms]

    def get_field_value(
        self,
    ) -> Series:

        return self.field_value
