from pathlib import Path
from typing import (
    Dict,
    Self,
)
from zipfile import ZipFile

from ..ib2d_file.ib2d_file_element import IB2DFileElement
from ..input_fields import (
    StringInputField,
    DictInputField,
)
from ..base import log_exception


class WildcardSet(
    IB2DFileElement,
):
    """
    Collection of wildcards, used to replace values.
    """

    description: StringInputField
    """
    Human-readable description of this Wildcard Set.
    """

    user_replacement_values: DictInputField
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
        description: str | None = None,
        user_replacement_values: Dict[str, str] | None = None,
    ):
        IB2DFileElement.__init__(
            self=self,
        )

        self.description = StringInputField(
            title='Description',
            value=description,
        )

        user_replacement_values_ = self.manager.dict()

        if user_replacement_values is not None:
            for key, value in user_replacement_values.items():
                user_replacement_values_[key] = value

        self.user_replacement_values = DictInputField(
            title='Wildcards',
            values=user_replacement_values_,
            key_column='Wildcard Name',
            value_column='Wildcard Value',
        )

        self.system_replacement_values = self.manager.dict()

    def __str__(
        self,
    ) -> str:

        return str(
            self.replacement_values,
        )

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

        system_replacement_values = dict(self.system_replacement_values)
        user_replacement_values = dict(self.user_replacement_values.values)

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
            description=instance_data['description'],
            user_replacement_values=instance_data['replacement_values'],
        )

    @log_exception
    def serialize(
        self,
        ib2d_file: ZipFile,
    ) -> Dict:

        return {
            'description': self.description,
            'replacement_values': self.user_replacement_values,
        }
