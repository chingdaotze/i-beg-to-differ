from pathlib import Path
from typing import (
    Callable,
    List,
    Dict,
    Self,
)
from zipfile import ZipFile
from functools import cached_property
from io import (
    StringIO,
    BytesIO,
)

from pandas import (
    DataFrame,
    ExcelWriter,
)

from ....ib2d_file.ib2d_file_element import IB2DFileElement
from ....compare_engine import (
    CompareEngine,
    AUTO_MATCH,
)
from ....input_fields import TextBoxInputField
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

    description: TextBoxInputField
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
        pk_fields: List[FieldPairPrimaryKey] | AUTO_MATCH | None = None,
        dt_fields: List[FieldPairData] | AUTO_MATCH | None = None,
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

        self.description = TextBoxInputField(
            title='Description',
            value=description,
        )

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

        pk_fields = instance_data['pk_fields']

        if isinstance(pk_fields, list):
            pk_fields = [
                FieldPairPrimaryKey.deserialize(
                    instance_data=pk_field_data,
                    working_dir_path=working_dir_path,
                    ib2d_file=ib2d_file,
                    wildcard_sets=wildcard_sets,
                )
                for pk_field_data in pk_fields
            ]

        dt_fields = instance_data['dt_fields']

        if isinstance(dt_fields, list):
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

        if isinstance(self.base_pk_fields, list):
            pk_fields = [
                instance.serialize(
                    ib2d_file=ib2d_file,
                )
                for instance in self.base_pk_fields
            ]

        else:
            pk_fields = self.base_pk_fields

        if isinstance(self.base_dt_fields, list):
            dt_fields = [
                instance.serialize(
                    ib2d_file=ib2d_file,
                )
                for instance in self.base_dt_fields
            ]

        else:
            dt_fields = self.base_dt_fields

        return {
            'description': self.description.value,
            'source': self.source,
            'target': self.target,
            'pk_fields': pk_fields,
            'dt_fields': dt_fields,
        }

    @cached_property
    def all_reports(
        self,
    ) -> Dict[str, DataFrame]:

        return {
            'schema_compare': self.data_source_pair.schema_comparison,
            'values_compare': self.values_comparison,
            'mismatches': self.mismatching_records,
            'matches': self.matching_records,
            'src_only': self.source_only_records,
            'tgt_only': self.target_only_records,
            'src_dup': self.source_duplicate_primary_key_records,
            'tgt_dup': self.target_duplicate_primary_key_records,
        }

    def to_parquet(
        self,
        dir_path: Path | str,
        file_name_prefix: str | None = None,
        file_name_suffix: str | None = None,
    ) -> None:
        """
        Writes all reports as *.parquet files to a specified directory.

        :param dir_path: Directory to save reports.
        :param file_name_prefix: File name prefix for *.parquet files.
        :param file_name_suffix: File name suffix for *.parquet files.
        :return:
        """

        if isinstance(dir_path, str):
            dir_path = Path(
                dir_path,
            )

        if file_name_prefix is None:
            file_name_prefix = ''

        if file_name_suffix is None:
            file_name_suffix = ''

        self.log_info(
            msg=f'Saving *.parquet file reports to location: "{str(dir_path.absolute())}" ...',
        )

        buffers = {report_name: BytesIO() for report_name in self.all_reports.keys()}

        for report_name, report_data in self.all_reports.items():
            report_data.to_parquet(
                path=buffers[report_name],
            )

        for report_name, buffer in buffers.items():
            file_path = (
                dir_path / f'{file_name_prefix}{report_name}{file_name_suffix}.parquet'
            )

            with open(file=file_path, mode='wb') as file:
                file.write(
                    buffer.getvalue(),
                )

        self.log_info(
            msg=f'Save complete: "{str(dir_path.absolute())}"',
        )

    def to_csv(
        self,
        dir_path: Path | str,
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

        if isinstance(dir_path, str):
            dir_path = Path(
                dir_path,
            )

        if file_name_prefix is None:
            file_name_prefix = ''

        if file_name_suffix is None:
            file_name_suffix = ''

        self.log_info(
            msg=f'Saving *.csv file reports to location: "{str(dir_path.absolute())}" ...',
        )

        buffers = {report_name: StringIO() for report_name in self.all_reports.keys()}

        for report_name, report_data in self.all_reports.items():
            report_data.to_csv(
                path_or_buf=buffers[report_name],
            )

        for report_name, buffer in buffers.items():
            file_path = (
                dir_path / f'{file_name_prefix}{report_name}{file_name_suffix}.csv'
            )

            with open(file=file_path, mode='w', newline='') as file:
                file.write(
                    buffer.getvalue(),
                )

        self.log_info(
            msg=f'Save complete: "{str(dir_path.absolute())}"',
        )

    def to_excel(
        self,
        path: Path | str,
    ) -> None:
        """
        Writes all reports as sheets in a specified Excel file.

        :param path: Path to the Excel file.
        :return:
        """

        if isinstance(path, str):
            path = Path(
                path,
            )

        self.log_info(
            msg=f'Saving Excel file report to location: "{str(path.absolute())}" ...',
        )

        excel_file_buffer = BytesIO()

        excel_writer = ExcelWriter(
            path=excel_file_buffer,
            engine='openpyxl',
        )

        for report_name, report_data in self.all_reports.items():
            report_data.to_excel(
                excel_writer=excel_writer,
                sheet_name=report_name,
            )

        excel_writer.close()

        with open(file=path, mode='wb') as excel_file:
            excel_file.write(
                excel_file_buffer.getvalue(),
            )

        self.log_info(
            msg=f'Save complete: "{str(path.absolute())}"',
        )
