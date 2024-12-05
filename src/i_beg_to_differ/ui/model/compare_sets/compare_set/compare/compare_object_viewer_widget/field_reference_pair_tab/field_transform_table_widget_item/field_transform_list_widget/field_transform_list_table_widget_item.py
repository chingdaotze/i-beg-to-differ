from ..........core.data_sources.data_source.field.field_transforms.field_transform import (
    FieldTransform,
)
from .........widgets import (
    TableWidgetItemDialog,
    Dialog,
)


class FieldTransformListTableWidgetItem(
    TableWidgetItemDialog,
):

    field_transform: FieldTransform

    def __init__(
        self,
        field_transform: FieldTransform,
    ):

        self.field_transform = field_transform

        TableWidgetItemDialog.__init__(
            self=self,
        )

    def get_text(
        self,
    ) -> str:

        return str(
            self.field_transform,
        )

    def open_dialog(
        self,
    ) -> None:

        dialog = Dialog(
            title='Edit Transform Parameters',
        )

        dialog.layout.addWidget(
            self.field_transform.object_viewer_widget,
            0,
            0,
        )

        dialog.exec()
