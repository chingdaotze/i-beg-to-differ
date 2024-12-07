from PySide6.QtWidgets import QMenu

from ..model_base_extension import ModelBaseExtension
from ....core.data_sources.data_source import DataSource
from ....core.wildcards_sets import WildcardSets
from ...view.main_window.main_widget.object_viewer import ObjectViewer


class ModelDataSource(
    ModelBaseExtension,
):

    def __init__(
        self,
        data_source: DataSource,
        wildcard_sets: WildcardSets,
        object_viewer: ObjectViewer,
    ):

        ModelBaseExtension.__init__(
            self=self,
            current_state=data_source,
            wildcard_sets=wildcard_sets,
            object_viewer=object_viewer,
        )

    @property
    def context_menu(
        self,
    ) -> QMenu:

        menu = QMenu()

        menu.addAction(
            'Edit',
            self.open_in_object_viewer,
        )

        menu.addAction(
            'Delete',
        )  # TODO: Delete Data source

        return menu
