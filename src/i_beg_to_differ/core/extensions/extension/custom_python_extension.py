from abc import ABC
from pathlib import Path
from typing import (
    Callable,
    Dict,
)
from uuid import uuid4
from inspect import (
    Signature,
    signature,
    Parameter,
)
from zipfile import ZipFile
from importlib.util import (
    spec_from_file_location,
    module_from_spec,
)
from sys import modules
from subprocess import call

from ...wildcards_sets import WildcardSets


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
        """
        Python function name that contains main extension logic. Used to build a new Python file.

        :return:
        """

        return self.extension_func.__name__

    @property
    def extension_func_signature(
        self,
    ) -> Signature:
        """
        Python function signature that contains main extension logic. Used to build a new Python file.

        :return:
        """

        extension_func_signature = signature(
            obj=self.extension_func,
        )

        parameters = {
            parameter_name: parameter
            for parameter_name, parameter in extension_func_signature.parameters.items()
        }

        parameters['wildcards'] = Parameter(
            name='wildcards',
            kind=Parameter.POSITIONAL_OR_KEYWORD,
            annotation=Dict[str, str],
        )

        extension_func_signature = Signature(
            parameters=[parameter for parameter in parameters.values()],
            return_annotation=extension_func_signature.return_annotation,
        )

        return extension_func_signature

    @property
    def extension_func_docstring(
        self,
    ) -> Signature:
        """
        Python function docstring that contains main extension logic. Used to build a new Python file.

        :return:
        """

        return self.extension_func.__doc__

    def inflate_py_file(
        self,
        ib2d_file: ZipFile,
    ) -> None:
        """
        Inflates the Python file rom an ``*.ib2d`` File to the working directory.

        :param ib2d_file:
        :return:
        """

        self.py_file_path = self.working_dir_path / self.py_file_name

        ib2d_file.extract(
            member=self.py_file_name,
            path=self.working_dir_path,
        )

    def deflate_py_file(
        self,
        ib2d_file: ZipFile,
    ) -> None:
        """
        Deflates the Python file from the working directory into an ``*.ib2d`` File.

        :param ib2d_file:
        :return:
        """

        # TODO: Deflate file

    def create_python_file(
        self,
    ) -> Path:
        """
        Creates a new Python file with an appropriate Python function signature.

        :return:
        """

        # TODO: Create a Python file with the appropriate signature
        pass

    def edit_python_file(
        self,
    ) -> None:
        """
        #. Opens file in default Python file editor.
        #. Once editing is complete, validates the python file.

        This call blocks until the editor process is closed.

        :return:
        """

        call(
            args=str(self.py_file_path),
            shell=True,
        )

        self.get_extension_func()

    def validate_extension_func(
        self,
        extension_func: Callable,
    ) -> None:
        """
        Validates a Python file to ensure a Python function exists with an appropriate signature.

        :param extension_func: Function to validate.
        :return:
        """

        assert extension_func.__name__ == self.extension_func_name
        assert signature(extension_func) == self.extension_func_signature

    def get_extension_func(
        self,
    ) -> Callable:
        """
        Loads and validates a Python module that contains extension logic. Reference:
        https://docs.python.org/3/library/importlib.html#importing-a-source-file-directly

        :return: Python function to call.
        """

        module_name = Path(
            self.py_file_name,
        ).stem

        spec = spec_from_file_location(
            name=module_name,
            location=self.py_file_path,
        )

        module = module_from_spec(
            spec=spec,
        )

        modules[module_name] = module

        spec.loader.exec_module(
            module=module,
        )

        extension_func = getattr(
            module,
            self.extension_func_name,
        )

        self.validate_extension_func(
            extension_func=extension_func,
        )

        return extension_func
