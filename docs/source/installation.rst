Installation
============

Prerequisites
-------------

Python 3.10

Repository
----------

To clone the repository from GitHub to a directory, run the following command:

.. code-block:: console

  $ git clone --recurse-submodules https://github.com/VeraKowalczuk/acept.git



On UNIX machines (Linux or macOS)
---------------------------------

Use the convenience setup script ``setup.sh`` for this project for UNIX based systems.
The script ...

1. Creates a new virtual environment (venv) for the acept project
2. Activates the virtual environment
3. Checks the python version. This should return ``.../venv/bin/python``
4. Installs the project requirements
5. Fetches additional dependencies and installs them:
  - The git submodule UrbanHeatPro in ``deps/UrbanHeatPro``

To run it, execute the following commands inside root directory of the repository:

.. code-block:: console

  $ ./setup.sh

Then activate the virtual environment:

.. code-block:: console

  $ source venv/bin/activate




On Windows machines
-------------------

It is recommended to use the Windows Subsystem for Linux (WSL).
Then the convenience script can also be used. Alternatively, follow the usual procedure on Windows
to ...

0. Navigate to the root directory of the cloned git repository of the ACEPT project
1. Create a new virtual environment

  .. code-block:: console

    $ python -m venv venv
2. Activate the virtual environment

  .. code-block:: console

      $ source venv/Scripts/activate
3. Install the project requirements

  .. code-block:: console

    $ pip install -e .
4. Fetch the additional dependencies or update the submodules

  .. code-block:: console

        $ git submodule update --init --recursive

5. Install the additional dependencies from the submodules

  .. code-block:: console

      $ pip install -e deps/UrbanHeatPro


Using conda
-----------
To use conda for the convenience script, you can modify the script to include the following steps or run them in order:

1. Create a new conda environment:

   .. code-block:: console

      $ conda create --name acept-env
2. Activate the conda environment:

   .. code-block:: console

      $ conda activate acept-env
3. Install the project requirements:

   .. code-block:: console

      $ pip install -e .
4. Fetch the additional dependencies:

   .. code-block:: console

      $ git submodule update --init --recursive
5. Install the additional dependencies:

  .. code-block:: console

      $ pip install -e deps/UrbanHeatPro

.. _As a package or library in used in other projects:

As a package or library in used in other projects
-------------------------------------------------

The project can be installed as a library or as a package in other projects.

We recommend integrating the project as a **git submodule** to your project. 

.. seealso::
      There is a guide on git submodules `here <https://git-scm.com/book/en/v2/Git-Tools-Submodules>`_.
      It explains how to add a git submodule to your project and how to use it.

This allows to use the folder structure expected by acept and use it from other packages.
Then follow these steps for installing the project as a editable package:

1. Go to the root directory of the cloned git repository of the ACEPT project

2. Install acept as an editable package:

   .. code-block:: console

      $ pip install -e .
3. Fetch the additional dependencies:

   .. code-block:: console

      $ git submodule update --init --recursive
4. Install the additional dependencies:

  .. code-block:: console

      $ pip install -e deps/UrbanHeatPro


As a developer working on the ``acept`` package
-----------------------------------------------

As a developer working on the ``acept`` package, it is recommended to install ``acept`` according to the guidelines above.
Additionally, the optional dependencies should be installed as follows:

.. code-block:: console

    $ pip install -e .[all]

This allows to also use the interactive notebooks of the project and build the documentation for the package.

After the installation
----------------------

Once the project is installed and you activated the created virtual environment, head to the :doc:`data_setup` section to find out
how to set up the data for the project and package and configure it for your needs.
