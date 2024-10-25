from ..base import ModelBase
from ....core.compare_sets import CompareSets
from .compare_set import ModelCompareSet


class ModelCompareSets(
    ModelBase,
):

    def __init__(
        self,
        compare_sets: CompareSets,
    ):

        ModelBase.__init__(
            self=self,
            current_state=compare_sets,
        )

        for name, compare_set in compare_sets.compare_sets.items():

            self.appendRow(
                ModelCompareSet(
                    object_name=name,
                    compare_set=compare_set,
                )
            )
