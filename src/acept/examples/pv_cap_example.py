"""Module for an example of building PV capacity profiles for an area around Schwabach.

Creates a PV capacity factor profile of 10 buildings in Schwabach.
Depends on the DWD TRY data available on the machine. If the data is not available for the year 2011, the TMY weather
data is used.

Also shows how to combine the downloaded DWD TRY data into a single file per month with all needed weather features.

"""

import geopandas as gpd
from shapely.geometry import Point

from acept.acept_utils import absolute_path_from_relative_posix
from acept.dwd_try_data_handling import combine_dwd_try_data_and_save, \
    check_for_un_compressed_dwd_try_data
from acept.plz_shape import get_single_plz_shape
from acept.pv_cap_factor_profiles import build_pv_capacity_for_selected_years, \
    build_pv_capacity_for_selected_year_with_combined_data, build_pv_capacity_profile_for_year

if __name__ == "__main__":

    # Schwabach
    plz = "91126"
    plz_shape = get_single_plz_shape(plz)
    print(plz_shape)

    b = gpd.read_file(absolute_path_from_relative_posix("../../data/bbd/TestBezirk/Res_9565000_10_buildings.shp"))

    # runtime 10 minutes for 10 buildings and 1 year
    # build_pv_capacity_for_selected_years(plz_shape, b, 2000, 2000)

    year = 2011
    # build_pv_capacity_for_selected_years_with_combined_data(plz_shape, b, year, year, uncompressed=True)
    build_pv_capacity_profile_for_year(plz_shape, b, year)

    # preprocessing downloaded DWD data into combined data (temperature, rad_direct, rad_global) for Bavaria
    combine_dwd_try_data_and_save(year_start=year, year_end=year, uncompressed_years=[year])
    build_pv_capacity_profile_for_year(plz_shape, b, year)

    # use TMY weather data:
    build_pv_capacity_profile_for_year(plz_shape, b, None)
