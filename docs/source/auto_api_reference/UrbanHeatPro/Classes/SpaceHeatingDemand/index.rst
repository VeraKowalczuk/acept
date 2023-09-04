:py:mod:`UrbanHeatPro.Classes.SpaceHeatingDemand`
=================================================

.. py:module:: UrbanHeatPro.Classes.SpaceHeatingDemand

.. autoapi-nested-parse::

   SpaceHeatingDemand.py
   A. Molar-Cruz @ TUM ENS



Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   UrbanHeatPro.Classes.SpaceHeatingDemand.SpaceHeatingDemand




.. py:class:: SpaceHeatingDemand(dt_vector, resolution, heated_area, Tamb, I, Tb0, dT_per_hour, eta, thermal_intertia, U, V, C, Tset, dTset, activity_vector, occupancy_vector, sh_prob, _solar_gains, _internal_gains, _night_set_back, schedule_nsb, T_nsb, power_reduction, window_areas, coords, debug)


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



