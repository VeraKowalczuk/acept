"""Module to calculate COP (Coefficient of Performance) profiles.

The COP (Coefficient of Performance) is a measure of the performance of a heat pump or heat exchanger.
The COP is calculated based on the temperature difference between the heat source and the heat sink.

Use this module to:
    - Build the COP heat pump data for a given DataFrame of buildings.
    - Save the COP heat pump data to a CSV file in the :py:const:`acept.acept_constants.TEMP_PATH` directory.
    - Build the COP heat pump air data for a given DataFrame of buildings and save it to a CSV file in the :py:const:`acept.acept_constants.TEMP_PATH` directory.

Use the :py:func:`acept.cop_profiles.build_cop_tve_profiles_csv` function to build the COP heat pump data for a given
DataFrame of buildings and save it to a CSV file in the :py:const:`acept.acept_constants.TEMP_PATH` directory.
"""

import os

import numpy as np
import pandas as pd

from acept import acept_utils
from acept.acept_constants import TEMP_PATH

COP_PARAMS = {'air': [6.0801, -0.0941, 0.0005], 'ground': [10.288, -0.2084, 0.0012], 'water': [9.9696, -0.2049, 0.0012]}
"""
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
"""

CORRECTION = 0.85
"""Correction factor for the COP values."""


def compute_sink_temperature_from_source_temperature(source_temperature: pd.Series) -> pd.DataFrame:
    """
    Compute the sink temperature from the source temperature.

    :param source_temperature: The source temperature data.
    :return: The sink temperature data, including the radiator temperature, floor temperature, water temperature
        for small buildings, and water temperature for large buildings.
    """
    # 50 for small buildings, 60 for large buildings
    return pd.DataFrame(pd.concat([(40 - source_temperature).rename('radiator'),
                                   (30 - source_temperature / 2).rename('floor'),
                                   pd.DataFrame([[50]], index=source_temperature.index,
                                                columns=['water_small']),
                                   pd.DataFrame([[60]], index=source_temperature.index,
                                                columns=['water_large'])], axis=1))


def cop_calc(delta_temp: float, heat_source_type: str = 'air') -> float:
    """
    Calculate the coefficient of performance (COP) for a given temperature difference.
    
    :param delta_temp: The temperature difference between the heat source and the heat sink.
    :param heat_source_type: The type of heat source being used. Defaults to 'air'.
    :return: The calculated coefficient of performance (COP).
    """
    return COP_PARAMS[heat_source_type][0] + COP_PARAMS[heat_source_type][1] * delta_temp + \
        COP_PARAMS[heat_source_type][2] * delta_temp ** 2


def build_cop_df(source_temperature: pd.Series, cap_value: int | None = None,
                 heat_source_type: str = 'air') -> pd.DataFrame:
    """
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
    """
    sink_temperature = compute_sink_temperature_from_source_temperature(source_temperature)

    delta_temperature = (sink_temperature.T - source_temperature).T
    # cap the delta temperature if cap_value is set
    if cap_value is not None:
        delta_temperature[delta_temperature < cap_value] = cap_value

    cop = delta_temperature.apply(lambda x: cop_calc(x, heat_source_type)) * CORRECTION
    cop.index.name = 't'
    return cop


def calculate_cop_tve(cop_df: pd.DataFrame, buildings: pd.DataFrame, space_heat: pd.DataFrame,
                      water_heat: pd.DataFrame) -> pd.DataFrame:
    """
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
    """

    # Determine heating type based on building Zensus/BBD year class:
    # if year class >6, floor. otherwise radiator.
    buildings['heating'] = np.where(buildings['year_class'] > 6, 'floor', 'radiator')

    cop_tve = pd.DataFrame()

    for bid in buildings.bid:
        # get the building type and heating type values
        building_type = buildings.loc[buildings['bid'] == bid]['building_type'].values[0]
        heating_type = buildings.loc[buildings['bid'] == bid]['heating'].values[0]
        space_heat_value = space_heat[f"bid_{bid}"]
        water_heat_value = water_heat[f"bid_{bid}"]

        if building_type in ['SFH', 'TH']:
            cop_water = cop_df['water_small']
        else:
            cop_water = cop_df['water_large']
        cop_space = cop_df[heating_type]
        try:
            cop_tve[f"bid_{bid}"] = (cop_space * space_heat_value + cop_water * water_heat_value) / (
                    space_heat_value + water_heat_value)
        except ZeroDivisionError:
            print(f"Zero division error for bid {bid}.")
            # cop_tve[f"bid_{bid}"] = 0

    cop_tve = cop_tve.bfill(axis=0).ffill(axis=0)
    return cop_tve


def build_cop_tve_profiles(buildings: pd.DataFrame, space_heat: pd.DataFrame, water_heat: pd.DataFrame,
                           source_temperature: pd.Series, cap_value: int | None = None,
                           heat_source_type: str = 'air') -> pd.DataFrame:
    """
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
    """
    print(f"Building COP heat pump air profiles for {len(buildings)} buildings.")
    cop_df = build_cop_df(source_temperature, cap_value, heat_source_type)
    cop_tve = calculate_cop_tve(cop_df, buildings, space_heat, water_heat)
    return cop_tve


def build_cop_tve_profiles_csv(area_id: str, buildings: pd.DataFrame, space_heat: pd.DataFrame,
                               water_heat: pd.DataFrame, source_temperature: pd.Series, cap_value: int | None = None,
                               heat_source_type: str = 'air') -> tuple[pd.DataFrame, str]:
    """
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
    """
    cop_tve = build_cop_tve_profiles(buildings, space_heat, water_heat, source_temperature, cap_value, heat_source_type)
    return cop_tve, save_heapump_air_to_csv(area_id, cop_tve)


def save_heapump_air_to_csv(area_id: str, cop_tve_df: pd.DataFrame) -> str:
    """
    Saves the COP (Coefficient of Performance) heat pump air data to a CSV file in the: py:const:`acept.acept_constants.TEMP_PATH` directory.

    :param area_id: The ID of the area COP data belongs to.
    :type area_id: str
    :param cop_tve_df: The DataFrame containing the heat pump air data.
    :type cop_tve_df: pd.DataFrame
    :return: The path to the saved CSV file.
    """
    temp_csv_output_path = os.path.join(TEMP_PATH, f"PLZ_{area_id}", f"heatpump_air_{area_id}.csv")
    os.makedirs(acept_utils.uppath(temp_csv_output_path, 1), exist_ok=True)

    # cop_df.to_csv(temp_csv_output_path, mode='w', sep=";", index=False, header=True)
    cop_tve_df.to_csv(temp_csv_output_path, mode='w', sep=",", index=False, header=True)
    return temp_csv_output_path
