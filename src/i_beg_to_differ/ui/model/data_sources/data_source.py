from ..model_base_extension import ModelBaseExtension
from ....core.data_sources.data_source import DataSource


class ModelDataSource(
    ModelBaseExtension,
):

    def __init__(
        self,
        object_name: str,
        data_source: DataSource,
    ):
        self._object_name = object_name

        ModelBaseExtension.__init__(
            self=self,
            current_state=data_source,
            object_name=object_name,
        )
