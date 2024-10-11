from pathlib import Path
from typing import Callable

from .extension import Extension


class CustomPythonExtension(
    Extension,
):

    working_dir_path: Path
    py_file_path: Path
    callable_name: str
    callable_signature: Signature

    def __init__(
        self,
        working_dir_path: Path,
        py_file_path: Path | None,
    ):

        Extension.__init__(
            self=self,
        )

        self.working_dir_path = working_dir_path

        if py_file_path is None:
            # TODO: Create python file
            pass

    def create_python_file(
        self,
    ) -> None:

        # TODO: Create a Python file with the appropriate signature
        pass

    def validate_python_file(
        self,
    ) -> None:

        # TODO: Check if callable name exists in Python File
        pass
