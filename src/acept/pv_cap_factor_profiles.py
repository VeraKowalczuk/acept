"""Module for building PV capacity factor profiles.

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
"""

import datetime
import gc
import os
from calendar import isleap

import geopandas as gpd
import gsee
import pandas as pd
import psutil
import xarray as xr

from acept import acept_utils
from acept.acept_constants import TEMP_PATH
from acept.dwd_try_data_handling import DWD_MIN_YEAR, DWD_MAX_YEAR, read_dwd_netcdf_file, preprocess_dwd_try_dataset, \
    preprocess_combined_dwd_try_dataset, check_for_un_compressed_dwd_try_data, check_for_dwd_try_data_year
from acept.exceptions import ValueOutsideRangeError
from acept.uhp_csv_io import write_geopandas_to_uhp_csv
from acept.weather_profile_api import build_weather_profile_for_typical_meteorological_year


# ----- Building PV capacity factor profiles without using the renewables.ninja rate-limited API


def build_pv_capacity_for_selected_years(selected_shape: gpd.GeoDataFrame, buildings: gpd.GeoDataFrame,
                                         year_start: int = DWD_MIN_YEAR, year_end: int = DWD_MAX_YEAR,
                                         building_specific_weather: bool = False,
                                         debug: bool = True) -> str:
    """
    Build PV capacity factor profiles for all years between year_start and year_end for all given buildings from the
    DWD TRY data. The weather data is expected as downloaded from the DWD OPENDATA portal. The profiles will be saved in
    a temporary directory in the :py:const:`acept.acept_constants.TEMP_PATH` directory as one CSV file per building per year.

    :param selected_shape: GeoDataFrame containing the shape of the area around the buildings.
    :param buildings: GeoDataFrame containing the buildings.
    :param year_start: Start year of the PV capacity factor profiles. Must be between DWD_MIN_YEAR and DWD_MAX_YEAR.
    :param year_end: End year of the PV capacity factor profiles. Must be between DWD_MIN_YEAR and DWD_MAX_YEAR.
    :param building_specific_weather: Whether to use building specific weather data. Defaults to False.
    :param debug: Whether to print debug messages. Defaults to True.
    :raises ValueOutsideRangeError: If year_start or year_end are outside the valid range (see DWD_MAX_RANGE)
    :return: Path to the directory containing the created CSV files.
    """
    if year_start > year_end or year_start < DWD_MIN_YEAR or year_end > DWD_MAX_YEAR:
        raise ValueOutsideRangeError(DWD_MIN_YEAR, DWD_MAX_YEAR)
    # Use the current time as an identifier
    current_time = datetime.datetime.now()
    run_id = current_time.strftime("%Y%m%d%H%M%S")

    # ---------
    dwd_features = ['temperature', 'rad_direct', 'rad_global']
    # buildings needs gpd.GeoDataFrame(buildings, columns=['bid', 'lat', 'lon', 'geometry'])
    buildings.sort_values('bid', inplace=True)

    # convert to projection of DWD try data
    selected_shape.to_crs(epsg=3034, inplace=True)
    buildings.to_crs(epsg=3034, inplace=True)
    if debug:
        print("selected_shape.crs:", selected_shape.crs)

    for year_spec in range(year_start, year_end + 1):
        for month_spec in range(1, 13):
            if debug:
                print("Free Memory @ begin of month:",
                      psutil.virtual_memory().available * 100 / psutil.virtual_memory().total)

            # collect data for all relevant DWD TRY features: temperature, SID, SIS
            try_clipped: xr.Dataset = None
            for try_feature in dwd_features:
                wd_data = read_dwd_netcdf_file(try_feature, year=year_spec, month=month_spec, debug=debug)

                wd_data = preprocess_dwd_try_dataset(wd_data, try_feature, debug=debug)

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

                # collect clipped data in one dataset
                if try_clipped is None:
                    try_clipped = wd_clipped
                else:
                    try_clipped[try_feature] = wd_clipped[try_feature]

                del wd_clipped
                if debug:
                    print("Free Memory w/o wd_clipped:",
                          psutil.virtual_memory().available * 100 / psutil.virtual_memory().total)

            if not building_specific_weather:
                x = selected_shape.iloc[0].geometry.centroid.x
                y = selected_shape.iloc[0].geometry.centroid.y
                weather = try_clipped.sel(X=x, Y=y, method="nearest")
                input_weather = calculate_gsee_input_weather_from_raw_weather(weather)

            # ---------
            # calculate PV capacity per hour for each building in the month year, append to csv per building
            # maybe use one csv with buildings as columns, rows as hourly timestamps and values as PV capacity?
            for building in buildings.index:
                # try_crs = ccrs.epsg(3034)
                lon, lat = buildings.loc[building, 'lon'], buildings.loc[building, 'lat']
                # # Transform the location from src_crs for lat/lon grid to try_crs
                # x, y = try_crs.transform_point(lon, lat, src_crs=ccrs.Geodetic())
                if building_specific_weather:
                    x = buildings.loc[building, "geometry"].centroid.x
                    y = buildings.loc[building, "geometry"].centroid.y
                    weather = try_clipped.sel(X=x, Y=y, method="nearest")
                    input_weather = calculate_gsee_input_weather_from_raw_weather(weather)

                pv_capacity_result: pd.Series = gsee.pv.run_model(
                    input_weather,
                    coords=(lat, lon),  # Latitude and longitude
                    tilt=30,  # 30 degrees tilt angle
                    azim=180,  # facing towards the equator,
                    tracking=0,  # fixed - no tracking
                    capacity=1.0,  # 1 W
                    system_loss=0.1,  # 10% loss
                )

                if building_specific_weather:
                    del input_weather

                # write result to csv file
                temp_csv_output_path = os.path.join(TEMP_PATH, run_id,
                                                    f"building_{buildings.loc[building, 'bid']}_pv_capacity_{year_spec}.csv")
                os.makedirs(acept_utils.uppath(temp_csv_output_path, 1), exist_ok=True)

                # add unit info and header according to UHP only at the beginning of the file
                if not os.path.exists(temp_csv_output_path):
                    header_temp = ['PV Capacity Factor']
                    unit_info = pd.DataFrame([[f"bid_{buildings.loc[building, 'bid']}"]], columns=header_temp)
                    unit_info.to_csv(temp_csv_output_path, mode='a', sep=";", index=False, columns=header_temp,
                                     header=True)

                with open(temp_csv_output_path) as f:
                    hours_in_year = (366 if isleap(year_spec) else 365) * 24
                    if sum(1 for _ in f) < hours_in_year + 2:
                        # append to csv
                        pv_capacity_result.to_csv(temp_csv_output_path, mode='a', sep=";", index=False,
                                                  header=False)
                    else:
                        print("already 8760 time steps (hours) in the csv file of the temperature profile for ",
                              year_spec, buildings.loc[building, 'bid'])

                del pv_capacity_result
                if debug:
                    print("Free Memory @ end of building w/o pv_capacity_result:",
                          psutil.virtual_memory().available * 100 / psutil.virtual_memory().total)
                pass
            del try_clipped
            if debug:
                print("Free Memory @ end of month:",
                      psutil.virtual_memory().available * 100 / psutil.virtual_memory().total)
            # force garbage collection to keep the memory usage acceptable
            gc.collect()
    return acept_utils.uppath(temp_csv_output_path, 1)


def build_pv_capacity_for_selected_year_with_combined_data(selected_shape: gpd.GeoDataFrame,
                                                           buildings: gpd.GeoDataFrame, year: int = 2011,
                                                           uncompressed: bool = False,
                                                           building_specific_weather: bool = False,
                                                           debug: bool = True) -> str:
    """
    Build PV capacity factor profiles for a single year between for all given buildings from the
    DWD TRY data. The weather data is expected as combined files for the different features - use the
    `acept.dwd_try_data_handling.combine_dwd_try_data_and_save()` function to combine the data. The profiles will be
    saved in a temporary directory in the :py:const:`acept.acept_constants.TEMP_PATH` directory as one CSV file per building.

    :param selected_shape: GeoDataFrame containing the shape of the area around the buildings.
    :param buildings: GeoDataFrame containing the buildings.
    :param year: Year the PV capacity factor profiles are calculated for. Must be between DWD_MIN_YEAR and DWD_MAX_YEAR.
    :param uncompressed: Whether to use uncompressed DWD TRY data files. Defaults to False.
    :param building_specific_weather: Whether to use building specific weather data. Defaults to False.
    :param debug: Whether to print debug messages. Defaults to True.
    :return: Path to the directory containing the created CSV files.
    """
    return build_pv_capacity_for_selected_years_with_combined_data(selected_shape=selected_shape, buildings=buildings,
                                                                   year_start=year, year_end=year,
                                                                   uncompressed=uncompressed,
                                                                   building_specific_weather=building_specific_weather,
                                                                   debug=debug)


def build_pv_capacity_for_selected_years_with_combined_data(selected_shape: gpd.GeoDataFrame,
                                                            buildings: gpd.GeoDataFrame, year_start: int = DWD_MIN_YEAR,
                                                            year_end: int = DWD_MAX_YEAR, uncompressed: bool = False,
                                                            building_specific_weather: bool = False,
                                                            debug: bool = True):
    """
    Build PV capacity factor profiles for all years between year_start and year_end for all given buildings from the
    DWD TRY data. The weather data is expected as combined files for the different features - use the
    acept.dwd_try_data_handling.combine_dwd_try_data_and_save() function to combine the data. The profiles will be saved
    in a temporary directory in the :py:const:`acept.acept_constants.TEMP_PATH` directory as one CSV file per building per year.

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
    """
    if year_start > year_end or year_start < DWD_MIN_YEAR or year_end > DWD_MAX_YEAR:
        raise ValueOutsideRangeError(DWD_MIN_YEAR, DWD_MAX_YEAR)
    # Use the current time as an identifier
    current_time = datetime.datetime.now()
    run_id = current_time.strftime("%Y%m%d%H%M%S")

    # ---------

    # buildings needs gpd.GeoDataFrame(buildings, columns=['bid', 'lat', 'lon', 'geometry'])
    buildings.sort_values('bid', inplace=True)

    # convert to projection of DWD try data
    selected_shape.to_crs(epsg=3034, inplace=True)
    buildings.to_crs(epsg=3034, inplace=True)
    if debug:
        print("selected_shape.crs:", selected_shape.crs)
        print("buildings.crs:", buildings.crs)

    for year_spec in range(year_start, year_end + 1):
        for month_spec in range(1, 13):
            if debug:
                print("Free Memory @ begin of month:",
                      psutil.virtual_memory().available * 100 / psutil.virtual_memory().total)

            if uncompressed:
                wd_data = read_dwd_netcdf_file("combined_try_uncompressed", year=year_spec, month=month_spec,
                                               debug=debug)
            else:
                wd_data = read_dwd_netcdf_file("combined_try", year=year_spec, month=month_spec, debug=debug)

            wd_data = preprocess_combined_dwd_try_dataset(wd_data, debug=debug)
            wd_clipped = wd_data

            # ---------
            # ### Clipping: only use to trade of saving memory for a longer runtime
            # wd_clipped: xr.Dataset = wd_data.rio.clip(selected_shape.geometry.values, selected_shape.crs,
            #                                           all_touched=True)

            # free up memory
            del wd_data
            if debug:
                print("Free Memory w/o wd_data:",
                      psutil.virtual_memory().available * 100 / psutil.virtual_memory().total)

            if not building_specific_weather:
                x = selected_shape.iloc[0].geometry.centroid.x
                y = selected_shape.iloc[0].geometry.centroid.y
                weather = wd_clipped.sel(X=x, Y=y, method="nearest")
                input_weather = calculate_gsee_input_weather_from_raw_weather(weather)

            # ---------
            # calculate PV capacity per hour for each building in the month year, append to csv per building
            # maybe use one csv with buildings as columns, rows as hourly timestamps and values as PV capacity?
            for building in buildings.index:
                # all buildings to one file or each building to its own file?
                # try_crs = ccrs.epsg(3034)
                lon, lat = buildings.loc[building, 'lon'], buildings.loc[building, 'lat']
                # # Transform the location from src_crs for lat/lon grid to try_crs
                # x, y = try_crs.transform_point(lon, lat, src_crs=ccrs.Geodetic())

                if building_specific_weather:
                    x = buildings.loc[building, "geometry"].centroid.x
                    y = buildings.loc[building, "geometry"].centroid.y
                    weather = wd_clipped.sel(X=x, Y=y, method="nearest")
                    input_weather = calculate_gsee_input_weather_from_raw_weather(weather)
                # -----

                pv_capacity_result: pd.Series = gsee.pv.run_model(
                    input_weather,
                    coords=(lat, lon),  # Latitude and longitude
                    tilt=30,  # 30 degrees tilt angle
                    azim=180,  # facing towards the equator,
                    tracking=0,  # fixed - no tracking
                    capacity=1.0,  # 1 W
                    system_loss=0.1,  # 10% loss
                )

                if building_specific_weather:
                    del input_weather

                # write result to csv file
                # TODO find suitable file naming scheme
                temp_csv_output_path = os.path.join(TEMP_PATH, run_id,
                                                    f"building_{buildings.loc[building, 'bid']}_pv_capacity_{year_spec}.csv")
                os.makedirs(acept_utils.uppath(temp_csv_output_path, 1), exist_ok=True)

                # add unit info and header according to UHP only at the beginning of the file
                if not os.path.exists(temp_csv_output_path):
                    header_temp = ['PV Capacity Factor']
                    unit_info = pd.DataFrame([[f"bid_{buildings.loc[building, 'bid']}"]], columns=header_temp)
                    unit_info.to_csv(temp_csv_output_path, mode='a', sep=";", index=False, columns=header_temp,
                                     header=True)

                with open(temp_csv_output_path) as f:
                    hours_in_year = (366 if isleap(year_spec) else 365) * 24
                    if sum(1 for _ in f) < hours_in_year + 2:
                        # append to csv
                        pv_capacity_result.to_csv(temp_csv_output_path, mode='a', sep=";", index=False,
                                                  header=False)
                    else:
                        print("already 8760 time steps (hours) in the csv file of the temperature profile for ",
                              year_spec, buildings.loc[building, 'bid'])

                del pv_capacity_result
                if debug:
                    print("Free Memory w/o pv_capacity_result:",
                          psutil.virtual_memory().available * 100 / psutil.virtual_memory().total)
                pass

            del wd_clipped
            if debug:
                print("Free Memory @ end of month:",
                      psutil.virtual_memory().available * 100 / psutil.virtual_memory().total)
            # force garbage collection to keep the memory usage acceptable
            gc.collect()
    return acept_utils.uppath(temp_csv_output_path, 1)


def calculate_gsee_input_weather_from_raw_weather(weather: xr.Dataset | pd.DataFrame,
                                                  rad_diffuse_col: bool = False) -> xr.Dataset | pd.DataFrame:
    """
    Calculate the GSEE input weather from the raw weather, including the diffuse fraction.

    :param weather: The raw weather data as xarray.Dataset or pandas.DataFrame
    :param rad_diffuse_col: Whether the diffuse radiation column exists or has to be calculated.
    :return: The GSEE input weather
    """
    # diffuse_fraction = rad_diffuse / rad_global = (rad_global - rad_direct) / rad_global
    if rad_diffuse_col:
        weather["diffuse_fraction"] = (weather["rad_diffuse"] / weather["rad_global"]).fillna(0)
    else:
        weather["diffuse_fraction"] = (
                (weather["rad_global"] - weather["rad_direct"]) / weather["rad_global"]).fillna(0)
    if isinstance(weather, xr.Dataset):
        input_weather = weather.to_dataframe().rename(columns={"rad_global": "global_horizontal"})
    else:
        input_weather = weather.rename(columns={"rad_global": "global_horizontal"})
    input_weather = input_weather.loc[:, ['global_horizontal', 'diffuse_fraction', 'temperature']]
    return input_weather


def build_pv_capacity_profile_for_year(selected_shape: gpd.GeoDataFrame, buildings: gpd.GeoDataFrame, year: int | None,
                                       debug: bool = True):
    """
    Build PV capacity factor profiles for a single year for all given buildings from the DWD TRY data. The profiles are
    saved in a temporary directory in the :py:const:`acept.acept_constants.TEMP_PATH` directory as one CSV file per building.

    :param selected_shape: GeoDataFrame containing the shape of the area around the buildings.
    :param buildings: GeoDataFrame containing the buildings.
    :param year: Year the PV capacity factor profiles are calculated for. Must be between DWD_MIN_YEAR and DWD_MAX_YEAR.
        If None, the PV capacity factor profiles are calculated for the typical meteorological year (TMY).
    :param debug: Whether to print debug messages. Defaults to True.
    :return: Path to the directory containing the created CSV files.
    """
    if year is None:
        return calculate_pv_capacity_profile_based_on_tmy_weather(selected_shape, buildings, debug=debug)
    if check_for_un_compressed_dwd_try_data(compressed=False, year_start=year, year_end=year):
        temp_dir = build_pv_capacity_for_selected_year_with_combined_data(selected_shape, buildings, year,
                                                                          uncompressed=True, debug=debug)
    elif check_for_un_compressed_dwd_try_data(compressed=True, year_start=year, year_end=year):
        print("The weather data is compressed. Combine and uncompress the data for year", year, "to get a better "
                                                                                                "response time.")
        temp_dir = build_pv_capacity_for_selected_year_with_combined_data(selected_shape, buildings, year,
                                                                          uncompressed=False, debug=debug)
    elif check_for_dwd_try_data_year(year, ['temperature', 'rad_direct', 'rad_global']):
        print("The weather data is compressed and not combined to a single file per month. Combine and uncompress the "
              "data for year", year, "to get a better response time.")
        temp_dir = build_pv_capacity_for_selected_years(selected_shape, buildings, year, year, debug=debug)
    else:
        # fall back to use TMY weather if the data is not downloaded
        return calculate_pv_capacity_profile_based_on_tmy_weather(selected_shape, buildings, debug=debug)
    return temp_dir


#####################################################################################################

# Use weather API of PVGIS to get the input weather data

def calculate_pv_capacity_profile_based_on_tmy_weather(selected_shape: gpd.GeoDataFrame, buildings: gpd.GeoDataFrame,
                                                       building_specific_weather: bool = False,
                                                       debug: bool = True):
    """
    Build PV capacity factor profiles for a typical meteorological year (TMY) for all given buildings from the
    using the PVGIS weather API. The profiles will be saved in a temporary directory in the :py:const:`acept.acept_constants.TEMP_PATH` directory as
    one CSV file per building.

    :param selected_shape: GeoDataFrame containing the shape of the area around the buildings.
    :param buildings: GeoDataFrame containing the buildings.
    :param building_specific_weather: Whether to use building specific weather data. Defaults to False.
    :param debug: Whether to print debug messages. Defaults to True.
    """
    # Use the current time as an identifier
    current_time = datetime.datetime.now()
    run_id = current_time.strftime("%Y%m%d%H%M%S")

    # buildings needs gpd.GeoDataFrame(buildings, columns=['bid', 'lat', 'lon', 'geometry'])
    buildings.sort_values('bid', inplace=True)

    # convert to projection of ETRS Lambert Azimuthal Equal Area projection to flat up the surface of Northern Europe
    saved_crs = buildings.crs
    selected_shape.to_crs(epsg=4326, inplace=True)
    buildings.to_crs(epsg=4326, inplace=True)
    if debug:
        print("selected_shape.crs:", selected_shape.crs)
        print("buildings.crs:", buildings.crs)

    if not building_specific_weather:
        lon_center = selected_shape.iloc[0].geometry.centroid.x
        lat_center = selected_shape.iloc[0].geometry.centroid.y
        input_weather = get_tmy_as_input_weather_for_gsee_pv_cap(lat_center, lon_center)

    # ---------
    # calculate PV capacity per hour for each building in the month year, append to csv per building
    # maybe use one csv with buildings as columns, rows as hourly timestamps and values as PV capacity?
    if 'lat' not in buildings.columns or 'lon' not in buildings.columns:
        buildings["lat"] = buildings["geometry"].centroid.x
        buildings["lon"] = buildings["geometry"].centroid.y

    for building in buildings.index:
        lon, lat = buildings.loc[building, 'lon'], buildings.loc[building, 'lat']

        if building_specific_weather:
            input_weather = get_tmy_as_input_weather_for_gsee_pv_cap(lat, lon)
        # -----

        pv_capacity_result: pd.Series = gsee.pv.run_model(
            input_weather,
            coords=(lat, lon),  # Latitude and longitude
            tilt=30,  # 30 degrees tilt angle
            azim=180,  # facing towards the equator,
            tracking=0,  # fixed - no tracking
            capacity=1.0,  # 1 W
            system_loss=0.1,  # 10% loss
        )

        if building_specific_weather:
            del input_weather

        # write result to csv file
        temp_csv_output_path = os.path.join(TEMP_PATH, run_id,
                                            f"building_{buildings.loc[building, 'bid']}_pv_capacity_tmy_weather.csv")
        os.makedirs(acept_utils.uppath(temp_csv_output_path, 1), exist_ok=True)
        write_geopandas_to_uhp_csv(temp_csv_output_path, pv_capacity_result, first_row_header=['PV Capacity Factor'],
                                   second_row_info=[f"bid_{buildings.loc[building, 'bid']}"], sep=";")

    # restore original crs for buildings
    buildings.to_crs(saved_crs, inplace=True)
    if debug:
        print("buildings.crs restored:", buildings.crs)
    return acept_utils.uppath(temp_csv_output_path, 1)


def get_tmy_as_input_weather_for_gsee_pv_cap(lat: float, lon: float) -> pd.DataFrame:
    """
    Build weather profile for a typical meteorological year (TMY) from the PVGIS API using the maximal time period
    of 2005 - 2020 (see PVGIS_MIN_YEAR and PVGIS_MAX_YEAR).

    :param lat: latitude of the location as a float.
    :param lon: longitude of the location as a float.
    :return: A pandas DataFrame with the weather profile.
    """
    weather_df, _ = build_weather_profile_for_typical_meteorological_year(lat, lon)
    # set uniform year to 2020
    weather_df.index = weather_df.index.map(lambda t: t.replace(year=2020))

    return calculate_gsee_input_weather_from_raw_weather(weather_df)
