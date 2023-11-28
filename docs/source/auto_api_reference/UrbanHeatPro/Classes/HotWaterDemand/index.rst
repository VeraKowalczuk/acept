:py:mod:`UrbanHeatPro.Classes.HotWaterDemand`
=============================================

.. py:module:: UrbanHeatPro.Classes.HotWaterDemand

.. autoapi-nested-parse::

   HotWaterDemand.py
   A. Molar-Cruz @ TUM ENS



Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   UrbanHeatPro.Classes.HotWaterDemand.HotWaterDemand




.. py:class:: HotWaterDemand(dt_vector, resolution, day_vector, seasonal_vector, activity_vector, Tw, daily_DHW, dhw_prob, hw_tank_capacity, hw_tank_limit, hw_tank_volume_t0, hw_flow, result_dir, use, year_class, btype, bid, debug, save_debug)


   
   HotWaterDemand class constructor

   :param dt_vector: Vector with datetime objects
   :param resolution: Resolution in min
   :param day_vector: Vector with day of year in simulation time frame
   :param seasonal_vector: Vector with seasonal variation
   :param activity_vector: Vector with building activity
   :param Tw: Supply temperature of water in degC
   :param daily_DHW: Mean daily hot water consumption [m3]
   :param dhw_prob: DWH-loads probability
   :param hw_tank_capacity: Hot water tank capacity in m3
   :param hw_tank_limit: Hot water tank limit in percentage
   :param hw_tank_volume_t0: State of hot water tank in m3
   :param hw_flow: Flow to refill hot water tank in L/min
   :param result_dir: Result directory
   :param use: Use of building
   :param year_class: Year class
   :param btype: Building type
   :param bid: Building id
   :param debug: Level of debug
   :param save_debug: Whether to save debug files

   .. py:method:: calculate()

      Calculates time series of domestic hot water demand in m3/min and W for the
      four dhw-load categories (0. Shower, 1. Bath, 2. Medium load and 3. Small load)
      for the whole simulation time.


   .. py:method:: calculate_dhw_consumption_in_time_step(time_step, dt_vector_index, day, day_in_year)

      Calculates hot water consumption events in every time step for the load categories:
          0   shower
          1   bath
          2   medium load
          3   small load

      :param time_step                   time step as datetime object:
      :param dt_vector_index             index of time step in simulation time frame dt_vector:
      :param day                                 number of day in day_vector:
      :param day_in_year                 number of day in year:
      :type day_in_year                 number of day in year: 1-366



