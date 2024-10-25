from ..base import ModelBase
from ....core.wildcards_sets.wildcard_set import WildcardSet


class ModelWildcardSet(
    ModelBase,
):

    def __init__(
        self,
        object_name: str,
        wildcard_set: WildcardSet,
    ):

        ModelBase.__init__(
            self=self,
            current_state=wildcard_set,
            object_name=object_name,
        )
