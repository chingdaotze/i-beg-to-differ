from abc import ABC
from typing import (
    Dict,
    Type,
)
from types import ModuleType
from pkgutil import iter_modules
from importlib import import_module
from inspect import (
    getmembers,
    isclass,
)

from ..base import Base
from .extension import Extension


class Extensions[T](
    Base,
    ABC,
):

    _collection: Dict[str, Type[T]]

    def __init__(
        self,
        namespace_package: ModuleType,
    ):

        Base.__init__(
            self=self,
        )

        self._collection = {}

        for module in iter_modules(
            path=namespace_package.__path__,
            prefix=namespace_package.__name__ + '.',
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
                        extension_type=member,
                    )

                    self.log_info(
                        msg=f'Registered extension: {member.get_extension_id()}',
                    )

    def __str__(
        self,
    ) -> str:

        return self.__module__

    def register(
        self,
        extension_type: Type[Extension],
    ) -> None:

        extension_id = extension_type.get_extension_id()

        if extension_id in self._collection:
            raise KeyError(
                f'Extension: {extension_id} has already been registered!',
            )

        else:
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
