:py:mod:`UrbanHeatPro.Classes.City`
===================================

.. py:module:: UrbanHeatPro.Classes.City

.. autoapi-nested-parse::

   City.py
   A. Molar-Cruz @ TUM ENS



Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   UrbanHeatPro.Classes.City.City




.. py:class:: City(NAME, SIMULATION, CITY, SPACE_HEATING, HOT_WATER, REPORTING)


   City class.

   .. note::

      This documentation might be incomplete or outdated, check the source code for more information.
      The types for the attributes might not be correct.

   .. attribute:: name

      The name of the simulation.

      :type: str

   .. attribute:: region

      The region of the simulation.

      :type: str

   .. attribute:: sce

      The scenario of the simulation.

      :type: str

   .. attribute:: dt_vector

      Vector of time steps as datetime objects.

      :type: list

   .. attribute:: dt_vector_excel

      Vector of time steps as excel date.

      :type: list

   .. attribute:: nts

      Number of time steps.

      :type: int

   .. attribute:: resolution

      Temporal resolution in minutes.

      :type: int

   .. attribute:: number_of_typ_days

      Number of typical days.

      :type: int

   .. attribute:: weights

      Weights of typical days.

      :type: list

   .. attribute:: processes

      Number of parallel processes.

      :type: int

   .. attribute:: chunk_size

      Number of buildings in chunk to save.

      :type: int

   .. attribute:: b_to_save_syncity

      Array to save synchronicity data.

      :type: ndarray

   .. attribute:: b_to_save_heat

      Array to save heat data.

      :type: ndarray

   .. attribute:: counter_syncity

      Counter for synchronicity data.

      :type: int

   .. attribute:: counter_heat

      Counter for heat data.

      :type: int

   .. attribute:: Tamb

      Ambient temperature vector in degrees Celsius.

      :type: list

   .. attribute:: I

      Solar radiation vector in W/m2 [I_Gh, I_Dh, I_ex, hs].

      :type: list

   .. attribute:: buildings

      Building data.

      :type: list

   .. attribute:: building_stock_stats

      Building data from statistics.

      :type: list

   .. attribute:: nb

      Number of buildings.

      :type: int

   .. attribute:: connection_factor

      Share of buildings connected to the network.

      :type: float

   .. attribute:: _space_heating

      Flag to calculate space heating demand.

      :type: bool

   .. attribute:: _hot_water

      Flag to calculate hot water demand.

      :type: bool

   .. attribute:: _energy_only

      Flag to calculate only aggregated demand.

      :type: bool

   .. attribute:: base_load

      Vector of base load in W.

      :type: ndarray

   .. attribute:: _internal_gains

      Flag to consider internal gains.

      :type: bool

   .. attribute:: _solar_gains

      Flag to consider solar gains.

      :type: bool

   .. attribute:: _active_population

      Flag to consider active population for occupancy vector.

      :type: bool

   .. attribute:: _workday_weekend

      Flag to consider difference between workdays and weekends.

      :type: bool

   .. attribute:: _monthly_sh_prob

      Flag to consider monthly probability of using heating.

      :type: bool

   .. attribute:: refurbishment_level

      Refurbishment level for all buildings.

      :type: float

   .. attribute:: Tb0_str

      Initial building temperature as 'ambient' or 'Tset'.

      :type: str

   .. attribute:: dTset

      Delta temperature (for Tset_min, Tset_max).

      :type: float

   .. attribute:: eta

      Heating process efficiency.

      :type: float

   .. attribute:: dT_per_hour

      Maximum dT allowed in building per hour in degrees Celsius.

      :type: float

   .. attribute:: thermal_inertia

      Thermal inertia of the heating system.

      :type: float

   .. attribute:: _night_set_back

      Share of buildings with night set-back.

      :type: float

   .. attribute:: schedule_nsb

      [start, end] of night set-back in hours.

      :type: list

   .. attribute:: T_nsb

      Night set-back temperature in degrees Celsius.

      :type: float

   .. attribute:: power_reduction

      Percentage of power reduced (as decimal).

      :type: float

   .. attribute:: Tw

      Hot water temperature in degrees Celsius.

      :type: float

   .. attribute:: hw_tank_limit

      Hot water tank limit as percentage (decimal).

      :type: float

   .. attribute:: hw_flow

      Flow to refill hot water tank in L/min.

      :type: float

   .. attribute:: dhw_prob

      Probabilities for calculation of hot water demand.

      :type: list

   .. attribute:: rid

      Run id.

      :type: int

   .. attribute:: result_dir

      Directory where results are stored.

      :type: str

   .. attribute:: plot

      Plot level [0, 1, 2].

      :type: int

   .. attribute:: save

      Save level [0, 1, 2].

      :type: int

   .. attribute:: debug

      Debug level [0, 1, 2].

      :type: int

   Initializes the City object.

   :param NAME: Name of the simulation.
   :type NAME: str
   :param SIMULATION: List containing the parameters related to the simulation.
   :type SIMULATION: list
   :param CITY: List containing the parameters related to the city.
   :type CITY: list
   :param SPACE_HEATING: List containing the parameters related to space heating demand.
   :type SPACE_HEATING: list
   :param HOT_WATER: List containing the parameters related to hot water demand.
   :type HOT_WATER: list
   :param REPORTING: List containing the parameters related to reporting.
   :type REPORTING: list

   .. py:method:: create_synthetic_city()

      Create a synthetic city representing the building stock based on statistics.


   .. py:method:: update_synthetic_city(ref_matrix_res, ref_matrix_nres)

      Create a synthetic city representing the building stock based on statistics.


   .. py:method:: feed_building_to_process(feederQueue, buildings_list)

      Feeds building data to Queue


   .. py:method:: call_create_synthetic_building(feederQueue, writerQueue)

      Calls function to create synthetic building


   .. py:method:: call_update_synthetic_building(feederQueue, writerQueue)

      Calls function to update synthetic building.
      To update:
          - Refurbishment level


   .. py:method:: create_synthetic_building(building)

      Creates building object and calculates missing building properties


   .. py:method:: update_synthetic_building(building)

      Updates synthetic building.
      To update:
          - Refurbishment level


   .. py:method:: write_to_synthetic_city(writerQueue, filename)

      Write synthetic building results to file


   .. py:method:: calculate_city_heat_demand()

      Paralellizes the calculation of heating energy demand per building using a
      given number of processes. Every process modifies a shared dictionary where
      the heat demand is stored as power and energy.


   .. py:method:: call_calculate_building_heat_demand(feederQueue, writerQueue)

      Calls function to calculate building heat demand


   .. py:method:: calculate_building_heat_demand(building)

      Extracts building information needed to create a Building object.
      If the building is connected to the district heating network, then a Building
      object is created and the heat demand is calculted. If it is not, then the
      heat demand is set to zero.

      :param building    dataframe with building information:
      :param iii                 building counter:


   .. py:method:: create_building_object(building)

      Creates instance of class Object


   .. py:method:: write_to_city_heat_demand(writerQueue, filename)

      Writes building properties and heat demand to file


   .. py:method:: initialize_dhw_probabilities()

      Calculates dhw probabilities (daily consumption, event loads, flow rate and
      duration as interpolate objects.


   .. py:method:: calculate_seasonal_variation_vector(amplitude=0.1, max_point=45)

      Creates a sine wave representing the change of the nominal consumption during
      the year due to the seasonal variation.

      :param amplitude: Variation of consumption (% of nominal load)
      :type amplitude: float
      :param max_point: Day in year with the highest hot water consumption (lowest ambient temperature)
      :type max_point: int

      :returns: seasonal_vector     <numpy array>


   .. py:method:: calculate_day_vector()

      Calculates a vector of the days in the year included in the simulation
      time frame. Maximum length is 366.

      :returns:

                self.day_vector, list of day numbers in simulation time frame
                                        with start and end indices
      :rtype: list


   .. py:method:: calculate_min_vector()

      Calculates a vector of the simulation time steps in minutes of year. Maximum length is
      366*24*60.

      :returns: self.min_vector, list of time steps in minutes
      :rtype: list


   .. py:method:: plot_timeseries(space_heating=True, hot_water=True, total=True, xticks=('month', 3))

      


   .. py:method:: save_csv_syn_city_header(filename)

      Saves key building parameters of every chunk.


   .. py:method:: save_csv_energy_header(filename)

      Saves key building parameters of every chunk.


   .. py:method:: save_csv_power()

      Saves heat demand timeseries in csv file (space heating, hot water and total).


   .. py:method:: save_csv_energy()

      Saves aggregated heat demand in csv file (space heating, hot water and total).



