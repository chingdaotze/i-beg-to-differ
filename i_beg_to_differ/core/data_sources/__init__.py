from typing import (
    Dict,
    Type,
)

from .data_source import DataSource


class DataSources:
    """
    Contains and manages all DataSource types for this package.
    """

    data_sources: Dict[str, Type[DataSource]]
    """
    Collection of registered DataSource definitions.
    """

    def __init__(
        self,
    ):
        self.data_sources = {}

    def register_data_source(
        self,
        new_data_source: Type[DataSource],
    ) -> None:
        """
        Register a new DataSource type. Call this method to add a custom DataSource.

        :param new_data_source: New DataSource class definition.
        :return:
        """

        self.data_sources[new_data_source.type_id] = new_data_source

    def get_data_source(
        self,
        type_id: str,
    ) -> Type[DataSource]:
        """
        Retrieve a DataSource type.

        :param type_id: DataSource type identifier.
        :return: DataSource class definition.
        """

        if type_id in self.data_sources:
            return self.data_sources[type_id]

        else:
            raise KeyError(
                f'DataSource type: "{type_id}" not defined! Ensure that the DataSource has been registered.',
            )
