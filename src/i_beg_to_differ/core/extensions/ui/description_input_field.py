"""
Contains definition of the CompareRuleExtensions class.
"""

from PySide6.QtWidgets import QWidget

from i_beg_to_differ.ui.widgets import DescriptionWidget
from .input_field import InputField
from ...wildcards_sets.wildcard_field import WildcardField


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

        if value is None:
            value = ''

        self.description = WildcardField(
            base_value=value,
        )

    @property
    def value(
        self,
    ) -> str:
        """
        Description text.
        """

        return self.description.base_value

    @property
    def layout_component(
        self,
    ) -> QWidget:

        description_widget = DescriptionWidget(
            wildcard_field=self.description,
        )

        return description_widget
