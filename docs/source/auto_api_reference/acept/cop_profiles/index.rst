:py:mod:`acept.cop_profiles`
============================

.. py:module:: acept.cop_profiles

.. autoapi-nested-parse::

   Module to calculate COP (Coefficient of Performance) profiles.

   The COP (Coefficient of Performance) is a measure of the performance of a heat pump or heat exchanger.
   The COP is calculated based on the temperature difference between the heat source and the heat sink.

   Use this module to:
       - Build the COP heat pump data for a given DataFrame of buildings.
       - Save the COP heat pump data to a CSV file in the :py:const:`acept.acept_constants.TEMP_PATH` directory.
       - Build the COP heat pump air data for a given DataFrame of buildings and save it to a CSV file in the :py:const:`acept.acept_constants.TEMP_PATH` directory.

   Use the :py:func:`acept.cop_profiles.build_cop_tve_profiles_csv` function to build the COP heat pump data for a given
   DataFrame of buildings and save it to a CSV file in the :py:const:`acept.acept_constants.TEMP_PATH` directory.



Module Contents
---------------


Functions
~~~~~~~~~

.. autoapisummary::

   acept.cop_profiles.compute_sink_temperature_from_source_temperature
   acept.cop_profiles.cop_calc
   acept.cop_profiles.build_cop_df
   acept.cop_profiles.calculate_cop_tve
   acept.cop_profiles.build_cop_tve_profiles
   acept.cop_profiles.build_cop_tve_profiles_csv
   acept.cop_profiles.save_heapump_air_to_csv



Attributes
~~~~~~~~~~

.. autoapisummary::

   acept.cop_profiles.COP_PARAMS
   acept.cop_profiles.CORRECTION


.. py:data:: COP_PARAMS

   COP parameters for air, ground, water.

   +------+---------+---------+---------+
   | type | air     | ground  | water   |
   +======+=========+=========+=========+
   | 0    | 6,0801  | 10,288  | 9,9696  |
   +------+---------+---------+---------+
   | 1    | -0,0941 | -0,2084 | -0,2049 |
   +------+---------+---------+---------+
   | 2    | 0,0005  | 0,0012  | 0,0012  |
   +------+---------+---------+---------+

.. py:data:: CORRECTION
   :value: 0.85

   Correction factor for the COP values.

.. py:function:: compute_sink_temperature_from_source_temperature(source_temperature: pandas.Series) -> pandas.DataFrame

   Compute the sink temperature from the source temperature.

   :param source_temperature: The source temperature data.
   :return: The sink temperature data, including the radiator temperature, floor temperature, water temperature
       for small buildings, and water temperature for large buildings.


.. py:function:: cop_calc(delta_temp: float, heat_source_type: str = 'air') -> float

   Calculate the coefficient of performance (COP) for a given temperature difference.

   :param delta_temp: The temperature difference between the heat source and the heat sink.
   :param heat_source_type: The type of heat source being used. Defaults to 'air'.
   :return: The calculated coefficient of performance (COP).


.. py:function:: build_cop_df(source_temperature: pandas.Series, cap_value: int | None = None, heat_source_type: str = 'air') -> pandas.DataFrame

   Builds a COP (Coefficient of Performance) DataFrame based on the given source temperature DataFrame,
   cap value, and heat source type.

   First calculates the sink temperature from the source temperature,
   then the COP values are calculated based on the temperature differences between the sink temperature and the source
   temperature and applying a correction factor.

   :param source_temperature: The DataFrame containing the source temperature data.
   :param cap_value: The maximum value to cap the delta temperature. If set, the delta temperature values
       will be capped at this value. Defaults to None.
   :param heat_source_type: The type of heat source. This parameter is used in the calculation of the COP values.
       Defaults to 'air'.
   :return: The COP DataFrame with the calculated COP values.


.. py:function:: calculate_cop_tve(cop_df: pandas.DataFrame, buildings: pandas.DataFrame, space_heat: pandas.DataFrame, water_heat: pandas.DataFrame) -> pandas.DataFrame

   Calculate the building specific average coefficients of performance (COP) depending on the room/water heating demands.

   :param cop_df: A DataFrame containing the COP values for different heating types.
   :type cop_df: pd.DataFrame
   :param buildings: A DataFrame containing information about the buildings.
   :type buildings: pd.DataFrame
   :param space_heat: A DataFrame containing the space heating values for each building.
   :type space_heat: pd.DataFrame
   :param water_heat: A DataFrame containing the water heating values for each building.
   :type water_heat: pd.DataFrame
   :return: A DataFrame containing the calculated COP profiles for the buildings.


.. py:function:: build_cop_tve_profiles(buildings: pandas.DataFrame, space_heat: pandas.DataFrame, water_heat: pandas.DataFrame, source_temperature: pandas.Series, cap_value: int | None = None, heat_source_type: str = 'air') -> pandas.DataFrame

   Builds the COP (Coefficient of Performance) heat pump air data for the given buildings.

   :param buildings: The GeoDataFrame containing the buildings.
   :type buildings: gpd.GeoDataFrame
   :param space_heat: The DataFrame containing the space heating values.
   :type space_heat: pd.DataFrame
   :param water_heat: The DataFrame containing the water heating values.
   :type water_heat: pd.DataFrame
   :param source_temperature: The source temperature data.
   :type source_temperature: pd.Series
   :param cap_value: The maximum allowed temperature difference between the heat source and the heat sink. If None,
       the difference is not capped. Defaults to None.
   :type cap_value: int | None, optional
   :param heat_source_type: The type of heat source being used. Defaults to 'air'.
   :type heat_source_type: str, optional
   :return: DataFrame with the COP heat pump air data.


.. py:function:: build_cop_tve_profiles_csv(area_id: str, buildings: pandas.DataFrame, space_heat: pandas.DataFrame, water_heat: pandas.DataFrame, source_temperature: pandas.Series, cap_value: int | None = None, heat_source_type: str = 'air') -> tuple[pandas.DataFrame, str]

   Builds the COP (Coefficient of Performance) heat pump air data for the given buildings and saves it to a CSV file
   in the: py:const:`acept.acept_constants.TEMP_PATH` directory.

   :param area_id: The ID of the area COP data belongs to.
   :type area_id: str
   :param buildings: The GeoDataFrame containing the buildings.
   :type buildings: gpd.GeoDataFrame
   :param space_heat: The DataFrame containing the space heating values.
   :type space_heat: pd.DataFrame
   :param water_heat: The DataFrame containing the water heating values.
   :type water_heat: pd.DataFrame
   :param source_temperature: The source temperature data.
   :type source_temperature: pd.Series
   :param cap_value: The maximum allowed temperature difference between the heat source and the heat sink. If None,
       the difference is not capped. Defaults to None.
   :type cap_value: int | None, optional
   :param heat_source_type: The type of heat source being used. Defaults to 'air'.
   :type heat_source_type: str, optional
   :return: A tuple containing the COP heat pump air data and the path to the saved CSV file.


.. py:function:: save_heapump_air_to_csv(area_id: str, cop_tve_df: pandas.DataFrame) -> str

   Saves the COP (Coefficient of Performance) heat pump air data to a CSV file in the: py:const:`acept.acept_constants.TEMP_PATH` directory.

   :param area_id: The ID of the area COP data belongs to.
   :type area_id: str
   :param cop_tve_df: The DataFrame containing the heat pump air data.
   :type cop_tve_df: pd.DataFrame
   :return: The path to the saved CSV file.


