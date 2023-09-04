"""Module for downloading Test Reference Years data from the open data portal of the Deutscher Wetterdienst.

The Deutscher Wetterdienst (DWD) provides open access the meteorological data of Germany.
The test reference years (TRY) are available for the years from 1995 to including 2012.
The data used in ACEPT contains hourly measurements of a 1 km x 1 km grid in Germany.
The data is divided into monthly files for each feature.

The test reference years are available for the following features:
    - Temperature (mean air temperature)
    - Direct radiation
    - Global radiation

Additional data is available for the following features, but not currently used in ACEPT:
    - Cloud cover
    - Dew point
    - Humidity
    - Pressure
    - Radiation (down welling, upwelling)
    - Vapour pressure
    - Wind direction
    - Wind speed

Use this module to:
    - Download TRY data from the DWD open data portal and save it to the corresponding folders
    - Setup TRY data for ACEPT by combining the data for the features for Bavaria for a single year

To download and setup TRY data for a single year <year>, use:
    setup_dwd_try_data_for_single_year(<year>)

Or run the following command in a terminal, where <year> is the year to download and setup:

.. code-block:: console

    $ python src/acept/dwd_try_data_setup.py <year>

Or execute the module directly:

.. code-block:: console

    $ python -m acept.dwd_try_data_setup.py

If <year> is not given, the year 2011 is used.


For more information about the TRY data, see:
    https://www.dwd.de/DE/leistungen/cdc/cdc_ueberblick-klimadaten.html

Note: Using leap years, e.g. 2012, is not recommended as they have a different number of days than non-leap years.
"""

import os
import subprocess
import sys

from acept.acept_constants import DWD_TRY_URL_BASE, DWD_TRY_URL_TEMP, DWD_TRY_URL_RAD_DIR, DWD_TRY_URL_RAD_GLOB, \
    TEMPERATURE_DATA_RAW_PATH, RADIATION_DIRECT_DATA_RAW_PATH, RADIATION_GLOBAL_DATA_RAW_PATH
from acept.dwd_try_data_handling import DWD_MIN_YEAR, DWD_MAX_YEAR, DWD_MAX_RANGE, combine_dwd_try_data_and_save, \
    check_for_dwd_try_data_year
from acept.exceptions import ValueOutsideRangeError


def download_dwd_data_single_feature(directory_path: str, download_url: str):
    """
    Download all files in the remote directory to the corresponding folder, if the folder is not full.

    :param directory_path: Path to the directory the files are downloaded to.
    :param download_url: URL to download the files from.
    """
    os.makedirs(directory_path, exist_ok=True)

    # check if the data from years 1995 to 2012 is already downloaded
    # should be 2 description files and monthly data from 1995 to including 2012
    full_folder = 2 + (DWD_MIN_YEAR - DWD_MAX_YEAR + 1) * 12
    count = len([name for name in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, name))])
    if count < full_folder:
        subprocess.run(
            ['wget', '-P', directory_path, '-r', '-q', '--show-progress', '--progress=bar:force', '--no-parent',
             '-nd', download_url], check=True)


def download_dwd_data_single_feature_for_single_year(directory_path: str, download_url: str, year: int):
    """
    Download all files in the remote directory to the corresponding folder, if the folder is not full.

    :param directory_path: Path to the directory the files are downloaded to.
    :param download_url: URL to download the files from.
    :param year: Year to download
    :raises ValueOutsideRangeError: if year is outside the allowed range (1995-2012)
    """
    if year not in DWD_MAX_RANGE:
        raise ValueOutsideRangeError(DWD_MIN_YEAR, DWD_MAX_YEAR)
    os.makedirs(directory_path, exist_ok=True)

    file_pattern = f"_{year:04d}"
    wildcard_pattern = f"*{file_pattern}*"

    # check if the twelve files for the given year are already downloaded
    full_folder = 12
    count = len([name for name in os.listdir(directory_path) if
                 os.path.isfile(os.path.join(directory_path, name)) and file_pattern in name])
    if count < full_folder:
        subprocess.run(['wget', '-P', directory_path, '-r', '-A', wildcard_pattern, '-q', '--show-progress',
                        '--progress=bar:force', '--no-parent', '-nd', download_url],
                       check=True)


def download_dwd_data(year: int | None = None):
    """
    Download all files in the relevant remote directories to the corresponding folders. Included features:
    temperature, direct and global radiation.

    :param year: (optional) Year to download. If None, download all years.
    """
    print("Downloading DWD TRY data")
    folder_to_suffix_mapping = {TEMPERATURE_DATA_RAW_PATH: DWD_TRY_URL_TEMP,
                                RADIATION_DIRECT_DATA_RAW_PATH: DWD_TRY_URL_RAD_DIR,
                                RADIATION_GLOBAL_DATA_RAW_PATH: DWD_TRY_URL_RAD_GLOB}
    for folder in folder_to_suffix_mapping.keys():
        if year is not None:
            download_dwd_data_single_feature_for_single_year(folder,
                                                             DWD_TRY_URL_BASE + folder_to_suffix_mapping[folder], year)
        else:
            download_dwd_data_single_feature(folder, DWD_TRY_URL_BASE + folder_to_suffix_mapping[folder])


def setup_dwd_try_data_for_single_year(year: int):
    """
    Download all files in the relevant remote directories to the corresponding folders. Included features:
    temperature, direct and global radiation. Combine the data for these features for Bavaria for the given year and
    save it uncompressed.

    :param year: Year to download and combine.
    """
    # check if all files are already downloaded
    if not check_for_dwd_try_data_year(year=year):
        download_dwd_data(year=year)
    # combine the data for the features for Bavaria for the given year and save it uncompressed
    if check_for_dwd_try_data_year(year=year):
        combine_dwd_try_data_and_save(year_start=year, year_end=year, uncompressed_years=[year])


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage to specify the year: dwd_try_data_setup.py <year>")
        print("The default year 2011 will be used")
        year_cli = 2011
    else:
        year_cli = sys.argv[1]
    setup_dwd_try_data_for_single_year(year_cli)
