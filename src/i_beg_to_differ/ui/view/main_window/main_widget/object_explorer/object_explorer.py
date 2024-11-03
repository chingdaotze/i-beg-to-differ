from PySide6.QtWidgets import QTreeView, QWidget
from PySide6.QtGui import QStandardItem

from .....model import Model
from .....model.base import ModelBase
from ..object_viewer import ObjectViewer


class ObjectExplorer(
    QTreeView,
):
    object_viewer: ObjectViewer

    def __init__(
        self,
        parent,
        object_viewer: ObjectViewer,
    ):

        QTreeView.__init__(
            self,
            parent=parent,
        )

        self.object_viewer = object_viewer

        self.setModel(
            Model(),
        )

        self.doubleClicked.connect(
            self.double_click,
        )

    def open_in_object_viewer(
        self,
        item: QStandardItem,
    ) -> None:

        if issubclass(type(item), ModelBase):
            item: ModelBase
            object_viewer_widget = item.object_viewer_widget

            if isinstance(object_viewer_widget, QWidget):
                self.object_viewer.addTab(
                    object_viewer_widget,
                    item.object_name,
                )

    def double_click(
        self,
        index,
    ) -> None:

        item = self.model().itemFromIndex(
            index,
        )

        self.open_in_object_viewer(
            item=item,
        )
