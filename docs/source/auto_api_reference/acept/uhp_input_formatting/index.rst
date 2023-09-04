:py:mod:`acept.uhp_input_formatting`
====================================

.. py:module:: acept.uhp_input_formatting

.. autoapi-nested-parse::

   Module for input formatting for UrbanHeatPro (UHP) and mapping of data to the values expected by UHP.

   Use this module to prepare the input data for UHP. This includes:
       - mapping of data to the values expected by UHP
       - mapping the building use type to their numerical values
       - mapping the construction year to the tabular construction year class
       - mapping the tabular construction year class to their numerical values
       - mapping the size class to their numerical values
       - mapping the refurbishment levels to their numerical values as in UHP

   When using this module, make sure to call:
       - the function :py:func:`map_building_use_types_to_numbers` before :py:func:`map_construction_year_to_tabular_construction_year_class`.
       - the function :py:func:`map_construction_year_to_tabular_construction_year_class` before :py:func:`map_tabular_construction_year_class_to_numbers`.



Module Contents
---------------


Functions
~~~~~~~~~

.. autoapisummary::

   acept.uhp_input_formatting.map_building_use_types_to_numbers
   acept.uhp_input_formatting.map_building_types_to_numeric_size_class
   acept.uhp_input_formatting.map_construction_year_to_tabular_construction_year_class
   acept.uhp_input_formatting.map_tabular_construction_year_class_to_numbers
   acept.uhp_input_formatting.map_refurbishment_levels_to_uhp_format



.. py:function:: map_building_use_types_to_numbers(buildings: geopandas.GeoDataFrame)

   Maps the buildings use type to their numerical values as in UHP and writes this into the "use" field of the
   buildings GeoDataFrame.

   :param buildings: GeoDataFrame with the buildings


.. py:function:: map_building_types_to_numeric_size_class(buildings: geopandas.GeoDataFrame)

   Maps the buildings type to their numerical values as in UHP and writes this into the "size_class" field of the
   buildings GeoDataFrame.

   :param buildings: GeoDataFrame with the buildings


.. py:function:: map_construction_year_to_tabular_construction_year_class(buildings: geopandas.GeoDataFrame)

   Maps the Zensus/BDB construction year classes to the TABULAR year classes as used in UHP.

   As there is no direct mapping, the construction year is mapped to the nearest tabular year class.

   :param buildings: GeoDataFrame with the buildings


.. py:function:: map_tabular_construction_year_class_to_numbers(buildings: geopandas.GeoDataFrame)

   Maps the TABULAR year classes to their numerical values as in UHP and writes this into the "year_class" field of the
   buildings GeoDataFrame. If the year_class field already exists, it is saved in the "year_class_zensus" field.

   :param buildings: GeoDataFrame with the buildings


.. py:function:: map_refurbishment_levels_to_uhp_format(buildings: geopandas.GeoDataFrame)

   Maps the refurbishment levels to their numerical values as in UHP and writes this into the 'ref_level_{type}' fields
   of the buildings GeoDataFrame (for types:'floor', 'wall', 'roof', 'window').

   :param buildings: GeoDataFrame with the buildings


