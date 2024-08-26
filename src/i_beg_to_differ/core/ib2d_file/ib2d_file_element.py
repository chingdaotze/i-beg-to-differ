from abc import (
    ABC,
    abstractmethod,
)
from pathlib import Path
from zipfile import ZipFile
from typing import (
    TYPE_CHECKING,
    Self,
    Dict,
    Union,
)

if TYPE_CHECKING:
    from ..wildcards_sets import WildcardSets

from ..base import Base


class IB2DFileElement(
    Base,
    ABC,
):
    """
    Element or component of an ``*.ib2d`` file.
    """

    def __init__(
        self,
    ):
        Base.__init__(
            self=self,
        )

    @classmethod
    @abstractmethod
    def deserialize(
        cls,
        instance_data: Dict,
        working_dir_path: Path,
        ib2d_file: ZipFile,
        wildcard_sets: Union['WildcardSets', None] = None,
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
