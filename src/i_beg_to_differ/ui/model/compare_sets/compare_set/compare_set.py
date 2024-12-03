from ...model_base import ModelBase
from .....core.compare_sets.compare_set import CompareSet
from .compare import ModelCompare


class ModelCompareSet(
    ModelBase,
):

    def __init__(
        self,
        object_name: str,
        compare_set: CompareSet,
    ):

        ModelBase.__init__(
            self=self,
            current_state=compare_set,
            object_name=object_name,
        )

        for name, compare in compare_set.compares.items():

            self.appendRow(
                ModelCompare(
                    object_name=name,
                    compare=compare,
                )
            )
