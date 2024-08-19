from abc import ABC
from typing import (
    Dict,
    Type,
)
from pkgutil import iter_modules
from importlib import import_module
from inspect import (
    getmembers,
    isclass,
)

from .extension import Extension


class Extensions[T](
    ABC,
):

    _collection: Dict[str, Type[Extension]]

    def __init__(
        self,
        path: str,
        name: str,
    ):
        self._collection = {}

        for module in iter_modules(
            path=path,
            prefix=f'{name}.',
        ):
            extension_module = import_module(
                name=module.name,
            )

            for _, member in getmembers(object=extension_module):
                if (
                    isclass(
                        member,
                    )
                    and issubclass(
                        member,
                        Extension,
                    )
                    and member.__module__ == extension_module.__name__
                ):
                    self.register(
                        extension_type=member, extension_id=module.name.split('.')[-1]
                    )

    def register(
        self,
        extension_type: Type[Extension],
        extension_id: str,
    ) -> None:

        if extension_id in self._collection:
            raise KeyError(
                f'Extension: {extension_id} has already been registered!',
            )

        else:
            extension_type.extension_id = extension_id
            self._collection[extension_id] = extension_type

    def __getitem__(
        self,
        extension_id: str,
    ) -> Type[T]:

        if extension_id in self._collection:
            return self._collection[extension_id]

        else:
            raise KeyError(
                f'Extension: {extension_id} has not been registered!',
            )
