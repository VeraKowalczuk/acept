:py:mod:`UrbanHeatPro.Classes.HotWaterDemand_D`
===============================================

.. py:module:: UrbanHeatPro.Classes.HotWaterDemand_D

.. autoapi-nested-parse::

   HotWaterDemand_D.py
   A. Molar-Cruz @ TUM ENS



Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   UrbanHeatPro.Classes.HotWaterDemand_D.HotWaterDemand_D




.. py:class:: HotWaterDemand_D(resolution, day_vector, Tw, daily_DHW)


   
   Initializes the HotWaterDemand class with the given parameters.

   :param resolution: The resolution of the simulation in minutes.
   :param day_vector: A list of integers representing the day of the year in the simulation time frame.
   :param Tw: The supply temperature of water in degrees Celsius.
   :param daily_DHW: The mean daily hot water consumption in cubic meters.

   .. py:method:: calculate()

      Calculates aggregated hot water demand



