:py:mod:`acept.plz_shape`
=========================

.. py:module:: acept.plz_shape

.. autoapi-nested-parse::

   Module for accessing the PLZ shapes.

   Use this module to
       - get information about the PLZ areas.
       - calculate the centroid of the PLZ area for a given PLZ.
       - read the shape file containing the PLZ areas.
       - get the PLZ shape for a given PLZ.

   Note: The path to the shape file is defined in :py:const: `accept.config.PLZ_PATH`



Module Contents
---------------


Functions
~~~~~~~~~

.. autoapisummary::

   acept.plz_shape.read_plz_shapefile
   acept.plz_shape.get_single_plz_shape
   acept.plz_shape.calculate_centroid_of_plz



.. py:function:: read_plz_shapefile(plz_path: str = PLZ_PATH) -> geopandas.GeoDataFrame

   Reads shape file defining the PLZ areas and returns it as a GeoDataFrame.

   :param plz_path: path to the shapefile defining the PLZ areas. Default: :py:const: `accept.config.PLZ_PATH`
   :return: GeoDataFrame defining all PLZ areas in EPSG:4326


.. py:function:: get_single_plz_shape(plz: str) -> geopandas.GeoDataFrame

   Reads the PLZ shape file and returns the information of a given PLZ.

   :param plz: The PLZ to be searched.
   :return: GeoDataFrame containing the information of the given PLZ.


.. py:function:: calculate_centroid_of_plz(plz: str) -> shapely.Point

   Calculates the centroid of the PLZ area.

   :param plz: The PLZ to be searched.
   :return: The centroid of the PLZ area as a Point(lon, lat).


