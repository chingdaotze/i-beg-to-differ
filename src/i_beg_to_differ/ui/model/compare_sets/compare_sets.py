from pathlib import Path

from PySide6.QtWidgets import QMenu

from ..model_base import ModelBase
from ....core.compare_sets import CompareSets
from ....core.wildcards_sets import WildcardSets
from ...view.main_window.main_widget.object_viewer import ObjectViewer
from ....core.compare_sets.compare_set import CompareSet
from .compare_set import ModelCompareSet
from ...widgets import (
    Dialog,
    LineEdit,
)


class ModelCompareSets(
    ModelBase,
):

    current_state: CompareSets
    working_dir_path: Path
    object_viewer: ObjectViewer

    def __init__(
        self,
        compare_sets: CompareSets,
        wildcard_sets: WildcardSets,
        object_viewer: ObjectViewer,
        working_dir_path: Path,
    ):

        ModelBase.__init__(
            self=self,
            current_state=compare_sets,
            wildcard_sets=wildcard_sets,
        )

        self.working_dir_path = working_dir_path
        self.object_viewer = object_viewer

        for compare_set in self.current_state.compare_sets.values():

            self.appendRow(
                ModelCompareSet(
                    compare_set=compare_set,
                    wildcard_sets=self.wildcard_sets,
                    object_viewer=self.object_viewer,
                    working_dir_path=working_dir_path,
                )
            )

    def add_compare_set(
        self,
    ) -> None:

        # Create / show Dialog
        dialog = Dialog(
            title='New Compare Set',
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

        # Create CompareSet object and update model
        compare_set_name = input_widget.text()

        compare_set = CompareSet(
            name=compare_set_name,
        )

        self.current_state.append(
            compare_set=compare_set,
        )

        self.appendRow(
            ModelCompareSet(
                compare_set=compare_set,
                wildcard_sets=self.wildcard_sets,
                working_dir_path=self.working_dir_path,
                object_viewer=self.object_viewer,
            )
        )

    @property
    def context_menu(
        self,
    ) -> QMenu:

        menu = QMenu()

        menu.addAction(
            'Add Compare Set',
            self.add_compare_set,
        )

        return menu
