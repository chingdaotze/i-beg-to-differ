from .input_field import InputField


class StringInputField(
    InputField,
):

    label: str
    value: str

    def __init__(
        self,
        label: str,
        value: str | None = None,
    ):

        self.label = label

        if value is None:
            value = ''

        self.value = value
