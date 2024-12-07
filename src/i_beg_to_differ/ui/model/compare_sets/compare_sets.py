from pathlib import Path

from PySide6.QtWidgets import QMenu

from ..model_base import ModelBase
from ....core.compare_sets import CompareSets
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

    def __init__(
        self,
        compare_sets: CompareSets,
        working_dir_path: Path,
    ):

        ModelBase.__init__(
            self=self,
            current_state=compare_sets,
        )

        self.working_dir_path = working_dir_path

        for name, compare_set in self.current_state.compare_sets.items():

            self.appendRow(
                ModelCompareSet(
                    object_name=name,
                    compare_set=compare_set,
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

        compare_set = CompareSet()

        self.current_state[compare_set_name] = compare_set

        self.appendRow(
            ModelCompareSet(
                object_name=compare_set_name,
                compare_set=compare_set,
                working_dir_path=self.working_dir_path,
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
