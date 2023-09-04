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



