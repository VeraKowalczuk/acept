"""Module for handling DWD TRY data.

Use this module to:
    - read DWD TRY data as a Xarray Dataset
    - preprocess DWD TRY data
    - combine multiple DWD TRY datasets (temperature, direct radiation, and global radiation) into a single Xarray Dataset for use in ACEPT
    - uncompress DWD TRY data to make file reading faster
    - check if DWD TRY data is available in the correct subdirectory of DWD_TRY_PATH

Raises:
    ValueOutsideRangeError: if years are outside the allowed range (see :py:const: ``DWD_MAX_RANGE``)
    ValueError: if an unknown DWD feature is requested

Note: To set up the DWD TRY data, use the module :py:mod:`acept.dwd_try_data_setup`

"""

import bz2
import gc
import gzip
import os

import geopandas as gpd
import psutil
import rioxarray
import xarray as xr
from tqdm import tqdm

from acept import acept_utils
from acept.acept_constants import TEMPERATURE_DATA_RAW_PATH, RADIATION_DIRECT_DATA_RAW_PATH, \
    RADIATION_GLOBAL_DATA_RAW_PATH, FED_STATES_PATH, TRY_BAVARIAN_PATH
from acept.exceptions import ValueOutsideRangeError

DWD_MIN_YEAR = 1995
"""Minimum year of DWD TRY data available to download."""
DWD_MAX_YEAR = 2012
"""Maximum year of DWD TRY data."""
DWD_MAX_RANGE = range(DWD_MIN_YEAR, DWD_MAX_YEAR + 1)


def read_dwd_netcdf_file(dwd_feature: str, year, month, debug: bool = True) -> xr.Dataset:
    """
    Read a DWD netCDF file and return the data as a Xarray Dataset.

    :param dwd_feature: The DWD feature to read. Valid options are "temperature", "rad_direct", and "rad_global"
        or "combined_try" for all three features in the same file.
    :param year: The year of the data.
    :param month: The month of the data.
    :param debug: (optional) Whether to print debug information. Defaults to True.
    :return: The data read from the netCDF file.
    """
    wd_filename = path_to_dwd_file(dwd_feature, year, month)
    if debug:
        print(wd_filename)
    # Read in netCDF as a Xarray Dataset
    if wd_filename.endswith(".bz2"):
        with bz2.open(wd_filename) as bz2_file:
            # weather dataset
            wd_data = xr.open_dataset(bz2_file)
            if debug:
                # print(wd_data.info)
                pass
    else:
        # if wd_filename.endswith(".nc.gz") or  wd_filename.endswith(".nc.gz") or other filename extension
        # weather dataset
        wd_data = xr.open_dataset(wd_filename)
        if debug:
            # print(wd_data.info)
            pass
    return wd_data


def preprocess_dwd_try_dataset(wd_data: xr.Dataset, dwd_feature: str, debug: bool = True) -> xr.Dataset:
    """
    Preprocess the DWD TRY dataset to make it ready for use.

    Use this function to preprocess the DWD TRY dataset for use in ACEPT.
    This is the same as ``preprocess_combined_dwd_try_dataset`` but for the individual DWD TRY datasets.
    This step is necessary to use to read the individual DWD TRY datasets.

    :param wd_data: The Xarray Dataset to preprocess.
    :param dwd_feature: The DWD feature to read. Valid options are "temperature", "rad_direct", and "rad_global"
        or "combined_try" for all three features in the same file.
    :param debug: (optional) Whether to print debug information. Defaults to True.
    :return: The preprocessed Xarray Dataset.
    """
    # Rename the DWD data variable
    if dwd_feature != "combined_try":
        dwd_feature_columns = {"temperature": "temperature", "rad_direct": "SID", "rad_global": "SIS"}
        wd_data = wd_data.rename({dwd_feature_columns[dwd_feature]: dwd_feature})
        if debug:
            # print("renamed wd_data.data_vars:", wd_data.data_vars)
            pass

    # Move data variable Lambert_Conformal to attributes
    # wd_data.rio.update_attrs({"Lambert_Conformal": wd_data.Lambert_Conformal}, inplace=True)
    # wd_data = wd_data.drop_vars("Lambert_Conformal", errors="ignore")

    # Set the dimensional variables to X and Y
    wd_data.rio.set_spatial_dims(x_dim="X", y_dim="Y", inplace=True)
    if debug:
        print("preprocess_dwd_try_dataset")
        # print(wd_data.info)
        pass

    # Set CRS of DWD data to EPSG:3034 (as specified in the description of the data set)
    # proj_str = ("+proj=lcc +lat_1=35 +lat_2=65 +lat_0=52 +lon_0=10 +x_0=4000000 +y_0=2800000 +ellps=GRS80 "
    #             "+units=m +k_0=0.017453292 +no_defs")
    # MAYBE scale factor k_0 has to be used somewhere???
    wd_data.rio.write_crs("EPSG:3034", inplace=True)
    if debug:
        print("wd_data.rio.crs: ", wd_data.rio.crs)
    wd_data[dwd_feature].rio.set_crs("EPSG:3034", inplace=True)
    if debug:
        print("wd_data." + dwd_feature + ".rio.crs: ", wd_data[dwd_feature].rio.crs)
    return wd_data


def preprocess_combined_dwd_try_dataset(wd_data: xr.Dataset, debug: bool = True) -> xr.Dataset:
    """
    Preprocess the combined DWD TRY dataset to make it ready for use.

    Use this function to preprocess the combined DWD TRY dataset for use in ACEPT.
    This is the same as ``preprocess_dwd_try_dataset`` but for the combined DWD TRY dataset.
    This step is necessary to use to read the combined DWD TRY dataset.

    :param wd_data: The Xarray Dataset to preprocess.
    :param debug: Whether to print debug information. Defaults to True.
    :return: The preprocessed Xarray Dataset.
    """
    # Move data variable Lambert_Conformal to attributes
    # wd_data.rio.update_attrs({"Lambert_Conformal": wd_data.Lambert_Conformal}, inplace=True)
    # wd_data = wd_data.drop_vars("Lambert_Conformal", errors="ignore")

    # Set the dimensional variables to X and Y
    wd_data.rio.set_spatial_dims(x_dim="X", y_dim="Y", inplace=True)
    if debug:
        print("preprocess_combined_dwd_try_dataset")
        # print(wd_data.info)
        pass

    # Set CRS of DWD data to EPSG:3034 (as specified in the description of the data set)
    # proj_str = ("+proj=lcc +lat_1=35 +lat_2=65 +lat_0=52 +lon_0=10 +x_0=4000000 +y_0=2800000 +ellps=GRS80 "
    #             "+units=m +k_0=0.017453292 +no_defs")
    # MAYBE scale factor k_0 has to be used somewhere???
    wd_data.rio.write_crs("EPSG:3034", inplace=True)
    if debug:
        print("wd_data.rio.crs: ", wd_data.rio.crs)
    for dwd_feature in ["temperature", "rad_direct", "rad_global"]:
        wd_data[dwd_feature].rio.set_crs("EPSG:3034", inplace=True)
        if debug:
            print("wd_data." + dwd_feature + ".rio.crs: ", wd_data[dwd_feature].rio.crs)
    return wd_data


def combine_dwd_try_data_and_save(year_start: int = DWD_MIN_YEAR, year_end: int = DWD_MAX_YEAR, debug: bool = True,
                                  uncompressed_years: None | list[int] = None):
    """
    Combine the DWD TRY data files (of 'temperature', 'rad_direct', 'rad_global') for **Bavaria** and save them as netCDF
    files.

    Included features: temperature, direct and global radiation. Combine the data for these features for Bavaria
    for the given years and the monthly files. This makes using the TRY data easier and more efficient.
    Store the data in uncompressed netCDF files to speed up reading the data.

    :param year_start: start year of the data set to be combined
    :param year_end: end year of the data set to be combined
    :raises ValueOutsideRangeError: if year_start or year_end is outside the allowed range (see ``DWD_MAX_RANGE``)
    :param debug: if True, print debug information
    :param uncompressed_years: optional list of years to be combined and saved without compression
    """
    if year_start > year_end or year_start < DWD_MIN_YEAR or year_end > DWD_MAX_YEAR or (
            uncompressed_years is not None and not all(x in DWD_MAX_RANGE for x in uncompressed_years)):
        raise ValueOutsideRangeError(DWD_MIN_YEAR, DWD_MAX_YEAR)

    # ---------
    bavaria_shape = gpd.read_file(FED_STATES_PATH)
    # modify the "Bayern" to the federal state of your choice to keep the data for another federal state
    bavaria_shape = bavaria_shape.loc[bavaria_shape["GEN"] == "Bayern"]
    bavaria_shape.to_crs(epsg=3034, inplace=True)
    if debug:
        print("bavaria_shape.crs:", bavaria_shape.crs)

    for year_spec in tqdm(range(year_start, year_end + 1), desc="Year Loop", leave=True):
        combine_dwd_try_data_and_save_single_year(bavaria_shape, year_spec, debug, uncompressed_years)


def combine_dwd_try_data_and_save_single_year(bavaria_shape: gpd.GeoDataFrame, year_spec: int, debug: bool = True,
                                              uncompressed_years: None | list[int] = None):
    """
    Combine the DWD TRY data files (of 'temperature', 'rad_direct', 'rad_global') for Bavaria and save them as netCDF
    files. Included features: temperature, direct and global radiation. Combine the data for these features for Bavaria
    for the given year and the monthly files.

    :param bavaria_shape: shape of Bavaria
    :param year_spec: year of the data set to be combined
    :raises ValueOutsideRangeError: if year_spec is outside the allowed range (see ``DWD_MAX_RANGE``)
    :param debug: if True, print debug information
    :param uncompressed_years: optional list of years to be combined and saved without compression. Defaults to None.
    """
    if year_spec not in DWD_MAX_RANGE or (
            uncompressed_years is not None and not all(x in DWD_MAX_RANGE for x in uncompressed_years)):
        raise ValueOutsideRangeError(DWD_MIN_YEAR, DWD_MAX_YEAR)
    for month_spec in tqdm(range(1, 13), desc="Month Loop", leave=True):
        if debug:
            print("Free Memory @ Start:", psutil.virtual_memory().available * 100 / psutil.virtual_memory().total)

        output_path = os.path.join(TRY_BAVARIAN_PATH, f"TRY_{year_spec:04d}{month_spec:02d}.nc.gz")
        if uncompressed_years is not None and year_spec in uncompressed_years:
            output_path = output_path.removesuffix(".gz")
        os.makedirs(acept_utils.uppath(output_path, 1), exist_ok=True)

        if os.path.isfile(output_path):
            if debug:
                print("File already exists:", output_path)
            continue

        # collect data for all relevant DWD TRY features: temperature, SID, SIS
        dwd_features = ['temperature', 'rad_direct', 'rad_global']
        try_clipped: xr.Dataset = None
        for try_feature in dwd_features:
            wd_data = read_dwd_netcdf_file(try_feature, year=year_spec, month=month_spec, debug=debug)

            wd_data = preprocess_dwd_try_dataset(wd_data, try_feature, debug=debug)

            # ---------
            # ### Clipping
            # all_touched – If True, all pixels touched by geometries will be burned in.
            # If false, only pixels whose center is within the polygon or that are selected by Bresenham’s line
            # algorithm will be burned in.
            wd_clipped: xr.Dataset = wd_data.rio.clip(bavaria_shape.geometry.values, bavaria_shape.crs,
                                                      all_touched=True)

            # free up memory
            del wd_data
            if debug:
                print("Free Memory @ after clipping:",
                      psutil.virtual_memory().available * 100 / psutil.virtual_memory().total)
            # ---------

            # collect clipped data in one dataset
            if try_clipped is None:
                try_clipped = wd_clipped
            else:
                try_clipped[try_feature] = wd_clipped[try_feature]

            del wd_clipped
            gc.collect()

        # resolve grid_mapping attribute issue
        vars_list = list(try_clipped.data_vars)
        for var in vars_list:
            try:
                del try_clipped[var].attrs['grid_mapping']
            except KeyError:
                pass

        # write to file
        if debug:
            print("Saving file...")

        if uncompressed_years is not None and year_spec in uncompressed_years:
            # write to raw netcdf os.path.join(TRY_BAVARIAN_PATH, f"TRY_{year_spec:04d}{month_spec:02d}.nc")
            try_clipped.to_netcdf(output_path)
            if debug:
                print("uncompressed written to", output_path.removesuffix('.gz'))
        else:
            # write to netcdf file and gzip it
            # output_path: os.path.join(TRY_BAVARIAN_PATH, f"TRY_{year_spec:04d}{month_spec:02d}.nc.gz")
            with gzip.open(output_path, 'wb') as f:
                f.write(try_clipped.to_netcdf())
            if debug:
                print("written to", output_path)

        del try_clipped
        gc.collect()
        if debug:
            print("Free Memory @ End:", psutil.virtual_memory().available * 100 / psutil.virtual_memory().total)


def check_for_un_compressed_dwd_try_data(compressed=True, year_start: int = DWD_MIN_YEAR,
                                         year_end: int = DWD_MAX_YEAR) -> bool:
    """
    Whether the combined DWD TRY data is downloaded in the correct directory for the given years. If not, return False.
    If yes, return True.

    :param compressed: whether the combined DWD TRY data is available in the correct directory
    :param year_start: start year of the data set to be checked
    :param year_end: end year of the data set to be checked
    :raises ValueOutsideRangeError: if year_start or year_end is outside the allowed range (see ``DWD_MAX_RANGE``)
    :return: whether the combined DWD TRY data is there
    """
    if year_start > year_end or year_start < DWD_MIN_YEAR or year_end > DWD_MAX_YEAR:
        raise ValueOutsideRangeError(DWD_MIN_YEAR, DWD_MAX_YEAR)
    for year in range(year_start, year_end + 1):
        for month in range(1, 13):
            if compressed:
                exists = check_for_dwd_try_data_year(year, types_to_check=['combined_try'])
            else:
                exists = check_for_dwd_try_data_year(year, types_to_check=['combined_try_uncompressed'])
            if not exists:
                return False
    return True


def check_for_dwd_try_data_year(year: int,
                                types_to_check: list[str] = ['temperature', 'rad_direct', 'rad_global']) -> bool:
    """
    Whether DWD TRY data was downloaded in the correct directory for the given year. If not, return False.
    If yes, return True.

    :param year: year of the data set to be checked
    :param types_to_check: list of types of data to be checked, allowed values are 'temperature', 'rad_direct',
        'rad_global', 'combined_try', 'combined_try_uncompressed'
    :raises ValueOutsideRangeError: if year is outside the allowed range (see ``DWD_MAX_RANGE``)
    :return: whether the specified DWD TRY data is there
    """
    if year not in range(DWD_MIN_YEAR, DWD_MAX_YEAR + 1):
        raise ValueOutsideRangeError(DWD_MIN_YEAR, DWD_MAX_YEAR)

    for feature in types_to_check:
        for month in range(1, 13):
            wd_filename = path_to_dwd_file(feature, year, month)
            if not os.path.exists(wd_filename):
                return False
    return True


def path_to_dwd_file(feature: str, year: int, month: int) -> str:
    """
    Path to the DWD TRY data file for the given feature, year, and month.

    :param feature: The DWD feature to read. Valid options are "temperature", "rad_direct", "rad_global",
        "combined_try", or "combined_try_uncompressed".
    :param year: The year of the data.
    :param month: The month of the data.
    :raises ValueError: If the feature is not valid.
    :return: The path to the DWD file.
    """
    dwd_feature_paths = {
        "temperature": os.path.join(TEMPERATURE_DATA_RAW_PATH, f"TT_{year}{month :02d}.nc.bz2"),
        "rad_direct": os.path.join(RADIATION_DIRECT_DATA_RAW_PATH, f"SID_{year}{month :02d}.nc.gz"),
        "rad_global": os.path.join(RADIATION_GLOBAL_DATA_RAW_PATH, f"SIS_{year}{month :02d}.nc.gz"),
        "combined_try": os.path.join(TRY_BAVARIAN_PATH, f"TRY_{year}{month :02d}.nc.gz"),
        "combined_try_uncompressed": os.path.join(TRY_BAVARIAN_PATH, f"TRY_{year}{month :02d}.nc")}
    if feature not in dwd_feature_paths:
        raise ValueError(f"Invalid feature: {feature}. Valid features are {list(dwd_feature_paths.keys())}")
    wd_filename = dwd_feature_paths[feature]
    return wd_filename


if __name__ == '__main__':
    # make sure that rioxarray is imported
    rioxarray.show_versions()
