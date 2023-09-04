:py:mod:`acept.buildings_information`
=====================================

.. py:module:: acept.buildings_information

.. autoapi-nested-parse::

   Module for adding and calculating information about the buildings in a GeoDataFrame.

   Use this module to add fields to a GeoDataFrame containing the buildings or calculating the shape around the buildings.

   The following fields are calculated and added to the GeoDataFrame:
       - bid: consecutive building number as ID
       - area: polygon area in m2
       - free_walls: free walls of the building, max: 4 walls
       - lat: latitude of the centroid in degrees
       - lon: longitude of the centroid in degrees
       - dist2hp: distance to the heat plant or a heat source in meters
       - construction: the class of the year of construction based on the Zensus data
       - year_class: the class of the year of construction based on the Zensus data as a numerical value
       - building_type: the typology of the building based on the Zensus data
       - size_class: the typology of the building based on the Zensus data as a numerical value
       - floors: the number of floors in the building
       - occupants: the number of occupants in the building
       - dwellings: the number of dwellings in the building
       - refurb_level_roof: the level of refurbishment of the roof (0, 1, or 2)
       - refurb_level_wall: the level of refurbishment of the walls (0, 1, or 2)
       - refurb_level_floor: the level of refurbishment of the floor (0, 1, or 2)
       - refurb_level_window: the level of refurbishment of the windows (0, 1, or 2)

   If the input GeoDataFrame already contains these fields, they will not be added them again.
   If there are fields with similar names as the calculated ones, the existing fields will be renamed to the expected
   names. If values are then still missing, they are calculated where possible.



Module Contents
---------------


Functions
~~~~~~~~~

.. autoapisummary::

   acept.buildings_information.calculate_missing_uhp_building_fields
   acept.buildings_information.calculate_bid
   acept.buildings_information.calculate_areas
   acept.buildings_information.calculate_free_walls
   acept.buildings_information.calculate_lat_lon
   acept.buildings_information.calculate_distance2hp
   acept.buildings_information.calculate_construction
   acept.buildings_information.calculate_year_class_from_construction
   acept.buildings_information.calculate_building_type
   acept.buildings_information.calculate_size_class
   acept.buildings_information.initialize_floors
   acept.buildings_information.initialize_occupants
   acept.buildings_information.initialize_dwellings
   acept.buildings_information.initialize_ref_level
   acept.buildings_information.calculate_shape_around_buildings



.. py:function:: calculate_missing_uhp_building_fields(buildings: geopandas.GeoDataFrame, debug: bool = True) -> tuple[geopandas.GeoDataFrame, bool]

   Calculates missing fields that are input to UrbanHeatPro.

   These are: bid, area, free_walls, lat, lon, dist2hp, construction, year_class, building_type, size_class, floors,
   occupants, dwellings, and the refurbishment levels.

   :param buildings: GeoDataFrame containing the buildings
   :param debug: Prints debug messages if True (default).
   :return: GeoDataFrame containing the buildings with missing fields added, and a flag indicating if any fields were
       added.


.. py:function:: calculate_bid(buildings: geopandas.GeoDataFrame)

   Adds field "bid" with a consecutive building number as id to the buildings GeoDataFrame.

   :param buildings: GeoDataFrame containing buildings.


.. py:function:: calculate_areas(buildings: geopandas.GeoDataFrame)

   Adds field "area" with the polygon area in m2 to the buildings GeoDataFrame or reuses the field footprint_area if it
   exists.

   :param buildings: GeoDataFrame containing buildings.


.. py:function:: calculate_free_walls(buildings: geopandas.GeoDataFrame)

   Adds field "free_walls" with the number of walls in direct contact with ambient temperature.

   It is assumed that all buildings have only four walls.

   :param buildings: GeoDataFrame containing buildings.


.. py:function:: calculate_lat_lon(buildings: geopandas.GeoDataFrame)

   Adds field "lat" and "lot" with the latitude and longitude values of the building centroid in degrees.

   If the (user defined fields) 'user_lat' and 'user_lon' exist, they are used

   :param buildings: GeoDataFrame containing buildings.


.. py:function:: calculate_distance2hp(buildings: geopandas.GeoDataFrame, default_value: int | float = 0, path_to_heat_plant_file: str | None = None, position_index_of_heat_plant: int = 0)

   Adds field "dist2hp" with the distance between building and heat plant.

   This can be done via the location of the heat plant (see shapefile) or if there is a user-defined distance in the
   field "user_dist_to_heat_source", this is used. If no heat plant is given and the field "user_dist_to_heat_source"
   does not exist or is empty, the default value is used.
   The heat plant location is given in a shapefile.

   :param buildings: GeoDataFrame containing buildings.
   :param default_value: Default distance to be used if the heat plant file or the specified index in it does not exist.
       Default: 0.
   :param path_to_heat_plant_file: Path to the shapefile containing the heat plant. If None, the default value is used.
   :param position_index_of_heat_plant: Index of the heat plant in the shapefile. Default: 0


.. py:function:: calculate_construction(buildings: geopandas.GeoDataFrame)

   Adds field "construction" with the construction year of the building or renames it if there already exists a field
   named "constructi" or "year.

   :param buildings: GeoDataFrame containing buildings.


.. py:function:: calculate_year_class_from_construction(buildings: geopandas.GeoDataFrame)

   Adds field "year_class" with the numerical year class of the construction year class. This is the classification
   used by the Zensus/BDB.

   :param buildings: GeoDataFrame containing buildings.


.. py:function:: calculate_building_type(buildings: geopandas.GeoDataFrame)

   Adds field "building_type" with the building type, or renames it if there already exists a field named "type",
   "btype" or "btype".

   :param buildings: GeoDataFrame containing buildings.


.. py:function:: calculate_size_class(buildings: geopandas.GeoDataFrame)

   Adds field "size_class" with the numerical size class corresponding to the building type. This classification
   is done independent of TABULAR classification (see EnvelopeArea_Residential.csv in UHP/input/Building Topology).
   Sets the building type to nan if no building type is given.

   :param buildings: GeoDataFrame containing buildings.


.. py:function:: initialize_floors(buildings: geopandas.GeoDataFrame)

   Adds the empty field "floor" with the number of floors in the building.

   :param buildings: GeoDataFrame containing buildings.


.. py:function:: initialize_occupants(buildings: geopandas.GeoDataFrame)

   Adds the empty field "occupants" with the number of occupants in the building.

   :param buildings: GeoDataFrame containing buildings.


.. py:function:: initialize_dwellings(buildings: geopandas.GeoDataFrame)

   Adds the empty field "dwellings" with the number of dwellings in the building. If there is already a field named
   "houses_per_building" it is renamed to "dwellings".

   :param buildings: GeoDataFrame containing buildings.


.. py:function:: initialize_ref_level(buildings: geopandas.GeoDataFrame, feature_name: str, default_value: int | None = None)

   Adds the field "ref_level_{feature_name}" with the reference level for the given feature.
   If there is already a field corresponding to the refurbishment level of the feature it is renamed to
   "ref_level_{feature_name}".

   :param buildings: GeoDataFrame containing buildings.
   :param feature_name: Name of the feature, must be 'roof', 'wall', 'window' or 'floor'.
   :param default_value: Value to use if there is no refurbishment level for the feature. Defaults to None.
   :raises ValueError: If feature_name is not 'roof', 'wall', 'window' or 'floor'.


.. py:function:: calculate_shape_around_buildings(buildings: geopandas.GeoDataFrame) -> geopandas.GeoDataFrame

   Calculate the shape around buildings in a GeoDataFrame.

   :param buildings: A GeoDataFrame containing the buildings.
   :return: The shape around the selected buildings in a GeoDataFrame.


