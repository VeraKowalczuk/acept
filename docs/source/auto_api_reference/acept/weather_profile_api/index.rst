:py:mod:`acept.weather_profile_api`
===================================

.. py:module:: acept.weather_profile_api

.. autoapi-nested-parse::

   Module for getting weather profiles from the PVGIS API.

   A typical meteorological year (TMY) is a set of meteorological data with data values for every hour in a year for a
   given geographical location. The data are selected from hourly data for the full time period available,
   currently 2005-2020 in PVGIS 5.2 for the PVGIS-SARAH2 data source. The data set has been produced by choosing for
   each month the most "typical" month out of the full time period available.

   Default DB for Europe, Asia, Africa and South America (below 20 S):
       - PVGIS-SARAH2: from satellite images
       - time period: 2005-2020
       - spatial resolution: 0.05° x 0.05° (~ 5 km)

   Use this module to:
       - send a request to the PVGIS API for a typical meteorological year
       - get TMY weather profiles from the PVGIS API for a given location
       - get TMY temperature profiles from the PVGIS API for a given location
       - calculate GSEE input weather from raw weather data from the PVGIS API for a given location

   Explanation of PVGIS fields:
       - T2m: 2-m air temperature (degree Celsius)
       - RH: relative humidity (%)
       - H_sun: Solar elevation angle (degree)
       - G(h): Global irradiance on the horizontal plane (W/m2)
       - Gb(n): Beam/direct irradiance on a plane always normal to sun rays (W/m2)
       - Gd(h): Diffuse irradiance on the horizontal plane (W/m2)
       - IR(h): Surface infrared (thermal) irradiance on a horizontal plane (W/m2)
       - WS10m: 10-m total wind speed (m/s)
       - WD10m: 10-m wind direction (0 = N, 90 = E) (degree)
       - SP: Surface (air) pressure (Pa)

   .. seealso::

      - Web tool: https://re.jrc.ec.europa.eu/pvg_tools/en/#TMY
      - PVGIS documentation: https://joint-research-centre.ec.europa.eu/photovoltaic-geographical-information-system-pvgis/pvgis-tools/pvgis-typical-meteorological-year-tmy-generator_en



Module Contents
---------------


Functions
~~~~~~~~~

.. autoapisummary::

   acept.weather_profile_api.send_request_to_pvgis
   acept.weather_profile_api.build_weather_profile_for_typical_meteorological_year
   acept.weather_profile_api.build_temperature_profile_for_tmy
   acept.weather_profile_api.build_temperature_profile_for_tmy_to_uhp_csv
   acept.weather_profile_api.build_weather_profile_for_tmy_to_csv
   acept.weather_profile_api.get_units_for_pvgis_variables



Attributes
~~~~~~~~~~

.. autoapisummary::

   acept.weather_profile_api.PVGIS_MIN_YEAR
   acept.weather_profile_api.PVGIS_MAX_YEAR
   acept.weather_profile_api.MAX_CALLS_PER_SECOND
   acept.weather_profile_api.PVGIS_VARIABLE_MAP


.. py:data:: PVGIS_MIN_YEAR
   :value: 2005

   The minimum year for the typical meteorological year (TMY) is 2005.

.. py:data:: PVGIS_MAX_YEAR
   :value: 2020

   The maximum year for the typical meteorological year (TMY) is 2020.

.. py:data:: MAX_CALLS_PER_SECOND
   :value: 30

   The maximum number of calls per second is 30.

.. py:data:: PVGIS_VARIABLE_MAP

   Mapping of PVGIS variable names to acept variable names.

.. py:function:: send_request_to_pvgis(lat: float, lon: float, start_year: int = PVGIS_MIN_YEAR, end_year: int = PVGIS_MAX_YEAR) -> dict

   Sends a request to the PVGIS API for a typical meteorological year and returns the response.
   As the PVGIS API is rate limited, the function will sleep and retry if the rate limit is exceeded.

   :param lat: latitude of the location as a float.
   :param lon: longitude of the location as a float.
   :param start_year: First year of the typical meteorological year.
   :param end_year: Last year of the typical meteorological year.
   :raises ValueError: If the end year is less than 10 years after the start year.
   :return: A dictionary containing the data, the months selected, the inputs, and the metadata.


.. py:function:: build_weather_profile_for_typical_meteorological_year(lat: float, lon: float, start_year: int = PVGIS_MIN_YEAR, end_year: int = PVGIS_MAX_YEAR, return_units: bool = False, debug: bool = True) -> tuple[pandas.DataFrame, pandas.DataFrame | None]

   Build weather profile for a typical meteorological year (TMY) from the PVGIS API.
   The time period has to be at least 10 years and between 2005 and 2020 (see :py:const:`PVGIS_MIN_YEAR` and
   :py:const:`PVGIS_MAX_YEAR`).

   :param lat: latitude of the location as a float.
   :param lon: longitude of the location as a float.
   :param start_year: First year of the typical meteorological year, must be between 2005 and 2020.
   :param end_year: Last year of the typical meteorological year, must be between 2005 and 2020.
   :param return_units: Whether to return the units of the returned DataFrame.
   :param debug: Whether to print debug information.
   :raises ValueError: If the end year is less than 10 years after the start year. If the start and end year are not
       between 2005 and 2020. If the latitude and longitude are not between -90 and 90 and -180 and 180.
   :return: A pandas DataFrame with the weather profile and optionally the units of the fields in the DataFrame.


.. py:function:: build_temperature_profile_for_tmy(lat: float, lon: float) -> pandas.DataFrame

   Build temperature profile for a typical meteorological year (TMY) from the PVGIS API using the maximal time period
   of 2005 - 2020 (see :py:const:`PVGIS_MIN_YEAR` and :py:const:`PVGIS_MAX_YEAR`).

   :param lat: latitude of the location as a float.
   :param lon: longitude of the location as a float.
   :return: A pandas DataFrame with the temperature profile.


.. py:function:: build_temperature_profile_for_tmy_to_uhp_csv(lat: float, lon: float, area_id: str) -> tuple[str, pandas.DataFrame]

   Create CSV with temperature profile for a typical meteorological year (TMY) from the PVGIS API using the maximal
   time period of 2005 - 2020 (see :py:const:`PVGIS_MIN_YEAR` and :py:const:`PVGIS_MAX_YEAR`).

   :param lat: latitude of the location as a float.
   :param lon: longitude of the location as a float.
   :param area_id: id of the area the location belongs to.
   :return: Path to the created CSV and a pandas DataFrame with the temperature profile.


.. py:function:: build_weather_profile_for_tmy_to_csv(lat: float, lon: float, area_id: str) -> tuple[str, pandas.DataFrame]

   Create CSV with weather profile for a typical meteorological year (TMY) from the PVGIS API using the maximal time
   period of 2005 - 2020 (see :py:const:`PVGIS_MIN_YEAR` and :py:const:`PVGIS_MAX_YEAR`).

   :param lat: latitude of the location as a float.
   :param lon: longitude of the location as a float.
   :param area_id: id of the area the location belongs to.
   :return: Path to the created CSV and a pandas DataFrame with the weather profile.


.. py:function:: get_units_for_pvgis_variables(metadata: dict) -> pandas.DataFrame

   Get units of PVGIS variables from PVGIS API response metadata and return them as a pandas DataFrame.

   :param metadata: PVGIS API response metadata.
   :return: A pandas DataFrame with the units of PVGIS variables.


