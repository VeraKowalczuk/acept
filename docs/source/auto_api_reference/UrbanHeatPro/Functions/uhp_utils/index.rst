:py:mod:`UrbanHeatPro.Functions.uhp_utils`
==========================================

.. py:module:: UrbanHeatPro.Functions.uhp_utils


Module Contents
---------------


Functions
~~~~~~~~~

.. autoapisummary::

   UrbanHeatPro.Functions.uhp_utils.nested_get
   UrbanHeatPro.Functions.uhp_utils.access_config_or_default



.. py:function:: nested_get(input_dict: dict, nested_key: list, not_there='NotThere') -> Any

   Get value from nested dictionary given a list of nested keys and return default for missing keys.

   :param input_dict: Nested dictionary.
   :param nested_key: List of keys to access from outer dictionary to inner.
   :param not_there: Default value to be returned in case key does not exist
   :return: Value for the given list of keys. If a key is not available, then returns the default value.



.. py:function:: access_config_or_default(config: dict, default_config: dict, nested_key) -> Any

   Get the value for a given configuration parameter and use the default configuration value if the configuration
   parameter is not in the configuration there.

   :param config: Nested dictionary.
   :param default_config:
   :param nested_key: List of keys to access from outer dictionary to inner.
   :return: Configuration value for the given list of keys. If a key is not available, raises a KeyError.


