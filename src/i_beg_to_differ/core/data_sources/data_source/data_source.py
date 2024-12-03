from abc import (
    ABC,
    abstractmethod,
)
from multiprocessing.managers import Namespace
from multiprocessing import Lock
from typing import (
    Dict,
    Tuple,
    List,
)

from pandas import (
    DataFrame,
    Series,
)

from ...ib2d_file.ib2d_file_element import IB2DFileElement
from ...extensions.extension import Extension
from ...extensions.ui import DescriptionInputField
from .field.field_transforms import FieldTransforms
from ...compare_sets.compare_set.compare.field_reference_pair.field_reference import (
    FieldReference,
)
from ...utils.dataframe import dict_to_dataframe


class DataSource(
    IB2DFileElement,
    Extension,
    ABC,
):
    """
    Abstract data source that functions as cached data storage. Primarily responsible for:
        #. Loading data into a DataFrame.
        #. Managing Fields, which serve as an abstraction layer over the data.

    This class must be pickleable.
    """

    description: DescriptionInputField
    """
    Human-readable description of this data source.
    """

    _cache_namespace: Namespace
    """
    Cache namespace; stores DataFrame for multiprocessing, under the cache attribute.
    """

    _cache_lock: Lock
    """
    Cache lock; synchronizes multiple processes during cache access. 
    """

    _field_transform_cache: Dict[Tuple[str, FieldTransforms], Series]
    """
    Cached computed values for transformed fields.
    """

    def __init__(
        self,
        description: str | None = None,
    ):

        IB2DFileElement.__init__(
            self=self,
        )

        self.description = DescriptionInputField(
            value=description,
        )

        self._cache_namespace = self.manager.Namespace()
        self._cache_namespace.cache = None
        self._cache_lock = self.manager.Lock()

        self._field_transform_cache = self.manager.dict()

    def __getitem__(
        self,
        field_reference: FieldReference,
    ) -> Series:
        # Lookup field name
        field_name = str(
            field_reference.field_name,
        )

        if field_name not in self._field_transform_cache:
            # Create new field entry in cache
            self._field_transform_cache[(field_name, FieldTransforms())] = self.cache[
                field_name
            ]

        # Lookup field transforms
        field_transforms = field_reference.transforms

        field_transform_cache_key = (
            field_name,
            field_transforms,
        )

        if field_transform_cache_key not in self._field_transform_cache:
            # Compute and save field transform
            self._field_transform_cache[field_transform_cache_key] = (
                field_transforms.apply(
                    values=self.cache[field_name],
                )
            )

        # Retrieve saved field transform
        transformed_values = self._field_transform_cache[field_transform_cache_key]

        return transformed_values

    @property
    def cache(
        self,
    ) -> DataFrame:
        """
        Cached copy of the data source, for quicker local processing.
        """

        self._cache_lock.acquire()

        if self._cache_namespace.cache is None:
            self._cache_namespace.cache = self.load()

        self._cache_lock.release()

        return self._cache_namespace.cache

    def clear(
        self,
    ) -> None:
        """
        Clears the cache.

        :return:
        """

        self._cache_namespace._cache = None

    @abstractmethod
    def load(
        self,
    ) -> DataFrame:
        """
        Reads data from a data source.

        :return: A DataFrame of loaded data.
        """

    @property
    @abstractmethod
    def native_types(
        self,
    ) -> Dict[str, str]:
        """
        Dictionary of native types. Keys are column names.

        :return: Dictionary of native types.
        """

    @property
    def py_types(
        self,
    ) -> Dict[str, str]:
        """
        Dictionary of python types. Keys are column names.

        :return: Dictionary of python types.
        """

        return {
            str(column): dtype.type.__name__
            for column, dtype in self.cache.dtypes.items()
        }

    @property
    def columns(
        self,
    ) -> List[str]:
        """
        List of columns.
        """

        return list(
            self.py_types.keys(),
        )

    @property
    def data_types(
        self,
    ) -> DataFrame:
        """
        DataFrame that contains data types.

        - ``column_name``: Name of the column.
        - ``native_type``: Data type recognized by the data source's underlying system.
        - ``py_type``: Data type recognized by Python.
        """

        native_types = dict_to_dataframe(
            data=self.native_types,
            index='column_name',
            column='native_type',
        )

        data_types = dict_to_dataframe(
            data=self.py_types,
            index='column_name',
            column='py_type',
        )

        data_types = native_types.join(
            other=data_types,
            how='inner',
        )

        data_types.reset_index(
            inplace=True,
        )

        return data_types

    def calculate_field(
        self,
        field_reference: FieldReference,
    ) -> Series:
        return self[field_reference]
