from typing import Dict

from ..dict_input_field import DictInputField
from ...wildcards_sets.wildcard_field import WildcardField
from ...wildcards_sets import WildcardSets


class WildcardDictInputField(
    DictInputField,
):

    values: Dict[WildcardField, WildcardField]

    def __init__(
        self,
        title: str | None = None,
        values: Dict[str, str] | None = None,
        key_column: str = 'Parameter',
        value_column: str = 'Value',
        wildcard_sets: WildcardSets | None = None,
    ):

        DictInputField.__init__(
            self=self,
            title=title,
            values=values,
            key_column=key_column,
            value_column=value_column,
        )

        self.values = {
            WildcardField(
                base_value=str(key),
                wildcard_sets=wildcard_sets,
            ): WildcardField(
                base_value=str(value),
                wildcard_sets=wildcard_sets,
            )
            for key, value in self.values.items()
        }
