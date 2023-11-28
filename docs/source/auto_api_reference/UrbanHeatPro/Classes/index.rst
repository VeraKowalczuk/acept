:py:mod:`UrbanHeatPro.Classes`
==============================

.. py:module:: UrbanHeatPro.Classes

.. autoapi-nested-parse::

   UrbanHeatPro
   A. Molar-Cruz @ TUM ENS



Submodules
----------
.. toctree::
   :titlesonly:
   :maxdepth: 1

   Building/index.rst
   City/index.rst
   HotWaterDemand/index.rst
   HotWaterDemand_D/index.rst
   Simulation/index.rst
   SpaceHeatingDemand/index.rst


Package Contents
----------------

Classes
~~~~~~~

.. autoapisummary::

   UrbanHeatPro.Classes.Building
   UrbanHeatPro.Classes.City
   UrbanHeatPro.Classes.HotWaterDemand
   UrbanHeatPro.Classes.Simulation
   UrbanHeatPro.Classes.SpaceHeatingDemand




.. py:class:: Building(b, building_stock_stats, dt_vectors, resolution, number_of_typ_days, weights, Tamb, I, _space_heating, _hot_water, _energy_only, Tb0_str, dTset, dT_per_hour, eta, thermal_inertia, _active_population, _workday_weekend, sh_prob, _solar_gains, _internal_gains, _night_set_back, schedule_nsb, T_nsb, power_reduction, Tw, dhw_prob, hw_tank_limit, hw_flow, day_vector, seasonal_vector, min_vector, result_dir, plot, save, debug)


   
   Initialize the Building object with the given parameters.

   :param b: Building dataframe
   :param building_stock_stats: Building stock statistics
   :param dt_vectors: Vector of time steps as datetime objects
   :param resolution: Temporal resolution in min
   :param number_of_typ_days: Number of typical days
   :param weights: Weights of typical days
   :param Tamb: Ambient temperature vector in degC
   :param I: Solar radiation vector in W/m2 [I_Gh, I_Dh, I_ex, hs]
   :param _space_heating: Calculate space heating demand?
   :param _hot_water: Calculate hot water demand?
   :param _energy_only: Calculate only aggregated demand?
   :param Tb0_str: Initial building temperature as string: 'ambient' or 'Tset'
   :param dTset: Delta temperature (for Tset_min, Tset_max)
   :param dT_per_hour: Maximum dT allowed in building per hour [degC]
   :param eta: Heating process efficiency
   :param thermal_inertia: Thermal inertia of the heating system
   :param _active_population: Consider active population for occupancy vector
   :param _workday_weekend: Consider dif between workdays and weekends
   :param sh_prob: Probability vector of using space heating
   :param _solar_gains: Consider solar gains?
   :param _internal_gains: Consider internal gains?
   :param _night_set_back: Share of buildings with nsb
   :param schedule_nsb: [start, end] of nsb in h
   :param T_nsb: Night set-back temperature in degC
   :param power_reduction: Percentage of power reduced (as decimal)
   :param Tw: Hot water temperature in [degC]
   :param dhw_prob: Probabilities for dhw-loads
   :param hw_tank_limit: Hot water tank limit as perc (decimal)
   :param hw_flow: Flow to refill hot water tank in L/min
   :param day_vector: Vector of days in simulation time frame
   :param seasonal_vector: Sinusoidal function for seasonal variations of DHW consumption
   :param min_vector: Vector of simulation time steps in minutes
   :param result_dir: Directory where results are stored
   :param plot: Whether to plot the results or not
   :param save: Whether to save the results or not
   :param debug: Whether to print debug information or not

   .. py:method:: calculate_space_heating_demand()

      Calculates building space heating demand as timeseries [W] and aggregated value [Wh]


   .. py:method:: calculate_hot_water_demand(save_debug=False)

      Calculates building hot water demand as timeseries [W] and [m3] and aggregated value [Wh].

      Only for residential buildings.

      :param save_debug: Is debug file saved?
      :type save_debug: boolean

      :returns: self.hot_water_m3
                self.hot_water_power
                self.dhw_energy


   .. py:method:: calculate_total_heat_demand()

      Agrregate the space heating and/or hot water demand time series.
      The total time series is delayed depending on the distance to the heat plant.


   .. py:method:: calculate_delayed_timeseries(flow_vel=1.0)

      Delays vector of heat demand depending on the distance of the building
      centroid to the (geothermal) heat plant. A flow velocity of 1 m/s in the district heating network is
      considered.


   .. py:method:: parametrize_building()

      Calculates missing building properties necessary for the heat demand calculation.


   .. py:method:: update_building_refurbishment_level(ref_matrix_res, ref_matrix_nres)

      Updates building refurbishment level based on desired refurbishment level
      from scenario and max percentage of refurbished buildings in region
      (MAX_REF_RES and MAX_REF_NRES).

      Refurbishment levels according to TABULA typology:
          - 1 National minimum requirement
          - 2 Improved standard
          - 3 Ambitious standard


   .. py:method:: categorize_building_residential()

      Probabilistic categorization building according to TABULA typologies.
      Construction year class and building type are calculated by comparing the residential
      building gross floor area (footprint_area) with the FOOTPRINT of typical buildings (from TABULA).
      Values are adapted to fit building stock statistics.


   .. py:method:: categorize_building_non_residential()

      Probabilistic categorization of non-residential buildings according to the
      building statistics and the following construction year classes:

      +-----+-------------------------+
      | int | construction year class |
      +=====+=========================+
      | 0   | < 1918                  |
      +-----+-------------------------+
      | 1   | 1919 - 1976             |
      +-----+-------------------------+
      | 2   | 1977 - 1983             |
      +-----+-------------------------+
      | 3   | 1984 - 1994             |
      +-----+-------------------------+
      | 4   | > 1995                  |
      +-----+-------------------------+

       >> Source for building stock missing


   .. py:method:: compute_current_refurbishment_level_residential()

      Computes the refurbishment level for the different building elements
      [roof, wall, floor, window] according to the current refurbishment statistics.

      Refurbishment levels according to TABULA typology:
          - 1 National minimum requirement
          - 2 Improved standard
          - 3 Ambitious standard


   .. py:method:: compute_current_refurbishment_level_non_residential()

      Computes the refurbishment level for the different building components
      [roof, wall, floor, window] according to the refurbishment statistics.

      Refurbishment levels according to TABULA typology:
          - 1 National minimum requirement
          - 2 Improved standard
          - 3 Ambitious standard

      >> Statistics on refurbishment in non-residential buildings missing


   .. py:method:: compute_scenario_refurbishment_level_residential(ref_matrix_res)

      Computes the refurbishment level for the different building elements
      [roof, wall, floor, window] according to the scenario refurbishment level
      per typology and the maximum share of refurbished buildings (MAX_REF_RES).

      Refurbishment levels according to TABULA typology:
          - 1 National minimum requirement
          - 2 Improved standard
          - 3 Ambitious standard


   .. py:method:: compute_scenario_refurbishment_level_non_residential(ref_matrix_nres)

      Computes the refurbishment level for the different building elements
      [roof, wall, floor, window] according to the scenario refurbishment level
      per typology and the maximum share of refurbished buildings (MAX_REF_NRES).

      Refurbishment levels according to TABULA typology:
          - 1 National minimum requirement
          - 2 Improved standard
          - 3 Ambitious standard


   .. py:method:: calculate_areas_residential()

      Calculate storey area and heated/conditioned area based on definitions
      from VDI 3807.


   .. py:method:: calculate_areas_non_residential()

      Calculate storey area and heated/conditioned area based on definitions
      from VDI 3807.


   .. py:method:: calculate_number_of_floors_residential()

      Calculates number of floors based on the TABULA typology.
      The number of floors calculated from TABULA are referenced to the conditioned
      or heated area but the number of floors are calculated using the storey area.


   .. py:method:: calculate_number_of_floors_non_residential(left=1, mode=2, right=3)

      Calculates number of floors as random sample number from the triangular
      distribution with lower limit left, peak at mode and upper limit right.

      >> Non-residential buildings are assumed to have two floors as mode and
          a maximum of three floors
          Source missing


   .. py:method:: calculate_number_of_dwellings()

      Calculates number of dwellings based on the building living area and mean dwelling size.
      It is assumed that SFH and TH have only 1 or 2 dwellings which is determined using the
      single-dwelling buildings statistics. For MFH and AB, the number of dweelings is calculated
      based on the average dwelling size.


   .. py:method:: determine_dwelling_size_category()

      Determine dwelling size category based on statistics
      https://ergebnisse.zensus2011.de/#StaticContent:091840148148,GWZ_4_3_2,m,table


   .. py:method:: calculate_number_of_occupants_residential()

      Calculates number of occupants based on household size and number of dwellings
      statistics.


   .. py:method:: calculate_number_of_occupants_non_residential(capacity=0.1)

      Calculates random number of occupants in the building based on the
      recommended area per person for different building types from
      https://www.engineeringtoolbox.com/number-persons-buildings-d_118.html.


   .. py:method:: get_building_thermal_properties_per_unit_area_residential()

      Gets building thermal properties from TABULA Web Tool data based on the
      building typology [year_class, btype]

      Sets the attributes:
          - list:     u: [u_roof, u_wall, u_floor, u_window] in W/(K m2)
          - list: v: [v_usage, v_infiltration] in 1/h
          - list:     c: [c_roof, c_wall, c_floor] in J/(K m2)


   .. py:method:: get_building_thermal_properties_per_unit_area_non_residential()

      Gets building thermal properties based on:
      >> source missing

      Sets the following attributes:
          - u list:   [u_roof, u_wall, u_floor, u_window] in W/(K m2)
          - v list:   [v_usage, v_infiltration] in 1/h
          - c list:   [c_roof, c_wall, c_floor] in J/(K m2)


   .. py:method:: calculate_building_envelope_areas_residential()

      Calculates building envelope areas (wall, roof and window).
      Residential: areas are calculated according to building typologies in TABULA.
      Only the heated area is considered.


   .. py:method:: calculate_building_envelope_areas_non_residential()

      Calculates building envelope areas (wall, roof and window).

      Non-residential: number of floors and window-to-wall ratio are
      derived from statistics and used to calculate the building areas.
      Only the heated area is considered.


   .. py:method:: calculate_building_window_areas()

      Calculate window areas in each direction to calculate solar gains.


   .. py:method:: calculate_building_thermal_properties()

      Calculates equivalent U-value, thermal capacitance (C) and time constant (Tau)
      for the building. These properties are used in the first order thermal model.


   .. py:method:: adjust_building_thermal_properties()

      Empirical adjustment of U-values to match TABULA results


   .. py:method:: calculate_building_Tset()

      Derives a target temperature by choosing a random temperature from Tset_mean
      +/- dT. Values differ for different building types.
      From http://tc76.org/spc100/docs/IBP%2018599/18599-10.pdf


   .. py:method:: calculate_building_active_hours()

      Assigns random start and end hours for building active hours.
      Values differ for different building types.

      Sets the following attributes:
          self.active_hours   list:           [(start0, end0), (start1, end1)] in h


   .. py:method:: calculate_daily_hot_water_demand()

      Returns the daily hot water demand by getting a random value
      from the cdf function based on the statistics from VDI 3807-3
      (specific dhw demand in m3/m2 of living area)


   .. py:method:: parametrize_hot_water_tank(X=1.5)

      Calculates size and initial state of hot water tank.
      Size is X times the calculated daily demand.


   .. py:method:: set_hot_water_tank_initial_state()

      


   .. py:method:: calculate_building_activity_occupancy_vector()

      Calculate vector of activity in building, i.e. percentage of occupied dwellings (for space heating)
      Active_hours (scheduled), building occupancy and weekends are considered


   .. py:method:: calculate_occupants_schedule()

      A schedule is assigned to every occupant based on studying/working schedule.

      Sets the following attributes:
          occupant_vector: list               = [dwelling, [occupant, [schedule]]] for occupant and dwelling in building


   .. py:method:: calculate_annual_demand(data)

      Calculate the annual energy demand by weighting the heating demand of typical days


   .. py:method:: plot_timeseries(space_heating=True, Tb=False, hot_water=True, total=True, xticks=('month', 3))

      Plots heat demand timeseries


   .. py:method:: save_csv()

      Saves key building parameters and heat demand (space heating, hot water and
      total) as timeseries.


   .. py:method:: save_load_duration_curve()

      Save sorted demand


   .. py:method:: save_dhw_debug_csv()

      Saves debug values for dhw demand.



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



.. py:class:: SpaceHeatingDemand(dt_vector, resolution, heated_area, Tamb, I, Tb0, dT_per_hour, eta, thermal_intertia, U, V, C, Tset, dTset, activity_vector, occupancy_vector, sh_prob, _solar_gains, _internal_gains, _night_set_back, schedule_nsb, T_nsb, power_reduction, window_areas, coords, debug)


   
   Initializes an instance of the SpaceHeatingDemand class.

   :param dt_vector: List of time steps as datetime objects.
   :param resolution: Resolution in minutes.
   :param heated_area: Heated area in square meters.
   :param Tamb: Ambient temperature vector in degrees Celsius.
   :param I: Solar radiation vector in W/m2.
   :param Tb0: Initial building temperature in degrees Celsius.
   :param dT_per_hour: Maximum change in temperature allowed per hour in degrees Celsius.
   :param eta: Heating process efficiency.
   :param thermal_intertia: Thermal inertia of the heating system.
   :param U: Building transmission losses in W/K.
   :param V: Building ventilation losses in W/K.
   :param C: Equivalent building thermal mass in J/K.
   :param Tset: Set temperature or target temperature in degrees Celsius.
   :param dTset: Delta temperature for Tset_min and Tset_max.
   :param activity_vector: Building activity vector (0, 1).
   :param occupancy_vector: Number of occupants in the building in each time step.
   :param sh_prob: Probability vector of using space heating.
   :param _solar_gains: Solar gains in W/m2.
   :param _internal_gains: Internal gains in W/m2.
   :param _night_set_back: Share of buildings with night set-back.
   :param schedule_nsb: Start and end of night set-back in hours.
   :param T_nsb: Night set-back temperature in degrees Celsius.
   :param power_reduction: Percentage of power reduced (as decimal).
   :param window_areas: Window area oriented to [E, S, W, N] in square meters.
   :param coords: (latitude, longitude) of the building centroid.
   :param debug: Debug flag.

   .. py:method:: calculate()

      Calculates the time series of space heating demand for a single building
      as the numerical solution of a first order building thermal model (1R1C).
      Transmission and ventilation losses through infiltration are included.

      :returns: self.Tb
                self.sh_power
                self.internal_gains
                self.solar_gains


   .. py:method:: calculate_Tset(iii)

      Returns Tset to original value or recalculates it depending on night set-back


   .. py:method:: calculate_flags(iii)

      Calculates if heating system is active based on building temperature and building occupancy


   .. py:method:: calculate_internal_gains(iii)

      Calculates heat gain in time step due to the activeness of the occupants:
          - 80 W/occupant during the night (23:00 to 6:00)
          - Random between 100 - 125 W/occupant for the rest of the day
      From Validation of RC Building Models for Application in Energy and DSM (Kuniyoshi, 2017)
      EESC Kramer
      [VDI 2078]

      :returns: self.internal_gains[iii]: Heat gain in W
      :rtype: float


   .. py:method:: calculate_solar_gains(iii, RED_FACTORS, ORIENTATION)

      Calculates solar gains based on the windows size and orientation.
      Method adapted from TABULA

      :returns: self.solar_gains[iii]: Heat gain in W
      :rtype: float


   .. py:method:: calculate_incident_solar_irradiation(day_of_year, hour, I_Gh, I_Dh, I_ex, hs, lat, lon, slope, orientation)

      Calculates the global incident solar irradiation on tilted surface in W/m2.
      Based on HDKR radiation model (anisotropic model) from
      High-resolution spatio-temporal matching of residential electricity consumption and
      PV power production at the urban scale (Molar-Cruz, 2015)

      :param I_Gh: Global horizonal radiation in W/m2
      :type I_Gh: float
      :param I_Dh: Diffuse horizontal radiation in W/m2
      :type I_Dh: float
      :param I_ex: Extraterrestrial solar radiation in W/m2
      :type I_ex: float
      :param hs: Sun elevation angle in deg
      :type hs: float
      :param lat: Latitude in degrees
      :type lat: float
      :param lon: Longitude in degrees
      :type lon: float
      :param slope: Inclination angle of window. Vertical = 90 deg
      :type slope: int
      :param orientation: Window orientation
      :type orientation: int

      :returns: I_Gt: Incident global solar radiation on tilted surface
      :rtype: float



