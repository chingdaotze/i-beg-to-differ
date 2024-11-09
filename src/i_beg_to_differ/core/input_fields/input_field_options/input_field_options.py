from abc import (
    ABC,
    abstractmethod,
)
from typing import List


class InputFieldOptions(
    ABC,
):

    @property
    @abstractmethod
    def options(
        self,
    ) -> List[str]:
        """
        Abstract property that returns a list of possible options.

        :return:
        """
