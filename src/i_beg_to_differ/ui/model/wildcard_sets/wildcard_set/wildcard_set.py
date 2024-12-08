from PySide6.QtWidgets import (
    QStatusBar,
    QWidget,
    QTabWidget,
    QMenu,
)

from ...model_base_object_viewer import ModelBaseObjectViewer
from .....core.wildcards_sets.wildcard_set import WildcardSet
from .wildcard_set_description_widget import WildcardSetDescriptionWidget
from .wildcard_set_widget import WildcardSetWidget
from .....core.wildcards_sets import WildcardSets
from ....view.main_window.main_widget.object_viewer import ObjectViewer


class ModelWildcardSet(
    ModelBaseObjectViewer,
):

    current_state: WildcardSet

    wildcard_set_description_widget: WildcardSetDescriptionWidget
    wildcard_set_widget: WildcardSetWidget

    def __init__(
        self,
        wildcard_set: WildcardSet,
        wildcard_sets: WildcardSets,
        status_bar: QStatusBar,
        object_viewer: ObjectViewer,
    ):

        ModelBaseObjectViewer.__init__(
            self=self,
            current_state=wildcard_set,
            wildcard_sets=wildcard_sets,
            status_bar=status_bar,
            object_viewer=object_viewer,
        )

        # Build description widget
        self.wildcard_set_description_widget = WildcardSetDescriptionWidget(
            wildcard_set=self.current_state,
        )

        # Build dictionary table widget
        self.wildcard_set_widget = WildcardSetWidget(
            wildcard_set=wildcard_set,
        )

    @property
    def object_viewer_widget(
        self,
    ) -> QWidget:

        # Add description
        tab_widget = QTabWidget()

        tab_widget.addTab(
            self.wildcard_set_description_widget,
            'Description',
        )

        # Add dict table
        tab_widget.addTab(
            self.wildcard_set_widget,
            'WildCards',
        )

        return tab_widget

    @property
    def context_menu(
        self,
    ) -> QMenu:

        menu = QMenu()

        menu.addAction(
            'Set Active',
        )  # TODO: Set this wildcard set as active

        menu.addAction(
            'Open',
            self.open_in_object_viewer,
        )

        menu.addAction(
            'Delete',
        )  # TODO: Delete wildcard set

        return menu
