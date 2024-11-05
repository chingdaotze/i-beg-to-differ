from typing import Dict

from .input_field import InputField
from ...wildcards_sets.wildcard_field import WildcardField
from ...wildcards_sets import WildcardSets


class WildcardDictInputField(
    InputField,
):

    values: Dict[WildcardField, WildcardField]
    key_column: str
    value_column: str

    def __init__(
        self,
        title: str | None = None,
        values: Dict[str, str] | None = None,
        key_column: str = 'Parameter',
        value_column: str = 'Value',
        wildcard_sets: WildcardSets | None = None,
    ):

        InputField.__init__(
            self=self,
            title=title,
        )

        self.key_column = key_column
        self.value_column = value_column

        if isinstance(values, dict):
            self.values = {
                WildcardField(
                    base_value=key,
                    wildcard_sets=wildcard_sets,
                ): WildcardField(
                    base_value=value,
                    wildcard_sets=wildcard_sets,
                )
                for key, value in values.items()
            }

        else:
            self.values = {}
