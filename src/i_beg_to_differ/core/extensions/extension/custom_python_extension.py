from abc import ABC
from pathlib import Path
from typing import Callable
from uuid import uuid4
from inspect import (
    Signature,
    signature,
    getfile,
)
from zipfile import ZipFile
from shutil import copyfile
from importlib.util import (
    spec_from_file_location,
    module_from_spec,
)
from sys import modules
from subprocess import call

from PySide6.QtWidgets import (
    QWidget,
    QPushButton,
)

from .extension import Extension
from ...wildcards_sets import WildcardSets
from ....ui.widgets import Widget


class CustomPythonExtension(
    Extension,
    ABC,
):

    working_dir_path: Path
    py_file_name: str
    py_file_path: Path
    extension_func_prototype: Callable
    extension_func_prototype_path: Path
    wildcard_sets: WildcardSets | None

    def __init__(
        self,
        working_dir_path: Path,
        extension_func_prototype: Callable,
        py_file_name: str | None = None,
        wildcard_sets: WildcardSets | None = None,
    ):

        Extension.__init__(
            self=self,
        )

        self.working_dir_path = working_dir_path
        self.extension_func_prototype = extension_func_prototype
        self.extension_func_prototype_path = Path(
            getfile(
                self.extension_func_prototype,
            ),
        )
        self.wildcard_sets = wildcard_sets

        if py_file_name is None:
            self.py_file_name = (
                str(
                    uuid4(),
                ).replace(
                    '-',
                    '_',
                )
                + '.py'
            )

        else:
            self.py_file_name = py_file_name

        self.py_file_path = self.working_dir_path / self.py_file_name

        if not self.py_file_path.exists():
            self.create_python_file()

    @property
    def extension_func_name(
        self,
    ) -> str:
        """
        Python function name that contains main extension logic. Used to build a new Python file.

        :return:
        """

        return self.extension_func_prototype.__name__

    @property
    def extension_func_signature(
        self,
    ) -> Signature:
        """
        Python function signature that contains main extension logic. Used to build a new Python file.

        :return:
        """

        extension_func_signature = signature(
            obj=self.extension_func_prototype,
        )

        return extension_func_signature

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

        ib2d_file.write(
            filename=self.py_file_path,
        )

    def create_python_file(
        self,
    ) -> None:
        """
        Creates a new Python file with an appropriate Python function signature.

        :return:
        """

        copyfile(
            src=self.extension_func_prototype_path,
            dst=self.py_file_path,
        )

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

        self.get_extension_func()  # Use this to validate the Python file

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

    @property
    def object_viewer_widget(
        self,
    ) -> QWidget:

        # Create button
        button = QPushButton(
            'Edit Python File',
        )

        button.clicked.connect(
            self.edit_python_file,
        )

        # Create widget
        widget = Widget()

        widget.layout.addWidget(
            button,
        )

        return widget
