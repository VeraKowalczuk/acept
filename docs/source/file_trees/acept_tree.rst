
.. full_tree_acept

.. code-block:: text

    📦acept
    ┣ 📂data
    ┃ ┣ 📂dwd
    ┃ ┃ ┗ 📂try_bavarian
    ┃ ┃ ┃ ┣ 📜TRY_201201.nc
    ┃ ┃ ┃ ┣ 📜TRY_201202.nc
    ┃ ┃ ┃ ┣ 📜TRY_201203.nc
    ┃ ┃ ┃ ┣ 📜TRY_201204.nc
    ┃ ┃ ┃ ┣ 📜TRY_201205.nc
    ┃ ┃ ┃ ┣ 📜TRY_201206.nc
    ┃ ┃ ┃ ┣ 📜TRY_201207.nc
    ┃ ┃ ┃ ┣ 📜TRY_201208.nc
    ┃ ┃ ┃ ┣ 📜TRY_201209.nc
    ┃ ┃ ┃ ┣ 📜TRY_201210.nc
    ┃ ┃ ┃ ┣ 📜TRY_201211.nc
    ┃ ┃ ┃ ┗ 📜TRY_201212.nc
    ┃ ┣ 📂fed_states
    ┃ ┃ ┣ 📜vg2500_bld.dbf
    ┃ ┃ ┣ 📜vg2500_bld.prj
    ┃ ┃ ┣ 📜vg2500_bld.shp
    ┃ ┃ ┗ 📜vg2500_bld.shx
    ┃ ┣ 📂plz
    ┃ ┃ ┣ 📜plz-5stellig.dbf
    ┃ ┃ ┣ 📜plz-5stellig.prj
    ┃ ┃ ┣ 📜plz-5stellig.shp
    ┃ ┃ ┗ 📜plz-5stellig.shx
    ┃ ┣ 📂plz_mappigs
    ┃ ┣ 📜plz-5stellig-daten.csv
    ┃ ┗ 📜zuordnung_plz_ort.csv
    ┣ 📂deps
    ┃ ┗ 📂UrbanHeatPro
    ┃ ┃ ┣ 📂UrbanHeatPro
    ┃ ┃ ┃ ┣ 📂Classes
    ┃ ┃ ┃ ┃ ┣ 📜Building.py
    ┃ ┃ ┃ ┃ ┣ 📜City.py
    ┃ ┃ ┃ ┃ ┣ 📜HotWaterDemand.py
    ┃ ┃ ┃ ┃ ┣ 📜HotWaterDemand_D.py
    ┃ ┃ ┃ ┃ ┣ 📜Simulation.py
    ┃ ┃ ┃ ┃ ┣ 📜SpaceHeatingDemand.py
    ┃ ┃ ┃ ┃ ┗ 📜__init__.py
    ┃ ┃ ┃ ┣ 📂Functions
    ┃ ┃ ┃ ┃ ┣ 📜__init__.py
    ┃ ┃ ┃ ┃ ┣ 📜plot.py
    ┃ ┃ ┃ ┃ ┣ 📜probabilistic.py
    ┃ ┃ ┃ ┃ ┣ 📜to_tuple.py
    ┃ ┃ ┃ ┃ ┗ 📜uhp_utils.py
    ┃ ┃ ┃ ┣ 📜__init__.py
    ┃ ┃ ┃ ┗ 📜run_uhp.py
    ┃ ┃ ┣ 📂input
    ┃ ┃ ┃ ┣ 📂Building Typology
    ┃ ┃ ┃ ┃ ┣ 📜AirFlowRate-1_Residential.csv
    ┃ ┃ ┃ ┃ ┣ 📜AirFlowRate-2_Residential.csv
    ┃ ┃ ┃ ┃ ┣ 📜AirFlowRate-3_Residential.csv
    ┃ ┃ ┃ ┃ ┣ 📜AirFlowRate_NonResidential.csv
    ┃ ┃ ┃ ┃ ┣ 📜AreaRatio_Residential.csv
    ┃ ┃ ┃ ┃ ┣ 📜C_NonResidential.csv
    ┃ ┃ ┃ ┃ ┣ 📜C_Residential.csv
    ┃ ┃ ┃ ┃ ┣ 📜EnvelopeArea_Residential.csv
    ┃ ┃ ┃ ┃ ┣ 📜Floors_Residential.csv
    ┃ ┃ ┃ ┃ ┣ 📜MonthlySpaceHeatingProbability.csv
    ┃ ┃ ┃ ┃ ┣ 📜Tset.csv
    ┃ ┃ ┃ ┃ ┣ 📜U-1_NonResidential.csv
    ┃ ┃ ┃ ┃ ┣ 📜U-1_Residential.csv
    ┃ ┃ ┃ ┃ ┣ 📜U-2_NonResidential.csv
    ┃ ┃ ┃ ┃ ┣ 📜U-2_Residential.csv
    ┃ ┃ ┃ ┃ ┣ 📜U-3_NonResidential.csv
    ┃ ┃ ┃ ┃ ┣ 📜U-3_Residential.csv
    ┃ ┃ ┃ ┃ ┣ 📜WindowOrientationRatio_Residential.csv
    ┃ ┃ ┃ ┃ ┗ 📜YMdhm.csv
    ┃ ┃ ┃ ┣ 📂Buildings
    ┃ ┃ ┃ ┃ ┗ 📜buildings_Unterhaching.csv
    ┃ ┃ ┃ ┣ 📂Domestic Hot Water
    ┃ ┃ ┃ ┃ ┣ 📜dhw_Demand.csv
    ┃ ┃ ┃ ┃ ┣ 📜dhw_Loads.csv
    ┃ ┃ ┃ ┃ ┣ 📜dhw_ProbDaytime.csv
    ┃ ┃ ┃ ┃ ┗ 📜dhw_ProbWeekday.csv
    ┃ ┃ ┃ ┣ 📂Regional Data
    ┃ ┃ ┃ ┃ ┣ 📂DE
    ┃ ┃ ┃ ┃ ┃ ┣ 📜ActiveHours_DE.csv
    ┃ ┃ ┃ ┃ ┃ ┣ 📜AverageDwellingSize_DE.csv
    ┃ ┃ ┃ ┃ ┃ ┣ 📜BuildingStock_NonResidential_DE.csv
    ┃ ┃ ┃ ┃ ┃ ┣ 📜BuildingStock_Residential_DE.csv
    ┃ ┃ ┃ ┃ ┃ ┣ 📜CurrentRefurbished_NonResidential_DE.csv
    ┃ ┃ ┃ ┃ ┃ ┣ 📜CurrentRefurbished_Residential_DE.csv
    ┃ ┃ ┃ ┃ ┃ ┣ 📜HouseholdSize_DE.csv
    ┃ ┃ ┃ ┃ ┃ ┣ 📜I_DE.csv
    ┃ ┃ ┃ ┃ ┃ ┣ 📜MaxRefurbished_NonResidential_DE.csv
    ┃ ┃ ┃ ┃ ┃ ┣ 📜MaxRefurbished_Residential_DE.csv
    ┃ ┃ ┃ ┃ ┃ ┣ 📜SingleDwellingBuildings_DE.csv
    ┃ ┃ ┃ ┃ ┃ ┗ 📜Tamb_DE.csv
    ┃ ┃ ┃ ┃ ┗ 📂Unterhaching
    ┃ ┃ ┃ ┃ ┃ ┣ 📜ActiveHours_Unterhaching.csv
    ┃ ┃ ┃ ┃ ┃ ┣ 📜AverageDwellingSize_Unterhaching.csv
    ┃ ┃ ┃ ┃ ┃ ┣ 📜BuildingStock_NonResidential_Unterhaching.csv
    ┃ ┃ ┃ ┃ ┃ ┣ 📜BuildingStock_Residential_Unterhaching.csv
    ┃ ┃ ┃ ┃ ┃ ┣ 📜CurrentRefurbished_NonResidential_Unterhaching.csv
    ┃ ┃ ┃ ┃ ┃ ┣ 📜CurrentRefurbished_Residential_Unterhaching.csv
    ┃ ┃ ┃ ┃ ┃ ┣ 📜HouseholdSize_Unterhaching.csv
    ┃ ┃ ┃ ┃ ┃ ┣ 📜I_Unterhaching.csv
    ┃ ┃ ┃ ┃ ┃ ┣ 📜MaxRefurbished_NonResidential_Unterhaching.csv
    ┃ ┃ ┃ ┃ ┃ ┣ 📜MaxRefurbished_Residential_Unterhaching.csv
    ┃ ┃ ┃ ┃ ┃ ┣ 📜SingleDwellingBuildings_Unterhaching.csv
    ┃ ┃ ┃ ┃ ┃ ┗ 📜Tamb_Unterhaching.csv
    ┃ ┃ ┃ ┗ 📂Styles
    ┃ ┃ ┃ ┃ ┣ 📜TUM.mplstyle
    ┃ ┃ ┃ ┃ ┗ 📜presentation.mplstyle
    ┃ ┃ ┣ 📂results
    ┃ ┃ ┣ 📂settings
    ┃ ┃ ┃ ┣ 📜uhp_default_settings.yaml
    ┃ ┃ ┃ ┣ 📜uhp_settings_currently_used.yaml
    ┃ ┃ ┃ ┗ 📜uhp_settings_example.yaml
    ┃ ┃ ┣ 📜.gitignore
    ┃ ┃ ┣ 📜LICENSE
    ┃ ┃ ┣ 📜README.md
    ┃ ┃ ┣ 📜requirements.txt
    ┃ ┃ ┣ 📜runme.py
    ┃ ┃ ┗ 📜setup.py
    ┣ 📂docs
    ┃ ┣ 📂build
    ┃ ┣ 📂source
    ┃ ┃ ┣ 📂_autosummary
    ┃ ┃ ┣ 📂_static
    ┃ ┃ ┃ ┗ 📜custom.css
    ┃ ┃ ┣ 📂_templates
    ┃ ┃ ┃ ┣ 📜custom-class-template.rst
    ┃ ┃ ┃ ┗ 📜custom-module-template.rst
    ┃ ┃ ┣ 📂file_trees
    ┃ ┃ ┃ ┣ 📜acept_tree.rst
    ┃ ┃ ┃ ┗ 📜uhp_tree.rst
    ┃ ┃ ┣ 📜acept.examples.rst
    ┃ ┃ ┣ 📜acept.rst
    ┃ ┃ ┣ 📜api.rst
    ┃ ┃ ┣ 📜conf.py
    ┃ ┃ ┣ 📜index.rst
    ┃ ┃ ┣ 📜installation.rst
    ┃ ┃ ┣ 📜modules.rst
    ┃ ┃ ┣ 📜project-setup.md
    ┃ ┃ ┣ 📜uhp.rst
    ┃ ┃ ┗ 📜usage.rst
    ┃ ┣ 📜Makefile
    ┃ ┣ 📜docs_requirements.txt
    ┃ ┗ 📜make.bat
    ┣ 📂settings
    ┃ ┣ 📜uhp_settings.yaml
    ┃ ┗ 📜uhp_settings_example.yaml
    ┣ 📂src
    ┃ ┗ 📂acept
    ┃ ┃ ┣ 📂acept_notebooks
    ┃ ┃ ┃ ┣ 📜bbd_plz_processsing_examples.ipynb
    ┃ ┃ ┃ ┣ 📜dwd_try_data.ipynb
    ┃ ┃ ┃ ┣ 📜idp_test_stuff.ipynb
    ┃ ┃ ┃ ┣ 📜input_data_analytics.ipynb
    ┃ ┃ ┃ ┣ 📜plz_shape_data_analytics.ipynb
    ┃ ┃ ┃ ┗ 📜temp_profiles.ipynb
    ┃ ┃ ┣ 📂examples
    ┃ ┃ ┃ ┣ 📜__init__.py
    ┃ ┃ ┃ ┣ 📜main_example.py
    ┃ ┃ ┃ ┗ 📜pv_cap_example.py
    ┃ ┃ ┣ 📜__init__.py
    ┃ ┃ ┣ 📜acept_constants.py
    ┃ ┃ ┣ 📜acept_utils.py
    ┃ ┃ ┣ 📜bbd_plz_preprocessing.py
    ┃ ┃ ┣ 📜buildings_information.py
    ┃ ┃ ┣ 📜cop_profiles.py
    ┃ ┃ ┣ 📜demand_profiles.py
    ┃ ┃ ┣ 📜dwd_try_data_handling.py
    ┃ ┃ ┣ 📜dwd_try_data_setup.py
    ┃ ┃ ┣ 📜exceptions.py
    ┃ ┃ ┣ 📜personal_settings.py
    ┃ ┃ ┣ 📜plz_shape.py
    ┃ ┃ ┣ 📜pv_cap_api.py
    ┃ ┃ ┣ 📜pv_cap_factor_profiles.py
    ┃ ┃ ┣ 📜temperature_profiles.py
    ┃ ┃ ┣ 📜uhp_csv_io.py
    ┃ ┃ ┣ 📜uhp_input_formatting.py
    ┃ ┃ ┗ 📜weather_profile_api.py
    ┣ 📂temp
    ┃ ┗ 📂PLZ_123459_20_1_0_1781549793
    ┃ ┃ ┣ 📜DWD_TRY_123459_20_1_0_1781549793_2012.csv
    ┃ ┃ ┗ 📜temperature_tmy_123459_20_1_0_1781549793.csv
    ┣ 📜.gitignore
    ┣ 📜.gitmodules
    ┣ 📜LICENSE
    ┣ 📜README.md
    ┣ 📜imported_requirements.txt
    ┣ 📜imported_requirements_install_requires.txt
    ┣ 📜pyproject.toml
    ┣ 📜requirements.txt
    ┣ 📜setup.cfg
    ┗ 📜setup.sh


.. short_tree_acept


.. code-block:: text

    📦acept 
    ┣ 📂data                                    Data directory
    ┃ ┣ 📂dwd                                   Weather data from the Deutscher Wetterdienst (DWD)
    ┃ ┃ ┗ 📂try_bavarian                        Bavarian TRY data
    ┃ ┣ 📂fed_states                            Shape files for the federal states of Germany
    ┃ ┣ 📂plz                                   PLZ shape files
    ┃ ┣ 📂plz_mappigs                           PLZ mapping data
    ┃ ┣ 📜plz-5stellig-daten.csv                Contains information on PLZ areas
    ┃ ┗ 📜zuordnung_plz_ort.csv                 Contains information for mapping PLZ to 
    ┣ 📂deps                                    Dependencies as git submodules
    ┃ ┗ 📂UrbanHeatPro                          UrbanHeatPro submodule, see ::ref:`UrbanHeatPro` 
    ┣ 📂docs                                    Documentation
    ┃ ┣ 📂build
    ┃ ┣ 📂source                                Source files for the documentation
    ┃ ┃ ┣ 📂_autosummary
    ┃ ┃ ┣ 📂_static                             Static files and style sheets
    ┃ ┃ ┣ 📂_templates                          HTML templates
    ┃ ┃ ┣ 📂file_trees                          File trees
    ┃ ┃ ┣ 📜acept.examples.rst
    ┃ ┃ ┣ 📜acept.rst
    ┃ ┃ ┣ 📜api.rst
    ┃ ┃ ┣ 📜conf.py
    ┃ ┃ ┣ 📜index.rst
    ┃ ┃ ┣ 📜installation.rst
    ┃ ┃ ┣ 📜modules.rst
    ┃ ┃ ┣ 📜project-setup.rst
    ┃ ┃ ┣ 📜uhp.rst
    ┃ ┃ ┗ 📜usage.rst
    ┃ ┣ 📜Makefile
    ┃ ┣ 📜docs_requirements.txt                 Requirements for building the documentation
    ┃ ┗ 📜make.bat
    ┣ 📂settings                                Settings files for UrbanHeatPro
    ┃ ┣ 📜uhp_settings.yaml                     Settings file for UrbanHeatPro
    ┃ ┗ 📜uhp_settings_example.yaml             Example settings file for UrbanHeatPro
    ┣ 📂src
    ┃ ┗ 📂acept
    ┃ ┃ ┣ 📂acept_notebooks                     Jupyther notebooks for using acept
    ┃ ┃ ┃ ┣ 📜bbd_plz_processsing_examples.ipynb
    ┃ ┃ ┃ ┣ 📜dwd_try_data.ipynb
    ┃ ┃ ┃ ┣ 📜idp_test_stuff.ipynb
    ┃ ┃ ┃ ┣ 📜input_data_analytics.ipynb
    ┃ ┃ ┃ ┣ 📜plz_shape_data_analytics.ipynb
    ┃ ┃ ┃ ┗ 📜temp_profiles.ipynb
    ┃ ┃ ┣ 📂examples                            Examples of using acept
    ┃ ┃ ┃ ┣ 📜__init__.py
    ┃ ┃ ┃ ┣ 📜main_example.py
    ┃ ┃ ┃ ┗ 📜pv_cap_example.py
    ┃ ┃ ┣ 📜__init__.py
    ┃ ┃ ┣ 📜acept_constants.py                  Constants for acept
    ┃ ┃ ┣ 📜acept_utils.py                      Utility functions for acept
    ┃ ┃ ┣ 📜bbd_plz_preprocessing.py            Module for preprocessing the BBD shapefiles with PLZ areas
    ┃ ┃ ┣ 📜buildings_information.py            Module for adding and calculating information about buildings
    ┃ ┃ ┣ 📜cop_profiles.py                     Module for calculating COP profiles
    ┃ ┃ ┣ 📜demand_profiles.py                  Module for calculating demand profiles
    ┃ ┃ ┣ 📜dwd_try_data_handling.py            Module for handling the DWD TRY data
    ┃ ┃ ┣ 📜dwd_try_data_setup.py               Module for setting up the DWD TRY data
    ┃ ┃ ┣ 📜exceptions.py                       Exceptions for acept
    ┃ ┃ ┣ 📜personal_settings.py                Personal settings, this has to be created
    ┃ ┃ ┣ 📜plz_shape.py                        Module for processing PLZ shapefiles
    ┃ ┃ ┣ 📜pv_cap_api.py                       Module for using the PV API of renewables.ninja
    ┃ ┃ ┣ 📜pv_cap_factor_profiles.py           Module for building PV capacity factor profiles
    ┃ ┃ ┣ 📜temperature_profiles.py             Module for building temperature profiles
    ┃ ┃ ┣ 📜uhp_csv_io.py                       Module for handling UrbanHeatPro CSV files
    ┃ ┃ ┣ 📜uhp_input_formatting.py             Module for formatting the UrbanHeatPro input
    ┃ ┃ ┗ 📜weather_profile_api.py              Module for using the weather API of PVGIS
    ┣ 📂temp                                    Directory temporary files are saved in
    ┣ 📜.gitignore                              A file that specifies which files and directories should be ignored by Git
    ┣ 📜.gitmodules                             A file specifying the submodule dependencies required by the project
    ┣ 📜LICENSE                                 The license file for the project
    ┣ 📜README.md                               The readme file for the project
    ┣ 📜imported_requirements.txt
    ┣ 📜imported_requirements_install_requires.txt
    ┣ 📜pyproject.toml                          The project configuration file
    ┣ 📜requirements.txt                        The requirements file
    ┣ 📜setup.cfg                               The setup configuration file
    ┗ 📜setup.sh                                The convenience setup script
