from typing import (
    List,
    Dict,
    Self,
)
from pathlib import Path
from zipfile import ZipFile
from io import (
    BytesIO,
    StringIO,
)

from pandas import (
    DataFrame,
    ExcelWriter,
)

from ....ib2d_file.ib2d_file_element import IB2DFileElement

from .compare_base import CompareBase
from .compare_values import CompareValues
from .compare_matching_records import CompareMatchingRecords
from .compare_mismatching_records import CompareMismatchingRecords
from .compare_source_only_records import CompareSourceOnlyRecords
from .compare_target_only_records import CompareTargetOnlyRecords
from .compare_source_duplicate_primary_key_records import (
    CompareSourceDuplicatePrimaryKeyRecords,
)
from .compare_target_duplicate_primary_key_records import (
    CompareTargetDuplicatePrimaryKeyRecords,
)
from .compare_schema import CompareSchema

from ....input_fields import TextBoxInputField
from ....data_sources import DataSources
from .data_source_reference import DataSourceReference
from .field_reference_pair import (
    FieldReferencePairPrimaryKey,
    FieldReferencePairData,
)
from .compare_base import AUTO_MATCH
from ....wildcards_sets import WildcardSets


class Compare(
    IB2DFileElement,
    CompareValues,
    CompareMatchingRecords,
    CompareMismatchingRecords,
    CompareSourceOnlyRecords,
    CompareTargetOnlyRecords,
    CompareSourceDuplicatePrimaryKeyRecords,
    CompareTargetDuplicatePrimaryKeyRecords,
    CompareSchema,
):

    description: TextBoxInputField
    """
    Human-readable description.
    """

    _data_sources: DataSources

    def __init__(
        self,
        source_data_source_ref: DataSourceReference,
        target_data_source_ref: DataSourceReference,
        data_sources: DataSources,
        pk_fields: List[FieldReferencePairPrimaryKey] | None = None,
        dt_fields: List[FieldReferencePairData] | AUTO_MATCH | None = None,
        wildcard_sets: WildcardSets | None = None,
        description: str | None = None,
    ):

        IB2DFileElement.__init__(
            self=self,
        )

        CompareBase.__init__(
            self=self,
            source_data_source_ref=source_data_source_ref,
            target_data_source_ref=target_data_source_ref,
            data_sources=data_sources,
            pk_fields=pk_fields,
            dt_fields=dt_fields,
            wildcard_sets=wildcard_sets,
        )

        self.description = TextBoxInputField(
            title='Description',
            value=description,
        )

    @classmethod
    def deserialize(
        cls,
        instance_data: Dict,
        working_dir_path: Path,
        ib2d_file: ZipFile,
        data_sources: DataSources = None,
        wildcard_sets: WildcardSets | None = None,
    ) -> Self:

        source_data_source_ref = DataSourceReference(
            data_source_name=instance_data['source'],
        )

        target_data_source_ref = DataSourceReference(
            data_source_name=instance_data['target'],
        )

        pk_fields = [
            FieldReferencePairPrimaryKey.deserialize(
                instance_data=pk_field_data,
                working_dir_path=working_dir_path,
                ib2d_file=ib2d_file,
                wildcard_sets=wildcard_sets,
            )
            for pk_field_data in instance_data['pk_fields']
        ]

        dt_fields = instance_data['dt_fields']

        if isinstance(dt_fields, list):
            dt_fields = [
                FieldReferencePairData.deserialize(
                    instance_data=dt_field_data,
                    working_dir_path=working_dir_path,
                    ib2d_file=ib2d_file,
                    wildcard_sets=wildcard_sets,
                )
                for dt_field_data in instance_data['dt_fields']
            ]

        return Compare(
            source_data_source_ref=source_data_source_ref,
            target_data_source_ref=target_data_source_ref,
            data_sources=data_sources,
            pk_fields=pk_fields,
            dt_fields=dt_fields,
            wildcard_sets=wildcard_sets,
            description=instance_data['description'],
        )

    def serialize(
        self,
        ib2d_file: ZipFile,
    ) -> Dict:

        pk_fields = [
            instance.serialize(
                ib2d_file=ib2d_file,
            )
            for instance in self.pk_fields
        ]

        if isinstance(self._dt_fields, list):
            dt_fields = [
                instance.serialize(
                    ib2d_file=ib2d_file,
                )
                for instance in self._dt_fields
            ]

        else:
            dt_fields = self._dt_fields

        return {
            'description': self.description.value,
            'source': self.source_data_source_ref.data_source_name.base_value,
            'target': self.target_data_source_ref.data_source_name.base_value,
            'pk_fields': pk_fields,
            'dt_fields': dt_fields,
        }

    @property
    def all_reports(
        self,
    ) -> Dict[str, DataFrame]:

        return {
            'schema_compare': self.schema_compare,
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

        all_reports = self.all_reports

        buffers = {report_name: BytesIO() for report_name in all_reports.keys()}

        for report_name, report_data in all_reports.items():
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

        all_reports = self.all_reports

        buffers = {report_name: StringIO() for report_name in all_reports.keys()}

        for report_name, report_data in all_reports.items():
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

        all_reports = self.all_reports

        for report_name, report_data in all_reports.items():
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
