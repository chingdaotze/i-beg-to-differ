from typing import Any

from .input_field import InputField
from ...wildcards_sets.wildcard_field import WildcardField
from ...wildcards_sets import WildcardSets


class WildcardInputField(
    InputField,
):

    label: str
    value: WildcardField

    def __init__(
        self,
        label: str,
        value: Any | None = None,
        wildcard_sets: WildcardSets | None = None,
    ):

        self.label = label

        self.value = WildcardField(
            base_value=str(value),
            wildcard_sets=wildcard_sets,
        )
