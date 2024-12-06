from typing import Dict

from pandas import Series


def transform(
    values: Series,
    wildcards: Dict[str, str],
) -> Series:
    """
    Transforms values for a single Field.

    :param values: Values to transform.
    :param wildcards: Current active wildcard set.
    :return: Transformed values.
    """

    return values
