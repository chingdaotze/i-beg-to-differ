from typing import (
    Callable,
    List,
)

from PySide6.QtWidgets import QWidget

from ...wildcards_sets.wildcard_field_base import WildcardFieldBase
from ...wildcards_sets.wildcard_field import WildcardField
from .input_field import InputField
from ....ui.widgets import (
    WildcardInputWidgetPreview,
    GroupBox,
)
from ...wildcards_sets import WildcardSets


class WildcardInputField(
    WildcardFieldBase,
    InputField,
):
    """
    Wildcard input field that also provides a widget interface. Creates a text input field with Wildcard
    value substitution. Options can be provided in several forms:
        - As a static list.
        - As a dynamic list, where a function provides option values. The function is recalculated every time
          the dropdown is activated.

    If options are provided, they appear as ``QComboBox`` options.
    """

    title: str | None
    wildcard_field: WildcardField
    options: List[str] | Callable[[], List[str]] | None

    def __init__(
        self,
        base_value: str,
        wildcard_sets: WildcardSets | None = None,
        title: str | None = None,
        options: List[str] | Callable[[], List[str]] | None = None,
    ):

        WildcardFieldBase.__init__(
            self=self,
            wildcard_sets=wildcard_sets,
        )

        self.title = title

        self.wildcard_field = WildcardField(
            base_value=base_value,
            wildcard_sets=wildcard_sets,
        )

        self.options = options

    @property
    def base_value(
        self,
    ) -> str:

        return self.wildcard_field.base_value

    @base_value.setter
    def base_value(
        self,
        value: str,
    ) -> None:

        self.wildcard_field.base_value = value

    @property
    def layout_component(
        self,
    ) -> QWidget:

        wildcard_input_widget = WildcardInputWidgetPreview(
            wildcard_field=self.wildcard_field,
            options=self.options,
        )

        if self.title is not None:
            layout_component = GroupBox(
                title=self.title,
            )

            layout_component.layout.addWidget(
                wildcard_input_widget,
                0,
                0,
            )

        else:
            layout_component = wildcard_input_widget

        return layout_component
