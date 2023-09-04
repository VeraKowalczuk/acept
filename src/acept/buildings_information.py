"""Module for adding and calculating information about the buildings in a GeoDataFrame.

Use this module to add fields to a GeoDataFrame containing the buildings or calculating the shape around the buildings.

The following fields are calculated and added to the GeoDataFrame:
    - bid: consecutive building number as ID
    - area: polygon area in m2
    - free_walls: free walls of the building, max: 4 walls
    - lat: latitude of the centroid in degrees
    - lon: longitude of the centroid in degrees
    - dist2hp: distance to the heat plant or a heat source in meters
    - construction: the class of the year of construction based on the Zensus data
    - year_class: the class of the year of construction based on the Zensus data as a numerical value
    - building_type: the typology of the building based on the Zensus data
    - size_class: the typology of the building based on the Zensus data as a numerical value
    - floors: the number of floors in the building
    - occupants: the number of occupants in the building
    - dwellings: the number of dwellings in the building
    - refurb_level_roof: the level of refurbishment of the roof (0, 1, or 2)
    - refurb_level_wall: the level of refurbishment of the walls (0, 1, or 2)
    - refurb_level_floor: the level of refurbishment of the floor (0, 1, or 2)
    - refurb_level_window: the level of refurbishment of the windows (0, 1, or 2)

If the input GeoDataFrame already contains these fields, they will not be added them again.
If there are fields with similar names as the calculated ones, the existing fields will be renamed to the expected
names. If values are then still missing, they are calculated where possible.

"""

import geopandas as gpd
import pandas as pd
from shapely import convex_hull
from shapely.ops import unary_union


def calculate_missing_uhp_building_fields(buildings: gpd.GeoDataFrame, debug: bool = True) -> tuple[
        gpd.GeoDataFrame, bool]:
    """
    Calculates missing fields that are input to UrbanHeatPro.

    These are: bid, area, free_walls, lat, lon, dist2hp, construction, year_class, building_type, size_class, floors,
    occupants, dwellings, and the refurbishment levels.

    :param buildings: GeoDataFrame containing the buildings
    :param debug: Prints debug messages if True (default).
    :return: GeoDataFrame containing the buildings with missing fields added, and a flag indicating if any fields were
        added.
    """
    # project to epsg: 32632 (Germany) so that area is in m2 (MAYBE set to 4326
    # 32632 is a UTM-projection, that uses meter as unit, and 4326 uses degree.
    buildings.to_crs(epsg=32632, inplace=True)
    if debug:
        print("Shape:", buildings.shape)

    # convert all column names to lowercase
    lowercase_columns = [str(x).lower() for x in buildings.columns]
    flag_modified = lowercase_columns != buildings.columns.to_list()
    buildings.columns = lowercase_columns

    # calculate building id
    if "bid" not in buildings.columns:
        calculate_bid(buildings)
        flag_modified = True
        if debug:
            print('      ' + "'bid' field added")

    # calculate building area
    if "area" not in buildings.columns:
        calculate_areas(buildings)
        flag_modified = True
        if debug:
            print('      ' + "'area' field added")

    # calculate free walls
    if "free_walls" not in buildings.columns:
        calculate_free_walls(buildings)
        flag_modified = True
        if debug:
            print('      ' + "'free_walls' field added")

    # calculate latitude and longitude from building centroid
    if "lat" not in buildings.columns:
        calculate_lat_lon(buildings)
        flag_modified = True
        if debug:
            print('      ' + "'lat' and 'lon' fields added")

    # calculate distance to heat plant
    if 'dist2hp' not in buildings.columns:
        calculate_distance2hp(buildings, 0)
        flag_modified = True
        if debug:
            print('      ' + "'dist2hp' field added")

    # calculate construction year or renames it if there already exists a field named "constructi" or "year"
    if 'construction' not in buildings.columns:
        calculate_construction(buildings)
        flag_modified = True
        if debug:
            print('      ' + "'construction' field added")

    # calculate year class from construction year (constructi / construction / year)
    if 'year_class' not in buildings.columns:
        calculate_year_class_from_construction(buildings)
        flag_modified = True
        if debug:
            print('      ' + "'year_class' field added")

    # calculate building type
    if 'building_type' not in buildings.columns:
        calculate_building_type(buildings)
        flag_modified = True
        if debug:
            print('      ' + "'building_type' field added")

    # calculate size class from building type
    if 'size_class' not in buildings.columns:
        calculate_size_class(buildings)
        flag_modified = True
        if debug:
            print('      ' + "'size_class' field added")

    # initialize number of floors
    if 'floors' not in buildings.columns:
        initialize_floors(buildings)
        flag_modified = True
        if debug:
            print('      ' + "'floors' field added")

    # initialize number of occupants
    if 'occupants' not in buildings.columns:
        initialize_occupants(buildings)
        flag_modified = True
        if debug:
            print('      ' + "'occupants' field added")

    # initialize number of dwellings
    if 'dwellings' not in buildings.columns:
        initialize_dwellings(buildings)
        flag_modified = True
        if debug:
            print('      ' + "'dwellings' field added")

    # initialize the refurbishment level of the roof
    if 'ref_level_roof' not in buildings.columns:
        initialize_ref_level(buildings, "roof", default_value=None)
        flag_modified = True
        if debug:
            print('      ' + "'ref_level_roof' field added")

    # initialize the refurbishment level of the walls
    if 'ref_level_wall' not in buildings.columns:
        initialize_ref_level(buildings, "wall", default_value=None)
        flag_modified = True
        if debug:
            print('      ' + "'ref_level_wall' field added")

    # initialize the refurbishment level of the floors
    if 'ref_level_floor' not in buildings.columns:
        initialize_ref_level(buildings, "floor", default_value=None)
        flag_modified = True
        if debug:
            print('      ' + "'ref_level_floor' field added")

    # initialize the refurbishment level of the windows
    if 'ref_level_window' not in buildings.columns:
        initialize_ref_level(buildings, "window", default_value=None)
        flag_modified = True
        if debug:
            print('      ' + "'ref_level_window' field added")

    return buildings, flag_modified


def calculate_bid(buildings: gpd.GeoDataFrame):
    """
    Adds field "bid" with a consecutive building number as id to the buildings GeoDataFrame.

    :param buildings: GeoDataFrame containing buildings.
    """

    # add field "bid" with row numbers
    buildings['bid'] = buildings.reset_index().index


def calculate_areas(buildings: gpd.GeoDataFrame):
    """
    Adds field "area" with the polygon area in m2 to the buildings GeoDataFrame or reuses the field footprint_area if it
    exists.

    :param buildings: GeoDataFrame containing buildings.
    """
    if 'footprint_area' in buildings.columns:
        buildings['area'] = buildings['footprint_area'].where(buildings['footprint_area'] > 0, buildings.geometry.area)
    else:
        buildings['area'] = buildings.geometry.area


def calculate_free_walls(buildings: gpd.GeoDataFrame):
    """
    Adds field "free_walls" with the number of walls in direct contact with ambient temperature.

    It is assumed that all buildings have only four walls.

    :param buildings: GeoDataFrame containing buildings.
    """

    # add field "free walls"
    buildings['free_walls'] = 4

    # calculate free walls
    for iii in range(len(buildings)):
        intersected = buildings[buildings.geometry.intersects(buildings.iloc[iii].geometry.buffer(0.1))]
        if len(intersected) > 1:  # the analyzed building is taken as intersected
            free_walls = 4 - (len(intersected) - 1)
            buildings.loc[iii, 'free_walls'] = free_walls


def calculate_lat_lon(buildings: gpd.GeoDataFrame):
    """
    Adds field "lat" and "lot" with the latitude and longitude values of the building centroid in degrees.

    If the (user defined fields) 'user_lat' and 'user_lon' exist, they are used

    :param buildings: GeoDataFrame containing buildings.
    """

    # project buildings to have lat/lon in degrees
    proj_buildings = buildings.to_crs(epsg=4326, inplace=False)

    if 'user_lat' in buildings.columns and 'user_lon' in buildings.columns:
        buildings['lat'] = buildings['user_lat'].where(buildings['user_lat'].notna(), proj_buildings.centroid.y)
        buildings['lon'] = buildings['user_lon'].where(buildings['user_lon'].notna(), proj_buildings.centroid.x)
    else:
        # calculate centroids and extract lat = y and lon = x
        buildings['lat'] = proj_buildings.centroid.y
        buildings['lon'] = proj_buildings.centroid.x


def calculate_distance2hp(buildings: gpd.GeoDataFrame, default_value: int | float = 0,
                          path_to_heat_plant_file: str | None = None,
                          position_index_of_heat_plant: int = 0):
    """
    Adds field "dist2hp" with the distance between building and heat plant.

    This can be done via the location of the heat plant (see shapefile) or if there is a user-defined distance in the
    field "user_dist_to_heat_source", this is used. If no heat plant is given and the field "user_dist_to_heat_source"
    does not exist or is empty, the default value is used.
    The heat plant location is given in a shapefile.

    :param buildings: GeoDataFrame containing buildings.
    :param default_value: Default distance to be used if the heat plant file or the specified index in it does not exist.
        Default: 0.
    :param path_to_heat_plant_file: Path to the shapefile containing the heat plant. If None, the default value is used.
    :param position_index_of_heat_plant: Index of the heat plant in the shapefile. Default: 0
    """

    if path_to_heat_plant_file is None:
        if 'user_dist_to_heat_source' in buildings.columns:
            buildings['dist2hp'] = buildings["user_dist_to_heat_source"].fillna(default_value)
        else:
            buildings['dist2hp'] = default_value
        return

    # import shapefile with heat plant
    hp = gpd.read_file(path_to_heat_plant_file)
    hp.to_crs(epsg=32632, inplace=True)

    try:
        # chose heat plant by numeric index
        hp = hp.iloc[position_index_of_heat_plant].geometry
        # calculate distance of buildings centroid to heat plant and add field "dist2hp"
        buildings['dist2hp'] = buildings.centroid.distance(hp)
    except IndexError:
        buildings['dist2hp'] = default_value


def calculate_construction(buildings: gpd.GeoDataFrame):
    """
    Adds field "construction" with the construction year of the building or renames it if there already exists a field
    named "constructi" or "year.

    :param buildings: GeoDataFrame containing buildings.
    """

    if "constructi" in buildings.columns:
        buildings.rename(columns={"constructi": "construction"}, inplace=True)
    elif "year" in buildings.columns:
        buildings.rename(columns={"year": "construction"}, inplace=True)
    else:
        # create field "construction" if no construction year field exists
        buildings["construction"] = pd.Series(dtype="string")


def calculate_year_class_from_construction(buildings: gpd.GeoDataFrame):
    """
    Adds field "year_class" with the numerical year class of the construction year class. This is the classification
    used by the Zensus/BDB.

    :param buildings: GeoDataFrame containing buildings.
    """

    mapping = {"-1919": 0, "1919-1948": 1, "1949-1978": 2, "1979-1986": 3,
               "1987-1990": 4, "1991-1995": 5, "1996-2000": 6, "2001-2004": 7,
               "2005-2008": 8, "2009-": 9}

    buildings["year_class"] = buildings["construction"].map(mapping)


def calculate_building_type(buildings: gpd.GeoDataFrame):
    """
    Adds field "building_type" with the building type, or renames it if there already exists a field named "type",
    "btype" or "btype".

    :param buildings: GeoDataFrame containing buildings.
    """

    if "type" in buildings.columns:
        buildings.rename(columns={"type": "building_type"}, inplace=True)
    elif "building_t" in buildings.columns:
        buildings.rename(columns={"building_t": "building_type"}, inplace=True)
    elif "btype" in buildings.columns:
        buildings.rename(columns={"btype": "building_type"}, inplace=True)
    else:
        # create field "building_type" if no building type field exists
        buildings["building_type"] = pd.Series(dtype="string")


def calculate_size_class(buildings: gpd.GeoDataFrame):
    """
    Adds field "size_class" with the numerical size class corresponding to the building type. This classification
    is done independent of TABULAR classification (see EnvelopeArea_Residential.csv in UHP/input/Building Topology).
    Sets the building type to nan if no building type is given.

    :param buildings: GeoDataFrame containing buildings.
    """

    mapping = {'SFH': 0, 'TH': 1, 'MFH': 2, 'AB': 3}
    if "building_type" in buildings.columns:
        buildings["size_class"] = buildings["building_type"].map(mapping)
    else:
        buildings["size_class"] = pd.Series(dtype="int")


def initialize_floors(buildings: gpd.GeoDataFrame):
    """
    Adds the empty field "floor" with the number of floors in the building.

    :param buildings: GeoDataFrame containing buildings.
    """

    buildings["floor"] = pd.Series(dtype="int")


def initialize_occupants(buildings: gpd.GeoDataFrame):
    """
    Adds the empty field "occupants" with the number of occupants in the building.

    :param buildings: GeoDataFrame containing buildings.
    """

    buildings["occupants"] = pd.Series(dtype="int")


def initialize_dwellings(buildings: gpd.GeoDataFrame):
    """
    Adds the empty field "dwellings" with the number of dwellings in the building. If there is already a field named
    "houses_per_building" it is renamed to "dwellings".

    :param buildings: GeoDataFrame containing buildings.
    """

    if "houses_per_building" in buildings.columns:
        buildings.rename(columns={"houses_per_building": "dwellings"}, inplace=True)
    else:
        buildings["dwellings"] = pd.Series(dtype="int")


def initialize_ref_level(buildings: gpd.GeoDataFrame, feature_name: str, default_value: int | None = None):
    """
    Adds the field "ref_level_{feature_name}" with the reference level for the given feature.
    If there is already a field corresponding to the refurbishment level of the feature it is renamed to
    "ref_level_{feature_name}".

    :param buildings: GeoDataFrame containing buildings.
    :param feature_name: Name of the feature, must be 'roof', 'wall', 'window' or 'floor'.
    :param default_value: Value to use if there is no refurbishment level for the feature. Defaults to None.
    :raises ValueError: If feature_name is not 'roof', 'wall', 'window' or 'floor'.
    """

    if feature_name not in ["roof", "wall", "window", "floor"]:
        raise ValueError("feature_name must be 'roof', 'wall', 'window', or 'floor'")

    # the short name for the feature, i.e. "roof" -> "roo", for 'floor' -> 'bas' (as in the database)
    feature_name_short = feature_name[0:3].replace("flo", "bas")

    if f"ref_{feature_name}" in buildings.columns:
        buildings.rename(columns={f"ref_roof": f"ref_level_{feature_name}"}, inplace=True)
    elif f"refurb_{feature_name_short}" in buildings.columns:
        buildings.rename(columns={f"refurb_{feature_name_short}": f"ref_level_{feature_name}"}, inplace=True)
    else:
        buildings[f"ref_level_{feature_name}"] = pd.Series(dtype="int")

    if default_value is not None:
        buildings[f"ref_level_{feature_name}"] = default_value


def calculate_shape_around_buildings(buildings: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """
    Calculate the shape around buildings in a GeoDataFrame.

    :param buildings: A GeoDataFrame containing the buildings.
    :return: The shape around the selected buildings in a GeoDataFrame.
    """
    building_shapes = buildings.geometry.to_list()
    selected_area = convex_hull(unary_union(building_shapes))
    selected_area_df = gpd.GeoDataFrame(geometry=[selected_area], crs=buildings.crs)
    return selected_area_df
