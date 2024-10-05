from pytest import fixture
from pathlib import Path
from typing import Dict
from pandas import (
    DataFrame,
    read_parquet,
)


@fixture
def parquet_benchmarks(
    benchmarks_dir: Path,
) -> Dict[str, DataFrame]:

    parquet_files = benchmarks_dir.glob(
        pattern='*.parquet',
    )

    return {
        path.stem: read_parquet(
            path=path,
        )
        for path in parquet_files
    }
