from typing import Dict

from PySide6.QtWidgets import QWidget

from ..input_field import InputField
from .wildcard_dict_table_widget import WildcardDictTableWidget
from ....wildcards_sets import WildcardSets
from ....wildcards_sets.wildcard_field import WildcardField
from .....ui.widgets import GroupBox


class WildcardDictTableInputField(
    InputField,
):
    """
    Wildcard dictionary input field. Creates a table of key-value pairs, with Wildcard value substitution in both
    keys and values.
    """

    title: str | None
    wildcard_dict_table_widget: WildcardDictTableWidget

    def __init__(
        self,
        values: Dict[str, str] | None = None,
        wildcard_sets: WildcardSets | None = None,
        title: str | None = None,
        key_column: str = 'Parameter',
        value_column: str = 'Value',
    ):

        InputField.__init__(
            self,
        )

        self.title = title

        self.wildcard_dict_table_widget = WildcardDictTableWidget(
            values=values,
            wildcard_sets=wildcard_sets,
            key_column=key_column,
            value_column=value_column,
        )

    @property
    def values(
        self,
    ) -> Dict[WildcardField, WildcardField]:

        return self.wildcard_dict_table_widget.values

    @property
    def layout_component(
        self,
    ) -> QWidget:

        if self.title is not None:
            layout_component = GroupBox(
                title=self.title,
            )

            layout_component.layout.addWidget(
                self.wildcard_dict_table_widget,
                0,
                0,
            )

        else:
            layout_component = self.wildcard_dict_table_widget

        return layout_component
