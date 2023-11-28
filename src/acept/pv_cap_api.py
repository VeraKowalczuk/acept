"""Module for using the PV capacity factor API of the renewables.ninja API to build the PV capacity profile for a PLZ.

See https://www.renewables.ninja for more details.
Note: The API is rate limited to 50 calls per hour and needs an API key.
This key can be obtained from https://www.renewables.ninja and has to be set in /src/acept/personal_settings.py.

Set the API key in the following way in /src/acept/personal_settings.py:

.. code-block:: python

    renewables_token = "your_api_key"


Raises:
    FileNotFoundError: if the file 'personal_settings.py' is not found.
    ValueError: if the 'renewables_token' is not set in /src/acept/personal_settings.py

"""

import io
import json
import os

import pandas as pd
import requests
from ratelimit import limits, sleep_and_retry

import acept.plz_shape as plz_shape
from acept.acept_utils import absolute_path_from_relative_posix
from acept.acept_constants import TEMP_PATH, RENEWABLES_NINJA_API_BASE
from acept.uhp_csv_io import write_geopandas_to_uhp_csv

if os.path.isfile(absolute_path_from_relative_posix("personal_settings.py")):
    import acept.personal_settings as secret
else:
    raise FileNotFoundError("Please set the 'renewables_token' in /src/acept/personal_settings.py")


###################################################################################################
###################################    PV capacity factor  ########################################
###################################################################################################
###################################################################################################

# ---------
# # PV Capacity factor API

# ---------

class PVQuery:
    """
    Class containing the arguments for the PV capacity factor API call.
    """

    def __init__(self, plz: str, year: int = 2022, capacity: float = 1.0, system_loss: float = 0.1,
                 tilt: float = 35, azim: float = 180):
        """
        Constructor for the PVQuery class.

        :param plz: The PLZ of the queried area.
        :param year: The year of the queried data.
        :param capacity: The maximum capacity of the PV system in kW.
        :param system_loss: The system loss of the PV system in %.
        :param tilt: The tilt of the PV system in degrees.
        :param azim: The azimuth of the PV system in degrees.
        :raises ValueError: If the queried year is not between 1980 and 2022.
        """
        ##
        # query settings
        ##

        # plz --> lat, lon of centroid??
        self.queried_plz = plz  # --> e.g. 'lat': 48.2595, 'lon': 11.4446,
        if year < 1980 or year > 2022:
            raise ValueError(f"The PV Capacity data is only available for years 1980-2022, but queried: {year}")
        self.year = year
        self.max_capacity = capacity
        self.system_loss = system_loss
        self.tilt = tilt
        self.azim = azim
        self.cent_point = plz_shape.calculate_centroid_of_plz(self.queried_plz)

    def to_args_dict(self):
        """
        Construct the arguments for the PV capacity factor API call as a dictionary.

        :return: the arguments as a dictionary
        """
        args = {
            'lat': self.cent_point.y,  # 48.2595,
            'lon': self.cent_point.x,  # 11.4446,
            'date_from': f'{self.year}-01-01',
            'date_to': f'{self.year}-12-31',
            'dataset': 'merra2',
            'capacity': self.max_capacity,
            'system_loss': self.system_loss,
            'tracking': 0,
            'tilt': self.tilt,
            'azim': self.azim,
            'raw': 'false',
            'format': 'json'
        }
        return args


class PVCapacityFactorCreator:
    """
    Class for querying the PV capacity factor API of the renewables.ninja API. See https://www.renewables.ninja
    """
    MAX_CALLS_PER_HOUR = 50
    """Rate limit of the renewables.ninja API as registered user: 50 per hour"""
    ONE_HOUR = 3600
    """Number of seconds in one hour"""

    def __init__(self):
        # secret token of registered user. See /src/acept/personal_settings.py
        if secret.renewables_token == "":
            raise ValueError("Please set the 'renewables_token' in /src/acept/personal_settings.py")
        self.token = secret.renewables_token
        self.api_base = RENEWABLES_NINJA_API_BASE
        self.session = requests.session()
        # Send token header with each request
        self.session.headers = {'Authorization': 'Token ' + self.token}

    # ---------

    @sleep_and_retry
    @limits(calls=MAX_CALLS_PER_HOUR, period=ONE_HOUR)
    def create_pv_api_query(self, pv_query: PVQuery) -> str:
        """
        Query the PV capacity factor API of the renewables.ninja API with the given query and save the result in
        a temporary directory as a CSV file. Be aware that the API is rate limited to 50 calls per hour.
        See https://www.renewables.ninja/documentation for more details.

        :param pv_query: The PV capacity factor query.
        """
        url = RENEWABLES_NINJA_API_BASE + 'data/pv'

        args = pv_query.to_args_dict()

        # send query to API
        api_response = self.session.get(url, params=args)

        # ---------
        if not api_response.ok:
            # If response code is not ok (200), print the resulting http error code with description
            api_response.raise_for_status()
            return
        else:
            # Parse JSON to get a pandas.DataFrame of data and dict of metadata
            parsed_response = api_response.json()

            el_out_data = pd.read_json(io.StringIO(json.dumps(parsed_response['data'])), orient='index')
            metadata = parsed_response['metadata']

        # The capacity factor (Volllaststunden) is defined as cap_fac = el_out (in kW) / max_capacity (in kW)
        cap_fac_data = el_out_data['electricity'] / pv_query.max_capacity

        # ---------
        # ### Save PV capacity data to temp file as csv
        pv_cap_csv_path = os.path.join(TEMP_PATH, f"{pv_query.queried_plz}_pv_cap_{pv_query.year}.csv")

        # add header row and unit info
        # MAYBE add timestamp? cap_fac_data.to_csv(pv_cap_csv_path, index=True, index_label="timestamp")
        return write_geopandas_to_uhp_csv(pv_cap_csv_path, cap_fac_data, ['PV Capacity Factor'], ['unitless'])
