:py:mod:`acept.acept_constants`
===============================

.. py:module:: acept.acept_constants

.. autoapi-nested-parse::

   Module for constants used in ACEPT

   This module contains constants used in ACEPT that define URLs and paths to files and directories.

   .. note::

      All constants of paths work independent of the operating system the code is running on.
      They are dynamically set depending on the operating system and the filesystem.



Module Contents
---------------

.. py:data:: DWD_TRY_URL_BASE
   :value: 'ftp://opendata.dwd.de/climate_environment/CDC/grids_germany/hourly/Project_TRY/'

   Base URL for the DWD TRY data.
   See https://opendata.dwd.de/climate_environment/CDC/grids_germany/hourly/Project_TRY/

.. py:data:: DWD_TRY_URL_TEMP
   :value: 'air_temperature_mean/'

   URL for the temperature data.
   See https://opendata.dwd.de/climate_environment/CDC/grids_germany/hourly/Project_TRY/air_temperature_mean/

.. py:data:: DWD_TRY_URL_RAD_DIR
   :value: 'radiation_direct/'

   URL for the direct radiation data.
   See https://opendata.dwd.de/climate_environment/CDC/grids_germany/hourly/Project_TRY/radiation_direct/

.. py:data:: DWD_TRY_URL_RAD_GLOB
   :value: 'radiation_global/'

   URL for the global radiation data.
   See https://opendata.dwd.de/climate_environment/CDC/grids_germany/hourly/Project_TRY/radiation_global/

.. py:data:: RENEWABLES_NINJA_API_BASE
   :value: 'https://www.renewables.ninja/api/'

   Base URL for the renewables.ninja API.
   See https://www.renewables.ninja

.. py:data:: PVGIS_API_BASE_URL
   :value: 'https://re.jrc.ec.europa.eu/api/v5_2/'

   Base URL for the PVGIS API.
   See https://re.jrc.ec.europa.eu/api/v5_2/

.. py:data:: UHP_PATH

   Path to the UrbanHeatPro directory.

   Path relative to the acept repository root directory: ``deps/UrbanHeatPro/``

   See https://github.com/VeraKowalczuk/UrbanHeatPro

.. py:data:: UHP_SETTINGS_PATH

   Path to the UrbanHeatPro settings file.

   Path relative to the acept repository root directory: ``deps/UrbanHeatPro/settings/uhp_settings.yaml``

   See https://github.com/VeraKowalczuk/UrbanHeatPro

.. py:data:: UHP_DEFAULT_SETTINGS_PATH

   Path to the default UrbanHeatPro settings file.

   Path relative to the acept repository root directory: ``deps/UrbanHeatPro/settings/uhp_default_settings.yaml``

   See https://github.com/VeraKowalczuk/UrbanHeatPro

.. py:data:: DWD_TRY_PATH

   Path to the local DWD TRY data directory.

   Path relative to the acept repository root directory: ``data/dwd/``

.. py:data:: TEMPERATURE_DATA_RAW_PATH

   Path to the local DWD TRY temperature data directory.

   Path relative to the acept repository root directory: ``data/dwd/temp_data_raw/``

.. py:data:: RADIATION_DIRECT_DATA_RAW_PATH

   Path to the local DWD TRY direct radiation data directory.

   Path relative to the acept repository root directory: ``data/dwd/rad_dir_data_raw/``

.. py:data:: RADIATION_GLOBAL_DATA_RAW_PATH

   Path to the local DWD TRY global radiation data directory.

   Path relative to the acept repository root directory: ``data/dwd/rad_glob_data_raw/``

.. py:data:: TRY_BAVARIAN_PATH

   Path to the local DWD TRY data directory with combined TRY data for Bavaria.

   Path relative to the acept repository root directory: ``data/dwd/try_bavarian/``

.. py:data:: PLZ_PATH

   Path to the PLZ shape file.

   Path relative to the acept repository root directory: ``data/plz/plz-5stellig.shp``

.. py:data:: FED_STATES_PATH

   Path to the federal states shape file.

   Path relative to the acept repository root directory: ``data/fed_states/federal_states_borders_germany.shp``

.. py:data:: TEMP_PATH

   Path to the temporary directory.

   Path relative to the acept repository root directory: ``temp/``

.. py:data:: BBD_ROOT_DIR_TEST

   Path to the local test data directory.

   Path relative to the acept repository root directory: ``../BBD/TestBezirk/``

.. py:data:: PLZ_MAPPING_JSON_DIR_TEST

   Path to the PLZ to municipality code mapping JSON file for the test data.

   Path relative to the acept repository root directory: ``data/plz_mappigs/test_plz_to_munc_dict.json``

.. py:data:: BBD_ROOT_DIR

   Path to the data directory for the unprocessed Bavarian Building Database (BBD).

   Path relative to the acept repository root directory: ``../BBD/``

.. py:data:: PLZ_MAPPING_JSON_DIR

   Path to the PLZ to municipality code mapping JSON file for the BBD.

   Path relative to the acept repository root directory: ``data/plz_to_munc_dict.json``

.. py:data:: BBD_WITH_PLZ_ROOT_PATH

   



   Path to the data directory for the preprocessed Bavarian Building Database (BBD).
       Includes the BBD with PLZ information and missing fields added.

   Path relative to the acept repository root directory: ``data/bbd``

