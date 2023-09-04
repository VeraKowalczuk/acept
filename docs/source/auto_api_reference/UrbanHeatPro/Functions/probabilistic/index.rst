:py:mod:`UrbanHeatPro.Functions.probabilistic`
==============================================

.. py:module:: UrbanHeatPro.Functions.probabilistic

.. autoapi-nested-parse::

   probabilistic.py
   A. Molar-Cruz @ TUM ENS



Module Contents
---------------


Functions
~~~~~~~~~

.. autoapisummary::

   UrbanHeatPro.Functions.probabilistic.create_normal_distribution
   UrbanHeatPro.Functions.probabilistic.create_interpolated_cdf



.. py:function:: create_normal_distribution(x, mean, sigma)

   Returns a vector of len(x) values distributed normally around the specific
   mean and standard deviation sigma.


.. py:function:: create_interpolated_cdf(x, p)

   Returns the cumulative density function (cdf) as a vector of len(x) values
   given a probability function, p. The cdf interpolated in case the probability
   function has fewer values than the given x vector.


