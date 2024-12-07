from typing import (
    List,
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

    _wildcard_sets: List[WildcardSet]
    _active_wildcard_set: WildcardSet | None
    _DEFAULT_WILDCARD_SET = 'Default'

    def __init__(
        self,
        wildcard_sets: List[WildcardSet] | None = None,
    ):
        IB2DFileElement.__init__(
            self=self,
        )

        # Init all wildcard sets
        self._wildcard_sets = self.manager.list()

        if wildcard_sets is None:
            self.append(
                WildcardSet(
                    name=self._DEFAULT_WILDCARD_SET,
                    description='Default system-provided Wildcard Set.',
                )
            )

        else:
            for wildcard_set in wildcard_sets:
                self.append(
                    wildcard_set=wildcard_set,
                )

        # Set active wildcard set
        if self._wildcard_sets:
            self.active_wildcard_set = self._wildcard_sets[0].name

        else:
            self.active_wildcard_set = None

    def __str__(
        self,
    ) -> str:

        return 'Wildcard Sets'

    def __getitem__(
        self,
        wildcard_set: str | WildcardSet,
    ) -> WildcardSet:

        key = str(
            wildcard_set,
        )

        return self.wildcard_sets[key]

    @property
    def wildcard_sets(
        self,
    ) -> Dict[str, WildcardSet]:
        """
        All wildcard sets, as a dictionary.
        """

        return {str(wildcard_set): wildcard_set for wildcard_set in self._wildcard_sets}

    def append(
        self,
        wildcard_set: WildcardSet,
    ) -> None:
        """
        Add wildcard set to the collection of wildcard sets.

        :param wildcard_set: Wildcard set to add.
        :return:
        """

        if wildcard_set not in self._wildcard_sets:
            self._wildcard_sets.append(
                wildcard_set,
            )

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
    # @log_exception
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

            wildcard_sets = self.wildcard_sets

            if name in wildcard_sets:
                self._active_wildcard_set = wildcard_sets[name]

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

        for name, wildcard_set_values in instance_data.items():
            wildcard_set_values['name'] = name

        return WildcardSets(
            wildcard_sets=[
                WildcardSet.deserialize(
                    instance_data=wildcard_set_values,
                    working_dir_path=working_dir_path,
                    ib2d_file=ib2d_file,
                    wildcard_sets=wildcard_sets,
                )
                for wildcard_set_values in instance_data.values()
            ],
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
