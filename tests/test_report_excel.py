from pathlib import Path
from typing import Dict

from pandas import (
    DataFrame,
    read_excel,
)

from .fixture_ib2d_file import ib2d_file
from .fixture_excel_file_benchmarks import excel_file_benchmarks
from i_beg_to_differ.core import IB2DFile
from .compare_benchmarks import compare_benchmark_data


def test_report_excel(
    ib2d_file: IB2DFile,
    tmp_path: Path,
    excel_file_benchmarks: Dict[str, DataFrame],
) -> None:
    with ib2d_file:

        compare_set = ib2d_file.compare_sets['CompareSet0']
        compare = compare_set['Compare1']

        report_path = tmp_path / 'report.xlsx'
        compare.to_excel(
            path=report_path,
        )

        excel_file = read_excel(
            io=report_path,
            sheet_name=None,
        )

        compare_benchmark_data(
            ib2d_file=ib2d_file,
            benchmarks=excel_file_benchmarks,
            test_reports=excel_file,
        )
