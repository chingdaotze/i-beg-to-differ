from pytest import fixture
from typing import Dict
from pandas import (
    DataFrame,
    read_parquet,
)
from pathlib import Path


@fixture
def parquet_files(
    request,
) -> Dict[str, DataFrame]:
    test_name = request.node.name
    test_dir = Path(
        f'tests/test_artifacts/{test_name}',
    )

    parquet_files = test_dir.glob(
        pattern='*.parquet',
    )

    return {path.stem: read_parquet(path=path) for path in parquet_files}
