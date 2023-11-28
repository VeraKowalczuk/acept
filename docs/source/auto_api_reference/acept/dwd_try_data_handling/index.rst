:py:mod:`acept.dwd_try_data_handling`
=====================================

.. py:module:: acept.dwd_try_data_handling

.. autoapi-nested-parse::

   Module for handling DWD TRY data.

   Use this module to:
       - read DWD TRY data as a Xarray Dataset
       - preprocess DWD TRY data
       - combine multiple DWD TRY datasets (temperature, direct radiation, and global radiation) into a single Xarray Dataset for use in acept
       - uncompress DWD TRY data to make file reading faster
       - check if DWD TRY data is available in the correct subdirectory of :py:const:`acept.acept_constants.DWD_TRY_PATH`

   :raises ValueOutsideRangeError: if years are outside the allowed range (see :py:const:`acept.dwd_try_data_handling.DWD_MAX_RANGE`)
   :raises ValueError: if an unknown DWD feature is requested

   .. note:: To set up the DWD TRY data, use the module :py:mod:`acept.dwd_try_data_setup`



Module Contents
---------------


Functions
~~~~~~~~~

.. autoapisummary::

   acept.dwd_try_data_handling.read_dwd_netcdf_file
   acept.dwd_try_data_handling.preprocess_dwd_try_dataset
   acept.dwd_try_data_handling.preprocess_combined_dwd_try_dataset
   acept.dwd_try_data_handling.combine_dwd_try_data_and_save
   acept.dwd_try_data_handling.combine_dwd_try_data_and_save_single_year
   acept.dwd_try_data_handling.check_for_un_compressed_dwd_try_data
   acept.dwd_try_data_handling.check_for_dwd_try_data_year
   acept.dwd_try_data_handling.path_to_dwd_file



Attributes
~~~~~~~~~~

.. autoapisummary::

   acept.dwd_try_data_handling.DWD_MIN_YEAR
   acept.dwd_try_data_handling.DWD_MAX_YEAR
   acept.dwd_try_data_handling.DWD_MAX_RANGE


.. py:data:: DWD_MIN_YEAR
   :value: 1995

   Minimum year of DWD TRY data available to download.

.. py:data:: DWD_MAX_YEAR
   :value: 2012

   Maximum year of DWD TRY data.

.. py:data:: DWD_MAX_RANGE

   1995-2012.

   :type: Maximum range of years of DWD TRY data available to download as a python range object

.. py:function:: read_dwd_netcdf_file(dwd_feature: str, year, month, debug: bool = True) -> xarray.Dataset

   Read a DWD netCDF file and return the data as a Xarray Dataset.

   :param dwd_feature: The DWD feature to read. Valid options are "temperature", "rad_direct", and "rad_global"
       or "combined_try" for all three features in the same file.
   :param year: The year of the data.
   :param month: The month of the data.
   :param debug: (optional) Whether to print debug information. Defaults to True.
   :return: The data read from the netCDF file.


.. py:function:: preprocess_dwd_try_dataset(wd_data: xarray.Dataset, dwd_feature: str, debug: bool = True) -> xarray.Dataset

   Preprocess the DWD TRY dataset to make it ready for use.

   Use this function to preprocess the DWD TRY dataset for use in ACEPT.
   This is the same as ``preprocess_combined_dwd_try_dataset`` but for the individual DWD TRY datasets.
   This step is necessary to use to read the individual DWD TRY datasets.

   :param wd_data: The Xarray Dataset to preprocess.
   :param dwd_feature: The DWD feature to read. Valid options are "temperature", "rad_direct", and "rad_global"
       or "combined_try" for all three features in the same file.
   :param debug: (optional) Whether to print debug information. Defaults to True.
   :return: The preprocessed Xarray Dataset.


.. py:function:: preprocess_combined_dwd_try_dataset(wd_data: xarray.Dataset, debug: bool = True) -> xarray.Dataset

   Preprocess the combined DWD TRY dataset to make it ready for use.

   Use this function to preprocess the combined DWD TRY dataset for use in ACEPT.
   This is the same as ``preprocess_dwd_try_dataset`` but for the combined DWD TRY dataset.
   This step is necessary to use to read the combined DWD TRY dataset.

   :param wd_data: The Xarray Dataset to preprocess.
   :param debug: Whether to print debug information. Defaults to True.
   :return: The preprocessed Xarray Dataset.


.. py:function:: combine_dwd_try_data_and_save(year_start: int = DWD_MIN_YEAR, year_end: int = DWD_MAX_YEAR, debug: bool = True, uncompressed_years: None | list[int] = None)

   Combine the DWD TRY data files (of 'temperature', 'rad_direct', 'rad_global') for **Bavaria** and save them as netCDF
   files.

   Included features: temperature, direct and global radiation. Combine the data for these features for Bavaria
   for the given years and the monthly files. This makes using the TRY data easier and more efficient.
   Store the data in uncompressed netCDF files to speed up reading the data.

   :param year_start: start year of the data set to be combined
   :param year_end: end year of the data set to be combined
   :raises ValueOutsideRangeError: if year_start or year_end is outside the allowed range
       (see :py:const:`acept.dwd_try_data_handling.DWD_MAX_RANGE`)
   :param debug: if True, print debug information
   :param uncompressed_years: optional list of years to be combined and saved without compression


.. py:function:: combine_dwd_try_data_and_save_single_year(bavaria_shape: geopandas.GeoDataFrame, year_spec: int, debug: bool = True, uncompressed_years: None | list[int] = None)

   Combine the DWD TRY data files (of 'temperature', 'rad_direct', 'rad_global') for Bavaria and save them as netCDF
   files. Included features: temperature, direct and global radiation. Combine the data for these features for Bavaria
   for the given year and the monthly files.

   :param bavaria_shape: shape of Bavaria
   :param year_spec: year of the data set to be combined
   :raises ValueOutsideRangeError: if year_spec is outside the allowed range
       (see :py:const:`acept.dwd_try_data_handling.DWD_MAX_RANGE`)
   :param debug: if True, print debug information
   :param uncompressed_years: optional list of years to be combined and saved without compression. Defaults to None.


.. py:function:: check_for_un_compressed_dwd_try_data(compressed=True, year_start: int = DWD_MIN_YEAR, year_end: int = DWD_MAX_YEAR) -> bool

   Whether the combined DWD TRY data is downloaded in the correct directory for the given years. If not, return False.
   If yes, return True.

   :param compressed: whether the combined DWD TRY data is available in the correct directory
   :param year_start: start year of the data set to be checked
   :param year_end: end year of the data set to be checked
   :raises ValueOutsideRangeError: if year_start or year_end is outside the allowed range
       (see :py:const:`acept.dwd_try_data_handling.DWD_MAX_RANGE`)
   :return: whether the combined DWD TRY data is there


.. py:function:: check_for_dwd_try_data_year(year: int, types_to_check: list[str] = ['temperature', 'rad_direct', 'rad_global']) -> bool

   Whether DWD TRY data was downloaded in the correct directory for the given year. If not, return False.
   If yes, return True.

   :param year: year of the data set to be checked
   :param types_to_check: list of types of data to be checked, allowed values are 'temperature', 'rad_direct',
       'rad_global', 'combined_try', 'combined_try_uncompressed'
   :raises ValueOutsideRangeError: if year is outside the allowed range
       (see :py:const:`acept.dwd_try_data_handling.DWD_MAX_RANGE`)
   :return: whether the specified DWD TRY data is there


.. py:function:: path_to_dwd_file(feature: str, year: int, month: int) -> str

   Path to the DWD TRY data file for the given feature, year, and month.

   :param feature: The DWD feature to read. Valid options are "temperature", "rad_direct", "rad_global",
       "combined_try", or "combined_try_uncompressed".
   :param year: The year of the data.
   :param month: The month of the data.
   :raises ValueError: If the feature is not valid.
   :return: The path to the DWD file.


