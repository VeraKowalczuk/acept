:py:mod:`UrbanHeatPro.Functions.to_tuple`
=========================================

.. py:module:: UrbanHeatPro.Functions.to_tuple

.. autoapi-nested-parse::

   to_tuple.py
   A. Molar-Cruz @ TUM ENS



Module Contents
---------------


Functions
~~~~~~~~~

.. autoapisummary::

   UrbanHeatPro.Functions.to_tuple.building_use_to_tuple
   UrbanHeatPro.Functions.to_tuple.year_class_to_tuple
   UrbanHeatPro.Functions.to_tuple.size_class_to_tuple



.. py:function:: building_use_to_tuple(use)

   Map building use to tuple (use_int, use_str)

   :param use: building use as string or integer
   :returns: tuple (use_int, use_str)


.. py:function:: year_class_to_tuple(use_int, year_class_int)

   Map year class to tuple (year_class_int, year_class_str)

   :param use_int: building use as integer
   :param year_class_int: year class as integer
   :returns: tuple (year_class_int, year_class_str)


.. py:function:: size_class_to_tuple(use_int, size_class_int)

   Map size class to tuple (size_class_int, size_class_str)

   :param use_int: building use as integer
   :param size_class_int: size class as integer
   :returns: tuple (size_class_int, size_class_str)


