from typing import TYPE_CHECKING

from PySide6.QtWidgets import QTabWidget

if TYPE_CHECKING:
    from ....model.model_base_object_viewer import ModelBaseObjectViewer


class ObjectViewer(
    QTabWidget,
):

    def __init__(
        self,
        parent,
    ):

        QTabWidget.__init__(
            self,
            parent=parent,
        )

        self.setTabsClosable(
            True,
        )

        self.tabCloseRequested.connect(
            self.close_tab,
        )

    def close_tab(
        self,
        index,
    ) -> None:

        self.removeTab(
            index,
        )

    def open(
        self,
        item: 'ModelBaseObjectViewer',
    ) -> None:
        # TODO: Check if item is already opened and activate tab. Do not allow duplicate items.

        object_viewer_widget = item.object_viewer_widget

        self.addTab(
            object_viewer_widget,
            f'{item.object_type}: {item.text()}',
        )

        self.setCurrentWidget(
            object_viewer_widget,
        )
