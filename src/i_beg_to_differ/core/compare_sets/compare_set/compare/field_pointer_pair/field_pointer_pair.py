from abc import ABC
from typing import ClassVar

from .....base import Base
from .field_pointer import FieldPointer
from .....wildcards_sets import WildcardSets
from .compare_rule import CompareRule
from .....extensions.compare_rules import CompareRuleExtensions


class FieldPointerPair(
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

    compare_rule: CompareRule
    """
    Comparison rule used to compare the source and target fields.
    """

    _compare_rule_extensions: ClassVar[CompareRuleExtensions] = CompareRuleExtensions()

    def __init__(
        self,
        source_field_pointer: FieldPointer | str,
        target_field_pointer: FieldPointer | str,
        wildcard_sets: WildcardSets | None = None,
        compare_rule: CompareRule | None = None,
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

        if compare_rule is None:
            self.compare_rule = self._compare_rule_extensions['compare_rule_equals']()

        else:
            self.compare_rule = compare_rule

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
