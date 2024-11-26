from abc import ABC

from .....base import Base
from .field_reference import FieldReference
from .....data_sources.data_source.field.field_transforms import FieldTransforms
from .....wildcards_sets import WildcardSets


class FieldReferencePair(
    Base,
    ABC,
):
    """
    Pair of Field References. Functions as a pointer to underlying
    Data Source > Field > Transform data structure.
    """

    source_field_ref: FieldReference
    """
    Source field pointer.
    """

    target_field_ref: FieldReference
    """
    Target field pointer.
    """

    is_primary_key: bool
    """
    Indicator for whether this field pair is a primary key.
    """

    def __init__(
        self,
        source_field_name: str,
        target_field_name: str,
        source_field_transforms: FieldTransforms | None = None,
        target_field_transforms: FieldTransforms | None = None,
        wildcard_sets: WildcardSets | None = None,
    ):

        Base.__init__(
            self=self,
        )

        self.source_field_ref = FieldReference(
            field_name=source_field_name,
            transforms=source_field_transforms,
            wildcard_sets=wildcard_sets,
        )

        self.target_field_ref = FieldReference(
            field_name=target_field_name,
            transforms=target_field_transforms,
            wildcard_sets=wildcard_sets,
        )

    def __str__(
        self,
    ) -> str:

        return f'{self.source_field_ref} | {self.target_field_ref}'
