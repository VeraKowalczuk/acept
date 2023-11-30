:py:mod:`acept.examples.main_example`
=====================================

.. py:module:: acept.examples.main_example

.. autoapi-nested-parse::

   Main example for building the scenario profiles for a given PLZ and year.

   To run the example use the following command with the venv activated:

   .. code-block:: console

       $ source venv/bin/activate
       $ cd src/acept
       $ python examples/main_example.py




Module Contents
---------------


Functions
~~~~~~~~~

.. autoapisummary::

   acept.examples.main_example.build_scenario_profiles_for_plz_year



Attributes
~~~~~~~~~~

.. autoapisummary::

   acept.examples.main_example.plz_cli


.. py:function:: build_scenario_profiles_for_plz_year(plz: int, year: int = 2011) -> dict

   Build the scenario profiles for the given input

   The scenario profiles are built for the temperature profile and the PV capacity factor profiles
   The scenario profiles are saved in the :py:const:`acept.acept_constants.TEMP_PATH` directory

   :param plz: PLZ to search
   :param year: year to use for the scenario profiles
   :return: The paths to the created scenario profiles in a dictionary


.. py:data:: plz_cli
   :value: 91126

   

