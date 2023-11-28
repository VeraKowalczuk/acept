:py:mod:`acept.exceptions`
==========================

.. py:module:: acept.exceptions

.. autoapi-nested-parse::

   Module for exceptions.



Module Contents
---------------

.. py:exception:: ValueOutsideRangeError(min_value: int, max_value: int, data_type: str = 'DWD TRY')


   Bases: :py:obj:`ValueError`

   Exception raised when a value is outside the allowed range.

   Initialize the exception, that will be raised when a value is outside the allowed range.

   :param min_value: minimum allowed value
   :param max_value: maximum allowed value
   :param data_type: name of the data type that is checked


