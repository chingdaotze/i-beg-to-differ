# TODO: Move this file elsewhere.

from abc import (
    ABC,
    abstractmethod,
)

from .extension import Extension


class CodeEditor(
    Extension,
    ABC,
):

    @abstractmethod
    def load(
        self,
        path: str,
    ) -> None:
        """
        Opens the file in the code editor.

        :param path: Path to the file.
        :return:
        """
