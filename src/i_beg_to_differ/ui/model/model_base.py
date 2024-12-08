from __future__ import annotations
from typing import Any
from functools import cached_property
from abc import abstractmethod

from PySide6.QtGui import (
    QStandardItem,
    Qt,
)
from PySide6.QtWidgets import (
    QMenu,
    QStatusBar,
)

from ...core.base import Base
from ...core.wildcards_sets import WildcardSets


class ModelBase(
    QStandardItem,
):

    _base_state: int
    current_state: Base
    wildcard_sets: WildcardSets
    status_bar: QStatusBar

    def __init__(
        self,
        current_state: Base,
        wildcard_sets: WildcardSets,
        status_bar: QStatusBar,
    ):

        QStandardItem.__init__(
            self,
        )
        self.wildcard_sets = wildcard_sets
        self.status_bar = status_bar

        self.base_state = current_state
        self.current_state = current_state

        self.setEditable(
            False,
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

    def data(
        self,
        role: Qt.ItemDataRole = Qt.ItemDataRole.DisplayRole,
    ):

        if role == Qt.ItemDataRole.DisplayRole:
            return str(
                self.current_state,
            )

        return None

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
    @abstractmethod
    def context_menu(
        self,
    ) -> QMenu:
        """
        Generates a menu, defined by the object.
        """

    def open_in_object_viewer(
        self,
    ):
        self.object_viewer.open(
            item=self,
        )
