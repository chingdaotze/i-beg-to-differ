from pathlib import Path

from PySide6.QtWidgets import (
    QWidget,
    QTabWidget,
)

from ...model_base_object_viewer import ModelBaseObjectViewer
from .compare_set_description_widget import CompareSetDescriptionWidget
from .....core.compare_sets.compare_set import CompareSet
from .compare import ModelCompare


class ModelCompareSet(
    ModelBaseObjectViewer,
):

    compare_set_description_widget: CompareSetDescriptionWidget

    def __init__(
        self,
        object_name: str,
        compare_set: CompareSet,
        working_dir_path: Path,
    ):

        ModelBaseObjectViewer.__init__(
            self=self,
            current_state=compare_set,
            object_name=object_name,
        )

        self.compare_set_description_widget = CompareSetDescriptionWidget(
            compare_set=compare_set,
        )

        for name, compare in compare_set.compares.items():

            self.appendRow(
                ModelCompare(
                    object_name=name,
                    compare=compare,
                    working_dir_path=working_dir_path,
                )
            )

    @property
    def object_viewer_widget(
        self,
    ) -> QWidget:

        # Add description
        tab_widget = QTabWidget()

        tab_widget.addTab(
            self.compare_set_description_widget,
            'Description',
        )

        return tab_widget
