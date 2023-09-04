:py:mod:`acept.uhp_csv_io`
==========================

.. py:module:: acept.uhp_csv_io

.. autoapi-nested-parse::

   Module for writing and reading .csv files for Urban Heat Pro (UHP).

   UHP expects .csv files in one of the following two formats:

   .. code-block:: text

       information;on;the;file;content;...
       column1;column2;column3;column4;column5;...
       value1;value2;value3;value4;value5;...
       ...

   .. code-block:: text

       column1;column2;column3;column4;column5;...
       unit1;unit2;unit3;unit4;unit5;...
       value1;value2;value3;value4;value5;...
       ...

   Use this module to:
       - Write a DataFrame to a .csv file in the UHP format.
       - Read a .csv file in the UHP format and return a DataFrame.
       - Prepare the input .csv file with the buildings for UHP from a GeoDataFrame.
       - Save a GeoDataFrame with the buildings or a BBD query result to a .csv file in the format expected by UHP.

   For buildings the format of the .csv file is:

   .. code-block:: text

       field1;field2;field3;field4;field5;...
       value1;value2;value3;value4;value5;...
       ...

   Buildings have the following required columns:
       - bid: ID of the building
       - area: The size of the area in m2
       - use: Use type of the building as a number from 0 to 3
       - free_walls: Number of free walls of the building
       - lat: Latitude in degrees
       - lon: Longitude in degrees
       - dist2hp: Distance to the heat pump in m
   These additional columns are optional:
       - year_class: TABULAR construction year class of the building as a number
       - size_class: TABULAR size class of the building as a number
       - floors: Number of floors
       - occupants: Number of occupants
       - dwellings: Number of dwellings
       - ref_level_roof: Refurbishment level of the roof
       - ref_level_wall: Refurbishment level of the walls
       - ref_level_floor: Refurbishment level of the floors
       - ref_level_window: Refurbishment level of the windows
   The refurbishment level is a number from 1 to 3:
       - 1 = National minimum requirement
       - 2 = Improved standard
       - 3 = Ambitious standard



Module Contents
---------------


Functions
~~~~~~~~~

.. autoapisummary::

   acept.uhp_csv_io.write_geopandas_to_uhp_csv
   acept.uhp_csv_io.read_uhp_csv_to_dataframe
   acept.uhp_csv_io.prepare_buildings_for_uhp_csv
   acept.uhp_csv_io.save_buildings_to_temp_uhp_csv



.. py:function:: write_geopandas_to_uhp_csv(filepath: str, values_df: pandas.DataFrame, first_row_header: list, second_row_info: list = [], sep: str = ';') -> str

   Writes a DataFrame to a .csv file in the format expected by UHP.

   Writes a .csv file to the given path with a header row, an optional second row with additional information on the
   data (e.g. units), followed by the data.

   :param filepath: Path where to save the .csv file.
   :param values_df: DataFrame to save. The column names in the DataFrame are not written to the file.
       The order of the columns has to be the same as in the header rows.
   :param first_row_header: List of column names to be written to the first line of the file.
   :param second_row_info: Optional list of information for each column written to the second line of the file.
   :param sep: Column seperator in the .csv file. Default: ';'.
   :return: Path to the saved file.


.. py:function:: read_uhp_csv_to_dataframe(filepath: str, header_row: int | tuple[int, list] = 0, ignore_index: bool = True, additional_info: int | None = -1, sep: str = ';') -> tuple[pandas.DataFrame, list[Any]]

   Reads a .csv file in the format expected by UHP.

   Reads a .csv file with a header row, an optional second row with additional information on the data (e.g. units),
   and returns a DataFrame with the data and a list of additional information if requested.
   The column names are optionally renamed.

   :param filepath: Path to the .csv file.
   :param header_row: Row number of the header row, or a tuple with the row number and a list of new column names.
       Default: 0.
   :param ignore_index: If True, the index is ignored. Default: True
   :param additional_info: Optional Integer indicating the row number of the row with additional information.
       If negative, the additional information is ignored. If None, no additional information exists. Default: -1.
   :param sep: Column seperator in the .csv file. Default: ';'.
   :raises ValueError: If header_row is not an int or a tuple of the form (int, list)
   :return: DataFrame with the data, and a list of additional information if requested.


.. py:function:: prepare_buildings_for_uhp_csv(area_id: str | int, buildings: geopandas.GeoDataFrame, debug: bool = True) -> str

   Prepare buildings GeoDataFrame as input CSV for UrbanHeatPro.

   Add missing fields and map the values to the UHP format.
   Writes the result to a .csv file in the format used by UrbanHeatPro in the respective /temp directory.

   :param area_id: The area ID e.g. PLZ.
   :param buildings: The GeoDataFrame of buildings.
   :param debug: Whether to enable debug mode and print debug messages. Default: True.
   :raises ValueError: If the required column names are not in the buildings GeoDataFrame
   :return: The path to the saved UHP CSV file.


.. py:function:: save_buildings_to_temp_uhp_csv(plz_or_area_id: str, result_gdf: geopandas.GeoDataFrame, building_use: str = 'All', debug: bool = True) -> str

   Save the buildings or a BBD query result to a .csv file in the format used by UrbanHeatPro in the /temp directory.

   :param plz_or_area_id: The queried PLZ or the ID of the area the buildings belong to.
   :param building_use: Use type of the buildings in the BBD query, default: 'All' selects all use types. Possible: 'All',
       'Residential', 'Industrial', 'Commercial', 'Public', 'Non-Residential'.
   :param result_gdf: GeoDataFrame with all buildings in result_gdf.
   :param debug: Whether to enable debug mode and print debug messages. Default: True.
   :raises ValueError: if the required column names are not in the result_gdf
   :return: File path to the CSV file with the buildings.


