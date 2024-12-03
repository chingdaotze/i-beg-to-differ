from PySide6.QtWidgets import (
    QWidget,
    QTabWidget,
)

from ...model_base_object_viewer import ModelBaseObjectViewer
from .....core.wildcards_sets.wildcard_set import WildcardSet
from .wildcard_set_description_widget import WildcardSetDescriptionWidget
from .wildcard_set_widget import WildcardSetWidget


class ModelWildcardSet(
    ModelBaseObjectViewer,
):

    current_state: WildcardSet

    wildcard_set_description_widget: WildcardSetDescriptionWidget
    wildcard_set_widget: WildcardSetWidget

    def __init__(
        self,
        object_name: str,
        wildcard_set: WildcardSet,
    ):

        ModelBaseObjectViewer.__init__(
            self=self,
            current_state=wildcard_set,
            object_name=object_name,
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
