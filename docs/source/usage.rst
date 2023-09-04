Usage
=====

To learn more about how to install and set up the project, go to the :doc:`installation` section followed by :doc:`data_setup`.

acept can be used standalone, as a library or a package as well as via the pylovo GUI.


Standalone
----------

The acept project can be used standalone.
Some examples how to use the project can be found in the :py:mod:`acept.examples` subpackage or in the Jupyter notebooks in the ``acept/acept_notebooks`` directory.
This includes:

* A simple example on how to use  ``acept`` to create a timeseries of the solar potential for a given area (:py:mod:`acept.examples.pv_cap_example`).
* Examples on how to use ``acept`` to create heat demand profiles for a given PLZ and year (:py:mod:`acept.examples.main_example`).
* Jupyter notebooks showcast how to use ``acept`` to...
    * create heat demand profiles for a collection of buildings.
    * create weather profiles for a given area or location.
    * analyse the performance of different ways to access the DWD TRY data.
    * find out more about the boundaries of the PLZ areas of Germany.
    * fill in missing fields for buildings.
    * build and use the BBD PLZ to municipality mapping.
    * and more.

To be able to run the Jupyter notebooks, please install the optional dependencies for interactive usage of the project.
To do so, use the following command in the root directory of the ``acept`` repository:

.. code-block:: console

    $ pip install -e .[interactive]

For more information on the API of the project, please refer to the :doc:`auto_api_reference/acept/index` API documentation.

As a library or package
-----------------------

The acept has to be installed before it can be used. We recommend using the 
section :ref:`As a package or library in used in other projects` in the :doc:`installation` guide.

To use the library or package, you need to import it:

.. code-block:: python

    import acept

Now you can use the acept package and all its modules in your project.
For more information on the API of the package, please refer to the :doc:`auto_api_reference/acept/index` API documentation.
There each module provides detailed information on the available functions, classes, 
and attributes as some examples.


Integration into the pylovo GUI
-------------------------------
The pylovo GUI is part of the pylovo project.

.. seealso:: 
    Please refer to the `pylovo documentation <https://pylovo.readthedocs.io>`_  for more information on the 
    pylovo project as well as the `pylovo GUI <https://pylovo.readthedocs.io/en/latest/docs_gui/index.html>`_ .

The functionality of ``acept`` was integrated into the pylovo GUI by adding it as a git submodule to the pylovo GUI.

The procedure to install the submodule as an editable package is the same as the instructions in section
:ref:`As a package or library in used in other projects` in the :doc:`installation` guide.
For the pylovo GUI, this involves the following commands in addition to the `pylovo GUI installation <https://pylovo.readthedocs.io/en/latest/docs_pylovo/installation.html>`_:

.. code-block:: console

  $ cd /path/to/pylovo/repository/root
  $ git submodule update --init --recursive
  $ pip install -e gui/acept
  $ pip install -e gui/acept/deps/UrbanHeatPro

The modified GUI supports the automatic generation of timeseries for each building in the network and adding the
generated timeseries to the configuration for ``urbs``.

.. Describe the main components and functionalities of the GUI
.. Walk users through the different sections and options available

Exploring the new GUI features
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The modified GUI is now available in the `pylovo GUI` and supports the following features:

* Automatic generation of timeseries for each building in the network.
* Assigning the generated timeseries to the buildings they belong to in the network.
* Adding the generated timeseries to the configuration for ``urbs``.
* Reuse of already generated timeseries if the same network is used multiple times.
* Resetting the selection of timeseries for each building in the network to the building-specific timeseries.

Find here a detailed guide on how to use the new GUI features:

.. toctree::
    :maxdepth: 2

    pylovo_gui




