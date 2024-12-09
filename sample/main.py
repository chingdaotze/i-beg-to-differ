from pathlib import Path

from i_beg_to_differ.core.ib2d_file import IB2DFile
from i_beg_to_differ.extensions.data_sources.data_source_csv import DataSourceCsv
from i_beg_to_differ.extensions.data_sources.data_source_excel import DataSourceExcel
from i_beg_to_differ.core.compare_sets.compare_set import CompareSet
from i_beg_to_differ.core.compare_sets.compare_set.compare import Compare
from i_beg_to_differ.core.compare_sets.compare_set.compare.data_source_reference import (
    DataSourceReference,
)
from i_beg_to_differ.core.compare_sets.compare_set.compare.field_reference_pair import (
    FieldReferencePairPrimaryKey,
)
from i_beg_to_differ.core import open_ib2d_file


def main() -> None:
    # Set up basic variables
    sample_dir = Path(
        __file__,
    ).parent

    input_dir = sample_dir / 'input'
    output_dir = sample_dir / 'output'

    # Create *.ib2d file object
    ib2d_file = IB2DFile()

    # Create Data Sources
    data_source_csv = DataSourceCsv(
        path=str(
            input_dir / 'sample.csv',
        ),
    )

    data_source_excel = DataSourceExcel(
        path=str(
            input_dir / 'sample.xlsx',
        ),
        sheet='Data',
    )

    # Attach Data Sources to *.ib2d file
    ib2d_file.data_sources.append(
        data_source=data_source_csv,
    )

    ib2d_file.data_sources.append(
        data_source=data_source_excel,
    )

    # Create Compare Set object
    compare_set = CompareSet(
        name='My Compare Set',
    )

    # Create Compares
    compare = Compare(
        name='My Compare',
        source_data_source_ref=DataSourceReference(
            data_source_name=str(
                data_source_csv,
            ),
        ),
        target_data_source_ref=DataSourceReference(
            data_source_name=str(
                data_source_excel,
            ),
        ),
        data_sources=ib2d_file.data_sources,
        pk_fields=[
            FieldReferencePairPrimaryKey(
                source_field_name='pk0',
                target_field_name='pk0',
            ),
            FieldReferencePairPrimaryKey(
                source_field_name='pk1',
                target_field_name='pk1',
            ),
        ],
    )

    compare.dt_fields = compare.auto_match_dt_fields

    # Attach Compare to Compare Set
    compare_set.append(
        compare=compare,
    )

    # Attach Compare Set to *.ib2d file
    ib2d_file.compare_sets.append(
        compare_set=compare_set,
    )

    # Run comparison, with Excel
    ib2d_file.compare_sets.to_excel(
        dir_path=output_dir,
    )

    # Save *.ib2d file
    ib2d_file_path = output_dir / 'sample.ib2d'

    ib2d_file.save(
        path=ib2d_file_path,
    )

    # Load *.ib2d file
    with open_ib2d_file(path=ib2d_file_path) as new_ib2d_file:

        # Run comparison again, this time with CSV
        new_ib2d_file.compare_sets.to_csv(
            dir_path=output_dir,
        )

    print(
        'Done!',
    )


if __name__ == '__main__':
    main()
