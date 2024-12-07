from pathlib import Path

from PySide6.QtWidgets import (
    QWidget,
    QMenu,
)

from ....model_base_object_viewer import ModelBaseObjectViewer
from ......core.compare_sets.compare_set.compare import Compare
from ......core.wildcards_sets import WildcardSets
from .....view.main_window.main_widget.object_viewer import ObjectViewer
from .compare_object_viewer_widget import CompareObjectViewerWidget


class ModelCompare(
    ModelBaseObjectViewer,
):

    current_state: Compare
    working_dir_path: Path

    def __init__(
        self,
        compare: Compare,
        wildcard_sets: WildcardSets,
        object_viewer: ObjectViewer,
        working_dir_path: Path,
    ):

        ModelBaseObjectViewer.__init__(
            self=self,
            current_state=compare,
            object_viewer=object_viewer,
            wildcard_sets=wildcard_sets,
        )

        self.working_dir_path = working_dir_path

    @property
    def object_viewer_widget(
        self,
    ) -> QWidget | None:

        return CompareObjectViewerWidget(
            compare=self.current_state,
            working_dir_path=self.working_dir_path,
        )

    @property
    def context_menu(
        self,
    ) -> QMenu:

        menu = QMenu()

        menu.addAction(
            'Open',
            self.open_in_object_viewer,
        )

        menu.addAction(
            'Delete',
        )  # TODO: Delete compare

        return menu
