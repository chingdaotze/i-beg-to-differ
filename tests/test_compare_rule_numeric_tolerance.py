from typing import Dict

from pandas import DataFrame

from .fixture_ib2d_file import ib2d_file
from .fixture_parquet_benchmarks import parquet_benchmarks
from i_beg_to_differ.core import IB2DFile


def test_compare_rule_numeric_tolerance(
    ib2d_file: IB2DFile,
    parquet_benchmarks: Dict[str, DataFrame],
) -> None:

    with ib2d_file:
        compare_set = ib2d_file.compare_sets['CompareSet0']
        compare = compare_set['Compare1']

        assert parquet_benchmarks['values_comparison'].equals(
            other=compare.values_comparison,
        )

        assert parquet_benchmarks['source_only_records'].equals(
            other=compare.source_only_records,
        )

        assert parquet_benchmarks['target_only_records'].equals(
            other=compare.target_only_records,
        )
