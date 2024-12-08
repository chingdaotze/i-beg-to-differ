from PySide6.QtWidgets import QWidget

from .input_field import InputField
from ...wildcards_sets.wildcard_field import WildcardField
from ....ui.widgets import DescriptionWidget


class DescriptionInputField(
    InputField,
):
    """
    Description input field. Creates a new Description tab and markdown editor.
    """

    description: WildcardField

    def __init__(
        self,
        value: str | None = None,
    ):

        self.description = WildcardField(
            base_value=value,
        )

    @property
    def value(
        self,
    ) -> str:

        return self.description.base_value

    @property
    def layout_component(
        self,
    ) -> QWidget:

        description_widget = DescriptionWidget(
            wildcard_field=self.description,
        )

        return description_widget
