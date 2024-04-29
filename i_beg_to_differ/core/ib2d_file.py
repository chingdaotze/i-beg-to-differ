from pathlib import Path
from zipfile import ZipFile
from json import load
from os import (
    PathLike,
    getenv,
)
from contextlib import contextmanager
from uuid import uuid4
from typing import Self

from .base import Base
from .compare_set import CompareSet


class IB2DFile(
    Base,
):
    """
    ``*.ib2d`` file object.
    """

    path: Path
    compare_set: CompareSet
    zip_file: ZipFile

    def __init__(
        self,
        path: Path,
        working_dir_path: Path,
    ):
        """
        Creates a CompareSet object. If file exists, deserialize file. If file does not exist,
        create an empty CompareSet object.

        :param path: ``*.ib2d`` file path.
        :param working_dir_path: Working directory path.
        """

        Base.__init__(
            self=self,
            working_dir_path=working_dir_path,
        )

        self.path = path

        if self.path.exists():
            # Deserialize
            with ZipFile(file=self.path, mode='r') as zip_file:

                json_file = zip_file.open(
                    name='compare_set.json',
                )

                instance_data = load(
                    fp=json_file,
                )

                self.compare_set = CompareSet.deserialize(
                    instance_data=instance_data,
                    working_dir_path=self.working_dir_path,
                    ib2d_file=self,
                )

        else:
            # TODO: Create empty archive

            # Create empty instance
            self.compare_set = CompareSet(
                working_dir_path=working_dir_path,
            )

    def __del__(
        self,
    ) -> None:
        """
        Cleans up the working directory.

        :return:
        """

        # TODO: Remove working directory

    def inflate(
        self,
        file_name: str,
    ) -> None:
        """
        Adds or overwrites a file from the working directory to the `*.ib2d`` file.

        :param file_name: Name of the file to add or overwrite.
        :return:
        """

        # TODO: Add file to zip

        pass

    def deflate(
        self,
        file_name: str,
    ) -> None:
        """
        Deflates a file within the `*.ib2d`` file to the working directory.

        :param file_name: Name of the file to extract to the working directory.
        :return:
        """

        # TODO: Extract file from zip

        pass

    @classmethod
    @contextmanager
    def open(
        cls,
        path: str | PathLike,
        working_dir_path: str | PathLike | None = None,
    ) -> Self:
        """
        Reads a ``*.ib2d`` file from disk and creates an instance. Also initializes the working directory.

        :param path: ``*.ib2d`` file path.
        :param working_dir_path: Working directory path.
        :return:
        """

        try:
            # Parse path
            if isinstance(path, str):
                path = Path(
                    path,
                )

            if not path.exists():
                raise FileNotFoundError(
                    f'Unable to locate *.ib2d file: "{str(path)}"!',
                )

            # Get working directory
            if working_dir_path is None:
                working_dir_path = getenv(
                    key='TEMP',
                )

                if working_dir_path is None:
                    raise KeyError(
                        'Unable to create default working directory: working_dir_path not specified '
                        'and could not locate "TEMP" environment variable.'
                    )

                working_dir_path = Path(
                    working_dir_path,
                )

                working_dir_path /= f'ib2d_{str(uuid4())}'

                working_dir_path.mkdir()

            else:
                working_dir_path = Path(
                    working_dir_path,
                )

            # Create instance
            ib2d_file = IB2DFile(
                path=path,
                working_dir_path=working_dir_path,
            )

            yield ib2d_file

        finally:

            # TODO: Delete working directory
            pass

    def save(
        self,
        path: str | PathLike,
    ) -> None:
        """
        Writes a ``*.ib2d`` file to disk.

        :param path: ``*.ib2d`` file path.
        :return:
        """

        # TODO: Serialize object, and write to JSON file
        json_data = self.compare_set.serialize(
            ib2d_file=self,
        )

        pass
