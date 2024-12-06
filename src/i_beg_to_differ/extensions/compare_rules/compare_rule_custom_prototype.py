from typing import Dict

from pandas import Series


def compare(
    source_field: Series,
    target_field: Series,
    wildcards: Dict[str, str],
) -> Series:
    """
    Compares values between source and target fields, using custom Python code.
    The return value should be a Series of booleans, where True indicates a match
    and False indicates a mismatch.

    :param source_field: Source field to compare.
    :param target_field: Target field to compare.
    :return: Series of booleans, where True indicates a match.
    """

    return source_field == target_field
