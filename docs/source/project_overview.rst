Project overview
================


Background
----------

The urgent need for a rapid transition towards locally sourced, decarbonized heat supply, especially at the building 
level, is evident from climate goals and recent political developments. 
Unlike in electricity system planning, where decisions are typically made in a top-down manner 
through the deployment of large-scale power system components, the heating sector requires a 
bottom-up approach due to the diverse building stock, existing heating systems, and local 
renewable resource availability. 
As a result, various regulatory bodies are working on communal heat planning guidelines, to facilitate 
individualized decision-making at the district or building level.

To address this challenge, the project *Energy – Sector Coupling and Microgrids*, in short *STROM*, aims to develop a digital, 
automated energy supply planning tool. This tool will utilize local data such as 
renewable resource potentials, energy demand, and a distribution grid topology for an
arbitrary district. 

The tool consists of two key components:

- ``pylovo``, a module that generates synthetic distribution grids for a user-defined research area
- the optimization framework ``urbs``, which is a linear programming model for multi-commodity
  energy systems. The primary objective of ``urbs`` is on determining optimal storage
  sizes and utilization.

By leveraging the ``urbs`` optimization framework, the tool conducts a multi-sector, system-scale cost optimization
to determine optimal transition pathways for meeting the energy demands of the district,
thereby assisting decision-making processes.

.. seealso::
    - ``urbs``: Please refer to the `urbs documentation <https://urbs.readthedocs.io>`_, or find the project on :octicon:`mark-github;1em;fa fa-github` `Github <https://github.com/tum-ens/urbs>`_
    - ``pylovo``: Please refer to the `pylovo documentation <https://pylovo.readthedocs.io>`_, or find the project on `Gitlab LRZ <https://pylovo.readthedocs.io/en/latest/>`_


The aim of the ACEPT project is to automate the process of sourcing input data for ``urbs``.
Additionally, it was integrated into the GUI of ``pylovo``, that allows a user to quickly visualize different grids and set parameters as well as results of the optimization of said grids

The ACEPT project is part of a Interdisciplinary Project (IDP) at the 
Chair of Renewable and Sustainable Energy Systems at the Technical University of Munich (TUM).

Features of acept
-----------------

Since the available data on buildings does not necessarily contain all needed information on the building,
``acept`` can be used to complement the existing data on buildings with additional knowledge.

There are a number of timeseries data sets that are needed as a input for ``urbs``.
These timeseries contain hourly data for one year. Since these timeseries are a describe a 
characteristic for a research area or equipment, we call them "profiles" for short.

``acept`` provides support to create such timeseries profiles for...

* the typical weather for a location or area,
* the ambient temperature for a location or area,
* heat demand profiles for all buildings in a specified area and the the area as a whole,
* solar profiles, that give the PV capacity factor for all buildings in a specified area,
* the Coefficient of Performance (COP) for heat pumps,
* ...

To calculate the heat demand profiles, ``acept`` leverages an upgraded version of the existing 
tool ``UrbanHeatPro``. For more information on this tool, please refer to the 
section :doc:`uhp`, the :doc:`auto_api_reference/UrbanHeatPro/index` API documentation, or find the project on :octicon:`mark-github;1em;fa fa-github`
`Github <https://github.com/VeraKowalczuk/UrbanHeatPro>`_.


Repository structure
--------------------


.. dropdown:: Repository structure
    :open:

      .. include:: file_trees/acept_tree.rst
            :start-after: short_tree_acept

      .. dropdown:: Full repository structure

            .. include:: file_trees/acept_tree.rst
                  :start-after: full_tree_acept
                  :end-before: short_tree_acept


* The ``data`` directory holds various data files and subdirectories such as weather data from the Deutscher Wetterdienst (DWD), 
  shape files for federal states and PLZ areas in Germany, and mapping data for PLZ areas. 
* The ``deps`` directory contains dependencies as git submodules, including the UrbanHeatPro submodule. 
* The ``docs`` directory contains documentation files, including the source files, build files, and configuration files 
  for generating the documentation. 
* The ``settings`` directory holds settings files for the UrbanHeatPro module. 
* The ``src`` directory contains the source code for the acept project, organized into subdirectories such as 
  notebooks for Jupyter usage, examples of using acept, and modules for various functionalities like preprocessing shapefiles, 
  calculating COP profiles, handling DWD TRY data, creating heat demand profiles, and more.
* The ``temp`` directory is used to store temporary files and outputs of the project.



