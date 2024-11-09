from typing import List

from .input_field_options import InputFieldOptions


class StaticInputFieldOptions(
    InputFieldOptions,
):

    _options: List[str]

    def __init__(
        self,
        options: List[str],
    ):

        self._options = options

    @property
    def options(
        self,
    ) -> List[str]:

        return self._options
