from ..input_field import InputField
from ..input_field_options import InputFieldOptions
from ...wildcards_sets.wildcard_field import WildcardField
from ...wildcards_sets import WildcardSets


class WildcardInputField(
    InputField,
    WildcardField,
):

    options: InputFieldOptions | None

    def __init__(
        self,
        base_value: str,
        title: str | None = None,
        wildcard_sets: WildcardSets | None = None,
        options: InputFieldOptions | None = None,
    ):

        InputField.__init__(
            self=self,
            title=title,
        )

        WildcardField.__init__(
            self=self,
            base_value=base_value,
            wildcard_sets=wildcard_sets,
        )

        self.options = options
