from pathlib import Path

from PySide6.QtWidgets import QWidget

from ....model_base_object_viewer import ModelBaseObjectViewer
from ......core.compare_sets.compare_set.compare import Compare
from .compare_object_viewer_widget import CompareObjectViewerWidget


class ModelCompare(
    ModelBaseObjectViewer,
):

    current_state: Compare
    working_dir_path: Path

    def __init__(
        self,
        object_name: str,
        compare: Compare,
        working_dir_path: Path,
    ):

        ModelBaseObjectViewer.__init__(
            self=self,
            current_state=compare,
            object_name=object_name,
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
