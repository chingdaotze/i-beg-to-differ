from typing import List

from .input_field import InputField
from ...wildcards_sets.wildcard_field import WildcardField
from ...wildcards_sets import WildcardSets


class PathInputField(
    InputField,
):

    label: str
    value: WildcardField
    options: List[str]

    def __init__(
        self,
        label: str,
        options: List[str],
        value: str | None = None,
        wildcard_sets: WildcardSets | None = None,
    ):

        self.label = label
        self.options = options

        self.value = WildcardField(
            base_value=value,
            wildcard_sets=wildcard_sets,
        )
