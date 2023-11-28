:py:mod:`acept.dwd_try_data_setup`
==================================

.. py:module:: acept.dwd_try_data_setup

.. autoapi-nested-parse::

   Module for downloading Test Reference Years data from the open data portal of the Deutscher Wetterdienst.

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

   .. code-block:: python

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

   .. note:: Using leap years, e.g. 2012, is not recommended as they have a different number of days than non-leap years.



Module Contents
---------------


Functions
~~~~~~~~~

.. autoapisummary::

   acept.dwd_try_data_setup.download_dwd_data_single_feature
   acept.dwd_try_data_setup.download_dwd_data_single_feature_for_single_year
   acept.dwd_try_data_setup.download_dwd_data
   acept.dwd_try_data_setup.setup_dwd_try_data_for_single_year



Attributes
~~~~~~~~~~

.. autoapisummary::

   acept.dwd_try_data_setup.year_cli


.. py:function:: download_dwd_data_single_feature(directory_path: str, download_url: str)

   Download all files in the remote directory to the corresponding folder, if the folder is not full.

   :param directory_path: Path to the directory the files are downloaded to.
   :param download_url: URL to download the files from.


.. py:function:: download_dwd_data_single_feature_for_single_year(directory_path: str, download_url: str, year: int)

   Download all files in the remote directory to the corresponding folder, if the folder is not full.

   :param directory_path: Path to the directory the files are downloaded to.
   :param download_url: URL to download the files from.
   :param year: Year to download
   :raises ValueOutsideRangeError: if year is outside the allowed range (1995-2012)


.. py:function:: download_dwd_data(year: int | None = None)

   Download all files in the relevant remote directories to the corresponding folders. Included features:
   temperature, direct and global radiation.

   :param year: (optional) Year to download. If None, download all years.


.. py:function:: setup_dwd_try_data_for_single_year(year: int)

   Download all files in the relevant remote directories to the corresponding folders. Included features:
   temperature, direct and global radiation. Combine the data for these features for Bavaria for the given year and
   save it uncompressed.

   :param year: Year to download and combine.


.. py:data:: year_cli
   :value: 2011

   

