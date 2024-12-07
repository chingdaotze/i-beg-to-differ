from PySide6.QtWidgets import QMenu

from ..model_base import ModelBase
from ....core.data_sources import DataSources
from ...view.main_window.main_widget.object_viewer import ObjectViewer
from ....core.wildcards_sets import WildcardSets
from ....core.data_sources.data_source import DataSource
from .data_source import ModelDataSource
from ...widgets import (
    Dialog,
    StaticComboBox,
)


class ModelDataSources(
    ModelBase,
):

    current_state: DataSources
    object_viewer: ObjectViewer

    def __init__(
        self,
        data_sources: DataSources,
        wildcard_sets: WildcardSets,
        object_viewer: ObjectViewer,
    ):

        ModelBase.__init__(
            self=self,
            current_state=data_sources,
            wildcard_sets=wildcard_sets,
        )

        self.object_viewer = object_viewer

        for name, data_source in data_sources.data_sources.items():

            self.appendRow(
                ModelDataSource(
                    data_source=data_source,
                    wildcard_sets=self.wildcard_sets,
                    object_viewer=self.object_viewer,
                )
            )

    def add_data_source(
        self,
    ) -> None:

        # Create / show Dialog
        dialog = Dialog(
            title='New Data Source',
        )

        extension_name_map = [
            (data_source.extension_name, data_source)
            for data_source in self.current_state.data_source_extensions.collection.values()
        ]

        input_widget = StaticComboBox(
            options=[
                extension_name_mapping[0]
                for extension_name_mapping in extension_name_map
            ],
            parent=dialog,
        )

        dialog.layout.addWidget(
            input_widget,
            0,
            0,
        )

        dialog.exec()

        # Create DataSource object and update model
        current_index = input_widget.currentIndex()
        data_source_type = extension_name_map[current_index][1]
        data_source: DataSource = data_source_type(
            wildcard_sets=self.wildcard_sets,
        )

        # Add DataSource to collection
        self.current_state.append(
            data_source=data_source,
        )

        self.appendRow(
            ModelDataSource(
                data_source=data_source,
                wildcard_sets=self.wildcard_sets,
                object_viewer=self.object_viewer,
            )
        )

    @property
    def context_menu(
        self,
    ) -> QMenu:

        menu = QMenu()

        menu.addAction(
            'Add Data Source',
            self.add_data_source,
        )

        return menu
