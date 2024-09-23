from typing import (
    List,
    Dict,
    Literal,
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
from ..compare_sets.compare_set.compare.field_pair.field_pair_primary_key import (
    FieldPairPrimaryKey,
)
from ..compare_sets.compare_set.compare.field_pair.field_pair_data import (
    FieldPairData,
)
from ..compare_sets.compare_set.compare.field_pair import FieldPair


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

    pk_fields: List[FieldPairPrimaryKey]
    """
    Primary key field pairs.
    """

    dt_fields: List[FieldPairData]
    """
    Data field pairs.
    """

    def __init__(
        self,
        data_sources: DataSources,
        source: str,
        target: str,
        pk_fields: List[FieldPairPrimaryKey] | None = None,
        dt_fields: List[FieldPairData] | None = None,
    ):

        Base.__init__(
            self=self,
        )

        self.data_sources = data_sources
        self.source = source
        self.target = target

        self.pk_fields = pk_fields
        self.dt_fields = dt_fields

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

    def get_joint_dataframe(
        self,
        how: Literal["left", "right", "inner", "outer", "cross"] = 'inner',
    ) -> DataFrame:
        """
        Creates a Dataframe containing both source and target data

        :return: Dataframe containing both source and target data.
        """

        joint_dataframe = self.source_dataframe.join(
            other=self.target_dataframe,
            how=how,
        )

        joint_dataframe = joint_dataframe[
            ~joint_dataframe.index.duplicated(
                keep=False,
            )
        ]

        column_order = []

        for field_pair in self.dt_fields:
            field_pair_name = self.field_pair_names[field_pair]

            column_order.extend(
                [
                    field_pair_name.source_field,
                    field_pair_name.target_field,
                ],
            )

        joint_dataframe = joint_dataframe[column_order]

        return joint_dataframe

    @cached_property
    def values_comparison(
        self,
    ) -> DataFrame:

        def apply_mask(
            diff_values: Series,
        ) -> None:

            diff_values.replace(
                to_replace=True,
                value='',
                inplace=True,
            )

            diff_values.replace(
                to_replace=False,
                value='*',
                inplace=True,
            )

        joint_dataframe = self.get_joint_dataframe(
            how='inner',
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
                callback=apply_mask,
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
    def source_only_records(
        self,
    ) -> DataFrame:

        pass

    @cached_property
    def target_only_records(
        self,
    ) -> DataFrame:

        pass

    @cached_property
    def source_duplicate_primary_key_records(
        self,
    ) -> DataFrame:

        pass

    @cached_property
    def target_duplicate_primary_key_records(
        self,
    ) -> DataFrame:

        pass
