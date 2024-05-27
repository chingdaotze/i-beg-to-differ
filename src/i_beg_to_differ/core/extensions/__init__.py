from abc import ABC
from typing import (
    Dict,
    Type,
)

from .extension import Extension


class Extensions[T](
    ABC,
):

    _collection: Dict[str, Type[Extension]]

    def __init__(
        self,
    ):

        self._collection = {}

    def register(
        self,
        extension_type: Type[Extension],
    ) -> None:

        if extension_type.extension_id in self._collection:

            raise KeyError(
                f"Extension: {extension_type.extension_id} has already been registered!",
            )

        else:

            self._collection[extension_type.extension_id] = new_type

    def __getitem__(
        self,
        extension_id: str,
    ) -> Type[T]:

        if extension_id in self._collection:

            return self._collection[extension_id]

        else:

            raise KeyError(
                f"Extension: {extension_id} has not been registered!",
            )
