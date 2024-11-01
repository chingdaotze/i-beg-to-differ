from .input_field import InputField
from ...wildcards_sets.wildcard_field import WildcardField
from ...wildcards_sets import WildcardSets


class WildcardInputField(
    InputField,
    WildcardField,
):

    label: str

    def __init__(
        self,
        label: str,
        base_value: str,
        wildcard_sets: WildcardSets | None = None,
    ):

        WildcardField.__init__(
            self=self,
            base_value=base_value,
            wildcard_sets=wildcard_sets,
        )

        self.label = label
