from typing import Dict
from multiprocessing.managers import DictProxy

from .input_field import InputField


class DictInputField(
    InputField,
):

    values: DictProxy
    key_column: str
    value_column: str

    def __init__(
        self,
        title: str | None = None,
        values: Dict[str, str] | DictProxy | None = None,
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
            self.values = self.manager.dict()

        elif isinstance(values, DictProxy):
            self.values = values

        else:
            self.values = self.manager.dict()

    def __str__(
        self,
    ) -> str:

        return str(
            id(
                self,
            ),
        )
