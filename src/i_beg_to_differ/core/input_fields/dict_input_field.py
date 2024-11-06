from typing import Dict

from .input_field import InputField


class DictInputField(
    InputField,
):

    values: Dict[str, str]
    key_column: str
    value_column: str

    def __init__(
        self,
        title: str | None = None,
        values: Dict[str, str] | None = None,
        key_column: str = 'Parameter',
        value_column: str = 'Value',
    ):

        InputField.__init__(
            self=self,
            title=title,
        )

        self.key_column = key_column
        self.value_column = value_column

        if isinstance(values, dict):
            self.values = values

        else:
            self.values = {}
