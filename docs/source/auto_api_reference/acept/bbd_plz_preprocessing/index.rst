:py:mod:`acept.bbd_plz_preprocessing`
=====================================

.. py:module:: acept.bbd_plz_preprocessing

.. autoapi-nested-parse::

   Module for the BBD shapefiles to PLZ mapping

   Use this module to:
       - read building data from BBD shapefiles (.shp) and calculate missing fields
       - build the mapping of the BBD shapefiles to post codes (PLZ)
       - lookup post codes (PLZ) in the mapping
       - query the BBD for the GeoDataFrame containing all buildings with the selected post code (PLZ)
       - save the BBD query result to a shape file in the /temp directory :py:const:`acept.acept_constants.TEMP_PATH`

   .. note::

      The BBD shapefiles are read from the :py:const:`acept.acept_constants.BBD_ROOT_DIR` directory. The modified BBD
      shapefiles are saved in the :py:const:`acept.acept_constants.BBD_WITH_PLZ_ROOT_PATH` directory.



Module Contents
---------------


Functions
~~~~~~~~~

.. autoapisummary::

   acept.bbd_plz_preprocessing.derive_bbd_output_path_from_filepath_shp
   acept.bbd_plz_preprocessing.read_building_data_from_shp
   acept.bbd_plz_preprocessing.calculate_plz
   acept.bbd_plz_preprocessing.calculate_plz_from_centroid
   acept.bbd_plz_preprocessing.build_plz_munc_id_db
   acept.bbd_plz_preprocessing.lookup_plz_in_mapping
   acept.bbd_plz_preprocessing.query_bbd_for_plz
   acept.bbd_plz_preprocessing.save_query_result_to_temp_shp
   acept.bbd_plz_preprocessing.compute_buildings_for_plz_shp
   acept.bbd_plz_preprocessing.compute_buildings_for_plz_to_uhp_csv



Attributes
~~~~~~~~~~

.. autoapisummary::

   acept.bbd_plz_preprocessing.VALID_BUILDING_USES
   acept.bbd_plz_preprocessing.NON_RES_BUILDING_USES


.. py:function:: derive_bbd_output_path_from_filepath_shp(output_base: str, filename: str) -> str

   Derives output file path for modified shape file (.shp) from input file path

   :param output_base: base directory path for modified shape files
   :param filename: path of input shape file
   :return: output path of modified shape file


.. py:function:: read_building_data_from_shp(parent_dir: str, filename_buildings: str, debug: bool = True) -> Tuple[str, geopandas.GeoDataFrame]

   Reads shapefile and calculates missing fields (bid, lat, lon, plz)

   Returns the modified shapefile and GeoDataFrame with missing fields added

   :param parent_dir: Path to the parent directory of the shapefile
   :param filename_buildings: Filename of the shapefile containing the buildings
   :param debug: Whether to print debug messages. Default is ``True``.
   :return: Path to the (modified) shapefile and (modified) GeoDataFrame containing the buildings


.. py:function:: calculate_plz(buildings: geopandas.GeoDataFrame, debug: bool = True) -> geopandas.GeoDataFrame

   Reads the PLZ shapefile and adds missing field (plz) to the buildings GeoDataFrame.

   :param buildings: GeoDataFrame containing buildings.
   :param debug: Whether to print debug messages. Default is ``True``.
   :return: Path to the (modified) shapefile and (modified) GeoDataFrame containing the buildings.


.. py:function:: calculate_plz_from_centroid(buildings: geopandas.GeoDataFrame, debug: bool = True) -> geopandas.GeoDataFrame

   Reads the PLZ shapefile and adds missing field (plz) to the buildings GeoDataFrame based on each building's
   centroid.

   :param buildings: GeoDataFrame containing buildings.
   :param debug: Whether to print debug messages. Default is ``True``.
   :return: Path to the (modified) shapefile and (modified) GeoDataFrame containing the buildings.


.. py:function:: build_plz_munc_id_db(debug: bool = True)

   Builds the mapping of the BBD shapefiles to post codes (PLZ) as a json file and updates the shapefiles with missing
   information. Calculates for all building shapefiles below the BBD root directory missing fields and saves the
   modified shapefiles.

   .. note::
       The BBD shapefiles are read from the :py:const:`acept.acept_constants.BBD_ROOT_DIR` directory. The modified BBD
       shapefiles are saved in the :py:const:`acept.acept_constants.BBD_WITH_PLZ_ROOT_PATH` directory.

   :param debug: Whether to print debug messages. Default is ``True``.


.. py:data:: VALID_BUILDING_USES
   :value: ['All', 'Residential', 'Industrial', 'Commercial', 'Public', 'Non-Residential']

   'All', 'Residential', 'Industrial',
   'Commercial', 'Public', 'Non-Residential'

   :type: Valid use types for buildings. 'All' selects all use types. Possible

.. py:data:: NON_RES_BUILDING_USES
   :value: ['Industrial', 'Commercial', 'Public']

   'Industrial', 'Commercial', 'Public'

   :type: Use types for non-residential buildings. Possible

.. py:function:: lookup_plz_in_mapping(plz: str | int) -> dict | None

   Make the lookup of the given PLZ in the saved mapping of PLZ -> paths to shape files.
   If there is no mapping to the PLZ None is returned.

   :param plz: PLZ to search.
   :return: Dictionary with information on the shape files with all buildings in of the PLZ.
       If there is no mapping to the PLZ None is returned.


.. py:function:: query_bbd_for_plz(plz: str, building_use: str = 'All', debug: bool = True) -> geopandas.GeoDataFrame

    Query the BBD for the GeoDataFrame containing all buildings with the selected post code (PLZ) and use type.
    Builds the mapping if is not yet there.

   :param plz: PLZ to search.
   :param building_use: Use type of the buildings, default: 'All' selects all use types. Possible: 'All',
       'Residential', 'Industrial', 'Commercial', 'Public', 'Non-Residential'.
   :param debug: default=True, give debug messages.
   :raise ValueError: if there is no data for the PLZ in the BBD
   :return: GeoDataFrame with the buildings with the selected post code (PLZ).


.. py:function:: save_query_result_to_temp_shp(plz: str, result_gdf: geopandas.GeoDataFrame, building_use: str = 'All', debug: bool = True) -> str

   Save the BBD query result to a shape file in the /temp directory.

   :param plz: PLZ to search.
   :param building_use: Use type of the buildings, default: 'All' selects all use types. Possible: 'All',
       'Residential', 'Industrial', 'Commercial', 'Public', 'Non-Residential'.
   :param result_gdf: GeoDataFrame with all buildings with PLZ and buildings use.
   :param debug: default=True, give debug messages.
   :return: File path to the BBD query result.


.. py:function:: compute_buildings_for_plz_shp(plz: str | int, building_use: str = 'All', debug: bool = True) -> str

   Query the BBD for all buildings with the selected post code (PLZ) and use type and save result to a shape file
   in the /temp directory.

   :param plz: PLZ to search.
   :param building_use: Use type of the buildings, default: 'All' selects all use types. Possible: 'All',
       'Residential', 'Industrial', 'Commercial', 'Public', 'Non-Residential'.
   :param debug: default=True, give debug messages.
   :return: Path to combined file of all buildings with PLZ and building use.


.. py:function:: compute_buildings_for_plz_to_uhp_csv(plz: str | int, building_use: str = 'All', debug: bool = True) -> str

   Query the BBD for all buildings with the selected post code (PLZ) and use type and save result to a .csv file
   in the format used by UrbanHeatPro in the /temp directory.

   :param plz: PLZ to search.
   :param building_use: Use type of the buildings, default: 'All' selects all use types. Possible: 'All',
       'Residential', 'Industrial', 'Commercial', 'Public', 'Non-Residential'.
   :param debug: default=True, give debug messages.
   :return: Path to combined file of all buildings with PLZ and building use


