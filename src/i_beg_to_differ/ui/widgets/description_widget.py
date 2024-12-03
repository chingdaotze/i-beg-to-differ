from PySide6.QtWidgets import (
    QWidget,
    QPlainTextEdit,
    QGridLayout,
    QSizePolicy,
)


class DescriptionWidget(
    QWidget,
):
    """
    Description text widget. Creates a markdown editor and viewer.
    """

    value: str
    text_edit: QPlainTextEdit

    def __init__(
        self,
        value: str | None = None,
        parent: QWidget | None = None,
    ):

        QWidget.__init__(
            self,
            parent,
        )

        # Init value
        if value is None:
            value = ''

        self.value = value

        # Text editor
        self.text_edit = QPlainTextEdit()

        self.text_edit.textChanged.connect(
            self.text_changed,
        )

        self.text_edit.setPlainText(
            value,
        )

        # Layout
        layout = QGridLayout()

        layout.addWidget(
            self.text_edit,
            0,
            0,
        )

        # Group box
        self.setLayout(
            layout,
        )

        self.setSizePolicy(
            QSizePolicy.Policy.Minimum,
            QSizePolicy.Policy.Maximum,
        )

    def text_changed(
        self,
    ) -> None:
        """
        Abstract method triggered whenever text is changed. Override this method to update values.
        """

        self.value = self.text_edit.toPlainText()
