Setting up additional data
==========================

Check out the :doc:`installation` section if you have not installed the project and its dependencies yet.

personal_settings.py
--------------------
There is an API of Renewables.ninja to create PV capacity factor profiles which provides very quick results.
Users that want to use this heavily rate-limited API need a personal Authorization Token.
As the ratelimit is currently at 50 calls per hour, which is not very much, this is not the recommended way of creating solar profiles.
Still, acept provides a wrapper for querying the API in the module :py:mod:`acept.pv_cap_api`.

To be able to use the API wrapper:

1. Go to https://www.renewables.ninja
2. Create an account
3. The API token is displayed on your account page, where you can also generate a new random token in case your current token has been compromised.
4. Copy the personal API token
5. Create the file
  .. code-block:: text

    src/acept/personal_settings.py

6. Paste the following in the file and replace ``your_token_here`` with the copied API token
  .. code-block:: python

      renewables_token = 'your_token_here'

.. note::
  The API wrapper creates one PV capacity factor profile per query. Multiple consecutive queries for different
  locations are possible, but there is no explicit method implemented for that.
  Instead use the more advanced :py:mod:`acept.pv_cap_factor_profiles` module.


Deutscher Wetterdienst (DWD) weather data
-----------------------------------------

The DWD provides meteorological data for Germany. The historic weather data that is used by ACEPT is from the Project TRY.
Project TRY collected hourly meteorological data for Germany for the test reference years (TRY) 1995 - 2012.
The measurement resolution is a 1km x 1km grid.
The data is available for the following years: 1995 - 2012.

The data is stored in compressed .nc files (netCDF). Each file contains one month of meteorological data for one type of weather feature,
e.g. temperature, direct radiation, etc.
However, the resulting data is very large. So, the DWD published the monthly files in a compressed format.
The combined file size for one year for one weather feature is approximately 1.3 GB if the data is compressed.

Since reading the compressed data is takes a detectable amount of time, it is recommended to preprocess the downloaded
data and store it uncompressed.

To handle the downloaded data, we use the :py:mod:`acept.dwd_try_data_handling` module.

How to download and setup the data
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To download the data from the open data portal of the DWD and set it up in acept:
Use the :py:mod:`acept.dwd_try_data_setup` module.
It provides functions to download all the needed data for acept for one or multiple test reference years.

.. note::
  Since leap years do not have the same number of days as non-leap years and have more than 8760 hours,
  it is recommended to use non-leap years, such as 2011.
  Hence, acept uses the year 2011 per default.

The following example shows how to download the data for the year 2011 and set it up in acept:

.. code-block:: python

    from acept.dwd_try_data_setup import setup_dwd_try_data_for_single_year
    setup_dwd_try_data_for_single_year(2011)

The function :py:func:`acept.dwd_try_data_setup.setup_dwd_try_data_for_single_year` ...
  * downloads the TRY data from the open data portal of the DWD to the correct location in the ``data/dwd`` directory,
  * combines the data of the different weather features,
  * clips the data to the area of **Bavaria**,
  * preprocesses it,
  * and stores it uncompressed as .nc files in a subdirectory of the ``data/dwd`` directory.

To run this example in a terminal, use **one** of the following commands:

.. code-block:: console

    $ python -m acept.dwd_try_data_setup.py

    $ python src/acept/dwd_try_data_setup.py

To download and setup the data for a specific year, e.g. 2010, use **one** of the following commands:

.. code-block:: console

    $ python -m acept/dwd_try_data_setup.py 2010

    $ python src/acept/dwd_try_data_setup.py 2010

.. note::
  The preprocessed uncompressed Bavarian TRY data for the year 2011 has a combined file size of 10.8 GB.

Why use the uncompressed data?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The uncompressed TRY data provides a much faster response time for accessing the DWD data.
As a result, it is recommended to use the uncompressed TRY data, however, it is also possible to use the
raw TRY data.

Why the reduction to the area of **Bavaria**?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Since uncompressed files for Germany would be very large, we focused on **Bavaria**.
To access the TRY data for **other regions** in Germany, use the raw compressed data or modify the source code of
the function :py:func:`acept.dwd_try_data_handling.combine_dwd_try_data.combine_dwd_try_data_and_save`.


Why use the DWD TRY data instead of another data source?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The DWD TRY data is very precise location-wise (1km x 1km grid) and it provides data for concrete years.
So, if you want to analyse a scenario for a specific year, use the DWD TRY data.

Alternatives to the DWD weather data
------------------------------------

Is it possible to use acept without downloading the DWD TRY data?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Yes, there is an alternative to the DWD TRY data.
The :py:mod:`acept.weather_profile_api` module that provides functions to access 
the **PVGIS API** for weather data for **all** regions in Germany (and in Europe).

This module is a wrapper for querying the **PVGIS API** for weather data for a typical 
meteorological year (TMY) for a single location.
It provides very quick results and the rate limit at 30 calls per second is suitable for most use cases.

Requesting the weather data from the API and using it in other modules of acept is also implemented.
For example :py:func:`acept.temperature_profiles.build_temperature_profile_for_year` choses the TMY
for if no year is given or the DWD TRY data is not set up.

For more information on the **PVGIS API** and what a TMY is, please refer to the :py:mod:`acept.weather_profile_api` module.


After the data setup
--------------------

Once you set up the data for the project, check out the :doc:`usage` section or find out more about :doc:`uhp`.