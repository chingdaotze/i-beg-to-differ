from enum import StrEnum
from abc import (
    ABC,
    abstractmethod,
)
from typing import Dict
from pathlib import Path

from pandas import (
    DataFrame,
    Series,
)

from .....ib2d_file.ib2d_file_element import IB2DFileElement
from .....extensions.extension import Extension


class FieldPairCompareRuleLinkage(
    StrEnum,
):
    AND = 'and'
    OR = 'or'


class FieldPairCompareRule(
    IB2DFileElement,
    Extension,
    ABC,
):
    """
    Base field pair compare rule class.
    """

    parameters: Dict
    """
    Compare rule parameters.
    """

    linkage: FieldPairCompareRuleLinkage
    """
    Linkage to next compare rule.
    """

    def __init__(
        self,
        linkage: FieldPairCompareRuleLinkage,
    ):
        IB2DFileElement.__init__(
            self=self,
        )

        self.linkage = linkage

    @abstractmethod
    def compare(
        self,
        raw_table: DataFrame,
        transformed_table: DataFrame,
        source_field: Series,
        target_field: Series,
    ) -> Series:
        """
        Compares values between source and target fields.

        :param raw_table: Read-only copy of the original table.
        :param transformed_table: Read-only copy of the transformed table.
        :param source_field: Source field to compare.
        :param target_field: Target field to compare.
        :return: Series of booleans, where True indicates a match.
        """
