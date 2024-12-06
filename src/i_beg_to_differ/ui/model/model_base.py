from __future__ import annotations
from typing import Any
from functools import cached_property

from PySide6.QtGui import QStandardItem

from ...core.base import Base


class ModelBase(
    QStandardItem,
):

    _base_state: int
    current_state: Base
    _object_name: str | None

    def __init__(
        self,
        current_state: Base,
        object_name: str = None,
    ):

        QStandardItem.__init__(
            self,
        )

        self._object_name = object_name

        self.base_state = current_state
        self.current_state = current_state

        self.setEditable(
            False,
        )

        self.setText(
            self.object_name,
        )

    @property
    def base_state(
        self,
    ) -> int:

        return self._base_state

    @base_state.setter
    def base_state(
        self,
        value: Any,
    ) -> None:

        self._base_state = hash(
            value,
        )

    def appendRow(
        self,
        item: 'ModelBase',
    ) -> None:

        type_name = QStandardItem(
            type(
                item.current_state,
            ).__name__,
        )

        type_name.setEditable(
            False,
        )

        modified_indicator = QStandardItem(
            item.modified_indicator,
        )

        modified_indicator.setEditable(
            False,
        )

        QStandardItem.appendRow(
            self,
            [
                item,
                type_name,
                modified_indicator,
            ],
        )

    @cached_property
    def object_type(
        self,
    ) -> str:

        return type(
            self.current_state,
        ).__name__

    @property
    def is_modified(
        self,
    ) -> bool:

        return (
            hash(
                self.current_state,
            )
            != self.base_state
        )

    @property
    def modified_indicator(
        self,
    ) -> str:

        if self.is_modified:
            return '*'

        else:
            return ''

    @property
    def object_name(
        self,
    ) -> str:

        if isinstance(self._object_name, str):
            return self._object_name

        else:
            return str(
                self.current_state,
            )