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

from i_beg_to_differ.core.base import Base
from i_beg_to_differ.core.wildcards import Wildcards

if TYPE_CHECKING:
    from i_beg_to_differ.core.ib2d_file import IB2DFile


class IB2DFileElement(
    Base,
    ABC,
):
    """
    Element or component of an ``*.ib2d`` file.
    """

    _wildcards: Wildcards

    def __init__(
        self,
        working_dir_path: Path,
        wildcards: Wildcards | None = None,
    ):
        Base.__init__(
            self=self,
            working_dir_path=working_dir_path,
        )

        if wildcards is None:
            self.wildcards = Wildcards(
                working_dir_path=self.working_dir_path,
            )

        else:
            self.wildcards = wildcards

    @property
    def wildcards(
        self,
    ) -> Wildcards:

        return self._wildcards

    @wildcards.setter
    @abstractmethod
    def wildcards(
        self,
        wildcards: Wildcards,
    ) -> None:
        """
        Sets wildcards on itself and all child objects.

        :param wildcards: Wildcards object to set.
        :return:
        """

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
