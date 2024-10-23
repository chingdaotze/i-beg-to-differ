from PySide6.QtGui import QStandardItemModel

from ...core.ib2d_file import IB2DFile
from ...core import open_ib2d_file


class Model(
    QStandardItemModel,
):

    ib2d_file: IB2DFile

    def __init__(
        self,
        parent,
        ib2d_file: IB2DFile | None = None,
    ):

        QStandardItemModel.__init__(
            self,
            parent=parent,
        )

        self.setHorizontalHeaderLabels(
            [
                '',
                'Object Name',
                'Object Type',
            ]
        )

        # TODO: If ib2d_file is None, create an empty one

        self.ib2d_file = ib2d_file

    def load(
        self,
    ) -> None:

        self.ib2d_file = open_ib2d_file()
