:py:mod:`acept.temperature_profiles`
====================================

.. py:module:: acept.temperature_profiles

.. autoapi-nested-parse::

   Module for building ambient temperature profiles

   The temperature profiles are created using the DWD TRY data or the PVGIS TMY weather data.
   Each temperature profile contains the hourly temperature values in degrees Celsius for the whole year.
   Typically, these are measurements of the air temperature of two meters above the ground.

   The temperature profiles are saved in a temporary directory in the :py:const:`acept.acept_constants.TEMP_PATH` directory
   as a CSV file.
   Since the temperature profiles are used in ACEPT to calculate demand profiles with UrbanHeatPro (UHP), the profiles
   are saved in the expected input format for UHP.

   Use this module to:
       - Create a temperature profile for the selected area
       - Create a temperature profile for the selected area for a single year
       - Create a temperature profile for the TMY for the center of the selected area
       - Create a temperature profile for the selected area for multiple years

   Use the :py:func:`acept.temperature_profiles.build_temperature_profile_for_year` function to build a temperature profile for a single
   year. This function builds temperature profiles based on the available weather data (DWD TRY or TMY) for the
   selected area.



Module Contents
---------------


Functions
~~~~~~~~~

.. autoapisummary::

   acept.temperature_profiles.build_temperature_profiles_for_selected_years
   acept.temperature_profiles.build_temperature_profiles_for_selected_years_with_combined_data
   acept.temperature_profiles.build_temperature_profile_for_selected_year_with_combined_data
   acept.temperature_profiles.build_temperature_profile_for_year
   acept.temperature_profiles.build_temperature_profile_for_tmy_for_shape



.. py:function:: build_temperature_profiles_for_selected_years(plz_or_region: int | str, selected_shape: geopandas.GeoDataFrame, year_start: int = DWD_MIN_YEAR, year_end: int = DWD_MAX_YEAR, debug: bool = True) -> str

   Creates a temperature profile for the selected year and the selected PLZ or Region using DWD TRY temperature data.

   :param plz_or_region: PLZ or Region for which the temperature profile should be created (area ID).
   :param selected_shape: GeoDataFrame of the selected area.
   :param year_start: First year for which the temperature profile should be created. Defaults to 1995.
   :param year_end: Last year for which the temperature profile should be created. Defaults to 2012.
   :param debug: If True, print debug information.
   :raises ValueOutsideRangeError: if year_start or year_end is outside the allowed range (1995-2012).
   :return: Path to the directory where the created CSV files are stored.


.. py:function:: build_temperature_profiles_for_selected_years_with_combined_data(plz_or_region: str | int, selected_shape: geopandas.GeoDataFrame, year_start: int = DWD_MIN_YEAR, year_end: int = DWD_MAX_YEAR, uncompressed: bool = False, debug: bool = True) -> str

   Creates a temperature profile for the selected year and the selected PLZ or Region using the combined DWD TRY data.

   :param plz_or_region: PLZ or Region for which the temperature profile should be created (area ID).
   :param selected_shape: GeoDataFrame of the selected area.
   :param year_start: First year for which the temperature profile should be created. Defaults to 1995.
   :param year_end: Last year for which the temperature profile should be created. Defaults to 2012.
   :param uncompressed: If True, use the uncompressed DWD TRY data.
   :param debug: If True, print debug information.
   :raises ValueOutsideRangeError: If year_start or year_end is outside the allowed range (1995-2012).
   :return: Path to the directory where the created CSV files are stored.


.. py:function:: build_temperature_profile_for_selected_year_with_combined_data(plz_or_region: str | int, selected_shape: geopandas.GeoDataFrame, year: int = 2011, uncompressed: bool = False, debug: bool = True) -> str

   Creates a temperature profile for the selected year and the selected PLZ or Region using the combined DWD TRY data.

   :param plz_or_region: PLZ or Region for which the temperature profile should be created (area ID).
   :param selected_shape: GeoDataFrame of the selected area.
   :param year: Year for which the temperature profile should be created.
   :param uncompressed: If True, use the uncompressed DWD TRY data.
   :param debug: If True, print debug information.
   :return: Path to the created CSV file.


.. py:function:: build_temperature_profile_for_year(plz_or_region: str | int, selected_shape: geopandas.GeoDataFrame, year: int | None, debug: bool = True) -> str

   Creates a temperature profile for the selected year and the selected PLZ or Region.

   If the selected year is None or no DWD TRY data is available, this function uses the TMY data
   from the PVGIS API.

   :param plz_or_region: PLZ or Region for which the temperature profile should be created (area ID).
   :param selected_shape: GeoDataFrame of the selected area.
   :param year: Year for which the temperature profile should be created. If None, uses the TMY data from the PVGIS API.
   :param debug: If True, print debug information.
   :return: Path to the created CSV file.


.. py:function:: build_temperature_profile_for_tmy_for_shape(plz_or_region: str | int, selected_shape: geopandas.GeoDataFrame, debug: bool = True) -> str

   Creates a temperature profile for the TMY for the center of the selected PLZ or Region, using the PVGIS API.

   :param plz_or_region: PLZ or Region for which the temperature profile should be created (area ID).
   :param selected_shape: GeoDataFrame of the selected area.
   :param debug: If True, print debug information.
   :return: Path to the created CSV file.


