"""Module for accessing the PLZ shapes.

Use this module to
    - get information about the PLZ areas.
    - calculate the centroid of the PLZ area for a given PLZ.
    - read the shape file containing the PLZ areas.
    - get the PLZ shape for a given PLZ.

Note:
    The path to the shape file is defined in :py:const:`accept.config.PLZ_PATH`
"""

import geopandas as gpd
from shapely import Point

from acept.acept_constants import PLZ_PATH


def read_plz_shapefile(plz_path: str = PLZ_PATH) -> gpd.GeoDataFrame:
    """
    Reads shape file defining the PLZ areas and returns it as a GeoDataFrame.

    :param plz_path: path to the shapefile defining the PLZ areas. Default: :py:const:`accept.config.PLZ_PATH`
    :return: GeoDataFrame defining all PLZ areas in EPSG:4326
    """
    gdf = gpd.read_file(plz_path, encoding='utf-8')
    gdf = gdf.to_crs(epsg=4326)
    return gdf


def get_single_plz_shape(plz: str) -> gpd.GeoDataFrame:
    """
    Reads the PLZ shape file and returns the information of a given PLZ.

    :param plz: The PLZ to be searched.
    :return: GeoDataFrame containing the information of the given PLZ.
    """
    plz_df = read_plz_shapefile(PLZ_PATH)
    plz_mask: gpd.GeoDataFrame = plz_df.loc[plz_df["plz"] == plz]
    return plz_mask

# ---------
# ## Calculate lon, lat of PLZ
# MAYBE use centroids in data/plz-5stellig-daten.csv


def calculate_centroid_of_plz(plz: str) -> Point:
    """
    Calculates the centroid of the PLZ area.

    :param plz: The PLZ to be searched.
    :return: The centroid of the PLZ area as a Point(lon, lat).
    """
    # read shapefile
    plz_df = get_single_plz_shape(plz)

    # calculate centroids
    # VERA check if this is the correct projection? but warning is missing now with .to_crs('+proj=cea')
    centroid = plz_df.to_crs('+proj=cea').centroid.to_crs(plz_df.crs)

    # note: lat = y and lon = x
    return centroid.values[0]
