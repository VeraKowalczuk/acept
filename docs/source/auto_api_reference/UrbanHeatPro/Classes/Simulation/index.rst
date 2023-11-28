:py:mod:`UrbanHeatPro.Classes.Simulation`
=========================================

.. py:module:: UrbanHeatPro.Classes.Simulation

.. autoapi-nested-parse::

   Simulation.py
   A. Molar-Cruz @ TUM ENS



Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   UrbanHeatPro.Classes.Simulation.Simulation




.. py:class:: Simulation(NAME, SIMULATION, CITY, SPACE_HEATING, HOT_WATER, REPORTING)


   
   Initialize the UrbanHeatPro Simulation object.

   :param NAME: The name of the simulation.
   :type NAME: str
   :param SIMULATION: A list containing the simulation parameters.
   :type SIMULATION: list
   :param CITY: A list containing the city parameters.
   :type CITY: list
   :param SPACE_HEATING: A list containing the space heating parameters.
   :type SPACE_HEATING: list
   :param HOT_WATER: A list containing the hot water parameters.
   :type HOT_WATER: list
   :param REPORTING: A list containing the reporting options.
   :type REPORTING: list

   .. py:method:: run(include_date=True)

      Runs a complete simulation of N runs of the city heat demand.


   .. py:method:: create_city_object(run, result_dir_run)

      Creates instance of class City


   .. py:method:: read_input_data_csv()

      Returns input data in csv files as numpy arrays.


   .. py:method:: read_raw_building_data()

      Reads building data from csv file. Returns a pd.DataFrame.
      Columns are renamed to variables in UrbanHeatPro.


   .. py:method:: read_syn_city(filename)

      Reads existing syn city file


   .. py:method:: read_Tamb()

      Reads Tamb data from csv file. The file contains the Tamb values for the whole year
      in simulation resolution. Only the simulation timesteps are extracted.


   .. py:method:: read_I()

      Reads solar radiation data from csv file. The file contains I values [W/m2] for the whole year
      in simulation resolution in the form [I_Gh, I_Dh, I_ex, hs]. Only the simulation timesteps are extracted.


   .. py:method:: filter_weather_data()

      Filter weather data with timesteps vector with typical days


   .. py:method:: update_Tamb()

      Updates Tamb of City object according to the scenario to simulate


   .. py:method:: read_refurbishment_matrices()

      Reads refurbishment matrix for residential and non residential buildings
      for scenario simulated.


   .. py:method:: prepare_result_directory(include_date=True)

      Creates a time stamped directory within the result folder.
      Returns path as string.


   .. py:method:: read_data_from_csv(my_file, usecols=None)

      Uses numpy to read csv file and returns content as numpy array.
      Two rows of header are always skipped.


   .. py:method:: calculate_typical_days()

      Calculates typical days based on Tamb timeseries.
      Based on Nahmmacher et al. (2016), Carpe diem: A novel approach to select
      representative days for long-term power system modeling.


   .. py:method:: calculate_dt_vector()

      Calculates a vector of datetime objects based on the raw dt_matrix of the
      form [Y, M, D, h, m] and the simulation time steps.

      :returns: self.dt_vector  <list>      List of datetime objects


   .. py:method:: convert_datetime_to_excel_date(dt)

      Converts a datetime object to an excel date


   .. py:method:: plot_power(space_heating=True, hot_water=True, total=True)

      Plot min, max, and mean power values for each time step.


   .. py:method:: plot_energy(space_heating=True, hot_water=True, total=True)

      Plots histogram of aggregated heat demand for all simulations


   .. py:method:: save_csv_power()

      Saves heat demand timeseries in csv files (space heating, hot water and total).


   .. py:method:: save_csv_energy()

      Saves key building parameters and heat energy demand (space heating, hot water and
      total).



