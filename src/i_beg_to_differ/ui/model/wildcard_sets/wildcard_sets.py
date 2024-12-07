from PySide6.QtWidgets import QMenu

from ..model_base import ModelBase
from ....core.wildcards_sets import WildcardSets
from ....core.wildcards_sets.wildcard_set import WildcardSet
from .wildcard_set import ModelWildcardSet
from ...widgets import (
    Dialog,
    LineEdit,
)
from ...view.main_window.main_widget.object_viewer import ObjectViewer


class ModelWildcardSets(
    ModelBase,
):

    current_state: WildcardSets
    object_viewer: ObjectViewer

    def __init__(
        self,
        wildcard_sets: WildcardSets,
        object_viewer: ObjectViewer,
    ):

        ModelBase.__init__(
            self=self,
            current_state=wildcard_sets,
            wildcard_sets=wildcard_sets,
        )

        self.object_viewer = object_viewer

        for wildcard_set in self.current_state.wildcard_sets.values():

            self.appendRow(
                ModelWildcardSet(
                    wildcard_set=wildcard_set,
                    wildcard_sets=self.current_state,
                    object_viewer=object_viewer,
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

        wildcard_set = WildcardSet(
            name=wildcard_set_name,
        )

        self.current_state.wildcard_sets[wildcard_set_name] = wildcard_set

        self.appendRow(
            ModelWildcardSet(
                wildcard_set=wildcard_set,
                wildcard_sets=self.current_state,
                object_viewer=self.object_viewer,
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
