# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join('..', '..', 'src')))
sys.path.insert(0, os.path.abspath(os.path.join('..', '..', 'deps', 'UrbanHeatPro', 'UrbanHeatPro')))


# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'acept'
copyright = '2023, Vera Kowalczuk'
author = 'Vera Kowalczuk'
release = '2023'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "myst_parser",
    'sphinx.ext.autodoc',
    # 'sphinx.ext.autosummary',
    "sphinx_autodoc_typehints",
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
    # 'sphinx_rtd_theme',
    # 'sphinx_rtd_size',
    'sphinx_design',
    'sphinx.ext.napoleon',
    'autoapi.extension'
    ]

intersphinx_mapping = {'python': ('https://docs.python.org/3', None),
                       'pandas': ('https://pandas.pydata.org/pandas-docs/stable', None),
                       'numpy': ('https://numpy.org/doc/stable', None),
                       'xarray': ('https://docs.xarray.dev/en/stable', None),
                       'geopandas': ('https://geopandas.org/en/stable', None),
                       'shapely': ('https://shapely.readthedocs.io/en/stable', None),
                       'cartopy': ('https://scitools.org.uk/cartopy/docs/latest', None),
                       'scipy': ('https://docs.scipy.org/doc/scipy/reference', None),
                       'matplotlib': ('https://matplotlib.org/stable', None),
                       'rioxarray': ('https://corteva.github.io/rioxarray/stable', None),
                       'setuptools': ('https://setuptools.pypa.io/en/latest', None),
                       }

# typehints options
typehints_use_rtype = False
typehints_use_signature = True
typehints_use_signature_return = True

# autodoc options
autodoc_typehints = "both"
# autodoc/autosummary options
# autosummary_generate = True  # Turn on sphinx.ext.autosummary
# autoclass_content = "both"  # Add __init__ doc (ie. params) to class summaries
# autosummary_generate_overwrite = False

autoapi_type = 'python'
autoapi_dirs = ['../../src', '../../deps/UrbanHeatPro/UrbanHeatPro/']
autoapi_generate_api_docs = True
autoapi_member_order = 'bysource'
autoapi_add_toctree_entry = False
autoapi_root = 'auto_api_reference'
autoapi_keep_files = True
autoapi_template_dir = "_templates/autoapi"
autoapi_python_class_content = "both"


myst_enable_extensions = ["colon_fence"]

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_css_files = [
    'custom.css',
    # "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.1/css/all.min.css"
]


