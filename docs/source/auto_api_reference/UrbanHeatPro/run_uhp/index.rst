:py:mod:`UrbanHeatPro.run_uhp`
==============================

.. py:module:: UrbanHeatPro.run_uhp

.. autoapi-nested-parse::

   Run the UrbanHeatPro model.



Module Contents
---------------


Functions
~~~~~~~~~

.. autoapisummary::

   UrbanHeatPro.run_uhp.run_uhp



.. py:function:: run_uhp(selected_region: str = None, simulation_name: str = None, buildings_use_filter='', settings_file='../settings/uhp_settings_example.yaml', result_dir=None)

   Read the configuration file and run the UrbanHeatPro model.

   Use this function to run the UrbanHeatPro model from another python package,module or script.
   This function expects the default configuration file at ``../settings/uhp_default_settings.yaml``.
   The configuration file can be changed using the ``settings_file`` parameter.
   To make changes to the configuration of the model, change the values in the configuration file with the path specified
   in ``settings_file``.

   :param selected_region: Name or identifier of the region to be simulated, defaults to None
   :param simulation_name: Name of the simulation, defaults to `None`.
       If None, the name of the region is used.
   :param buildings_use_filter: Optional usetype identifier for the buildings file, defaults to ''
   :param settings_file: Path to the settings file, defaults to ``'../settings/uhp_settings_example.yaml'``
   :param result_dir: Path to the result directory, defaults to None. If None, the ``../results/`` directory is used.


