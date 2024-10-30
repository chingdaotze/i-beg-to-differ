from .input_field import InputField
from ...wildcards_sets.wildcard_field import WildcardField
from ...wildcards_sets import WildcardSets


class PathInputField(
    InputField,
):

    label: str
    path: WildcardField

    def __init__(
        self,
        label: str,
        path: str | None = None,
        wildcard_sets: WildcardSets | None = None,
    ):

        self.label = label

        self.path = WildcardField(
            base_value=path,
            wildcard_sets=wildcard_sets,
        )
