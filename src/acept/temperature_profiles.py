"""Module for building ambient temperature profiles

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
"""

import gc
import os
from calendar import monthrange, isleap

import geopandas as gpd
import pandas as pd
import psutil
import rioxarray
import xarray as xr

from acept import acept_utils
from acept import plz_shape
from acept.acept_constants import TEMP_PATH
from acept.dwd_try_data_handling import read_dwd_netcdf_file, preprocess_dwd_try_dataset, DWD_MIN_YEAR, DWD_MAX_YEAR, \
    preprocess_combined_dwd_try_dataset, check_for_un_compressed_dwd_try_data, check_for_dwd_try_data_year
from acept.exceptions import ValueOutsideRangeError
from acept.weather_profile_api import build_temperature_profile_for_tmy_to_uhp_csv


def build_temperature_profiles_for_selected_years(plz_or_region: int | str, selected_shape: gpd.GeoDataFrame,
                                                  year_start: int = DWD_MIN_YEAR, year_end: int = DWD_MAX_YEAR,
                                                  debug: bool = True) -> str:
    """
    Creates a temperature profile for the selected year and the selected PLZ or Region using DWD TRY temperature data.

    :param plz_or_region: PLZ or Region for which the temperature profile should be created (area ID).
    :param selected_shape: GeoDataFrame of the selected area.
    :param year_start: First year for which the temperature profile should be created. Defaults to 1995.
    :param year_end: Last year for which the temperature profile should be created. Defaults to 2012.
    :param debug: If True, print debug information.
    :raises ValueOutsideRangeError: if year_start or year_end is outside the allowed range (1995-2012).
    :return: Path to the directory where the created CSV files are stored.
    """
    if year_start > year_end or year_start < DWD_MIN_YEAR or year_end > DWD_MAX_YEAR:
        raise ValueOutsideRangeError(DWD_MIN_YEAR, DWD_MAX_YEAR)

    plz_or_region = str(plz_or_region)
    if selected_shape is None and plz_or_region.isdigit() and len(plz_or_region) == 5:
        # get shape of queried plz
        selected_shape = plz_shape.get_single_plz_shape(plz_or_region)

    # convert to projection of DWD try data
    selected_shape = selected_shape.to_crs(epsg=3034)
    if debug:
        print("plz_mask.crs:", selected_shape.crs)

    for year_spec in range(year_start, year_end + 1):
        for month_spec in range(1, 13):
            if debug:
                print("Free Memory 1:", psutil.virtual_memory().available * 100 / psutil.virtual_memory().total)

            wd_data = read_dwd_netcdf_file("temperature", year=year_spec, month=month_spec, debug=True)

            wd_data = preprocess_dwd_try_dataset(wd_data, "temperature")

            # ---------
            # ### Clipping
            # all_touched – If True, all pixels touched by geometries will be burned in.
            # If false, only pixels whose center is within the polygon or that are selected by Bresenham’s line
            # algorithm will be burned in.
            wd_clipped: xr.Dataset = wd_data.rio.clip(selected_shape.geometry.values, selected_shape.crs,
                                                      all_touched=True)

            # free up memory
            del wd_data
            if debug:
                print("Free Memory 2:", psutil.virtual_memory().available * 100 / psutil.virtual_memory().total)
            # ---------
            # Create timeseries of average temperature for each hour over the PLZ area (clipped xarray)
            avg_temp_over_hours = wd_clipped.mean(("X", "Y"))
            avg_temp_over_hours_ds = avg_temp_over_hours.temperature.to_pandas()

            hours_in_month = 24 * monthrange(year_spec, month_spec)[1]
            if avg_temp_over_hours_ds.shape[0] != hours_in_month:
                raise Exception("month:", month_spec, "/", year_spec, " -----  avg_temp_over_hours_ds.shape[0] =",
                                avg_temp_over_hours_ds.shape[0], "not 720")

            del wd_clipped
            del avg_temp_over_hours
            if debug:
                print("Free Memory w/o wd_clipped, avg_temp_over_hours:",
                      psutil.virtual_memory().available * 100 / psutil.virtual_memory().total)
            # ---------
            # append timeseries to csv
            temp_csv_output_path = os.path.join(TEMP_PATH, f"PLZ_{plz_or_region}",
                                                f"DWD_TRY_{plz_or_region}_{year_spec}.csv")
            os.makedirs(acept_utils.uppath(temp_csv_output_path, 1), exist_ok=True)

            # add unit info and header according to UHP only at the beginning of the file
            if not os.path.exists(temp_csv_output_path):
                header_temp = ['AMBIENT TEMPERATURE']
                unit_info = pd.DataFrame([['degC']], columns=header_temp)
                unit_info.to_csv(temp_csv_output_path, mode='a', sep=";", index=False, columns=header_temp,
                                 header=True)

            with open(temp_csv_output_path) as f:
                hours_in_year = (366 if isleap(year_spec) else 365) * 24
                if sum(1 for _ in f) < hours_in_year + 2:
                    # append to csv
                    avg_temp_over_hours_ds.to_csv(temp_csv_output_path, mode='a', sep=";", index=False,
                                                  header=False)
                else:
                    print("already 8760 time steps (hours) in the csv file of the temperature profile for ",
                          year_spec, plz_or_region)

            if debug:
                print("Free Memory @ end of month:",
                      psutil.virtual_memory().available * 100 / psutil.virtual_memory().total)
            # force garbage collection to keep the memory usage acceptable
            gc.collect()
    return acept_utils.uppath(temp_csv_output_path, 1)


def build_temperature_profiles_for_selected_years_with_combined_data(plz_or_region: str | int,
                                                                     selected_shape: gpd.GeoDataFrame,
                                                                     year_start: int = DWD_MIN_YEAR,
                                                                     year_end: int = DWD_MAX_YEAR,
                                                                     uncompressed: bool = False,
                                                                     debug: bool = True) -> str:
    """
    Creates a temperature profile for the selected year and the selected PLZ or Region using the combined DWD TRY data.

    :param plz_or_region: PLZ or Region for which the temperature profile should be created (area ID).
    :param selected_shape: GeoDataFrame of the selected area.
    :param year_start: First year for which the temperature profile should be created. Defaults to 1995.
    :param year_end: Last year for which the temperature profile should be created. Defaults to 2012.
    :param uncompressed: If True, use the uncompressed DWD TRY data.
    :param debug: If True, print debug information.
    :raises ValueOutsideRangeError: If year_start or year_end is outside the allowed range (1995-2012).
    :return: Path to the directory where the created CSV files are stored.
    """
    if year_start > year_end or year_start < DWD_MIN_YEAR or year_end > DWD_MAX_YEAR:
        raise ValueOutsideRangeError(DWD_MIN_YEAR, DWD_MAX_YEAR)

    plz_or_region = str(plz_or_region)

    # convert to projection of DWD try data
    selected_shape = selected_shape.to_crs(epsg=3034)
    if debug:
        print("selected_shape.crs:", selected_shape.crs)

    for year_spec in range(year_start, year_end + 1):
        for month_spec in range(1, 13):
            if debug:
                print("Free Memory 1:", psutil.virtual_memory().available * 100 / psutil.virtual_memory().total)

            if uncompressed:
                wd_data = read_dwd_netcdf_file("combined_try_uncompressed", year=year_spec, month=month_spec,
                                               debug=debug)
            else:
                wd_data = read_dwd_netcdf_file("combined_try", year=year_spec, month=month_spec, debug=debug)

            wd_data = preprocess_combined_dwd_try_dataset(wd_data, debug)

            # reduce the dataset to the temperature data
            wd_data = wd_data.drop_vars(["rad_direct", "rad_global"])

            # ---------
            # ### Clipping
            # all_touched – If True, all pixels touched by geometries will be burned in.
            # If false, only pixels whose center is within the polygon or that are selected by Bresenham’s line
            # algorithm will be burned in.
            wd_clipped: xr.Dataset = wd_data.rio.clip(selected_shape.geometry.values, selected_shape.crs,
                                                      all_touched=True)

            # free up memory
            del wd_data
            if debug:
                print("Free Memory w/o wd_data:",
                      psutil.virtual_memory().available * 100 / psutil.virtual_memory().total)
            # ---------
            # Create timeseries of average temperature for each hour over the PLZ area (clipped xarray)
            avg_temp_over_hours = wd_clipped.mean(("X", "Y"))
            avg_temp_over_hours_ds = avg_temp_over_hours.temperature.to_pandas()

            hours_in_month = 24 * monthrange(year_spec, month_spec)[1]
            if avg_temp_over_hours_ds.shape[0] != hours_in_month:
                raise Exception("month:", month_spec, "/", year_spec, " -----  avg_temp_over_hours_ds.shape[0] =",
                                avg_temp_over_hours_ds.shape[0], "not 720")

            del wd_clipped
            del avg_temp_over_hours
            if debug:
                print("Free Memory w/o wd_clipped:",
                      psutil.virtual_memory().available * 100 / psutil.virtual_memory().total)
            # ---------
            # append timeseries to csv
            temp_csv_output_path = os.path.join(TEMP_PATH, f"PLZ_{plz_or_region}",
                                                f"DWD_TRY_{plz_or_region}_{year_spec}.csv")
            os.makedirs(acept_utils.uppath(temp_csv_output_path, 1), exist_ok=True)

            # add unit info and header according to UHP only at the beginning of the file
            if not os.path.exists(temp_csv_output_path):
                header_temp = ['AMBIENT TEMPERATURE']
                unit_info = pd.DataFrame([['degC']], columns=header_temp)
                unit_info.to_csv(temp_csv_output_path, mode='a', sep=";", index=False, columns=header_temp,
                                 header=True)

            with open(temp_csv_output_path) as f:
                hours_in_year = (366 if isleap(year_spec) else 365) * 24
                if sum(1 for _ in f) < hours_in_year + 2:
                    # append to csv
                    avg_temp_over_hours_ds.to_csv(temp_csv_output_path, mode='a', sep=";", index=False,
                                                  header=False)
                else:
                    print("already 8760 time steps (hours) in the csv file of the temperature profile for ",
                          year_spec, plz_or_region)

            if debug:
                print("Free Memory @ end of month:",
                      psutil.virtual_memory().available * 100 / psutil.virtual_memory().total)
            # force garbage collection to keep the memory usage acceptable
            gc.collect()
    return acept_utils.uppath(temp_csv_output_path, 1)


def build_temperature_profile_for_selected_year_with_combined_data(plz_or_region: str | int,
                                                                   selected_shape: gpd.GeoDataFrame,
                                                                   year: int = 2011, uncompressed: bool = False,
                                                                   debug: bool = True) -> str:
    """
    Creates a temperature profile for the selected year and the selected PLZ or Region using the combined DWD TRY data.

    :param plz_or_region: PLZ or Region for which the temperature profile should be created (area ID).
    :param selected_shape: GeoDataFrame of the selected area.
    :param year: Year for which the temperature profile should be created.
    :param uncompressed: If True, use the uncompressed DWD TRY data.
    :param debug: If True, print debug information.
    :return: Path to the created CSV file.
    """
    dir_path = build_temperature_profiles_for_selected_years_with_combined_data(plz_or_region=plz_or_region,
                                                                                selected_shape=selected_shape,
                                                                                year_start=year, year_end=year,
                                                                                uncompressed=uncompressed, debug=debug)
    file_name = f"DWD_TRY_{plz_or_region}_{year}.csv"
    return os.path.join(dir_path, file_name)


def build_temperature_profile_for_year(plz_or_region: str | int, selected_shape: gpd.GeoDataFrame, year: int | None,
                                       debug: bool = True) -> str:
    """
    Creates a temperature profile for the selected year and the selected PLZ or Region. 
    
    If the selected year is None or no DWD TRY data is available, this function uses the TMY data 
    from the PVGIS API.

    :param plz_or_region: PLZ or Region for which the temperature profile should be created (area ID).
    :param selected_shape: GeoDataFrame of the selected area.
    :param year: Year for which the temperature profile should be created. If None, uses the TMY data from the PVGIS API.
    :param debug: If True, print debug information.
    :return: Path to the created CSV file.
    """
    if year is None:
        return build_temperature_profile_for_tmy_for_shape(plz_or_region, selected_shape, debug)
    if debug:
        print("Creating a temperature profile for year", year, "for", plz_or_region)
    if check_for_un_compressed_dwd_try_data(compressed=False, year_start=year, year_end=year):
        return build_temperature_profile_for_selected_year_with_combined_data(plz_or_region, selected_shape, year,
                                                                              uncompressed=True, debug=debug)
    elif check_for_un_compressed_dwd_try_data(compressed=True, year_start=year, year_end=year):
        return build_temperature_profile_for_selected_year_with_combined_data(plz_or_region, selected_shape, year,
                                                                              uncompressed=False, debug=debug)
    elif check_for_dwd_try_data_year(year, ["temperature"]):
        dir_path = build_temperature_profiles_for_selected_years(plz_or_region, selected_shape, year, year, debug)
        file_name = f"DWD_TRY_{plz_or_region}_{year}.csv"
        return os.path.join(dir_path, file_name)
    else:
        # Fall back to use the TMY if no data is downloaded for the selected year
        return build_temperature_profile_for_tmy_for_shape(plz_or_region, selected_shape, debug)


def build_temperature_profile_for_tmy_for_shape(plz_or_region: str | int, selected_shape: gpd.GeoDataFrame,
                                                debug: bool = True) -> str:
    """
    Creates a temperature profile for the TMY for the center of the selected PLZ or Region, using the PVGIS API.

    :param plz_or_region: PLZ or Region for which the temperature profile should be created (area ID).
    :param selected_shape: GeoDataFrame of the selected area.
    :param debug: If True, print debug information.
    :return: Path to the created CSV file.
    """
    if debug:
        print("Creating a temperature profile for the TMY", "for", plz_or_region)
    plz_or_region = str(plz_or_region)
    selected_shape.to_crs(epsg=4326, inplace=True)
    if debug:
        print("selected_shape.crs:", selected_shape.crs)

    lon_center = selected_shape.iloc[0].geometry.centroid.x
    lat_center = selected_shape.iloc[0].geometry.centroid.y
    file_path, _ = build_temperature_profile_for_tmy_to_uhp_csv(lat_center, lon_center, plz_or_region)
    return file_path


# ###################################################################################################################


if __name__ == '__main__':
    # rioxarray extends xarray with the rio accessor. The rio accessor is activated by importing rioxarray like so:
    # import rioxarray
    # Do not delete this line otherwise the import might get deleted
    rioxarray.show_versions()
