from abc import abstractmethod

from PySide6.QtWidgets import QWidget

from .model_base import ModelBase
from ...core.base import Base


class ModelBaseObjectViewer(
    ModelBase,
):
    """
    QStandardItem for objects that render in an Object Viewer. Relies on Extension to provide Object Viewer widget.
    """

    def __init__(
        self,
        current_state: Base,
        object_name: str = None,
    ):

        ModelBase.__init__(
            self=self,
            current_state=current_state,
            object_name=object_name,
        )

    @property
    @abstractmethod
    def object_viewer_widget(
        self,
    ) -> QWidget:
        """
        Abstract method to provide an Object Viewer widget.

        :return:
        """
