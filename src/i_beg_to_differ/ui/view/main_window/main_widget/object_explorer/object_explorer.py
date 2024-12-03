from PySide6.QtWidgets import QTreeView
from PySide6.QtCore import QModelIndex

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
        item: ModelBase,
    ) -> None:

        # TODO: Check if item is already opened and activate tab. Do not allow duplicate items.

        if isinstance(item, ModelBaseObjectViewer):
            object_viewer_widget = item.object_viewer_widget

            self.object_viewer.addTab(
                object_viewer_widget,
                f'{item.object_type}: {item.object_name}',
            )

            self.object_viewer.setCurrentWidget(
                object_viewer_widget,
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
