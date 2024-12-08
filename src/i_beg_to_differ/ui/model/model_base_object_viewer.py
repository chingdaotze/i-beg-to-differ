from abc import abstractmethod

from PySide6.QtWidgets import (
    QWidget,
    QStatusBar,
)

from .model_base import ModelBase
from ...core.base import Base
from ...core.wildcards_sets import WildcardSets
from ..view.main_window.main_widget.object_viewer import ObjectViewer


class ModelBaseObjectViewer(
    ModelBase,
):
    """
    QStandardItem for objects that render in an Object Viewer. Relies on Extension to provide Object Viewer widget.
    """

    object_viewer: ObjectViewer

    def __init__(
        self,
        current_state: Base,
        wildcard_sets: WildcardSets,
        status_bar: QStatusBar,
        object_viewer: ObjectViewer,
    ):

        ModelBase.__init__(
            self=self,
            current_state=current_state,
            wildcard_sets=wildcard_sets,
            status_bar=status_bar,
        )

        self.object_viewer = object_viewer

    @property
    @abstractmethod
    def object_viewer_widget(
        self,
    ) -> QWidget:
        """
        Abstract method to provide an Object Viewer widget.

        :return:
        """

    def open_in_object_viewer(
        self,
    ):
        self.object_viewer.open(
            item=self,
        )
