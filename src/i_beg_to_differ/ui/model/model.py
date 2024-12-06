from pathlib import Path
from typing import Self

from PySide6.QtGui import QStandardItemModel

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
            )
        )

        self.appendRow(
            ModelDataSources(
                data_sources=self.ib2d_file.data_sources,
            )
        )

        self.appendRow(
            ModelWildcardSets(
                wildcard_sets=self.ib2d_file.wildcard_sets,
            )
        )

    @classmethod
    def load(
        cls,
        path: Path | str,
    ) -> Self:

        if isinstance(path, str):
            path = Path(
                path,
            )

        with open_ib2d_file(path=path) as ib2d_file:
            return Model(
                ib2d_file=ib2d_file,
            )
