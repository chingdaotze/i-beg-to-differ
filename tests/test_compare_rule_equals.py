from .fixture_ib2d_file import ib2d_file
from .fixture_logger import logger
from .fixture_parquet_files import parquet_files


def test_compare_rule_equals(
    ib2d_file,
    logger,
    parquet_files,
) -> None:
    with ib2d_file:

        compare_set = ib2d_file.compare_sets['CompareSet0']
        compare = compare_set['Compare1']

        values_comparison = compare.values_comparison
        source_only_records = compare.source_only_records
        target_only_records = compare.target_only_records
        schema_comparison = compare.data_source_pair.schema_comparison
        source_duplicate_records = compare.source_duplicate_primary_key_records
        target_duplicate_records = compare.target_duplicate_primary_key_records

        pass
