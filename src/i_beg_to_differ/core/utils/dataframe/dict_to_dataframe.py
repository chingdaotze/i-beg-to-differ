from typing import Dict

from pandas import DataFrame


def dict_to_dataframe(
    data: Dict,
    index: str,
    column: str,
) -> DataFrame:
    """
    Converts a dictionary to a DataFrame, where keys are the Index and values are Values.

    :param data: Dictionary of data to convert.
    :param index: Desired index name.
    :param column: Desired column name.
    :return: DataFrame, where keys are the Index and values are Values.
    """

    index_values = []
    column_values = []

    for key, value in data.items():
        index_values.append(
            key,
        )

        column_values.append(
            value,
        )

    data = DataFrame(
        data={
            index: index_values,
            column: column_values,
        }
    )

    data.set_index(
        keys=[index],
        inplace=True,
    )

    return data
