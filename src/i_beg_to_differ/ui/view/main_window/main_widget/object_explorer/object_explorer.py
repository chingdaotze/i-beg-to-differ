from PySide6.QtWidgets import (
    QTreeView,
    QStatusBar,
    QAbstractItemView,
    QWidget,
)
from PySide6.QtCore import QModelIndex
from PySide6.QtGui import QCursor

from .....model import Model
from .....model.model_base import ModelBase
from .....model.model_base_object_viewer import ModelBaseObjectViewer
from ..object_viewer import ObjectViewer


class ObjectExplorer(
    QTreeView,
):
    object_viewer: ObjectViewer

    def __init__(
        self,
        object_viewer: ObjectViewer,
        status_bar: QStatusBar,
        parent: QWidget | None = None,
    ):

        QTreeView.__init__(
            self,
            parent=parent,
        )

        self.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers,
        )

        self.object_viewer = object_viewer

        self.setModel(
            Model(
                status_bar=status_bar,
                object_viewer=self.object_viewer,
            ),
        )

        self.doubleClicked.connect(
            self.double_click,
        )

    def open_in_object_viewer(
        self,
        item: ModelBase,
    ) -> None:

        if isinstance(item, ModelBaseObjectViewer):
            self.object_viewer.open(
                item=item,
            )

    def double_click(
        self,
        index: QModelIndex,
    ) -> None:

        model = self.model()

        """
        index = model.index(
            index.row(),
            0,
        )
        """

        item = model.itemFromIndex(
            index,
        )

        self.open_in_object_viewer(
            item=item,
        )

    def contextMenuEvent(
        self,
        arg__1,
    ):

        index = self.currentIndex()

        item = self.model().itemFromIndex(
            index,
        )

        if isinstance(item, ModelBase):

            item.context_menu.exec_(
                QCursor.pos(),
            )
