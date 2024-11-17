from .....base import (
    Base,
)
from .....input_fields.wildcard_input_fields import WildcardInputField
from .....data_sources.data_source.field.field_transforms import FieldTransforms
from .....wildcards_sets import WildcardSets


class FieldPointer(
    Base,
):
    """
    Points at a particular field within a Data Source. Offers additional attributes for the compare engine.
    """

    field_name: WildcardInputField
    """
    Name of a field within a Data Source.
    """

    field_name_alias: str
    """
    Human-friendly display value.
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

        self.field_name = WildcardInputField(
            base_value=field_name,
            wildcard_sets=wildcard_sets,
        )

        self.field_name_alias = str(
            self.field_name,
        )

        if transforms is None:
            self.transforms = FieldTransforms()

        else:
            self.transforms = transforms

    def __str__(
        self,
    ) -> str:

        return self.field_ref

    @property
    def field_ref(
        self,
    ) -> str:
        """
        Pointer to a field within a Data Source.
        """

        field_name = f'[{self.field_name}]'

        if self.transforms:
            field_name += f' >> {self.transforms}'

        return field_name

    @property
    def field_name_short(
        self,
    ) -> str:
        """
        Truncated identifier for the field, used in reports.
        """

        field_name = f'[{self.field_name}]'

        if self.transforms:
            field_name += '(T*)'

        return field_name
