from typing import (
    Final,
    List,
    Dict,
)
from functools import cached_property

from pandas import (
    DataFrame,
    concat,
    Series,
)

from ..base import (
    Base,
    log_exception,
    log_runtime,
)
from ..data_sources import DataSources
from ..compare_sets.compare_set.compare.field_pair import (
    FieldPairPrimaryKey,
    FieldPairData,
    FieldPair,
)


AUTO_MATCH: Final[str] = 'auto_match'


class FieldPairName:
    """
    Object that serves as a name mapping for a field pair.
    """

    source_field: str
    """
    Source field name.
    """

    target_field: str
    """
    Target field name.
    """

    def __init__(
        self,
        source_field: str,
        target_field: str,
    ):

        self.source_field = source_field
        self.target_field = target_field

    @property
    def diff_field(
        self,
    ) -> str:

        return f'dif.({self.source_field} | {self.target_field})'


class CompareEngine(
    Base,
):
    """
    Object that contains diffing logic.
    """

    data_sources: DataSources
    """
    Global data sources.
    """

    source: str
    """
    Pointer to source data source.
    """

    target: str
    """
    Pointer to target data source.
    """

    _pk_fields: List[FieldPairPrimaryKey] | AUTO_MATCH
    _dt_fields: List[FieldPairData] | AUTO_MATCH

    def __init__(
        self,
        data_sources: DataSources,
        source: str,
        target: str,
        pk_fields: List[FieldPairPrimaryKey] | AUTO_MATCH | None = None,
        dt_fields: List[FieldPairData] | AUTO_MATCH | None = None,
    ):

        Base.__init__(
            self=self,
        )

        self.data_sources = data_sources
        self.source = source
        self.target = target

        if pk_fields is not None:
            self._pk_fields = pk_fields

        else:
            self._pk_fields = []

        if dt_fields is not None:
            self._dt_fields = dt_fields

        else:
            self._dt_fields = []

    def __str__(
        self,
    ) -> str:

        return f'Compare Engine: {id(self)}'

    @cached_property
    def field_pair_names(
        self,
    ) -> Dict[FieldPair, FieldPairName]:

        source_field_counts = {}
        target_field_counts = {}
        field_pair_names = {}

        for field_pair in self.fields:
            # Calculate and store field counts
            source_field = str(field_pair.source_field)

            if source_field not in source_field_counts:
                source_field_counts[source_field] = 0

            source_field_count = source_field_counts[source_field]
            source_field_count += 1
            source_field_counts[source_field] = source_field_count

            target_field = str(field_pair.target_field)

            if target_field not in target_field_counts:
                target_field_counts[target_field] = 0

            target_field_count = target_field_counts[target_field]
            target_field_count += 1
            target_field_counts[target_field] += target_field_count

            # Create and store names
            source_field_name = field_pair.source_field_name_short

            if source_field_count > 1:
                source_field_name += f'({source_field_count})'

            target_field_name = field_pair.target_field_name_short

            if target_field_count > 1:
                target_field_name += f'({target_field_count})'

            field_pair_names[field_pair] = FieldPairName(
                source_field=source_field_name,
                target_field=target_field_name,
            )

        return field_pair_names

    def get_auto_match_fields(
        self,
        exclude: List[FieldPair] | None = None,
    ) -> List[FieldPair]:
        """
        Get a matching list of field pairs between the source and target data sources,
        using column names to match.

        :param exclude: List of ``FieldPair``'s to exclude from the matching list.
        :return: List of matching ``FieldPair``'s, less any ``FieldPair``'s explicitly excluded.
        """

        source_columns = [
            columns for columns in self.data_sources[self.source].py_types.keys()
        ]
        target_columns = [
            columns for columns in self.data_sources[self.target].py_types.keys()
        ]

        matching_columns = [
            column for column in source_columns if column in target_columns
        ]

        field_pairs = [
            FieldPair(
                source_field=field,
                target_field=field,
            )
            for field in matching_columns
        ]

        if exclude is not None:
            field_pairs = [
                field_pair for field_pair in field_pairs if field_pair not in exclude
            ]

        return field_pairs

    @cached_property
    def pk_fields(
        self,
    ) -> List[FieldPairPrimaryKey]:
        """
        Primary key field pairs, using these rules:

        #. If primary key fields are provided, those will be used.
        #. If primary key fields are set to ``AUTO_MATCH``, those will be matched, less any provided data fields.

        :return:
        """

        if self._pk_fields == AUTO_MATCH:
            if self._dt_fields == AUTO_MATCH:
                dt_fields = []

            else:
                dt_fields = self._dt_fields

            auto_match_fields = self.get_auto_match_fields(
                exclude=dt_fields,
            )

            pk_fields = [
                FieldPairPrimaryKey(
                    source_field=field.source_field,
                    target_field=field.target_field,
                )
                for field in auto_match_fields
            ]

        else:
            pk_fields = self._pk_fields

        return pk_fields

    @cached_property
    def dt_fields(
        self,
    ) -> List[FieldPairData]:
        """
        Data field pairs, using these rules:

        #. If data fields are provided, those will be used.
        #. If data fields are set to ``AUTO_MATCH``, those will be matched, less any computed primary keys.

        :return:
        """

        if self._dt_fields == AUTO_MATCH:
            auto_match_fields = self.get_auto_match_fields(
                exclude=self.pk_fields,
            )

            dt_fields = [
                FieldPairData(
                    source_field=field.source_field,
                    target_field=field.target_field,
                )
                for field in auto_match_fields
            ]

        else:
            dt_fields = self._dt_fields

        return dt_fields

    @cached_property
    def fields(
        self,
    ) -> List[FieldPair]:
        """
        All fields, including both primary key and data fields.

        :return:
        """

        return self.pk_fields + self.dt_fields

    @log_exception
    @log_runtime
    def init_field_transforms(
        self,
    ) -> None:
        """
        Calculates field transformations in parallel, if they do not already exist.

        :return:
        """

        # TODO: Final data type conversion for compare rule should be performed outside the scope of this

        source_data_source = self.data_sources[self.source]
        target_data_source = self.data_sources[self.target]

        futures = []

        for field_pair in self.fields:
            source_field = source_data_source[str(field_pair.source_field)]

            source_field.append(
                field_pair.source_transforms,
            )

            source_field_transformed = source_field.field_transforms[
                field_pair.source_transforms
            ]

            if source_field_transformed is None:
                futures.append(
                    self.pool.apply_async(
                        func=source_field.init_field_transforms,
                        kwds={
                            'field_transforms': field_pair.source_transforms,
                        },
                    ),
                )

            target_field = target_data_source[str(field_pair.target_field)]

            target_field.append(
                field_pair.target_transforms,
            )

            target_field_transformed = target_field.field_transforms[
                field_pair.target_transforms
            ]

            if target_field_transformed is None:
                futures.append(
                    self.pool.apply_async(
                        func=target_field.init_field_transforms,
                        kwds={
                            'field_transforms': field_pair.target_transforms,
                        },
                    ),
                )

        for future in futures:
            future.get()

    @cached_property
    def source_dataframe(
        self,
    ) -> DataFrame:
        """
        DataFrame containing transformed source fields.
        """

        self.init_field_transforms()

        dataframe = concat(
            objs=[
                self.data_sources[self.source][str(field_pair.source_field)][
                    field_pair.source_transforms
                ]
                for field_pair in self.fields
            ],
            axis=1,
        )

        columns = {
            str(field_pair.source_field): str(field_pair)
            for field_pair in self.pk_fields
        } | {
            str(field_pair.source_field): self.field_pair_names[field_pair].source_field
            for field_pair in self.dt_fields
        }

        dataframe.rename(
            columns=columns,
            inplace=True,
        )

        if self.pk_fields:
            dataframe.set_index(
                keys=[str(field_pair) for field_pair in self.pk_fields],
                inplace=True,
            )

        return dataframe

    @cached_property
    def source_dataframe_deduplicated(
        self,
    ) -> DataFrame:

        deduplicated_dataframe = self.source_dataframe[
            ~self.source_dataframe.index.duplicated(
                keep=False,
            )
        ]

        return deduplicated_dataframe

    @cached_property
    def target_dataframe(
        self,
    ) -> DataFrame:
        """
        DataFrame containing transformed target fields.
        """

        self.init_field_transforms()

        dataframe = concat(
            objs=[
                self.data_sources[self.target][str(field_pair.target_field)][
                    field_pair.target_transforms
                ]
                for field_pair in self.fields
            ],
            axis=1,
        )

        columns = {
            str(field_pair.target_field): str(field_pair)
            for field_pair in self.pk_fields
        } | {
            str(field_pair.target_field): self.field_pair_names[field_pair].target_field
            for field_pair in self.dt_fields
        }

        dataframe.rename(
            columns=columns,
            inplace=True,
        )

        if self.pk_fields:
            dataframe.set_index(
                keys=[str(field_pair) for field_pair in self.pk_fields],
                inplace=True,
            )

        return dataframe

    @cached_property
    def target_dataframe_deduplicated(
        self,
    ) -> DataFrame:

        deduplicated_dataframe = self.target_dataframe[
            ~self.target_dataframe.index.duplicated(
                keep=False,
            )
        ]

        return deduplicated_dataframe

    @log_exception
    def _validate_fields(
        self,
    ) -> None:

        if not self.pk_fields:
            raise ValueError(
                'No primary keys provided or computed for comparison!',
            )

    @cached_property
    def values_comparison_unmasked(
        self,
    ) -> DataFrame:

        joint_dataframe = self.source_dataframe_deduplicated.merge(
            right=self.target_dataframe_deduplicated,
            how='inner',
            left_index=True,
            right_index=True,
        )

        results = {}
        column_order = []

        for field_pair in self.dt_fields:

            field_pair_name = self.field_pair_names[field_pair]

            results[field_pair_name.diff_field] = self.pool.apply_async(
                func=field_pair.compare_rule.compare,
                kwds={
                    'source_field': joint_dataframe[field_pair.source_field_name],
                    'target_field': joint_dataframe[field_pair.target_field_name],
                },
            )

            column_order.extend(
                [
                    field_pair_name.source_field,
                    field_pair_name.target_field,
                    field_pair_name.diff_field,
                ],
            )

        for diff_field_name, future in results.items():
            joint_dataframe[diff_field_name] = future.get()

        joint_dataframe = joint_dataframe[column_order]

        return joint_dataframe

    @cached_property
    def values_comparison(
        self,
    ) -> DataFrame:

        values_comparison = self.values_comparison_unmasked.copy(
            deep=True,
        )

        for field_pair in self.dt_fields:
            field_pair_name = self.field_pair_names[field_pair]

            values_comparison[field_pair_name.diff_field].replace(
                to_replace={
                    True: '',
                    False: '*',
                },
                inplace=True,
            )

        return values_comparison

    @cached_property
    def matching_records(
        self,
    ) -> DataFrame:

        matching_records = self.values_comparison_unmasked.copy(
            deep=True,
        )

        keep_rows = Series(
            data=True,
            index=matching_records.index,
        )

        for field_pair in self.dt_fields:
            field_pair_name = self.field_pair_names[field_pair]

            diff_values = matching_records[field_pair_name.diff_field]
            keep_rows = keep_rows & diff_values

        matching_records = matching_records[keep_rows]

        for field_pair in self.dt_fields:
            field_pair_name = self.field_pair_names[field_pair]

            matching_records[field_pair_name.diff_field].replace(
                to_replace={
                    True: '',
                    False: '*',
                },
                inplace=True,
            )

        return matching_records

    @cached_property
    def mismatching_records(
        self,
    ) -> DataFrame:

        mismatching_records = self.values_comparison_unmasked.copy(
            deep=True,
        )

        keep_rows = Series(
            data=False,
            index=mismatching_records.index,
        )

        for field_pair in self.dt_fields:
            field_pair_name = self.field_pair_names[field_pair]

            diff_values = mismatching_records[field_pair_name.diff_field]
            keep_rows = keep_rows | ~diff_values

        mismatching_records = mismatching_records[keep_rows]

        for field_pair in self.dt_fields:
            field_pair_name = self.field_pair_names[field_pair]

            mismatching_records[field_pair_name.diff_field].replace(
                to_replace={
                    True: '',
                    False: '*',
                },
                inplace=True,
            )

        return mismatching_records

    @cached_property
    def source_only_records(
        self,
    ) -> DataFrame:

        self._validate_fields()

        inner_index = self.source_dataframe_deduplicated.index.join(
            other=self.target_dataframe_deduplicated.index,
            how='inner',
        )

        source_only_records = self.source_dataframe_deduplicated.loc[
            ~self.source_dataframe_deduplicated.index.isin(
                values=inner_index.values,
            )
        ]

        source_only_records.index.rename(
            names=[
                self.field_pair_names[field_pair].source_field
                for field_pair in self.pk_fields
            ],
            inplace=True,
        )

        return source_only_records

    @cached_property
    def target_only_records(
        self,
    ) -> DataFrame:

        self._validate_fields()

        inner_index = self.source_dataframe_deduplicated.index.join(
            other=self.target_dataframe_deduplicated.index,
            how='inner',
        )

        target_only_records = self.target_dataframe_deduplicated.loc[
            ~self.target_dataframe_deduplicated.index.isin(
                values=inner_index.values,
            )
        ]

        target_only_records.index.rename(
            names=[
                self.field_pair_names[field_pair].target_field
                for field_pair in self.pk_fields
            ],
            inplace=True,
        )

        return target_only_records

    @cached_property
    def source_duplicate_primary_key_records(
        self,
    ) -> DataFrame:

        self._validate_fields()

        duplicated_dataframe = self.source_dataframe[
            self.source_dataframe.index.duplicated(
                keep=False,
            )
        ]

        duplicated_dataframe.index.rename(
            names=[
                self.field_pair_names[field_pair].source_field
                for field_pair in self.pk_fields
            ],
            inplace=True,
        )

        return duplicated_dataframe

    @cached_property
    def target_duplicate_primary_key_records(
        self,
    ) -> DataFrame:

        self._validate_fields()

        duplicated_dataframe = self.target_dataframe[
            self.target_dataframe.index.duplicated(
                keep=False,
            )
        ]

        duplicated_dataframe.index.rename(
            names=[
                self.field_pair_names[field_pair].target_field
                for field_pair in self.pk_fields
            ],
            inplace=True,
        )

        return duplicated_dataframe
