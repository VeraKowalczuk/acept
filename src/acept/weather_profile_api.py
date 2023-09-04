"""Module for getting weather profiles from the PVGIS API.

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

See Also:
    - Web tool: https://re.jrc.ec.europa.eu/pvg_tools/en/#TMY
    - PVGIS documentation: https://joint-research-centre.ec.europa.eu/photovoltaic-geographical-information-system-pvgis/pvgis-tools/pvgis-typical-meteorological-year-tmy-generator_en
"""

import os

import pandas as pd
import pvlib.iotools as iot
from pandas import DataFrame
from ratelimit import sleep_and_retry, limits

from acept.acept_constants import TEMP_PATH, PVGIS_API_BASE_URL
from acept.uhp_csv_io import write_geopandas_to_uhp_csv

PVGIS_MIN_YEAR = 2005
"""The minimum year for the typical meteorological year (TMY) is 2005."""
PVGIS_MAX_YEAR = 2020
"""The maximum year for the typical meteorological year (TMY) is 2020."""

MAX_CALLS_PER_SECOND = 30
"""The maximum number of calls per second is 30."""

PVGIS_VARIABLE_MAP = {
    'G(h)': 'rad_global',
    'Gb(n)': 'rad_direct',
    'Gd(h)': 'rad_diffuse',
    'IR(h)': 'rad_thermal',
    'H_sun': 'solar_elevation',
    'T2m': 'temperature',
    'RH': 'relative_humidity',
    'SP': 'pressure',
    'WS10m': 'wind_speed',
    'WD10m': 'wind_direction',
}
"""Mapping of PVGIS variable names to acept variable names."""


@sleep_and_retry
@limits(calls=MAX_CALLS_PER_SECOND, period=1)
def send_request_to_pvgis(lat: float, lon: float, start_year: int = PVGIS_MIN_YEAR,
                          end_year: int = PVGIS_MAX_YEAR) -> dict:
    """
    Sends a request to the PVGIS API for a typical meteorological year and returns the response.
    As the PVGIS API is rate limited, the function will sleep and retry if the rate limit is exceeded.

    :param lat: latitude of the location as a float.
    :param lon: longitude of the location as a float.
    :param start_year: First year of the typical meteorological year.
    :param end_year: Last year of the typical meteorological year.
    :raises ValueError: If the end year is less than 10 years after the start year.
    :return: A dictionary containing the data, the months selected, the inputs, and the metadata.
    """
    if end_year - start_year < 10:
        raise ValueError("End year must be at least 10 years after start year.")
    data, months_selected, inputs, metadata = iot.get_pvgis_tmy(latitude=lat, longitude=lon, startyear=start_year,
                                                                endyear=end_year, usehorizon=True, map_variables=False,
                                                                url=PVGIS_API_BASE_URL)

    return {"data": data, "months_selected": months_selected, "inputs": inputs, "metadata": metadata}


def build_weather_profile_for_typical_meteorological_year(lat: float, lon: float, start_year: int = PVGIS_MIN_YEAR,
                                                          end_year: int = PVGIS_MAX_YEAR, return_units: bool = False,
                                                          debug: bool = True) -> tuple[
        pd.DataFrame, pd.DataFrame | None]:
    """
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
    """
    if debug:
        print(f"TMY weather for lat: {lat}, lon: {lon}, Start year: {start_year}, End year: {end_year}")
    # check input data
    if end_year - start_year < 10:
        raise ValueError("End year must be at least 10 years after start year.")
    if start_year < PVGIS_MIN_YEAR or start_year > PVGIS_MAX_YEAR:
        raise ValueError(f"Start year must be between {PVGIS_MIN_YEAR} and {PVGIS_MAX_YEAR}.")
    if end_year < PVGIS_MIN_YEAR or end_year > PVGIS_MAX_YEAR:
        raise ValueError(f"End year must be between {PVGIS_MIN_YEAR} and {PVGIS_MAX_YEAR}.")

    if (lat < -90) or (lat > 90) or (lon < -180) or (lon > 180):
        raise ValueError("Latitude and longitude must be between -90 and 90 and -180 and 180.")

    result = send_request_to_pvgis(lat, lon, start_year, end_year)

    data = result['data'].rename(columns=PVGIS_VARIABLE_MAP, errors='ignore')

    if return_units:
        return data, get_units_for_pvgis_variables(result['metadata'])
    return data, None


def build_temperature_profile_for_tmy(lat: float, lon: float) -> pd.DataFrame:
    """
    Build temperature profile for a typical meteorological year (TMY) from the PVGIS API using the maximal time period
    of 2005 - 2020 (see :py:const:`PVGIS_MIN_YEAR` and :py:const:`PVGIS_MAX_YEAR`).

    :param lat: latitude of the location as a float.
    :param lon: longitude of the location as a float.
    :return: A pandas DataFrame with the temperature profile.
    """
    weather_df, _ = build_weather_profile_for_typical_meteorological_year(lat, lon)
    weather_df.reset_index(inplace=True, drop=True)
    cols_to_drop = [x for x in weather_df.columns.to_list() if x != 'temperature']
    return weather_df.drop(columns=cols_to_drop, inplace=False)


def build_temperature_profile_for_tmy_to_uhp_csv(lat: float, lon: float, area_id: str) -> tuple[str, DataFrame]:
    """
    Create CSV with temperature profile for a typical meteorological year (TMY) from the PVGIS API using the maximal
    time period of 2005 - 2020 (see :py:const:`PVGIS_MIN_YEAR` and :py:const:`PVGIS_MAX_YEAR`).

    :param lat: latitude of the location as a float.
    :param lon: longitude of the location as a float.
    :param area_id: id of the area the location belongs to.
    :return: Path to the created CSV and a pandas DataFrame with the temperature profile.
    """
    output_path = os.path.join(TEMP_PATH, f"PLZ_{area_id}", f"temperature_tmy_{area_id}.csv")
    weather_df = build_temperature_profile_for_tmy(lat, lon)
    write_geopandas_to_uhp_csv(output_path, weather_df["temperature"], ['AMBIENT TEMPERATURE'], ['degC'], sep=';')
    return output_path, weather_df["temperature"]


def build_weather_profile_for_tmy_to_csv(lat: float, lon: float, area_id: str) -> tuple[str, DataFrame]:
    """
    Create CSV with weather profile for a typical meteorological year (TMY) from the PVGIS API using the maximal time
    period of 2005 - 2020 (see :py:const:`PVGIS_MIN_YEAR` and :py:const:`PVGIS_MAX_YEAR`).

    :param lat: latitude of the location as a float.
    :param lon: longitude of the location as a float.
    :param area_id: id of the area the location belongs to.
    :return: Path to the created CSV and a pandas DataFrame with the weather profile.
    """
    output_path = os.path.join(TEMP_PATH, f"PLZ_{area_id}", f"weather_profile_tmy_{area_id}.csv")
    weather_df, units = build_weather_profile_for_typical_meteorological_year(lat, lon, return_units=True)
    write_geopandas_to_uhp_csv(output_path, weather_df, weather_df.columns,
                               units['unit'].to_list(), sep=';')
    return output_path, weather_df


def get_units_for_pvgis_variables(metadata: dict) -> pd.DataFrame:
    """
    Get units of PVGIS variables from PVGIS API response metadata and return them as a pandas DataFrame.

    :param metadata: PVGIS API response metadata.
    :return: A pandas DataFrame with the units of PVGIS variables.
    """
    var = metadata['outputs']['tmy_hourly']['variables']
    units = {}
    for i, v in enumerate(var):
        units[i] = [v, var[v]["units"]]
    units_df = pd.DataFrame.from_dict(units, columns=['field_pvgis', 'unit'], orient='index')
    units_df['field'] = units_df['field_pvgis'].map(PVGIS_VARIABLE_MAP)
    units_df.set_index('field', inplace=True)
    return units_df
