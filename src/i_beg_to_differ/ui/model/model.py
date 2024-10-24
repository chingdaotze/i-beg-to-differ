from pathlib import Path
from typing import Self

from PySide6.QtGui import QStandardItemModel

from ...core.ib2d_file import IB2DFile
from ...core import open_ib2d_file
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
            ModelWildcardSets(
                wildcard_sets=self.ib2d_file.wildcard_sets,
            )
        )

        pass

    @classmethod
    def load(
        cls,
        path: Path,
    ) -> Self:

        with open_ib2d_file(path=path) as ib2d_file:
            return Model(
                ib2d_file=ib2d_file,
            )
