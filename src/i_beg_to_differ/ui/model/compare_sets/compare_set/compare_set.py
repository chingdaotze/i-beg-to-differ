from pathlib import Path

from PySide6.QtWidgets import (
    QWidget,
    QTabWidget,
    QMenu,
    QFileDialog,
)

from ...model_base_object_viewer import ModelBaseObjectViewer
from .compare_set_description_widget import CompareSetDescriptionWidget
from .....core.compare_sets.compare_set import CompareSet
from .....core.data_sources import DataSources
from .....core.compare_sets.compare_set.compare.data_source_reference import (
    DataSourceReference,
)
from .....core.wildcards_sets import WildcardSets
from ....view.main_window.main_widget.object_viewer import ObjectViewer
from .compare import ModelCompare
from ....widgets import (
    Dialog,
    LineEdit,
)
from .....core.compare_sets.compare_set.compare import Compare


class ModelCompareSet(
    ModelBaseObjectViewer,
):

    current_state: CompareSet
    data_sources: DataSources
    working_dir_path: Path
    compare_set_description_widget: CompareSetDescriptionWidget

    def __init__(
        self,
        compare_set: CompareSet,
        data_sources: DataSources,
        wildcard_sets: WildcardSets,
        object_viewer: ObjectViewer,
        working_dir_path: Path,
    ):

        ModelBaseObjectViewer.__init__(
            self=self,
            current_state=compare_set,
            wildcard_sets=wildcard_sets,
            object_viewer=object_viewer,
        )

        self.data_sources = data_sources
        self.working_dir_path = working_dir_path

        self.compare_set_description_widget = CompareSetDescriptionWidget(
            compare_set=compare_set,
        )

        for compare in compare_set.compares.values():

            self.appendRow(
                ModelCompare(
                    compare=compare,
                    wildcard_sets=self.wildcard_sets,
                    object_viewer=self.object_viewer,
                    working_dir_path=self.working_dir_path,
                )
            )

    @property
    def object_viewer_widget(
        self,
    ) -> QWidget:

        # Add description
        tab_widget = QTabWidget()

        tab_widget.addTab(
            self.compare_set_description_widget,
            'Description',
        )

        return tab_widget

    def add_compare(
        self,
    ) -> None:

        # Create / show Dialog
        dialog = Dialog(
            title='New Compare',
        )

        input_widget = LineEdit(
            parent=dialog,
        )

        dialog.layout.addWidget(
            input_widget,
            0,
            0,
        )

        dialog.exec()

        # Create CompareSet object and update model
        compare_name = input_widget.text()

        compare = Compare(
            name=compare_name,
            source_data_source_ref=DataSourceReference(
                data_source_name='',
                wildcard_sets=self.wildcard_sets,
            ),
            target_data_source_ref=DataSourceReference(
                data_source_name='',
                wildcard_sets=self.wildcard_sets,
            ),
            data_sources=self.data_sources,
        )

        self.current_state.append(
            compare=compare,
        )

        self.appendRow(
            ModelCompare(
                compare=compare,
                wildcard_sets=self.wildcard_sets,
                object_viewer=self.object_viewer,
                working_dir_path=self.working_dir_path,
            )
        )

    def create_report(
        self,
        output_type: str,
    ) -> None:

        # Open File Dialog
        dir_path = QFileDialog.getExistingDirectory(
            caption='Select Output Directory',
        )

        if dir_path:
            if output_type == 'csv':
                self.current_state.to_csv(
                    dir_path=dir_path,
                )

            elif output_type == 'parquet':
                self.current_state.to_parquet(
                    dir_path=dir_path,
                )

            elif output_type == 'excel':
                self.current_state.to_excel(
                    dir_path=dir_path,
                )

    def create_csv_files(
        self,
    ) -> None:

        self.create_report(
            output_type='csv',
        )

    def create_parquet_files(
        self,
    ) -> None:

        self.create_report(
            output_type='parquet',
        )

    def create_excel_files(
        self,
    ) -> None:

        self.create_report(
            output_type='excel',
        )

    @property
    def context_menu(
        self,
    ) -> QMenu:

        menu = QMenu()

        menu.addAction(
            'Perform Compare (CSV)',
            self.create_csv_files,
        )

        menu.addAction(
            'Perform Compare (Parquet)',
            self.create_parquet_files,
        )

        menu.addAction(
            'Perform Compare (Excel)',
            self.create_excel_files,
        )

        menu.addSeparator()

        menu.addAction(
            'Add Compare',
            self.add_compare,
        )

        menu.addAction(
            'Open',
            self.open_in_object_viewer,
        )

        menu.addAction(
            'Delete',
        )  # TODO: Delete compare set

        return menu
