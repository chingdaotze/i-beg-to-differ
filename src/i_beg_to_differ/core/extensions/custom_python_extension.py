from abc import ABC
from pathlib import Path
from typing import Callable
from uuid import uuid4
from inspect import (
    Signature,
    signature,
)
from zipfile import ZipFile

from ..wildcards_sets import WildcardSets


class CustomPythonExtension(
    ABC,
):

    working_dir_path: Path
    py_file_name: str
    py_file_path: Path
    extension_func: Callable
    wildcard_sets: WildcardSets | None

    def __init__(
        self,
        working_dir_path: Path,
        extension_func: Callable,
        py_file_name: str | None = None,
        wildcard_sets: WildcardSets | None = None,
    ):

        self.working_dir_path = working_dir_path
        self.extension_func = extension_func
        self.wildcard_sets = wildcard_sets

        if py_file_name is None:
            self.py_file_name = str(
                uuid4(),
            ).replace(
                '-',
                '_',
            )

        else:
            self.py_file_name = py_file_name

        py_file_path = self.working_dir_path / py_file_name

        if isinstance(py_file_path, Path):
            if not py_file_path.exists():
                self.py_file_path = self.create_python_file()

            else:
                self.py_file_path = py_file_path

        else:
            self.py_file_path = self.create_python_file()

    @property
    def extension_func_name(
        self,
    ) -> str:

        return self.extension_func.__name__

    @property
    def extension_func_signature(
        self,
    ) -> Signature:

        return signature(
            obj=self.extension_func,
        )

    @property
    def extension_func_docstring(
        self,
    ) -> Signature:

        return self.extension_func.__doc__

    def inflate_py_file(
        self,
    ) -> None:

        pass

    def deflate_py_file(
        self,
        ib2d_file: ZipFile,
    ) -> None:

        pass

    def create_python_file_content(
        self,
    ) -> str:

        # TODO: Create Python file content
        pass

    def create_python_file(
        self,
    ) -> Path:

        # TODO: Create a Python file with the appropriate signature
        pass

    def validate_python_file(
        self,
    ) -> None:

        # TODO: Check if callable name and signature exists in Python File
        pass

    def get_extension_func(
        self,
    ) -> Callable:

        # TODO: Load the python file and set attribute
        self.validate_python_file()

        pass
