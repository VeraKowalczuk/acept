"""Module for input formatting for UrbanHeatPro (UHP) and mapping of data to the values expected by UHP.

Use this module to prepare the input data for UHP. This includes:
    - mapping of data to the values expected by UHP
    - mapping the building use type to their numerical values
    - mapping the construction year to the tabular construction year class
    - mapping the tabular construction year class to their numerical values
    - mapping the size class to their numerical values
    - mapping the refurbishment levels to their numerical values as in UHP

When using this module, make sure to call:
    - the function :py:func:`map_building_use_types_to_numbers` before :py:func:`map_construction_year_to_tabular_construction_year_class`.
    - the function :py:func:`map_construction_year_to_tabular_construction_year_class` before :py:func:`map_tabular_construction_year_class_to_numbers`.
"""

import geopandas as gpd
import numpy as np


def map_building_use_types_to_numbers(buildings: gpd.GeoDataFrame):
    """
    Maps the buildings use type to their numerical values as in UHP and writes this into the "use" field of the
    buildings GeoDataFrame.

    :param buildings: GeoDataFrame with the buildings
    """
    mapping = {'Commercial': 0, 'Industrial': 1, 'Public': 2, 'Residential': 3, 0: 0, 1: 1, 2: 2, 3: 3}
    buildings["use"] = buildings["use"].map(mapping).fillna(np.nan)


def map_building_types_to_numeric_size_class(buildings: gpd.GeoDataFrame):
    """
    Maps the buildings type to their numerical values as in UHP and writes this into the "size_class" field of the
    buildings GeoDataFrame.

    :param buildings: GeoDataFrame with the buildings
    """
    mapping = {'SFH': 0, 'TH': 1, 'MFH': 2, 'AB': 3}
    buildings["size_class"] = buildings["building_type"].map(mapping)


def map_construction_year_to_tabular_construction_year_class(buildings: gpd.GeoDataFrame):
    """
    Maps the Zensus/BDB construction year classes to the TABULAR year classes as used in UHP.

    As there is no direct mapping, the construction year is mapped to the nearest tabular year class.

    :param buildings: GeoDataFrame with the buildings
    """
    mapping = {"-1919": "<1859", "1919-1948": "1919-1948", "1949-1978": "1949-1957", "1979-1986": "1979-1983",
               "1987-1990": "1984-1994", "1991-1995": "1984-1994", "1996-2000": "1995-2001", "2001-2004": "2002-2009",
               "2005-2008": "2002-2009", "2009-": ">2009"}

    buildings["construction_year"] = buildings["construction"].map(mapping)
    return buildings


def map_tabular_construction_year_class_to_numbers(buildings: gpd.GeoDataFrame):
    """
    Maps the TABULAR year classes to their numerical values as in UHP and writes this into the "year_class" field of the
    buildings GeoDataFrame. If the year_class field already exists, it is saved in the "year_class_zensus" field.

    :param buildings: GeoDataFrame with the buildings
    """
    residential_year_class = {
        '<1859': 0,
        '1860-1918': 1,
        '1919-1948': 2,
        '1949-1957': 3,
        '1958-1968': 4,
        '1969-1978': 5,
        '1979-1983': 6,
        '1984-1994': 7,
        '1995-2001': 8,
        '2002-2009': 9,
        '>2009': 10
    }

    non_residential_year_class = {
        '<1918': 0,
        '1919-1976': 1,
        '1977-1983': 2,
        '1984-1994': 3,
        '>1995': 4
    }

    # remove the existing year class field
    if 'year_class' in buildings.columns:
        buildings['year_class_zensus'] = buildings['year_class'].copy()

    is_residential = buildings['use'].isin(['residential', 3])
    is_not_residential = ~is_residential

    buildings.loc[is_residential, 'year_class'] = buildings.loc[is_residential, 'construction_year'].map(
        residential_year_class).fillna(np.NaN)
    buildings.loc[is_not_residential, 'year_class'] = buildings.loc[is_not_residential, 'construction_year'].map(
        non_residential_year_class).fillna(np.NaN)


def map_refurbishment_levels_to_uhp_format(buildings: gpd.GeoDataFrame):
    """
    Maps the refurbishment levels to their numerical values as in UHP and writes this into the 'ref_level_{type}' fields
    of the buildings GeoDataFrame (for types:'floor', 'wall', 'roof', 'window').

    :param buildings: GeoDataFrame with the buildings
    """
    mapping = {0: 1, 1: 2, 2: 3}
    for feature_name in ['floor', 'wall', 'roof', 'window']:
        buildings[f'ref_level_{feature_name}'] = buildings[f'ref_level_{feature_name}'].map(mapping).fillna(np.NaN)
