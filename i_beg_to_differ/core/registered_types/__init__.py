from abc import ABC
from typing import (
    Dict,
    Type,
)

from .registered_type import RegisteredType


class RegisteredTypes[T](
    ABC,
):

    _collection: Dict[str, Type[RegisteredType]]

    def __init__(
        self,
    ):

        self._collection = {}

    def register(
        self,
        new_type: Type[RegisteredType],
    ) -> None:

        if new_type.name in self._collection:

            raise KeyError(
                f"Type: {new_type.name} has already been registered!",
            )

        else:

            self._collection[new_type.name] = new_type

    def __getitem__(
        self,
        name: str,
    ) -> Type[T]:

        if name in self._collection:

            return self._collection[name]

        else:

            raise KeyError(
                f"{name} has not been registered!",
            )
