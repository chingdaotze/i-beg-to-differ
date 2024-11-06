from typing import Dict

from PySide6.QtWidgets import (
    QWidget,
)

from .dict_table_widget import DictTableWidget
from ........core.wildcards_sets.wildcard_field import WildcardField


class WildcardDictTableWidget(
    DictTableWidget,
):

    values = Dict[WildcardField, WildcardField]

    def __init__(
        self,
        values: Dict[WildcardField, WildcardField],
        key_column: str = 'Parameter',
        value_column: str = 'Value',
        parent: QWidget | None = None,
    ):

        DictTableWidget.__init__(
            self,
            values=values,
            key_column=key_column,
            value_column=value_column,
            parent=parent,
        )

    @staticmethod
    def key_to_str(
        key: WildcardField,
    ) -> str:

        return key.base_value

    @staticmethod
    def str_to_key(
        key: str,
    ) -> WildcardField:

        return WildcardField(
            base_value=key,
        )

    @staticmethod
    def value_to_str(
        value: WildcardField,
    ) -> str:

        return value.base_value

    @staticmethod
    def str_to_value(
        value: str,
    ) -> WildcardField:

        return WildcardField(
            base_value=value,
        )
