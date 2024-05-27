from abc import (
    ABC,
    abstractmethod,
)
from pathlib import Path
from zipfile import ZipFile
from typing import (
    Self,
    Dict,
)

from ..base import Base
from ..wildcards_sets import WildcardSets


class IB2DFileElement(
    Base,
    ABC,
):
    """
    Element or component of an ``*.ib2d`` file.
    """

    def __init__(
        self,
        working_dir_path: Path,
    ):
        Base.__init__(
            self=self,
            working_dir_path=working_dir_path,
        )

    @staticmethod
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

    @classmethod
    @abstractmethod
    def deserialize(
        cls,
        instance_data: Dict,
        working_dir_path: Path,
        ib2d_file: ZipFile,
        wildcard_sets: WildcardSets | None = None,
    ) -> Self:
        """
        Constructs an instance from a dictionary. Also extracts any supporting files from the ``*.compare``
        file to the working directory.
        :param instance_data: Dictionary that contains instance data.
        :param working_dir_path: Working directory path.
        :param ib2d_file: ``*.ib2d`` file.
        :param wildcard_sets: Wildcard sets.
        :return: An instance of this class.
        """

    @abstractmethod
    def serialize(
        self,
        ib2d_file: ZipFile,
    ) -> Dict:
        """
        Constructs a dictionary from an instance. Also compresses any supporting files from the working
        directory to a ``*.ib2d`` file.

        :param ib2d_file: ``*.ib2d`` file.
        :return: Dictionary that contains instance data.
        """
