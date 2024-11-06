from .wildcard_input_field import WildcardInputField
from ...wildcards_sets import WildcardSets


class WildcardPathInputField(
    WildcardInputField,
):

    file_dialog_caption: str
    file_dialog_filter: str

    def __init__(
        self,
        path: str,
        file_dialog_caption: str,
        file_dialog_filter: str,
        title: str | None = None,
        wildcard_sets: WildcardSets | None = None,
    ):

        WildcardInputField.__init__(
            self=self,
            title=title,
            base_value=path,
            wildcard_sets=wildcard_sets,
        )

        self.file_dialog_caption = file_dialog_caption
        self.file_dialog_filter = file_dialog_filter
