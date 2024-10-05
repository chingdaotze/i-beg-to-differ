from pathlib import Path
from typing import (
    Callable,
    List,
    Dict,
    Self,
)
from zipfile import ZipFile
from io import (
    StringIO,
    BytesIO,
)

from pandas import ExcelWriter

from ....ib2d_file.ib2d_file_element import IB2DFileElement
from ....compare_engine import CompareEngine
from .data_source_pair import DataSourcePair
from .field_pair import (
    FieldPairPrimaryKey,
    FieldPairData,
)
from ....base import log_exception
from ....data_sources import DataSources
from ....wildcards_sets import WildcardSets


class Compare(
    IB2DFileElement,
    CompareEngine,
):
    """
    Compare object.
    """

    description: str | None
    """
    Human-readable description.
    """

    data_source_pair: DataSourcePair
    """
    Data source pair.
    """

    init_caches: Callable
    """
    Convenience stub to underlying data_sources.init_caches.
    """

    def __init__(
        self,
        data_sources: DataSources,
        data_source_pair: DataSourcePair,
        pk_fields: List[FieldPairPrimaryKey] | None = None,
        dt_fields: List[FieldPairData] | None = None,
        description: str | None = None,
    ):
        IB2DFileElement.__init__(
            self=self,
        )

        CompareEngine.__init__(
            self=self,
            data_sources=data_sources,
            source=data_source_pair.source,
            target=data_source_pair.target,
            pk_fields=pk_fields,
            dt_fields=dt_fields,
        )

        self.description = description
        self.data_source_pair = data_source_pair
        self.init_caches = self.data_source_pair.init_caches

    def __str__(
        self,
    ) -> str:
        # TODO: Implement hash to make this unique

        return str(
            self.data_source_pair,
        )

    @classmethod
    @log_exception
    def deserialize(
        cls,
        instance_data: Dict,
        working_dir_path: Path,
        ib2d_file: ZipFile,
        data_sources: DataSources,
        wildcard_sets: WildcardSets | None = None,
    ) -> Self:

        data_source_pair = DataSourcePair.deserialize(
            instance_data=instance_data,
            working_dir_path=working_dir_path,
            ib2d_file=ib2d_file,
            data_sources=data_sources,
            wildcard_sets=wildcard_sets,
        )

        pk_fields = [
            FieldPairPrimaryKey.deserialize(
                instance_data=pk_field_data,
                working_dir_path=working_dir_path,
                ib2d_file=ib2d_file,
                wildcard_sets=wildcard_sets,
            )
            for pk_field_data in instance_data['pk_fields']
        ]

        dt_fields = [
            FieldPairData.deserialize(
                instance_data=dt_field_data,
                working_dir_path=working_dir_path,
                ib2d_file=ib2d_file,
                wildcard_sets=wildcard_sets,
            )
            for dt_field_data in instance_data['dt_fields']
        ]

        return Compare(
            data_sources=data_sources,
            data_source_pair=data_source_pair,
            pk_fields=pk_fields,
            dt_fields=dt_fields,
            description=instance_data['description'],
        )

    @log_exception
    def serialize(
        self,
        ib2d_file: ZipFile,
    ) -> Dict:

        return {
            'description': self.description,
            'source': self.source,
            'target': self.target,
            'pk_fields': [
                instance.serialize(
                    ib2d_file=ib2d_file,
                )
                for instance in self.pk_fields
            ],
            'dt_fields': [
                instance.serialize(
                    ib2d_file=ib2d_file,
                )
                for instance in self.dt_fields
            ],
        }

    def to_csv(
        self,
        dir_path: Path,
        file_name_prefix: str | None = None,
        file_name_suffix: str | None = None,
    ) -> None:
        """
        Writes all reports as *.csv files to a specified directory.

        :param dir_path: Directory to save reports.
        :param file_name_prefix: File name prefix for *.csv files.
        :param file_name_suffix: File name suffix for *.csv files.
        :return:
        """

        if file_name_prefix is None:
            file_name_prefix = ''

        if file_name_suffix is None:
            file_name_suffix = ''

        self.log_info(
            msg=f'Saving *.csv file reports to location: "{str(dir_path.absolute())}" ...',
        )

        csv_buffers = {
            'schema_compare': StringIO(),
            'values_compare': StringIO(),
            'src_only': StringIO(),
            'tgt_only': StringIO(),
            'src_dup': StringIO(),
            'tgt_dup': StringIO(),
        }

        self.data_source_pair.schema_comparison.to_csv(
            path_or_buf=csv_buffers['schema_compare'],
        )

        self.values_comparison.to_csv(
            path_or_buf=csv_buffers['values_compare'],
        )

        self.source_only_records.to_csv(
            path_or_buf=csv_buffers['src_only'],
        )

        self.target_only_records.to_csv(
            path_or_buf=csv_buffers['tgt_only'],
        )

        self.source_duplicate_primary_key_records.to_csv(
            path_or_buf=csv_buffers['src_dup'],
        )

        self.source_duplicate_primary_key_records.to_csv(
            path_or_buf=csv_buffers['tgt_dup'],
        )

        for csv_name, buffer in csv_buffers.items():
            csv_path = dir_path / f'{file_name_prefix}{csv_name}{file_name_suffix}.csv'

            with open(file=csv_path, mode='w') as csv_file:
                csv_file.write(
                    buffer.getvalue(),
                )

        self.log_info(
            msg=f'Save complete: "{str(dir_path.absolute())}"',
        )

    def to_excel(
        self,
        path: Path,
    ) -> None:
        """
        Writes all reports as sheets in a specified Excel file.

        :param path: Path to the Excel file.
        :return:
        """

        self.log_info(
            msg=f'Saving Excel file report to location: "{str(path.absolute())}" ...',
        )

        excel_file_buffer = BytesIO()

        excel_writer = ExcelWriter(
            path=excel_file_buffer,
            engine='openpyxl',
        )

        self.data_source_pair.schema_comparison.to_excel(
            excel_writer=excel_writer,
            sheet_name='schema_compare',
        )

        self.values_comparison.to_excel(
            excel_writer=excel_writer,
            sheet_name='values_compare',
        )

        self.source_only_records.to_excel(
            excel_writer=excel_writer,
            sheet_name='src_only',
        )

        self.target_only_records.to_excel(
            excel_writer=excel_writer,
            sheet_name='tgt_only',
        )

        self.source_duplicate_primary_key_records.to_excel(
            excel_writer=excel_writer,
            sheet_name='src_dup',
        )

        self.source_duplicate_primary_key_records.to_excel(
            excel_writer=excel_writer,
            sheet_name='tgt_dup',
        )

        excel_writer.close()

        with open(file=path, mode='wb') as excel_file:
            excel_file.write(
                excel_file_buffer.getvalue(),
            )

        self.log_info(
            msg=f'Save complete: "{str(path.absolute())}"',
        )
