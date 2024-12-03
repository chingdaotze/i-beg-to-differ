from PySide6.QtWidgets import QWidget

from .model_base_object_viewer import ModelBaseObjectViewer
from ...core.extensions.extension import Extension


class ModelBaseExtension(
    ModelBaseObjectViewer,
):
    """
    QStandardItem for Extensions. Relies on Extension to provide Object Viewer widget.
    """

    current_state: Extension

    def __init__(
        self,
        current_state: Extension,
        object_name: str = None,
    ):

        ModelBaseObjectViewer.__init__(
            self=self,
            current_state=current_state,
            object_name=object_name,
        )

    @property
    def object_viewer_widget(
        self,
    ) -> QWidget:
        """
        Returns an Object Viewer widget defined in the Extension.

        :return:
        """

        return self.current_state.object_viewer_widget
