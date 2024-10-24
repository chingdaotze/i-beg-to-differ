from copy import deepcopy
from functools import cached_property

from PySide6.QtGui import QStandardItem

from ...core.base import Base


class ModelBase(
    QStandardItem,
):

    base_state: Base
    current_state: Base

    def __init__(
        self,
        current_state: Base,
    ):

        QStandardItem.__init__(
            self,
        )

        self.base_state = deepcopy(
            current_state,
        )
        self.current_state = current_state

        self.setEditable(
            False,
        )

        self.setText(
            self.object_name,
        )

    @cached_property
    def object_type(
        self,
    ) -> str:

        return str(
            type(
                self.current_state,
            ),
        )

    @property
    def is_modified(
        self,
    ) -> bool:

        return self.current_state != self.base_state

    @property
    def object_name(
        self,
    ) -> str:

        return str(
            self.current_state,
        )

    def save(
        self,
    ) -> None:

        self.base_state = self.current_state

    def undo(
        self,
    ) -> None:

        self.current_state = self.base_state
