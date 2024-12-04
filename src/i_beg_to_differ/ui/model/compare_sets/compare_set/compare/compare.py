from PySide6.QtWidgets import QWidget

from ....model_base_object_viewer import ModelBaseObjectViewer
from ......core.compare_sets.compare_set.compare import Compare
from .compare_object_viewer_widget import CompareObjectViewerWidget


class ModelCompare(
    ModelBaseObjectViewer,
):

    current_state: Compare

    def __init__(
        self,
        object_name: str,
        compare: Compare,
    ):

        ModelBaseObjectViewer.__init__(
            self=self,
            current_state=compare,
            object_name=object_name,
        )

    @property
    def object_viewer_widget(
        self,
    ) -> QWidget | None:

        return CompareObjectViewerWidget(
            compare=self.current_state,
        )
