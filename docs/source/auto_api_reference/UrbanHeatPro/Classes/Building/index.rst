:py:mod:`UrbanHeatPro.Classes.Building`
=======================================

.. py:module:: UrbanHeatPro.Classes.Building

.. autoapi-nested-parse::

   Building.py
   A. Molar-Cruz @ TUM ENS



Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   UrbanHeatPro.Classes.Building.Building




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



