from pathlib import Path
from typing import (
    TYPE_CHECKING,
    Dict,
    Self,
)
from zipfile import ZipFile

from ..ib2d_file.ib2d_file_element import IB2DFileElement

if TYPE_CHECKING:
    from ..wildcards_sets import WildcardSets


class WildcardSet(
    IB2DFileElement,
):
    """
    Collection of wildcards, used to replace values.
    """

    description: str
    """
    Human-readable description of this Wildcard Set.
    """

    replacement_values: Dict[str, str]
    """
    Wildcard replacement values.
    """

    _MAX_REPLACEMENT_DEPTH = 1000

    def __init__(
        self,
        working_dir_path: Path,
        description: str | None = None,
        replacement_values: Dict[str, str] | None = None,
    ):
        IB2DFileElement.__init__(
            self=self,
            working_dir_path=working_dir_path,
        )

        self.description = description
        self.replacement_values = replacement_values

    def replace_wildcards(
        self,
        string: str,
        recursion_depth: int = 1,
    ) -> str:
        """
        Replaces wildcards in a provided string. Wildcards should take the form of ``${wildcard}``.
        Wildcards can contain wildcards, however there is a maximum replacement depth (to avoid
        infinite recursion), defined by _MAX_REPLACEMENT_DEPTH.

        :param string: Original string.
        :param recursion_depth: Current recursion depth.
        :return: String with wildcard replacement.
        """

        # TODO: Implement wildcard replacement

        pass

    @classmethod
    def deserialize(
        cls,
        instance_data: Dict,
        working_dir_path: Path,
        ib2d_file: ZipFile,
        wildcard_sets: Self | None = None,
    ) -> Self:

        return WildcardSet(
            working_dir_path=working_dir_path,
            description=instance_data['description'],
            replacement_values=instance_data['replacement_values'],
        )

    def serialize(
        self,
        ib2d_file: ZipFile,
    ) -> Dict:

        return {
            'description': self.description,
            'replacement_values': self.replacement_values,
        }
