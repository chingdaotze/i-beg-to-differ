from PySide6.QtWidgets import (
    QStatusBar,
    QWidget,
)

from .model_base_object_viewer import ModelBaseObjectViewer
from ...core.extensions.extension import Extension
from ...core.wildcards_sets import WildcardSets
from ..view.main_window.main_widget.object_viewer import ObjectViewer


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
        wildcard_sets: WildcardSets,
        status_bar: QStatusBar,
        object_viewer: ObjectViewer,
    ):

        ModelBaseObjectViewer.__init__(
            self=self,
            current_state=current_state,
            wildcard_sets=wildcard_sets,
            status_bar=status_bar,
            object_viewer=object_viewer,
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
