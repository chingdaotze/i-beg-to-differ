from abc import (
    ABC,
    abstractmethod,
)
from pathlib import Path
from typing import (
    TYPE_CHECKING,
    Self,
    Dict,
)

from .base import Base

if TYPE_CHECKING:
    from .ib2d_file import IB2DFile


class IB2DFileElement(
    Base,
    ABC,
):
    """
    Element or component of a ``*.ib2d`` file.
    """

    def __init__(
        self,
        working_dir_path: Path,
    ):
        Base.__init__(
            self=self,
            working_dir_path=working_dir_path,
        )

    @classmethod
    @abstractmethod
    def deserialize(
        cls,
        instance_data: Dict,
        working_dir_path: Path,
        ib2d_file: 'IB2DFile',
    ) -> Self:
        """
        Constructs an instance from a dictionary. Also extracts any supporting files from the ``*.compare``
        file to the working directory.
        :param instance_data: Dictionary that contains instance data.
        :param working_dir_path: Working directory path.
        :param ib2d_file: ``*.ib2d`` file.
        :return: An instance of this class.
        """

    @abstractmethod
    def serialize(
        self,
        ib2d_file: 'IB2DFile',
    ) -> Dict:
        """
        Constructs a dictionary from an instance. Also compresses any supporting files from the working
        directory to a ``*.ib2d`` file.

        :param ib2d_file: ``*.ib2d`` file.
        :return: Dictionary that contains instance data.
        """
