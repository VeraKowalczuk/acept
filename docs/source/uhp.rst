The UrbanHeatPro dependency
===========================

.. include:: ../../deps/UrbanHeatPro/README.md
      :parser: myst_parser.sphinx_
      :start-after: (marker_text_start_description)
      :end-before: (marker_text_end_description)

Installation
------------
While UrbanHeatPro is a dependency of ``acept``, it is not installed as a normal dependency.
Instead it is included as a git submodule in the ``acept`` project and should be to be installed as an
editable package.

If the dependency is not yet installed, install UrbanHeatPro as an editable package for this project by running:

.. code-block:: console

  $ pip install -e deps/UrbanHeatPro

This allows to use the folder structure expected by UrbanHeatPro and use it from other packages.

To fetch updates from the remote repository, run:

.. code-block:: console

  $ git submodule update --init --recursive

For more information on installing UrbanHeatPro, see the ``README.md`` file in the ``deps/UrbanHeatPro`` folder.

.. seealso::
      :octicon:`mark-github;1em;fa fa-github` Repository: https://github.com/VeraKowalczuk/UrbanHeatPro


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
      As the original UrbanHeatPro project is not actively maintained, ACEPT uses a :octicon:`repo-forked;1em;fa fa-github` fork of the project.

      The :octicon:`repo-forked;1em;fa fa-github` fork includes:
        * bug fixes
        * support for configuration files
        * updated dependencies
        * the conversion to an installable package that can be used by other packages as a library
        * ...

.. seealso::
      *  :octicon:`mark-github;1em;fa fa-github` :octicon:`repo-forked;1em;fa fa-github` Fork: https://github.com/VeraKowalczuk/UrbanHeatPro
      *  :octicon:`mark-github;1em;fa fa-github` original UrbanHeatPro project: https://github.com/tum-ens/UrbanHeatPro
