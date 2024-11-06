from typing import (
    Dict,
    Self,
)
from pathlib import Path
from zipfile import ZipFile

from ..ib2d_file.ib2d_file_element import IB2DFileElement
from ..base import log_exception
from .wildcard_set import WildcardSet


class WildcardSets(
    IB2DFileElement,
):
    """
    Collection of wildcard sets, used to replace values.
    """

    wildcard_sets: Dict[str, WildcardSet]
    _active_wildcard_set: WildcardSet | None
    _DEFAULT_WILDCARD_SET = 'Default'

    def __init__(
        self,
        wildcard_sets: Dict[str, WildcardSet] | None = None,
    ):
        IB2DFileElement.__init__(
            self=self,
        )

        self.wildcard_sets = self.manager.dict()

        if wildcard_sets is None:
            self.wildcard_sets[self._DEFAULT_WILDCARD_SET] = WildcardSet(
                description='Default system-provided Wildcard Set.'
            )

        else:
            for key, value in wildcard_sets.items():
                self.wildcard_sets[key] = value

        if self.wildcard_sets:
            self.active_wildcard_set = next(iter(self.wildcard_sets))

        else:
            self.active_wildcard_set = None

    def __str__(
        self,
    ) -> str:

        return 'Wildcard Sets'

    @property
    def active_wildcard_set(
        self,
    ) -> WildcardSet:
        """
        Gets the current active wildcard set.

        :return: Active wildcard set.
        """

        return self._active_wildcard_set

    @active_wildcard_set.setter
    @log_exception
    def active_wildcard_set(
        self,
        name: str | None,
    ) -> None:
        """
        Sets the current active wildcard set, using the wildcard set's name.

        :param name: Wildcard set name.
        :return:
        """

        if name is not None:

            if name in self.wildcard_sets:
                self._active_wildcard_set = self.wildcard_sets[name]

            else:
                raise KeyError(
                    f'Wildcard set: "{name}" not found!',
                )

        else:

            self._active_wildcard_set = None

    @log_exception
    def replace_wildcards(
        self,
        string: str,
    ) -> str:
        """
        Replaces wildcards in a provided string, using the current active wildcard set.

        :param string: Original string.
        :return: String with wildcard replacement.
        """

        if isinstance(self.active_wildcard_set, WildcardSet):

            return self.active_wildcard_set.replace_wildcards(
                string=string,
            )

        else:

            return string

    @log_exception
    def update_system_wildcard(
        self,
        key: str,
        value: str,
    ) -> None:

        for instance in self.wildcard_sets.values():

            instance.system_replacement_values[key] = value

    @classmethod
    @log_exception
    def deserialize(
        cls,
        instance_data: Dict,
        working_dir_path: Path,
        ib2d_file: ZipFile,
        wildcard_sets: Self | None = None,
    ) -> Self:

        return WildcardSets(
            wildcard_sets={
                name: WildcardSet.deserialize(
                    instance_data=wildcard_set_values,
                    working_dir_path=working_dir_path,
                    ib2d_file=ib2d_file,
                    wildcard_sets=wildcard_sets,
                )
                for name, wildcard_set_values in instance_data.items()
            },
        )

    @log_exception
    def serialize(
        self,
        ib2d_file: ZipFile,
    ) -> Dict:

        return {
            name: instance.serialize(
                ib2d_file=ib2d_file,
            )
            for name, instance in self.wildcard_sets.items()
        }
