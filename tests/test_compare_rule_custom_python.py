from pathlib import Path
from typing import Dict

from pandas import DataFrame

from .fixture_ib2d_file import ib2d_file
from .fixture_parquet_benchmarks import parquet_benchmarks
from i_beg_to_differ.core import IB2DFile
from .compare_benchmarks import compare_benchmarks


def test_compare_rule_custom_python(
    ib2d_file: IB2DFile,
    tmp_path: Path,
    parquet_benchmarks: Dict[str, DataFrame],
) -> None:

    compare_benchmarks(
        ib2d_file=ib2d_file,
        tmp_path=tmp_path,
        benchmarks=parquet_benchmarks,
    )
