from .....base import (
    Base,
)
from .....wildcards_sets.wildcard_field import WildcardField
from .....data_sources.data_source.field.field_transforms import FieldTransforms
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

    def __init__(
        self,
        field_name: str,
        transforms: FieldTransforms | None = None,
        wildcard_sets: WildcardSets | None = None,
    ):

        Base.__init__(
            self=self,
        )

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
