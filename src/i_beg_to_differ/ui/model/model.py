from pathlib import Path
from typing import Self

from PySide6.QtGui import QStandardItemModel

from ..view.main_window.main_widget.object_viewer import ObjectViewer
from ...core.ib2d_file import IB2DFile
from ...core import open_ib2d_file
from .compare_sets import ModelCompareSets
from .data_sources import ModelDataSources
from .wildcard_sets import ModelWildcardSets


class Model(
    QStandardItemModel,
):

    ib2d_file: IB2DFile

    def __init__(
        self,
        object_viewer: ObjectViewer,
        ib2d_file: IB2DFile | None = None,
    ):

        QStandardItemModel.__init__(
            self,
        )

        self.setHorizontalHeaderLabels(
            [
                'Object Name',
                'Object Type',
                'Modified',
            ]
        )

        if ib2d_file is None:
            ib2d_file = IB2DFile()

        self.ib2d_file = ib2d_file

        self.appendRow(
            ModelCompareSets(
                compare_sets=self.ib2d_file.compare_sets,
                working_dir_path=self.ib2d_file.working_dir_path,
                object_viewer=object_viewer,
                wildcard_sets=self.ib2d_file.wildcard_sets,
            )
        )

        self.appendRow(
            ModelDataSources(
                data_sources=self.ib2d_file.data_sources,
                object_viewer=object_viewer,
                wildcard_sets=self.ib2d_file.wildcard_sets,
            )
        )

        self.appendRow(
            ModelWildcardSets(
                object_viewer=object_viewer,
                wildcard_sets=self.ib2d_file.wildcard_sets,
            )
        )

    @classmethod
    def load(
        cls,
        object_viewer: ObjectViewer,
        path: Path | str,
    ) -> Self:

        if isinstance(path, str):
            path = Path(
                path,
            )

        with open_ib2d_file(path=path) as ib2d_file:
            return Model(
                object_viewer=object_viewer,
                ib2d_file=ib2d_file,
            )
