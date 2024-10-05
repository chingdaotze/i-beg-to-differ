from pytest import fixture
from pathlib import Path
from typing import Dict

from pandas import (
    DataFrame,
    read_excel,
)


@fixture
def excel_file_benchmarks(
    benchmarks_dir: Path,
    test_name: str,
) -> Dict[str, DataFrame]:

    excel_file_path = benchmarks_dir / f'{test_name}.xlsx'

    excel_data = read_excel(
        io=excel_file_path,
        sheet_name=None,
    )

    return excel_data
