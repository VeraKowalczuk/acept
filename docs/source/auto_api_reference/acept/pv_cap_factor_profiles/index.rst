:py:mod:`acept.pv_cap_factor_profiles`
======================================

.. py:module:: acept.pv_cap_factor_profiles

.. autoapi-nested-parse::

   Module for building PV capacity factor profiles.

   This module contains functions for building PV capacity factor profiles.
   The **capacity factor** is the unitless ratio of energy generated over a time period divided by the installed capacity.
   The installed capacity is defined as the theoretical maximum capacity of the PV system.

   The PV capacity factor profiles are build using weather data for the selected region. Each building has its own PV
   capacity factor profile as the PV capacity factor is specific to the location of the building.
   The profiles contain the series of PV capacity factor values for each hour of the year.

   For the computation of the PV capacity factor profiles, the library GSEE is used.
   GSEE (Global Solar Energy Estimator) is a solar energy simulation library designed for rapid calculations and ease of
   use. Renewables.ninja uses GSEE. Since the current official GSEE library is not maintained anymore, we recommend to
   use fork of the library from https://github.com/VeraKowalczuk/gsee.
   For more information about GSEE, see https://github.com/renewables-ninja/gsee or https://gsee.readthedocs.io/

   Use this module to:
       - Build PV capacity factor profiles for a single year for all given buildings
       - Build PV capacity factor profiles for the typical meteorological year for all given buildings
       - Build PV capacity factor profiles for a single year for all given buildings from the DWD TRY data
       - Build PV capacity factor profiles for multiple years for all given buildings from the DWD TRY data

   Use the :py:func:`build_pv_capacity_profile_for_year()` function to build a PV capacity factor profile for a single
   year. This function builds PV capacity factor profiles based on the available weather data (DWD TRY or TMY) for the
   selected region.



Module Contents
---------------


Functions
~~~~~~~~~

.. autoapisummary::

   acept.pv_cap_factor_profiles.build_pv_capacity_for_selected_years
   acept.pv_cap_factor_profiles.build_pv_capacity_for_selected_year_with_combined_data
   acept.pv_cap_factor_profiles.build_pv_capacity_for_selected_years_with_combined_data
   acept.pv_cap_factor_profiles.calculate_gsee_input_weather_from_raw_weather
   acept.pv_cap_factor_profiles.build_pv_capacity_profile_for_year
   acept.pv_cap_factor_profiles.calculate_pv_capacity_profile_based_on_tmy_weather
   acept.pv_cap_factor_profiles.get_tmy_as_input_weather_for_gsee_pv_cap



.. py:function:: build_pv_capacity_for_selected_years(selected_shape: geopandas.GeoDataFrame, buildings: geopandas.GeoDataFrame, year_start: int = DWD_MIN_YEAR, year_end: int = DWD_MAX_YEAR, building_specific_weather: bool = False, debug: bool = True) -> str

   Build PV capacity factor profiles for all years between year_start and year_end for all given buildings from the
   DWD TRY data. The weather data is expected as downloaded from the DWD OPENDATA portal. The profiles will be saved in
   a temporary directory in the:py:const:`acept.acept_constants.TEMP_PATH` directory as one CSV file per building per year.

   :param selected_shape: GeoDataFrame containing the shape of the area around the buildings.
   :param buildings: GeoDataFrame containing the buildings.
   :param year_start: Start year of the PV capacity factor profiles. Must be between DWD_MIN_YEAR and DWD_MAX_YEAR.
   :param year_end: End year of the PV capacity factor profiles. Must be between DWD_MIN_YEAR and DWD_MAX_YEAR.
   :param building_specific_weather: Whether to use building specific weather data. Defaults to False.
   :param debug: Whether to print debug messages. Defaults to True.
   :raises ValueOutsideRangeError: If year_start or year_end are outside the valid range (see DWD_MAX_RANGE)
   :return: Path to the directory containing the created CSV files.


.. py:function:: build_pv_capacity_for_selected_year_with_combined_data(selected_shape: geopandas.GeoDataFrame, buildings: geopandas.GeoDataFrame, year: int = 2011, uncompressed: bool = False, building_specific_weather: bool = False, debug: bool = True) -> str

   Build PV capacity factor profiles for a single year between for all given buildings from the
   DWD TRY data. The weather data is expected as combined files for the different features - use the
   `acept.dwd_try_data_handling.combine_dwd_try_data_and_save()` function to combine the data. The profiles will be
   saved in a temporary directory in the:py:const:`acept.acept_constants.TEMP_PATH` directory as one CSV file per building.

   :param selected_shape: GeoDataFrame containing the shape of the area around the buildings.
   :param buildings: GeoDataFrame containing the buildings.
   :param year: Year the PV capacity factor profiles are calculated for. Must be between DWD_MIN_YEAR and DWD_MAX_YEAR.
   :param uncompressed: Whether to use uncompressed DWD TRY data files. Defaults to False.
   :param building_specific_weather: Whether to use building specific weather data. Defaults to False.
   :param debug: Whether to print debug messages. Defaults to True.
   :return: Path to the directory containing the created CSV files.


.. py:function:: build_pv_capacity_for_selected_years_with_combined_data(selected_shape: geopandas.GeoDataFrame, buildings: geopandas.GeoDataFrame, year_start: int = DWD_MIN_YEAR, year_end: int = DWD_MAX_YEAR, uncompressed: bool = False, building_specific_weather: bool = False, debug: bool = True)

   Build PV capacity factor profiles for all years between year_start and year_end for all given buildings from the
   DWD TRY data. The weather data is expected as combined files for the different features - use the
   acept.dwd_try_data_handling.combine_dwd_try_data_and_save() function to combine the data. The profiles will be saved
   in a temporary directory in the:py:const:`acept.acept_constants.TEMP_PATH` directory as one CSV file per building per year.

   :param selected_shape: GeoDataFrame containing the shape of the area around the buildings.
   :param buildings: GeoDataFrame containing the buildings.
   :param year_start: First year the PV capacity factor profiles are calculated for. Must be between DWD_MIN_YEAR and
       DWD_MAX_YEAR.
   :param year_end: Last year the PV capacity factor profiles are calculated for. Must be between DWD_MIN_YEAR and
       DWD_MAX_YEAR.
   :param uncompressed: Whether to use uncompressed DWD TRY data files. Defaults to False.
   :param building_specific_weather: Whether to use building specific weather data. Defaults to False.
   :param debug: Whether to print debug messages. Defaults to True.
   :raises ValueOutsideRangeError: If year_start or year_end is outside the allowed range (see DWD_MAX_RANGE).
   :return: Path to the directory containing the created CSV files.


.. py:function:: calculate_gsee_input_weather_from_raw_weather(weather: xarray.Dataset | pandas.DataFrame, rad_diffuse_col: bool = False) -> xarray.Dataset | pandas.DataFrame

   Calculate the GSEE input weather from the raw weather, including the diffuse fraction.

   :param weather: The raw weather data as xarray.Dataset or pandas.DataFrame
   :param rad_diffuse_col: Whether the diffuse radiation column exists or has to be calculated.
   :return: The GSEE input weather


.. py:function:: build_pv_capacity_profile_for_year(selected_shape: geopandas.GeoDataFrame, buildings: geopandas.GeoDataFrame, year: int | None, debug: bool = True)

   Build PV capacity factor profiles for a single year for all given buildings from the DWD TRY data. The profiles are
   saved in a temporary directory in the:py:const:`acept.acept_constants.TEMP_PATH` directory as one CSV file per building.

   :param selected_shape: GeoDataFrame containing the shape of the area around the buildings.
   :param buildings: GeoDataFrame containing the buildings.
   :param year: Year the PV capacity factor profiles are calculated for. Must be between DWD_MIN_YEAR and DWD_MAX_YEAR.
       If None, the PV capacity factor profiles are calculated for the typical meteorological year (TMY).
   :param debug: Whether to print debug messages. Defaults to True.
   :return: Path to the directory containing the created CSV files.


.. py:function:: calculate_pv_capacity_profile_based_on_tmy_weather(selected_shape: geopandas.GeoDataFrame, buildings: geopandas.GeoDataFrame, building_specific_weather: bool = False, debug: bool = True)

   Build PV capacity factor profiles for a typical meteorological year (TMY) for all given buildings from the
   using the PVGIS weather API. The profiles will be saved in a temporary directory in the:py:const:`acept.acept_constants.TEMP_PATH` directory as
   one CSV file per building.

   :param selected_shape: GeoDataFrame containing the shape of the area around the buildings.
   :param buildings: GeoDataFrame containing the buildings.
   :param building_specific_weather: Whether to use building specific weather data. Defaults to False.
   :param debug: Whether to print debug messages. Defaults to True.


.. py:function:: get_tmy_as_input_weather_for_gsee_pv_cap(lat: float, lon: float) -> pandas.DataFrame

   Build weather profile for a typical meteorological year (TMY) from the PVGIS API using the maximal time period
   of 2005 - 2020 (see PVGIS_MIN_YEAR and PVGIS_MAX_YEAR).

   :param lat: latitude of the location as a float.
   :param lon: longitude of the location as a float.
   :return: A pandas DataFrame with the weather profile.


