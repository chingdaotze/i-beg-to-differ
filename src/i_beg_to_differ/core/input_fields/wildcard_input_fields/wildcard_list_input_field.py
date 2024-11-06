from typing import List

from .wildcard_input_field import WildcardInputField
from ...wildcards_sets import WildcardSets


class WildcardListInputField(
    WildcardInputField,
):

    options: List[str]

    def __init__(
        self,
        options: List[str],
        base_value: str,
        title: str | None = None,
        wildcard_sets: WildcardSets | None = None,
    ):

        WildcardInputField.__init__(
            self=self,
            title=title,
            base_value=base_value,
            wildcard_sets=wildcard_sets,
        )

        self.options = options
