from ..base import ModelBase
from ....core.data_sources import DataSources


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
