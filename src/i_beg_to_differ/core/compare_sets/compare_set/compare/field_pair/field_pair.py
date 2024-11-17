from abc import ABC

from .....base import Base
from .field_pointer import FieldPointer
from .....wildcards_sets import WildcardSets


class FieldPair(
    Base,
    ABC,
):
    """
    Pair of Fields. Functions as a pointer to underlying
    Data Source > Field > Transform data structure.
    """

    source_field_pointer: FieldPointer
    """
    Source field pointer.
    """

    target_field_pointer: FieldPointer
    """
    Target field pointer.
    """

    def __init__(
        self,
        source_field_pointer: FieldPointer | str,
        target_field_pointer: FieldPointer | str,
        wildcard_sets: WildcardSets | None = None,
    ):

        Base.__init__(
            self=self,
        )

        if isinstance(source_field_pointer, str):
            source_field_pointer = FieldPointer(
                field_name=source_field_pointer,
                wildcard_sets=wildcard_sets,
            )

        self.source_field_pointer = source_field_pointer

        if isinstance(target_field_pointer, str):
            target_field_pointer = FieldPointer(
                field_name=target_field_pointer,
                wildcard_sets=wildcard_sets,
            )

        self.target_field_pointer = target_field_pointer

    def __str__(
        self,
    ) -> str:

        return f'{self.source_field_name} | {self.target_field_name}'

    @property
    def source_field_name(
        self,
    ) -> str:
        """
        Unique identifier for the source field.

        :return:
        """

        return f'src.{self.source_field_pointer}'

    @property
    def source_field_name_short(
        self,
    ) -> str:
        """
        Truncated identifier for the source field, used in reports.

        :return:
        """

        return f'src.{self.source_field_pointer.field_name_short}'

    @property
    def target_field_name(
        self,
    ) -> str:
        """
        Unique identifier for the target field.

        :return:
        """

        return f'tgt.{self.target_field_pointer}'

    @property
    def target_field_name_short(
        self,
    ) -> str:
        """
        Truncated identifier for the target field, used in reports.

        :return:
        """

        return f'tgt.{self.target_field_pointer.field_name_short}'
