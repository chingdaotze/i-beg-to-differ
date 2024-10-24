from ..base import ModelBase
from ....core.wildcards_sets import WildcardSets
from .wildcard_set import ModelWildcardSet


class ModelWildcardSets(
    ModelBase,
):

    def __init__(
        self,
        wildcard_sets: WildcardSets,
    ):

        ModelBase.__init__(
            self=self,
            current_state=wildcard_sets,
        )

        for name, wildcard_set in wildcard_sets.wildcard_sets.items():

            self.appendRow(
                ModelWildcardSet(
                    object_name=name,
                    wildcard_set=wildcard_set,
                )
            )
