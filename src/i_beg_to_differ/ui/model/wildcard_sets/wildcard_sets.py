from PySide6.QtWidgets import QMenu

from ..model_base import ModelBase
from ....core.wildcards_sets import WildcardSets
from ....core.wildcards_sets.wildcard_set import WildcardSet
from .wildcard_set import ModelWildcardSet
from ...widgets import (
    Dialog,
    LineEdit,
)


class ModelWildcardSets(
    ModelBase,
):

    current_state: WildcardSets

    def __init__(
        self,
        wildcard_sets: WildcardSets,
    ):

        ModelBase.__init__(
            self=self,
            current_state=wildcard_sets,
        )

        for name, wildcard_set in self.current_state.wildcard_sets.items():

            self.appendRow(
                ModelWildcardSet(
                    object_name=name,
                    wildcard_set=wildcard_set,
                )
            )

    def add_wildcard_set(
        self,
    ) -> None:

        # Create / show Dialog
        dialog = Dialog(
            title='New Wildcard Set',
        )

        input_widget = LineEdit(
            parent=dialog,
        )

        dialog.layout.addWidget(
            input_widget,
            0,
            0,
        )

        dialog.exec()

        # Create WildcardSet object and update model
        wildcard_set_name = input_widget.text()

        wildcard_set = WildcardSet()

        self.current_state.wildcard_sets[wildcard_set_name] = wildcard_set

        self.appendRow(
            ModelWildcardSet(
                object_name=wildcard_set_name,
                wildcard_set=wildcard_set,
            )
        )

    @property
    def context_menu(
        self,
    ) -> QMenu:

        menu = QMenu()

        menu.addAction(
            'Add Wildcard Set',
            self.add_wildcard_set,
        )

        return menu
