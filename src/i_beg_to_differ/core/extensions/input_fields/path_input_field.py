from .wildcard_input_field import WildcardInputField
from ...wildcards_sets import WildcardSets


class PathInputField(
    WildcardInputField,
):

    def __init__(
        self,
        label: str,
        path: str,
        wildcard_sets: WildcardSets | None = None,
    ):

        WildcardInputField.__init__(
            self=self,
            label=label,
            base_value=path,
            wildcard_sets=wildcard_sets,
        )
