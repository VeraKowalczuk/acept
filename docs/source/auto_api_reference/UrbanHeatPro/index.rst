:py:mod:`UrbanHeatPro`
======================

.. py:module:: UrbanHeatPro


Subpackages
-----------
.. toctree::
   :titlesonly:
   :maxdepth: 3

   Classes/index.rst
   Functions/index.rst


Submodules
----------
.. toctree::
   :titlesonly:
   :maxdepth: 1

   run_uhp/index.rst


Package Contents
----------------


Functions
~~~~~~~~~

.. autoapisummary::

   UrbanHeatPro.access_config_or_default
   UrbanHeatPro.nested_get
   UrbanHeatPro.run_uhp



.. py:function:: access_config_or_default(config: dict, default_config: dict, nested_key) -> Any

   Get the value for a given configuration parameter and use the default configuration value if the configuration
   parameter is not in the configuration there.

   :param config: Nested dictionary.
   :param default_config:
   :param nested_key: List of keys to access from outer dictionary to inner.
   :return: Configuration value for the given list of keys. If a key is not available, raises a KeyError.


.. py:function:: nested_get(input_dict: dict, nested_key: list, not_there='NotThere') -> Any

   Get value from nested dictionary given a list of nested keys and return default for missing keys.

   :param input_dict: Nested dictionary.
   :param nested_key: List of keys to access from outer dictionary to inner.
   :param not_there: Default value to be returned in case key does not exist
   :return: Value for the given list of keys. If a key is not available, then returns the default value.



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


