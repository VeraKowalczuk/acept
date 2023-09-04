:py:mod:`UrbanHeatPro.Functions.plot`
=====================================

.. py:module:: UrbanHeatPro.Functions.plot

.. autoapi-nested-parse::

   plot.py
   A. Molar-Cruz @ TUM ENS



Module Contents
---------------


Functions
~~~~~~~~~

.. autoapisummary::

   UrbanHeatPro.Functions.plot.plot_timeseries
   UrbanHeatPro.Functions.plot.plot_stacked_timeseries
   UrbanHeatPro.Functions.plot.plot_histogram
   UrbanHeatPro.Functions.plot.plot_histogram_table
   UrbanHeatPro.Functions.plot.plot_imshow_comparison
   UrbanHeatPro.Functions.plot.plot_typical_days



.. py:function:: plot_timeseries(dt_vector, timeseries, legend, fig_name, xticks=('month', 3), ynumticks='auto', ylabel='Power [kW]', ylim0=True, yfactor=1000.0)

   Plots timeseries as steps

   :param dt_vector: list of datetime objects
   :type dt_vector: list
   :param timeseries: timeseries to plot [ts1, ts2, ts3]
   :type timeseries: list
   :param legend: list of legends [leg1, leg2, leg3]
   :type legend: list
   :param fig_name: figure name
   :type fig_name: string
   :param xticks: Every X months/days/hours. Possible values:
                  ('month', X), ('day', X), ('hour', X)
   :type xticks: tuple
   :param ynumticks:
   :param ylabel:
   :param ylim0:
   :param yfactor:


.. py:function:: plot_stacked_timeseries(dt_vector, timeseries, legend, fig_name, xticks=('month', 3), ynumticks='auto', ylabel='Power [kW]', ylim0=True, yfactor=1000.0)

   Plots timeseries as steps

   :param dt_vector: list of datetime objects
   :type dt_vector: list
   :param timeseries: timeseries to stack [ts1, ts2]
   :type timeseries: list
   :param legend: list of legends [leg1, leg2, leg3]
   :type legend: list
   :param fig_name: figure name
   :type fig_name: string
   :param xticks: Every X months/days/hours. Possible values:
                  ('month', X), ('day', X), ('hour', X)
   :type xticks: tuple
   :param ynumticks:
   :param ylabel:
   :param ylim0:
   :param yfactor:


.. py:function:: plot_histogram(values, ylabel, fig_name, factor=1000.0, statistics=[])

   Plots simple histogram


.. py:function:: plot_histogram_table(use, thermal_property, title, fig_name, factor=1000.0, statistics=[], figsize=(30, 25))

   Plots a histogram showing the values of the thermal properties for all buildings in
   the city (only residential). A histogram per year construction class and building type
   is shown.


.. py:function:: plot_imshow_comparison(use, sim_stock, stat_stock, fig_name, cmap='RdBu')

   Shows a figure with two tables:
       Left    The distribution of residential buildings in the diff categories (year_class, btype)
               according to the statistics used to generate the synthetic building stock
       Right   The distribution of residential buildings in the diff categories (year_class, btype)
               in the synthetic building stock


.. py:function:: plot_typical_days(days_in_year, data_in_days, Z, number_of_clusters, min_distance_day, avg_day, clusters, clusters_per_month, month_names, timeseries_min, timeseries_avg, result_dir)

   Figures: calculation of typical days


