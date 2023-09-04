:py:mod:`acept.demand_profiles`
===============================

.. py:module:: acept.demand_profiles

.. autoapi-nested-parse::

   Module for building demand profiles.

   Use this module to create demand profiles for the selected area and buildings using UrbanHeatPro.

   This module is the interface to the UrbanHeatPro project (https://github.com/VeraKowalczuk/UrbanHeatPro) that is a
   dependency for the ACEPT project and is integrated to the ACEPT project as a submodule in /deps/UrbanHeatPro.



Module Contents
---------------


Functions
~~~~~~~~~

.. autoapisummary::

   acept.demand_profiles.run_uhp_for_selected_buildings_year



.. py:function:: run_uhp_for_selected_buildings_year(plz_or_region: int | str, buildings: geopandas.GeoDataFrame = None, year: int | None = 2011, temperature_profile: str = None, demand_unit: str = 'W') -> dict[str, str | pandas.DataFrame]

   Creates demand profiles for the selected area and buildings using UrbanHeatPro.

   :param plz_or_region: PLZ or Region for which the demand profile should be created (area ID).
   :param buildings: GeoDataFrame of the selected buildings.
   :param year: Year for which the demand profile should be created. Defaults to 2011. If None, the temperature profile
       for the typical meterological year (TMY) will be used.
   :param temperature_profile: Path to the temperature profile. If None, the temperature profile is expected at the
       default location according to the year and plz_or_region.
   :param demand_unit: Unit of the demand. Defaults to 'W'. Valid values are 'W', 'Wh', 'kW', 'kWh', 'MW', and 'MWh'.
       As the timeseries have hourly resolution, the values of 'W' and 'Wh' are equivalent.
   :return: A dictionary containing the paths to the demand profiles and the dataframes containing the profiles.


