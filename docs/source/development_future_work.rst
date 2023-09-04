Further development opportunities
=================================

Unfortunately, ``acept`` does not yet support the automation of generating all different input data for ``urbs``.

In the pylovo GUI, additional functionality can be developed in the following
ways:

* Automatic fill in of the building information in the *Building* tab with information from
    * the building database
    * the building database in combination with using the :py:mod:`acept.buildings_information` module to fill in missing
      building fields
    * the ``UrbanHeatPro`` synthetic buildings equivalent to the selected buildings in the network:
          * UrbanHeatPro fills in the missing information based on statistics and returns the updated synthetic buildings in a csv file.
          * Be aware of the different meaning of the ``UrbanHeatPro`` building fields, e.g. the 'year_class' field in ``UrbanHeatPro`` is a number based
            on the TABULAR classification, which differs from the information in the building database.
          * Either fill in only the missing information or overwrite all user input in the *Building* tab after generating
            the synthetic buildings with ``UrbanHeatPro``.
* Generation of timeseries for the other demands in the *Demand* tab:
    * Generation of timeseries for the electricity demands (electricity, electricity-reactive).
    * Generation of timeseries for the mobility demand.
* Generation of timeseries for the other demands in the *Time variable efficiency* tab (TVE):
    * Generation of timeseries for charging stations.
    * Generation of timeseries for Heatpump Air Heizstrom.
* Using user-defined input from the *Building* tab to adjust the input of the ``UrbanHeatPro`` synthetic
  buildings.
    * Modify the functions in the :py:mod:`acept.buildings_information` module to use user-defined
      inputs, e.g. the ``year_class`` field or the ``size_class`` field (in ``acept`` these fields have the prefix ``'user_'``).


Already provided functionality to support new features
------------------------------------------------------

To ease the development of new features, the new pylovo GUI provides the following
functionality:

* Loading data from dynamically added timeseries in the *Demand* (D), *Time variable efficiency* (TVE), or *Intermittent Supply* (SupIm):
    * The JavaScript module :js:mod:`urbs_editor.support_profile_generation` in ``pylovo`` can be used to load data from timeseries, that
      are dynamically generated in the backend for each building in the network, into the GUI.
    * As an example on how to integrate data from dynamically generated timeseries specific to the buildings in the
      network into the GUI, use...
        * the function :js:func:`urbs_editor.timevareff_editor.generateHeatpumpAirProfiles` in the :js:mod:`urbs_editor.timevareff_editor`
          JavaScript module
            * This function showcases how to fetch generated data for a single feature.
        * the function :js:func:`urbs_editor.demand_editor.generateHeatDemandProfiles` in the :js:mod:`urbs_editor.demand_editor`
          JavaScript module:
            * This function showcases how to fetch generated data for multiple features.
    * The functions for the routes of the urbs editor that generate timeseries data and return it to the frontend can be
      found in the :py:mod:`urbs_editor.routes` module in the :py:mod:`maptool.urbs_editor` of ``pylovo``.
        * Use these as example how to integrate the generation of other building-specific timeseries into the pylovo GUI.
        * This typically involves the following steps:
            * retrieving the building data from the database and the frontend
            * checking if the timeseries are already generated for the selected buildings
            * if yes, return the existing timeseries to the frontend
            * if not, generate the timeseries for the selected buildings and return them to the frontend
            * also add the generated timeseries to the available timeseries in the pandapower2urbs dataset by appending
              the generated timeseries to the pre-defined timeseries (in the ``pandapower2urbs_dataset_template`` directory) and saving the
              updated dataset in the respective csv file.