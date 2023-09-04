"""Module for writing and reading .csv files for Urban Heat Pro (UHP).

UHP expects .csv files in one of the following two formats:

.. code-block:: text

    information;on;the;file;content;...
    column1;column2;column3;column4;column5;...
    value1;value2;value3;value4;value5;...
    ...

.. code-block:: text

    column1;column2;column3;column4;column5;...
    unit1;unit2;unit3;unit4;unit5;...
    value1;value2;value3;value4;value5;...
    ...

Use this module to:
    - Write a DataFrame to a .csv file in the UHP format.
    - Read a .csv file in the UHP format and return a DataFrame.
    - Prepare the input .csv file with the buildings for UHP from a GeoDataFrame.
    - Save a GeoDataFrame with the buildings or a BBD query result to a .csv file in the format expected by UHP.

For buildings the format of the .csv file is:

.. code-block:: text

    field1;field2;field3;field4;field5;...
    value1;value2;value3;value4;value5;...
    ...

Buildings have the following required columns:
    - bid: ID of the building
    - area: The size of the area in m2
    - use: Use type of the building as a number from 0 to 3
    - free_walls: Number of free walls of the building
    - lat: Latitude in degrees
    - lon: Longitude in degrees
    - dist2hp: Distance to the heat pump in m
These additional columns are optional:
    - year_class: TABULAR construction year class of the building as a number
    - size_class: TABULAR size class of the building as a number
    - floors: Number of floors
    - occupants: Number of occupants
    - dwellings: Number of dwellings
    - ref_level_roof: Refurbishment level of the roof
    - ref_level_wall: Refurbishment level of the walls
    - ref_level_floor: Refurbishment level of the floors
    - ref_level_window: Refurbishment level of the windows
The refurbishment level is a number from 1 to 3:
    - 1 = National minimum requirement
    - 2 = Improved standard
    - 3 = Ambitious standard

"""

import os
from typing import Any

import geopandas as gpd
import pandas as pd
from pandas import DataFrame

from acept import acept_utils
from acept.acept_constants import TEMP_PATH
from acept.buildings_information import calculate_missing_uhp_building_fields
from acept.uhp_input_formatting import map_building_use_types_to_numbers, map_building_types_to_numeric_size_class, \
    map_construction_year_to_tabular_construction_year_class, map_tabular_construction_year_class_to_numbers, \
    map_refurbishment_levels_to_uhp_format


def write_geopandas_to_uhp_csv(filepath: str, values_df: pd.DataFrame, first_row_header: list,
                               second_row_info: list = [], sep: str = ";") -> str:
    """ Writes a DataFrame to a .csv file in the format expected by UHP.

    Writes a .csv file to the given path with a header row, an optional second row with additional information on the
    data (e.g. units), followed by the data.

    :param filepath: Path where to save the .csv file.
    :param values_df: DataFrame to save. The column names in the DataFrame are not written to the file.
        The order of the columns has to be the same as in the header rows.
    :param first_row_header: List of column names to be written to the first line of the file.
    :param second_row_info: Optional list of information for each column written to the second line of the file.
    :param sep: Column seperator in the .csv file. Default: ';'.
    :return: Path to the saved file.
    """
    os.makedirs(acept_utils.uppath(filepath, 1), exist_ok=True)
    # header (and optional unit info)
    if not second_row_info:
        # list is empty
        column_info_df = pd.DataFrame([], columns=first_row_header)
    else:
        # list is not empty
        column_info_df = pd.DataFrame([second_row_info], columns=first_row_header)

    column_info_df.to_csv(filepath, mode='w', sep=sep, index=False, columns=first_row_header, header=True)
    values_df.to_csv(filepath, mode='a', sep=sep, index=False, header=False)
    return filepath


def read_uhp_csv_to_dataframe(filepath: str, header_row: int | tuple[int, list] = 0, ignore_index: bool = True,
                              additional_info: int | None = -1, sep: str = ";") -> tuple[DataFrame, list[Any]]:
    """Reads a .csv file in the format expected by UHP.

    Reads a .csv file with a header row, an optional second row with additional information on the data (e.g. units),
    and returns a DataFrame with the data and a list of additional information if requested.
    The column names are optionally renamed.

    :param filepath: Path to the .csv file.
    :param header_row: Row number of the header row, or a tuple with the row number and a list of new column names.
        Default: 0.
    :param ignore_index: If True, the index is ignored. Default: True
    :param additional_info: Optional Integer indicating the row number of the row with additional information.
        If negative, the additional information is ignored. If None, no additional information exists. Default: -1.
    :param sep: Column seperator in the .csv file. Default: ';'.
    :raises ValueError: If header_row is not an int or a tuple of the form (int, list)
    :return: DataFrame with the data, and a list of additional information if requested.
    """
    if type(header_row) is int:
        df = pd.read_csv(filepath, sep=sep, header=header_row,
                         skiprows=[abs(additional_info)] if additional_info is not None else None,
                         index_col=False if ignore_index else None)
    elif type(header_row) is tuple and type(header_row[0]) is int and type(header_row[1]) is list:
        df = pd.read_csv(filepath, sep=sep,
                         skiprows=[header_row[0], abs(additional_info)] if additional_info is not None else [
                             header_row[0]],
                         names=header_row[1],
                         index_col=False if ignore_index else None)
    else:
        raise ValueError("header_row must be an int or a tuple of (int, list) is: " + str(type(header_row)))
    if additional_info < 0:
        additional_info_val = []
    else:
        additional_info_val = pd.read_csv(filepath, sep=sep, header=additional_info,
                                          index_col=False if ignore_index else None).columns.to_list()
    return df, additional_info_val


def prepare_buildings_for_uhp_csv(area_id: str | int, buildings: gpd.GeoDataFrame, debug: bool = True) -> str:
    """Prepare buildings GeoDataFrame as input CSV for UrbanHeatPro.

    Add missing fields and map the values to the UHP format.
    Writes the result to a .csv file in the format used by UrbanHeatPro in the respective /temp directory.

    :param area_id: The area ID e.g. PLZ.
    :param buildings: The GeoDataFrame of buildings.
    :param debug: Whether to enable debug mode and print debug messages. Default: True.
    :raises ValueError: If the required column names are not in the buildings GeoDataFrame
    :return: The path to the saved UHP CSV file.
    """
    buildings, _ = calculate_missing_uhp_building_fields(buildings, debug)
    column_names = ['bid', 'area', 'use', 'free_walls', 'lat', 'lon', 'dist2hp']
    if not set(column_names).issubset(buildings.columns.to_list()):
        raise ValueError("Something is wrong with the input buildings. The required column names are not in "
                         "buildings.columns")

    # add optional fields and map the values to the UHP format
    map_building_use_types_to_numbers(buildings)
    map_building_types_to_numeric_size_class(buildings)
    map_construction_year_to_tabular_construction_year_class(buildings)
    map_tabular_construction_year_class_to_numbers(buildings)
    map_refurbishment_levels_to_uhp_format(buildings)

    return save_buildings_to_temp_uhp_csv(str(area_id), buildings, "All", debug)


def save_buildings_to_temp_uhp_csv(plz_or_area_id: str, result_gdf: gpd.GeoDataFrame, building_use: str = "All",
                                   debug: bool = True) -> str:
    """
    Save the buildings or a BBD query result to a .csv file in the format used by UrbanHeatPro in the /temp directory.

    :param plz_or_area_id: The queried PLZ or the ID of the area the buildings belong to.
    :param building_use: Use type of the buildings in the BBD query, default: 'All' selects all use types. Possible: 'All',
        'Residential', 'Industrial', 'Commercial', 'Public', 'Non-Residential'.
    :param result_gdf: GeoDataFrame with all buildings in result_gdf.
    :param debug: Whether to enable debug mode and print debug messages. Default: True.
    :raises ValueError: if the required column names are not in the result_gdf
    :return: File path to the CSV file with the buildings.
    """
    # save result to file
    if building_use == "All":
        combined_filepath = os.path.join(TEMP_PATH, f"PLZ_{plz_or_area_id}", f"buildings_{plz_or_area_id}.csv")
    else:
        combined_filepath = os.path.join(TEMP_PATH, f"PLZ_{plz_or_area_id}",
                                         f"buildings_{plz_or_area_id}_{building_use}.csv")
    # recursively create output directory
    os.makedirs(acept_utils.uppath(combined_filepath, 1), exist_ok=True)
    # header of the csv file
    column_names = ['bid', 'area', 'use', 'free_walls', 'lat', 'lon', 'dist2hp', 'year_class', 'size_class', 'floors',
                    'dwellings', 'occupants', 'ref_level_roof', 'ref_level_wall', 'ref_level_floor', 'ref_level_window']
    # note: all column names are lowercase in the (PLZ) modified BBD
    print(result_gdf.columns.to_list())
    if not set(column_names[0:7]).issubset(result_gdf.columns.to_list()):
        raise ValueError("Something is wrong with the input result_gdf. The required column names are not in "
                         "result_gdf.columns")
    body_df = result_gdf[column_names]
    write_geopandas_to_uhp_csv(combined_filepath, body_df, column_names)
    if debug:
        print('  buildings or query BBD result as UHP input .csv file saved at: ' + combined_filepath)
    return combined_filepath
