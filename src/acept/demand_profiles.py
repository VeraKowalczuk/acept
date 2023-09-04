"""Module for building demand profiles.

Use this module to create demand profiles for the selected area and buildings using UrbanHeatPro.

This module is the interface to the UrbanHeatPro project (https://github.com/VeraKowalczuk/UrbanHeatPro) that is a
dependency for the ACEPT project and is integrated to the ACEPT project as a submodule in /deps/UrbanHeatPro.

"""
import glob
import os

import geopandas as gpd
import pandas as pd

import UrbanHeatPro
from acept.acept_constants import UHP_PATH, TEMP_PATH, UHP_SETTINGS_PATH
from acept.acept_utils import copy_file_or_directory_recursively, rename_files_in_directory, \
    delete_files_or_directory_recursively_with_pattern, combine_csv_profiles_with_pattern, \
    get_bid_from_uhp_building_specific_files
from acept.buildings_information import calculate_shape_around_buildings
from acept.temperature_profiles import build_temperature_profile_for_tmy_for_shape
from acept.uhp_csv_io import prepare_buildings_for_uhp_csv, read_uhp_csv_to_dataframe


def run_uhp_for_selected_buildings_year(plz_or_region: int | str, buildings: gpd.GeoDataFrame = None,
                                        year: int | None = 2011, temperature_profile: str = None,
                                        demand_unit: str = 'W') -> dict[
    str, str | pd.DataFrame]:
    """
    Creates demand profiles for the selected area and buildings using UrbanHeatPro.

    :param plz_or_region: PLZ or Region for which the demand profile should be created (area ID).
    :param buildings: GeoDataFrame of the selected buildings.
    :param year: Year for which the demand profile should be created. Defaults to 2011. If None, the temperature profile
        for the typical meterological year (TMY) will be used.
    :param temperature_profile: Path to the temperature profile. If None, the temperature profile is expected at the
        default location according to the year and plz_or_region.
    :param demand_unit: Unit of the demand. Defaults to 'W'. Valid values are 'W', 'Wh', 'kW', 'kWh', 'MW', and 'MWh'.
        As the timeseries have hourly resolution, the values of 'W' and 'Wh' are equivalent.
    :return: A dictionary containing the paths to the demand profiles and the dataframes containing the profiles.
    """
    if demand_unit not in ['W', 'Wh', 'kW', 'kWh', 'MW', 'MWh']:
        raise ValueError("Invalid demand_unit. Valid values are 'W', 'Wh', 'kW', 'kWh', 'MW', and 'MWh'.")
    plz_or_region = str(plz_or_region)

    print("Selected region: ", plz_or_region, "for UrbanHeatPro")
    print("Setting up the input data for UrbanHeatPro")

    buildings_csv = prepare_buildings_for_uhp_csv(plz_or_region, buildings, debug=True)

    if temperature_profile is None:
        if year is None:
            selected_shape = calculate_shape_around_buildings(buildings)
            temperature_profile = build_temperature_profile_for_tmy_for_shape(plz_or_region, selected_shape, debug=True)
        else:
            temperature_profile = os.path.join(TEMP_PATH, f"PLZ_{plz_or_region}", f"DWD_TRY_{plz_or_region}_{year}.csv")

    path_mapping = {
        # UHP/input/Regional Data/DE -> UHP/input/Regional Data/{plz}
        os.path.join(UHP_PATH, "input", "Regional Data", "DE"):
            os.path.join(UHP_PATH, "input", "Regional Data", plz_or_region),
        # /temp/buildingsXYZ.csv -> /input/Buildings/buildings_{plz}.csv
        buildings_csv:
            os.path.join(UHP_PATH, "input", "Buildings", f"buildings_{plz_or_region}.csv"),
        # /temperature profile -> UHP/input/Regional Data/{plz}/Tamb_{plz}.csv
        temperature_profile:
            os.path.join(UHP_PATH, "input", "Regional Data", plz_or_region, f"Tamb_{plz_or_region}.csv")
    }
    for src, dest in path_mapping.items():
        copy_file_or_directory_recursively(src, dest)
    rename_files_in_directory(os.path.join(UHP_PATH, "input", "Regional Data", plz_or_region), "_DE",
                              f"_{plz_or_region}")

    uhp_result_dir = os.path.join(UHP_PATH, "results")

    UrbanHeatPro.run_uhp(plz_or_region, settings_file=UHP_SETTINGS_PATH, result_dir=uhp_result_dir)

    # clean up after session
    # remove input files
    print("\nCleaning up input files for UrbanHeatPro")
    delete_files_or_directory_recursively_with_pattern(os.path.join(UHP_PATH, "input", "**"), f"*{plz_or_region}*")

    # get latest uhp result directory for the selected plz/region
    uhp_result_dirs_list = [os.path.join(uhp_result_dir, d) for d in os.listdir(uhp_result_dir) if
                            os.path.isdir(os.path.join(uhp_result_dir, d)) and f"{plz_or_region}_" in d]
    latest_result_dir = max(uhp_result_dirs_list, key=os.path.getmtime)

    # Extract space heating and water heating demand from results
    pattern = os.path.join("**", "Buildings", "HeatDemand_*.csv")
    csv_space_heating = os.path.join(TEMP_PATH, f"PLZ_{plz_or_region}", f"space_heat_{plz_or_region}.csv")
    header = sorted(buildings["bid"].to_list())
    header = [f"bid_{x}" for x in header]
    space_heating_df = combine_csv_profiles_with_pattern(latest_result_dir, pattern, csv_space_heating, header,
                                                         get_bid_from_uhp_building_specific_files, skip_rows=0,
                                                         column_name="SpaceHeatingD_W")
    csv_water_heating = os.path.join(TEMP_PATH, f"PLZ_{plz_or_region}", f"water_heat_{plz_or_region}.csv")
    water_heating_df = combine_csv_profiles_with_pattern(latest_result_dir, pattern, csv_water_heating, header,
                                                         get_bid_from_uhp_building_specific_files, skip_rows=0,
                                                         column_name="HotWaterD_W")

    # retrieve updated buildings file from the UHP run
    csv_updated_buildings_file_list = glob.glob(os.path.join(latest_result_dir, "**",
                                                             f"SynCity_{plz_or_region}_*.csv"))
    if len(csv_updated_buildings_file_list) > 0:
        csv_updated_buildings_file_list.sort()
        csv_updated_buildings_file = csv_updated_buildings_file_list[-1]
    else:
        # if no SynCity csv file was generated, use the original buildings csv
        csv_updated_buildings_file = buildings_csv

    # read and copy updated buildings file for the return value
    updated_buildings_df, _ = read_uhp_csv_to_dataframe(csv_updated_buildings_file, header_row=1, ignore_index=True,
                                                        additional_info=0, sep=";")
    csv_updated_buildings_out = os.path.join(TEMP_PATH, f"PLZ_{plz_or_region}",
                                             f"updated_buildings_{plz_or_region}.csv")
    copy_file_or_directory_recursively(csv_updated_buildings_file, csv_updated_buildings_out)

    # convert from W (UHP output) to the desired unit
    if demand_unit in ["kW", "kWh"]:
        space_heating_df /= 1000
        water_heating_df /= 1000
    elif demand_unit in ["MW", "MWh"]:
        space_heating_df /= 1000000
        water_heating_df /= 1000000

    # replace NaN with 0 and save to csv again
    space_heating_df.fillna(0, inplace=True)
    space_heating_df.to_csv(csv_space_heating, index=False)
    water_heating_df.fillna(0, inplace=True)
    water_heating_df.to_csv(csv_water_heating, index=False)

    # clear uhp_result_dir, all results
    delete_files_or_directory_recursively_with_pattern(uhp_result_dir, "*")

    # clean up temporary files
    if temperature_profile.startswith(os.path.join(TEMP_PATH, f"PLZ_{plz_or_region}")):
        delete_files_or_directory_recursively_with_pattern(os.path.join(TEMP_PATH, f"PLZ_{plz_or_region}"),
                                                           os.path.basename(temperature_profile))
    if buildings_csv.startswith(os.path.join(TEMP_PATH, f"PLZ_{plz_or_region}")):
        delete_files_or_directory_recursively_with_pattern(os.path.join(TEMP_PATH, f"PLZ_{plz_or_region}"),
                                                           os.path.basename(buildings_csv))

    return {"space_heating_df": space_heating_df, "csv_space_heating": csv_space_heating,
            "water_heating_df": water_heating_df, "csv_water_heating": csv_water_heating,
            "updated_buildings_df": updated_buildings_df, "buildings_csv": csv_updated_buildings_out}
