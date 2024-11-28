from pathlib import Path
from typing import Dict

from pandas import DataFrame

from .fixture_ib2d_file import ib2d_file
from i_beg_to_differ.core import IB2DFile


def compare_benchmark_data(
    ib2d_file: IB2DFile,
    benchmarks: Dict[str, DataFrame],
    test_reports: Dict[str, DataFrame],
) -> None:
    test_failure = False

    for benchmark_name, benchmark_data in benchmarks.items():
        test_data = test_reports[benchmark_name]

        if not benchmark_data.equals(
            other=test_data,
        ):
            ib2d_file.log_info(
                f'{benchmark_name} Test Failure!\n\nBenchmark:\n\n{benchmark_data.to_markdown()}'
                f'\n\nTest Data:\n\n{test_data.to_markdown()}\n\n'
            )

            test_failure = True

    if test_failure:
        raise ValueError(
            'Benchmark(s) do not match test data! See log for details.',
        )


def compare_benchmarks(
    ib2d_file: IB2DFile,
    tmp_path: Path,
    benchmarks: Dict[str, DataFrame],
) -> None:
    with ib2d_file:

        compare_set = ib2d_file.compare_sets['CompareSet0']
        compare = compare_set['Compare1']

        report_path = tmp_path / 'report.xlsx'
        compare.to_excel(
            path=report_path,
        )
        compare.to_parquet(
            dir_path=tmp_path,
        )

        compare_benchmark_data(
            ib2d_file=ib2d_file,
            benchmarks=benchmarks,
            test_reports=compare.all_reports,
        )
