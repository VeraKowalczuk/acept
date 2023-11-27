The UrbanHeatPro dependency
===========================

.. include:: ../../deps/UrbanHeatPro/README.md
      :parser: myst_parser.sphinx_
      :start-after: (marker_text_start_description)
      :end-before: (marker_text_end_description)

Installation
------------

If the dependency is not yet installed, install UrbanHeatPro as an editable package for this project by running:

.. code-block:: console

  $ pip install -e deps/UrbanHeatPro

This allows to use the folder structure expected by UrbanHeatPro and use it from other packages.

To fetch updates from the remote repository, run:

.. code-block:: console

  $ git submodule update --init --recursive

For more information on installing UrbanHeatPro, see the ``README.md`` file in the ``deps/UrbanHeatPro`` folder.

.. seealso::
      :fab:`github` Repository: https://github.com/VeraKowalczuk/UrbanHeatPro


Repository folder structure & settings
--------------------------------------



.. dropdown:: Repository tree

      .. include:: file_trees/uhp_tree.rst
            :start-after: short_tree_uhp
            :end-before: explanation_of_the_tree

      .. dropdown:: Full repository structure

            .. include:: file_trees/uhp_tree.rst
                  :end-before: short_tree_uhp


.. include:: ../../deps/UrbanHeatPro/README.md
      :parser: myst_parser.sphinx_
      :start-after: (marker_text_start_folders_files)
      :end-before: (marker_text_end_folders_files)


Version used in ACEPT
---------------------

.. note::
      As the original UrbanHeatPro project is not actively maintained, ACEPT uses a fork of the project.

      The fork includes:
        * bug fixes
        * support for configuration files
        * updated dependencies
        * the conversion to an installable package that can be used by other packages as a library
        * ...

.. seealso::
      *  :fab:`github` Fork: https://github.com/VeraKowalczuk/UrbanHeatPro
      *  :fab:`github` original UrbanHeatPro project: https://github.com/tum-ens/UrbanHeatPro
