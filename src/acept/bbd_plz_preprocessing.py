"""
Module for the BBD shapefiles to PLZ mapping

Use this module to:
    - read building data from BBD shapefiles (.shp) and calculate missing fields
    - build the mapping of the BBD shapefiles to post codes (PLZ)
    - lookup post codes (PLZ) in the mapping
    - query the BBD for the GeoDataFrame containing all buildings with the selected post code (PLZ)
    - save the BBD query result to a shape file in the /temp directory :py:const:`acept.acept_constants.TEMP_PATH`

Note:
    The BBD shapefiles are read from the :py:const:`acept.acept_constants.BBD_ROOT_DIR` directory. The modified BBD
    shapefiles are saved in the :py:const:`acept.acept_constants.BBD_WITH_PLZ_ROOT_PATH` directory.
"""

import glob
import json
import os
import re
from typing import Tuple

import geopandas as gpd
import pandas as pd

from acept import acept_utils
from acept import plz_shape
from acept.acept_constants import TEMP_PATH, BBD_ROOT_DIR, PLZ_MAPPING_JSON_DIR, BBD_WITH_PLZ_ROOT_PATH
from acept.buildings_information import calculate_missing_uhp_building_fields
from acept.uhp_input_formatting import map_building_use_types_to_numbers


# ---------
def derive_bbd_output_path_from_filepath_shp(output_base: str, filename: str) -> str:
    """
    Derives output file path for modified shape file (.shp) from input file path

    :param output_base: base directory path for modified shape files
    :param filename: path of input shape file
    :return: output path of modified shape file
    """
    return acept_utils.derive_output_path_from_filepath(output_base, filename, file_extension=".shp",
                                                        mod_filename_suffix="_mod", up=3)


def read_building_data_from_shp(parent_dir: str, filename_buildings: str, debug: bool = True) -> Tuple[
        str, gpd.GeoDataFrame]:
    """
    Reads shapefile and calculates missing fields (bid, lat, lon, plz)

    Returns the modified shapefile and GeoDataFrame with missing fields added

    :param parent_dir: Path to the parent directory of the shapefile
    :param filename_buildings: Filename of the shapefile containing the buildings
    :param debug: Whether to print debug messages. Default is ``True``.
    :return: Path to the (modified) shapefile and (modified) GeoDataFrame containing the buildings
    """

    filename = os.sep.join([parent_dir, filename_buildings])

    if debug:
        print('\nBuilding data (shp)')
        print('  ' + filename)

    # read the shapefile
    buildings = gpd.read_file(filename)

    buildings, flag_modified = calculate_missing_uhp_building_fields(buildings, debug)

    # calculate the plz of buildings
    if "plz" not in buildings.columns:
        buildings = calculate_plz(buildings, debug)
        flag_modified = True
        if debug:
            print('      ' + "'plz' field added")

    # save shapefile with new fields
    if flag_modified:
        filename_new = derive_bbd_output_path_from_filepath_shp(BBD_WITH_PLZ_ROOT_PATH, filename)
        # recursively create output directory
        os.makedirs(acept_utils.uppath(filename_new, 1), exist_ok=True)
        buildings.to_file(filename_new)
        if debug:
            print('  ' + "Shapefile with modifications saved as")
            print('    ' + filename_new)
        return filename_new, buildings  # .drop(columns = ['geometry'])
    return filename, buildings  # .drop(columns = ['geometry'])


def calculate_plz(buildings: gpd.GeoDataFrame, debug: bool = True) -> gpd.GeoDataFrame:
    """
    Reads the PLZ shapefile and adds missing field (plz) to the buildings GeoDataFrame.

    :param buildings: GeoDataFrame containing buildings.
    :param debug: Whether to print debug messages. Default is ``True``.
    :return: Path to the (modified) shapefile and (modified) GeoDataFrame containing the buildings.
    """

    if debug:
        print('\nPLZ data (shp)')

    # read shapefile
    plz_gdf = plz_shape.read_plz_shapefile()

    # cannot not use predicate = 'within' because buildings with multiple PLZ in intersect have PLZ nan then
    buildings_mod = buildings.to_crs(epsg=4326, inplace=False).sjoin(plz_gdf, how='left', predicate='intersects')

    columns_to_drop = ['index_right', 'note', 'einwohner', 'qkm']
    return buildings_mod.drop(columns=columns_to_drop)


def calculate_plz_from_centroid(buildings: gpd.GeoDataFrame, debug: bool = True) -> gpd.GeoDataFrame:
    """
    Reads the PLZ shapefile and adds missing field (plz) to the buildings GeoDataFrame based on each building's
    centroid.

    :param buildings: GeoDataFrame containing buildings.
    :param debug: Whether to print debug messages. Default is ``True``.
    :return: Path to the (modified) shapefile and (modified) GeoDataFrame containing the buildings.
    """

    if debug:
        print('\nPLZ data (shp)')

    # read shapefile
    plz_gdf = plz_shape.read_plz_shapefile()

    # temporarily set centroid as geometry
    buildings["centroid"] = buildings.geometry.centroid
    buildings["polygeom"] = buildings.geometry
    buildings = buildings.set_geometry("centroid")
    buildings = buildings.set_geometry("polygeom")

    buildings_mod = buildings.to_crs(epsg=4326, inplace=False).sjoin(plz_gdf, how='left')  # , predicate = 'within')

    buildings.set_geometry("polygeom", inplace=True)

    columns_to_drop = ['index_right', 'note', 'einwohner', 'qkm']
    return buildings_mod.drop(columns=columns_to_drop)


# ---------
# ## Build PLZ mapping json database

def build_plz_munc_id_db(debug: bool = True):
    """
    Builds the mapping of the BBD shapefiles to post codes (PLZ) as a json file and updates the shapefiles with missing
    information. Calculates for all building shapefiles below the BBD root directory missing fields and saves the
    modified shapefiles.

    .. note::
        The BBD shapefiles are read from the :py:const:`acept.acept_constants.BBD_ROOT_DIR` directory. The modified BBD
        shapefiles are saved in the :py:const:`acept.acept_constants.BBD_WITH_PLZ_ROOT_PATH` directory.

    :param debug: Whether to print debug messages. Default is ``True``.
    """
    if debug:
        print("Building the mapping of the BBD shapefiles to post codes (PLZ)...")

    plz_to_munc = {}  # {plz mapping to list of munc_ids} # maybe also the other way around

    for shapefile_path in glob.iglob(BBD_ROOT_DIR + '**' + os.sep + '*.shp', recursive=True):
        if shapefile_path.endswith("_mod.shp"):
            continue
        shapefile_name = os.path.basename(shapefile_path)[:-4]
        parent_dir = os.path.relpath(os.path.dirname(shapefile_path))
        shapefile_path_new, buildings_df = read_building_data_from_shp(parent_dir, shapefile_name + ".shp", debug=debug)
        plz_list = buildings_df['plz'].unique().tolist()

        # maybe add 0 as is in definition of AGS
        # munc_id = "0" + re.sub(r'[^0-9]', '', shapefile_name)
        munc_id = re.sub(r'[^0-9]', '', shapefile_name)

        for p in plz_list:
            # save the mapping
            if p not in plz_to_munc:
                plz_to_munc[p] = {}
            plz_to_munc[p].setdefault("munc_id", set()).add(munc_id)
            plz_to_munc[p].setdefault("files", set()).add(os.path.relpath(shapefile_path_new))

    # check if there is a PLZ with multiple munc_id and convert sets to JSON friendly lists
    for p in plz_to_munc:
        # convert sets to lists
        plz_to_munc[p]["munc_id"] = list(plz_to_munc[p]["munc_id"])
        plz_to_munc[p]["files"] = list(plz_to_munc[p]["files"])

        if len(plz_to_munc[p]["munc_id"]) > 1:
            if debug:
                print(p, plz_to_munc[p]["munc_id"])

        if len(plz_to_munc[p]["files"]) > 2:
            if debug:
                print(p, plz_to_munc[p]["files"])

    with open(PLZ_MAPPING_JSON_DIR, 'w') as f:
        json.dump(plz_to_munc, f)

    print("finished building plz db")


VALID_BUILDING_USES = ['All', 'Residential', 'Industrial', 'Commercial', 'Public', 'Non-Residential']
"""Valid use types for buildings. 'All' selects all use types. Possible: 'All', 'Residential', 'Industrial', 
'Commercial', 'Public', 'Non-Residential'"""
NON_RES_BUILDING_USES = ['Industrial', 'Commercial', 'Public']  # numerical in range(0,3) or < 3
"""Use types for non-residential buildings. Possible: 'Industrial', 'Commercial', 'Public'"""


def lookup_plz_in_mapping(plz: str | int) -> dict | None:
    """
    Make the lookup of the given PLZ in the saved mapping of PLZ -> paths to shape files.
    If there is no mapping to the PLZ None is returned.

    :param plz: PLZ to search.
    :return: Dictionary with information on the shape files with all buildings in of the PLZ.
        If there is no mapping to the PLZ None is returned.
    """
    if not os.path.isfile(PLZ_MAPPING_JSON_DIR):
        return None
    with open(PLZ_MAPPING_JSON_DIR, 'r') as f:
        plz_lookup: dict = json.load(f)
    lookup_res_dict = plz_lookup.get(str(plz))
    return lookup_res_dict


def query_bbd_for_plz(plz: str, building_use: str = "All", debug: bool = True) -> gpd.GeoDataFrame:
    """
     Query the BBD for the GeoDataFrame containing all buildings with the selected post code (PLZ) and use type.
     Builds the mapping if is not yet there.

    :param plz: PLZ to search.
    :param building_use: Use type of the buildings, default: 'All' selects all use types. Possible: 'All',
        'Residential', 'Industrial', 'Commercial', 'Public', 'Non-Residential'.
    :param debug: default=True, give debug messages.
    :raise ValueError: if there is no data for the PLZ in the BBD
    :return: GeoDataFrame with the buildings with the selected post code (PLZ).
    """

    if not os.path.isfile(PLZ_MAPPING_JSON_DIR):
        if debug:
            print("The BBD PLZ mapping database does no exist. Building the mapping now ....")
        build_plz_munc_id_db(debug)

    lookup_res_dict = lookup_plz_in_mapping(plz)
    if lookup_res_dict is None:
        if debug:
            print("There is no data for PLZ:", plz)
            print("Building the mapping for all data again ....")
        build_plz_munc_id_db(debug)
        lookup_res_dict = lookup_plz_in_mapping(plz)
        if lookup_res_dict is None:
            print("There is no data for PLZ:", plz)
            raise ValueError("PLZ Error: There is no data in the BBD for PLZ:", plz)

    if debug:
        print(f"BBD query for plz: {plz}, use: {building_use}")
        print('  buildings with plz in shape files: ' + str(lookup_res_dict["files"]))

    res_gdf_list = []
    for fp in lookup_res_dict["files"]:
        # read file to gdf
        buildings = gpd.read_file(acept_utils.absolute_path_from_relative(fp))
        if building_use == "All" or building_use not in VALID_BUILDING_USES:
            # default case
            buildings = buildings.loc[buildings["plz"] == plz]
        elif building_use == 'Non-Residential':
            buildings = buildings.loc[(buildings["plz"] == plz) & (buildings["use"].isin(NON_RES_BUILDING_USES))]
        else:
            buildings = buildings.loc[(buildings["plz"] == plz) & (buildings["use"] == building_use)]
        res_gdf_list.append(buildings)
    res_gdf: gpd.GeoDataFrame = pd.concat(res_gdf_list)
    if debug:
        print('  queried buildings combined')
    return res_gdf


# MAYBE use factory pattern: https://dagster.io/blog/python-factory-patterns
def save_query_result_to_temp_shp(plz: str, result_gdf: gpd.GeoDataFrame, building_use: str = "All",
                                  debug: bool = True) -> str:
    """
    Save the BBD query result to a shape file in the /temp directory.

    :param plz: PLZ to search.
    :param building_use: Use type of the buildings, default: 'All' selects all use types. Possible: 'All',
        'Residential', 'Industrial', 'Commercial', 'Public', 'Non-Residential'.
    :param result_gdf: GeoDataFrame with all buildings with PLZ and buildings use.
    :param debug: default=True, give debug messages.
    :return: File path to the BBD query result.
    """
    # save result to file
    if building_use == "All":
        combined_filepath = os.path.join(TEMP_PATH, f"PLZ_{plz}", f"{plz}.shp")
    else:
        combined_filepath = os.path.join(TEMP_PATH, f"PLZ_{plz}", f"{plz}_{building_use}.shp")
    # recursively create output directory
    os.makedirs(acept_utils.uppath(combined_filepath, 1), exist_ok=True)
    result_gdf.to_file(combined_filepath)
    if debug:
        print('  query BBD result saved at: ' + combined_filepath)
    return combined_filepath


def compute_buildings_for_plz_shp(plz: str | int, building_use: str = "All", debug: bool = True) -> str:
    """
    Query the BBD for all buildings with the selected post code (PLZ) and use type and save result to a shape file
    in the /temp directory.

    :param plz: PLZ to search.
    :param building_use: Use type of the buildings, default: 'All' selects all use types. Possible: 'All',
        'Residential', 'Industrial', 'Commercial', 'Public', 'Non-Residential'.
    :param debug: default=True, give debug messages.
    :return: Path to combined file of all buildings with PLZ and building use.
    """
    res_gdf = query_bbd_for_plz(str(plz), building_use, debug)
    return save_query_result_to_temp_shp(str(plz), res_gdf, building_use, debug)


def compute_buildings_for_plz_to_uhp_csv(plz: str | int, building_use: str = "All", debug: bool = True) -> str:
    """
    Query the BBD for all buildings with the selected post code (PLZ) and use type and save result to a .csv file
    in the format used by UrbanHeatPro in the /temp directory.

    :param plz: PLZ to search.
    :param building_use: Use type of the buildings, default: 'All' selects all use types. Possible: 'All',
        'Residential', 'Industrial', 'Commercial', 'Public', 'Non-Residential'.
    :param debug: default=True, give debug messages.
    :return: Path to combined file of all buildings with PLZ and building use
    """
    from acept.uhp_csv_io import save_buildings_to_temp_uhp_csv

    res_gdf = query_bbd_for_plz(str(plz), building_use, debug)
    res_gdf = map_building_use_types_to_numbers(res_gdf)
    return save_buildings_to_temp_uhp_csv(str(plz), res_gdf, building_use, debug)
