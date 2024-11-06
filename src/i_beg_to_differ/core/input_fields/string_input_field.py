from .input_field import InputField


class StringInputField(
    InputField,
):

    value: str

    def __init__(
        self,
        title: str | None = None,
        value: str | None = None,
    ):

        InputField.__init__(
            self=self,
            title=title,
        )

        if value is None:
            value = ''

        self.value = value

    def __str__(
        self,
    ) -> str:

        return str(
            id(
                self,
            ),
        )
