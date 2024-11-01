from typing import List

from .wildcard_input_field import WildcardInputField
from ...wildcards_sets import WildcardSets


class ListInputField(
    WildcardInputField,
):

    options: List[str]

    def __init__(
        self,
        label: str,
        options: List[str],
        base_value: str,
        wildcard_sets: WildcardSets | None = None,
    ):

        WildcardInputField.__init__(
            self=self,
            label=label,
            base_value=base_value,
            wildcard_sets=wildcard_sets,
        )

        self.options = options
