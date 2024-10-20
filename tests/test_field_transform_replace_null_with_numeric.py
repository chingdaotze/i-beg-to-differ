from pathlib import Path
from typing import Dict

from pandas import DataFrame

from .fixture_ib2d_file import ib2d_file
from .fixture_parquet_benchmarks import parquet_benchmarks
from i_beg_to_differ.core import IB2DFile


def test_field_transform_replace_null_with_numeric(
    ib2d_file: IB2DFile,
    tmp_path: Path,
    parquet_benchmarks: Dict[str, DataFrame],
) -> None:
    with ib2d_file:

        compare_set = ib2d_file.compare_sets['CompareSet0']
        compare = compare_set['Compare1']

        report_path = tmp_path / 'report.xlsx'
        compare.to_excel(
            path=report_path,
        )

        for benchmark_name, benchmark_data in parquet_benchmarks.items():
            assert benchmark_data.equals(
                other=compare.all_reports[benchmark_name],
            )
