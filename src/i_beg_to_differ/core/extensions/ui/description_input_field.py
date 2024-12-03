from PySide6.QtWidgets import QWidget

from .input_field import InputField
from ....ui.widgets import DescriptionWidget


class DescriptionInputField(
    InputField,
):
    """
    Description input field. Creates a new Description tab and markdown editor.
    """

    description_widget: DescriptionWidget

    def __init__(
        self,
        value: str | None = None,
    ):

        self.description_widget = DescriptionWidget(
            value=value,
        )

    @property
    def value(
        self,
    ) -> str:

        return self.description_widget.value

    @property
    def layout_component(
        self,
    ) -> QWidget:

        return self.description_widget
