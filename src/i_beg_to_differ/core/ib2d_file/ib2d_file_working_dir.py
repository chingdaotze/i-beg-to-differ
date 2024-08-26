from abc import ABC
from pathlib import Path
from zipfile import ZipFile

from ..base import (
    Base,
    log_exception,
)


class IB2DFileWorkingDir(
    Base,
    ABC,
):
    """
    Element or component of an ``*.ib2d`` file.
    """

    working_dir_path: Path
    """
    Working directory path.
    """

    def __init__(
        self,
        working_dir_path: Path,
    ):

        Base.__init__(
            self=self,
        )

        self.working_dir_path = working_dir_path

    @staticmethod
    @log_exception
    def inflate(
        file_name: str,
        working_dir_path: Path,
        ib2d_file: ZipFile,
    ) -> None:
        """
        Inflates a file within the `*.ib2d`` file to the working directory.

        :param file_name: Name of the file to add or overwrite.
        :param working_dir_path: Working directory path.
        :param ib2d_file: ``*.ib2d`` file.
        :return:
        """

        # TODO: Extract file from zip

        pass

    @staticmethod
    @log_exception
    def deflate(
        file_name: str,
        working_dir_path: Path,
        ib2d_file: ZipFile,
    ) -> None:
        """
        Adds or overwrites a file from the working directory to the `*.ib2d`` file.

        :param file_name: Name of the file to add or overwrite.
        :param working_dir_path: Working directory path.
        :param ib2d_file: ``*.ib2d`` file.
        :return:
        """

        # TODO: Add file to zip

        pass
