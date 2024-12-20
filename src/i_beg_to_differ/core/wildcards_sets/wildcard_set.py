from pathlib import Path
from typing import (
    Dict,
    Self,
)
from zipfile import ZipFile

from ..ib2d_file.ib2d_file_element import IB2DFileElement
from ..base import log_exception


class WildcardSet(
    IB2DFileElement,
):
    """
    Collection of wildcards, used to replace values.
    """

    name: str
    """
    Unique name for this Wildcard Set.
    """

    description: str | None
    """
    Human-readable description of this Wildcard Set.
    """

    user_replacement_values: Dict[str, str]
    """
    User-defined wildcard replacement values.
    """

    system_replacement_values: Dict[str, str]
    """
    System-defined wildcard replacement values.
    """

    _MAX_REPLACEMENT_DEPTH = 1000

    def __init__(
        self,
        name: str,
        description: str | None = None,
        user_replacement_values: Dict[str, str] | None = None,
    ):
        IB2DFileElement.__init__(
            self=self,
        )

        self.name = name

        if description is None:
            description = ''

        self.description = description

        self.user_replacement_values = self.manager.dict()

        if user_replacement_values is not None:
            for key, value in user_replacement_values.items():
                self.user_replacement_values[key] = value

        self.system_replacement_values = self.manager.dict()

    def __str__(
        self,
    ) -> str:

        return self.name

    @property
    @log_exception
    def __replacement_values(
        self,
    ) -> Dict[str, str]:

        return {f'${{{key}}}': value for key, value in self.replacement_values.items()}

    @property
    def replacement_values(
        self,
    ) -> Dict[str, str]:

        system_replacement_values = dict(
            self.system_replacement_values,
        )

        user_replacement_values = dict(
            self.user_replacement_values,
        )

        return system_replacement_values | user_replacement_values

    @log_exception
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

        for key, value in self.__replacement_values.items():
            string = string.replace(
                key,
                value,
            )

        if any(key in string for key in self.__replacement_values.keys()):
            recursion_depth += 1

            string = self.replace_wildcards(
                string=string,
                recursion_depth=recursion_depth,
            )

        return string

    @classmethod
    @log_exception
    def deserialize(
        cls,
        instance_data: Dict,
        working_dir_path: Path,
        ib2d_file: ZipFile,
        wildcard_sets: Self | None = None,
    ) -> Self:

        return WildcardSet(
            name=instance_data['name'],
            description=instance_data['description'],
            user_replacement_values=instance_data['replacement_values'],
        )

    @log_exception
    def serialize(
        self,
        ib2d_file: ZipFile,
    ) -> Dict:

        replacement_values = dict(
            self.user_replacement_values,
        )

        return {
            'description': self.description,
            'replacement_values': replacement_values,
        }
