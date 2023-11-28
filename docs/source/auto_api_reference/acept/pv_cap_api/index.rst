:py:mod:`acept.pv_cap_api`
==========================

.. py:module:: acept.pv_cap_api

.. autoapi-nested-parse::

   Module for using the PV capacity factor API of the renewables.ninja API to build the PV capacity profile for a PLZ.

   See https://www.renewables.ninja for more details.
   Note: The API is rate limited to 50 calls per hour and needs an API key.
   This key can be obtained from https://www.renewables.ninja and has to be set in /src/acept/personal_settings.py.

   Set the API key in the following way in /src/acept/personal_settings.py:

   .. code-block:: python

       renewables_token = "your_api_key"


   :raises FileNotFoundError: if the file 'personal_settings.py' is not found.
   :raises ValueError: if the 'renewables_token' is not set in /src/acept/personal_settings.py



Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   acept.pv_cap_api.PVQuery
   acept.pv_cap_api.PVCapacityFactorCreator




.. py:class:: PVQuery(plz: str, year: int = 2022, capacity: float = 1.0, system_loss: float = 0.1, tilt: float = 35, azim: float = 180)


   Class containing the arguments for the PV capacity factor API call.

   Constructor for the PVQuery class.

   :param plz: The PLZ of the queried area.
   :param year: The year of the queried data.
   :param capacity: The maximum capacity of the PV system in kW.
   :param system_loss: The system loss of the PV system in %.
   :param tilt: The tilt of the PV system in degrees.
   :param azim: The azimuth of the PV system in degrees.
   :raises ValueError: If the queried year is not between 1980 and 2022.

   .. py:method:: to_args_dict()

      Construct the arguments for the PV capacity factor API call as a dictionary.

      :return: the arguments as a dictionary



.. py:class:: PVCapacityFactorCreator


   Class for querying the PV capacity factor API of the renewables.ninja API. See https://www.renewables.ninja

   .. py:attribute:: MAX_CALLS_PER_HOUR
      :value: 50

      50 per hour

      :type: Rate limit of the renewables.ninja API as registered user

   .. py:attribute:: ONE_HOUR
      :value: 3600

      Number of seconds in one hour

   .. py:method:: create_pv_api_query(pv_query: PVQuery) -> str

      Query the PV capacity factor API of the renewables.ninja API with the given query and save the result in
      a temporary directory as a CSV file. Be aware that the API is rate limited to 50 calls per hour.
      See https://www.renewables.ninja/documentation for more details.

      :param pv_query: The PV capacity factor query.



