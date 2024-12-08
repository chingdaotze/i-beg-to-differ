from pathlib import Path

from PySide6.QtWidgets import (
    QStatusBar,
    QMenu,
    QFileDialog,
)

from ..model_base import ModelBase
from ....core.compare_sets import CompareSets
from ....core.data_sources import DataSources
from ....core.wildcards_sets import WildcardSets
from ...view.main_window.main_widget.object_viewer import ObjectViewer
from ....core.compare_sets.compare_set import CompareSet
from .compare_set import ModelCompareSet
from ...widgets import (
    Dialog,
    LineEdit,
)


class ModelCompareSets(
    ModelBase,
):

    current_state: CompareSets
    data_sources: DataSources
    working_dir_path: Path
    object_viewer: ObjectViewer

    def __init__(
        self,
        compare_sets: CompareSets,
        wildcard_sets: WildcardSets,
        status_bar: QStatusBar,
        data_sources: DataSources,
        object_viewer: ObjectViewer,
        working_dir_path: Path,
    ):

        ModelBase.__init__(
            self=self,
            current_state=compare_sets,
            wildcard_sets=wildcard_sets,
            status_bar=status_bar,
        )

        self.data_sources = data_sources
        self.working_dir_path = working_dir_path
        self.object_viewer = object_viewer

        for compare_set in self.current_state.compare_sets.values():

            self.appendRow(
                ModelCompareSet(
                    compare_set=compare_set,
                    wildcard_sets=self.wildcard_sets,
                    status_bar=self.status_bar,
                    object_viewer=self.object_viewer,
                    data_sources=self.data_sources,
                    working_dir_path=self.working_dir_path,
                )
            )

    def add_compare_set(
        self,
    ) -> None:

        # Create / show Dialog
        dialog = Dialog(
            title='New Compare Set',
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
        compare_set_name = input_widget.text()

        compare_set = CompareSet(
            name=compare_set_name,
        )

        self.current_state.append(
            compare_set=compare_set,
        )

        self.appendRow(
            ModelCompareSet(
                compare_set=compare_set,
                wildcard_sets=self.wildcard_sets,
                status_bar=self.status_bar,
                object_viewer=self.object_viewer,
                data_sources=self.data_sources,
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
            self.status_bar.showMessage(
                f'Saving comparison: {dir_path} ...',
            )

            self.status_bar.repaint()

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

            self.status_bar.showMessage(
                f'Done! Comparison saved here: {dir_path}',
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
            'Add Compare Set',
            self.add_compare_set,
        )

        return menu
