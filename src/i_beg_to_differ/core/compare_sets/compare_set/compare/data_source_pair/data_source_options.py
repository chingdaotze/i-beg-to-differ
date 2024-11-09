from typing import List

from .....data_sources import DataSources
from .....input_fields.input_field_options import InputFieldOptions


class DataSourceOptions(
    InputFieldOptions,
):

    data_sources: DataSources

    def __init__(
        self,
        data_sources: DataSources,
    ):

        self.data_sources = data_sources

    @property
    def options(
        self,
    ) -> List[str]:

        return list(
            self.data_sources.data_sources.keys(),
        )
