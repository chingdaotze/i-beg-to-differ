from pathlib import Path
from pytest import fixture
from typing import Dict
from pandas import (
    DataFrame,
    read_csv,
)


def load_csv_files(
    path: Path,
) -> Dict[str, DataFrame]:

    csv_files = path.glob(
        pattern='*.csv',
    )

    return {
        path.stem: read_csv(
            filepath_or_buffer=path,
        )
        for path in csv_files
    }


@fixture
def csv_benchmarks(
    benchmarks_dir: Path,
) -> Dict[str, DataFrame]:

    return load_csv_files(
        path=benchmarks_dir,
    )
