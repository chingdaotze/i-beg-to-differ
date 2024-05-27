from abc import (
    ABC,
    abstractmethod,
)

from ..extension import Extension


class CodeEditor(
    Extension,
    ABC,
):

    def __init__(
        self,
        extension_id: str,
        extension_name: str,
    ):

        Extension.__init__(
            self=self,
            extension_id=extension_id,
            extension_name=extension_name,
        )

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
