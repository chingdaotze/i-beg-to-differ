from pathlib import Path

from PySide6.QtWidgets import (
    QWidget,
    QMenu,
    QFileDialog,
)

from ....model_base_object_viewer import ModelBaseObjectViewer
from ......core.compare_sets.compare_set.compare import Compare
from ......core.wildcards_sets import WildcardSets
from .....view.main_window.main_widget.object_viewer import ObjectViewer
from .compare_object_viewer_widget import CompareObjectViewerWidget


class ModelCompare(
    ModelBaseObjectViewer,
):

    current_state: Compare
    working_dir_path: Path

    def __init__(
        self,
        compare: Compare,
        wildcard_sets: WildcardSets,
        object_viewer: ObjectViewer,
        working_dir_path: Path,
    ):

        ModelBaseObjectViewer.__init__(
            self=self,
            current_state=compare,
            object_viewer=object_viewer,
            wildcard_sets=wildcard_sets,
        )

        self.working_dir_path = working_dir_path

    @property
    def object_viewer_widget(
        self,
    ) -> QWidget | None:

        return CompareObjectViewerWidget(
            compare=self.current_state,
            working_dir_path=self.working_dir_path,
        )

    def create_report(
        self,
        output_type: str,
    ) -> None:

        if output_type == 'csv':
            dir_path = QFileDialog.getExistingDirectory(
                caption='Select Output Directory',
            )

            if dir_path:
                self.current_state.to_csv(
                    dir_path=dir_path,
                )

        elif output_type == 'parquet':
            dir_path = QFileDialog.getExistingDirectory(
                caption='Select Output Directory',
            )

            if dir_path:
                self.current_state.to_parquet(
                    dir_path=dir_path,
                )

        elif output_type == 'excel':
            path, _ = QFileDialog.getSaveFileName(
                caption='Save Output File',
                filter='Office Open XML Workbook (*.xlsx)',
            )

            if path:
                self.current_state.to_excel(
                    path=path,
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
            'Open',
            self.open_in_object_viewer,
        )

        menu.addAction(
            'Delete',
        )  # TODO: Delete compare

        return menu
