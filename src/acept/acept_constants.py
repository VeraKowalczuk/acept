"""Module for constants used in ACEPT

This module contains constants used in ACEPT that define URLs and paths to files and directories.

Note:
    All constants of paths work independent of the operating system the code is running on.
    They are dynamically set depending on the operating system and the filesystem.
"""

import os.path

from acept.acept_utils import absolute_path_from_relative_posix

# ------------------ URLs --------------------------------------------------
DWD_TRY_URL_BASE = "ftp://opendata.dwd.de/climate_environment/CDC/grids_germany/hourly/Project_TRY/"
"""Base URL for the DWD TRY data. 
See https://opendata.dwd.de/climate_environment/CDC/grids_germany/hourly/Project_TRY/
"""
DWD_TRY_URL_TEMP = "air_temperature_mean/"
"""URL for the temperature data. 
See https://opendata.dwd.de/climate_environment/CDC/grids_germany/hourly/Project_TRY/air_temperature_mean/
"""
DWD_TRY_URL_RAD_DIR = "radiation_direct/"
"""URL for the direct radiation data. 
See https://opendata.dwd.de/climate_environment/CDC/grids_germany/hourly/Project_TRY/radiation_direct/
"""
DWD_TRY_URL_RAD_GLOB = "radiation_global/"
"""URL for the global radiation data. 
See https://opendata.dwd.de/climate_environment/CDC/grids_germany/hourly/Project_TRY/radiation_global/
"""

RENEWABLES_NINJA_API_BASE = 'https://www.renewables.ninja/api/'
"""Base URL for the renewables.ninja API. 
See https://www.renewables.ninja
"""

PVGIS_API_BASE_URL = 'https://re.jrc.ec.europa.eu/api/v5_2/'
"""Base URL for the PVGIS API. 
See https://re.jrc.ec.europa.eu/api/v5_2/
"""

# ------------------ Paths relative to /src/acept directory -------------------
UHP_PATH = absolute_path_from_relative_posix("../../deps/UrbanHeatPro/")
"""Path to the UrbanHeatPro directory. 

Path relative to the acept repository root directory: ``deps/UrbanHeatPro/``

See https://github.com/VeraKowalczuk/UrbanHeatPro
"""

UHP_SETTINGS_PATH = absolute_path_from_relative_posix("../../settings/uhp_settings.yaml")
"""Path to the UrbanHeatPro settings file. 

Path relative to the acept repository root directory: ``deps/UrbanHeatPro/settings/uhp_settings.yaml``

See https://github.com/VeraKowalczuk/UrbanHeatPro
"""

UHP_DEFAULT_SETTINGS_PATH = os.path.join(UHP_PATH, "settings/uhp_default_settings.yaml")
"""Path to the default UrbanHeatPro settings file. 

Path relative to the acept repository root directory: ``deps/UrbanHeatPro/settings/uhp_default_settings.yaml``

See https://github.com/VeraKowalczuk/UrbanHeatPro
"""


DWD_TRY_PATH = absolute_path_from_relative_posix("../../data/dwd/")
"""Path to the local DWD TRY data directory.

Path relative to the acept repository root directory: ``data/dwd/``
"""

TEMPERATURE_DATA_RAW_PATH = absolute_path_from_relative_posix("../../data/dwd/temp_data_raw/")
"""Path to the local DWD TRY temperature data directory.

Path relative to the acept repository root directory: ``data/dwd/temp_data_raw/``
"""

RADIATION_DIRECT_DATA_RAW_PATH = absolute_path_from_relative_posix("../../data/dwd/rad_dir_data_raw/")
"""Path to the local DWD TRY direct radiation data directory.

Path relative to the acept repository root directory: ``data/dwd/rad_dir_data_raw/``
"""

RADIATION_GLOBAL_DATA_RAW_PATH = absolute_path_from_relative_posix("../../data/dwd/rad_glob_data_raw/")
"""Path to the local DWD TRY global radiation data directory.

Path relative to the acept repository root directory: ``data/dwd/rad_glob_data_raw/``
"""

TRY_BAVARIAN_PATH = absolute_path_from_relative_posix("../../data/dwd/try_bavarian/")
"""Path to the local DWD TRY data directory with combined TRY data for Bavaria.

Path relative to the acept repository root directory: ``data/dwd/try_bavarian/``
"""

PLZ_PATH = absolute_path_from_relative_posix("../../data/plz/plz-5stellig.shp")
"""Path to the PLZ shape file.

Path relative to the acept repository root directory: ``data/plz/plz-5stellig.shp``
"""

FED_STATES_PATH = absolute_path_from_relative_posix("../../data/fed_states/vg2500_bld.shp")
"""Path to the federal states shape file.

Path relative to the acept repository root directory: ``data/fed_states/vg2500_bld.shp``
"""

TEMP_PATH = absolute_path_from_relative_posix("../../temp/")
"""Path to the temporary directory.

Path relative to the acept repository root directory: ``temp/``
"""


# ------- Example data
BBD_ROOT_DIR_TEST = absolute_path_from_relative_posix("../../../BBD/TestBezirk/")
"""Path to the local test data directory.

Path relative to the acept repository root directory: ``../BBD/TestBezirk/``
"""

PLZ_MAPPING_JSON_DIR_TEST = absolute_path_from_relative_posix("../../data/plz_mappigs/test_plz_to_munc_dict.json")
"""Path to the PLZ to municipality code mapping JSON file for the test data.

Path relative to the acept repository root directory: ``data/plz_mappigs/test_plz_to_munc_dict.json``
"""


# -------- Real data (production)
BBD_ROOT_DIR = absolute_path_from_relative_posix("../../../BBD/")
"""Path to the data directory for the unprocessed Bavarian Building Database (BBD).

Path relative to the acept repository root directory: ``../BBD/``
"""

PLZ_MAPPING_JSON_DIR = absolute_path_from_relative_posix("../../data/plz_to_munc_dict.json")
"""Path to the PLZ to municipality code mapping JSON file for the BBD.

Path relative to the acept repository root directory: ``data/plz_to_munc_dict.json``
"""

BBD_WITH_PLZ_ROOT_PATH = absolute_path_from_relative_posix("../../data/bbd")
"""Path to the data directory for the preprocessed Bavarian Building Database (BBD).
    Includes the BBD with PLZ information and missing fields added.
    
Path relative to the acept repository root directory: ``data/bbd``
"""
