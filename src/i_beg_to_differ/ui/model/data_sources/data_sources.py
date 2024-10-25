from ..base import ModelBase
from ....core.data_sources import DataSources
from .data_source import ModelDataSource


class ModelDataSources(
    ModelBase,
):

    def __init__(
        self,
        data_sources: DataSources,
    ):

        ModelBase.__init__(
            self=self,
            current_state=data_sources,
        )

        for name, data_source in data_sources.data_sources.items():

            self.appendRow(
                ModelDataSource(
                    object_name=name,
                    data_source=data_source,
                )
            )
