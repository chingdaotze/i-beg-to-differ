from pathlib import Path
from typing import Dict

from pandas import DataFrame

from .fixture_ib2d_file import ib2d_file
from .fixture_csv_benchmarks import (
    csv_benchmarks,
    load_csv_files,
)
from i_beg_to_differ.core import IB2DFile
from .compare_benchmarks import compare_benchmark_data


def test_report_csv(
    ib2d_file: IB2DFile,
    tmp_path: Path,
    csv_benchmarks: Dict[str, DataFrame],
) -> None:
    with ib2d_file:

        compare_set = ib2d_file.compare_sets['CompareSet0']
        compare = compare_set['Compare1']

        compare.to_csv(
            dir_path=tmp_path,
        )

        csv_files = load_csv_files(
            path=tmp_path,
        )

        compare_benchmark_data(
            ib2d_file=ib2d_file,
            benchmarks=csv_benchmarks,
            test_reports=csv_files,
        )
