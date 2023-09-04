The file structure of the UrbanHeatPro project:

.. code-block:: text

    📦UrbanHeatPro
    ┣ 📂UrbanHeatPro
    ┃ ┣ 📂Classes
    ┃ ┃ ┣ 📜Building.py
    ┃ ┃ ┣ 📜City.py
    ┃ ┃ ┣ 📜HotWaterDemand.py
    ┃ ┃ ┣ 📜HotWaterDemand_D.py
    ┃ ┃ ┣ 📜Simulation.py
    ┃ ┃ ┣ 📜SpaceHeatingDemand.py
    ┃ ┃ ┗ 📜__init__.py
    ┃ ┣ 📂Functions
    ┃ ┃ ┣ 📜__init__.py
    ┃ ┃ ┣ 📜plot.py
    ┃ ┃ ┣ 📜probabilistic.py
    ┃ ┃ ┣ 📜to_tuple.py
    ┃ ┃ ┗ 📜uhp_utils.py
    ┃ ┣ 📜__init__.py
    ┃ ┗ 📜run_uhp.py
    ┣ 📂input
    ┃ ┣ 📂Building Typology
    ┃ ┃ ┣ 📜AirFlowRate-1_Residential.csv
    ┃ ┃ ┣ 📜AirFlowRate-2_Residential.csv
    ┃ ┃ ┣ 📜AirFlowRate-3_Residential.csv
    ┃ ┃ ┣ 📜AirFlowRate_NonResidential.csv
    ┃ ┃ ┣ 📜AreaRatio_Residential.csv
    ┃ ┃ ┣ 📜C_NonResidential.csv
    ┃ ┃ ┣ 📜C_Residential.csv
    ┃ ┃ ┣ 📜EnvelopeArea_Residential.csv
    ┃ ┃ ┣ 📜Floors_Residential.csv
    ┃ ┃ ┣ 📜MonthlySpaceHeatingProbability.csv
    ┃ ┃ ┣ 📜Tset.csv
    ┃ ┃ ┣ 📜U-1_NonResidential.csv
    ┃ ┃ ┣ 📜U-1_Residential.csv
    ┃ ┃ ┣ 📜U-2_NonResidential.csv
    ┃ ┃ ┣ 📜U-2_Residential.csv
    ┃ ┃ ┣ 📜U-3_NonResidential.csv
    ┃ ┃ ┣ 📜U-3_Residential.csv
    ┃ ┃ ┣ 📜WindowOrientationRatio_Residential.csv
    ┃ ┃ ┗ 📜YMdhm.csv
    ┃ ┣ 📂Buildings
    ┃ ┃ ┗ 📜buildings_Unterhaching.csv
    ┃ ┣ 📂Domestic Hot Water
    ┃ ┃ ┣ 📜dhw_Demand.csv
    ┃ ┃ ┣ 📜dhw_Loads.csv
    ┃ ┃ ┣ 📜dhw_ProbDaytime.csv
    ┃ ┃ ┗ 📜dhw_ProbWeekday.csv
    ┃ ┣ 📂Regional Data
    ┃ ┃ ┣ 📂DE
    ┃ ┃ ┃ ┣ 📜ActiveHours_DE.csv
    ┃ ┃ ┃ ┣ 📜AverageDwellingSize_DE.csv
    ┃ ┃ ┃ ┣ 📜BuildingStock_NonResidential_DE.csv
    ┃ ┃ ┃ ┣ 📜BuildingStock_Residential_DE.csv
    ┃ ┃ ┃ ┣ 📜CurrentRefurbished_NonResidential_DE.csv
    ┃ ┃ ┃ ┣ 📜CurrentRefurbished_Residential_DE.csv
    ┃ ┃ ┃ ┣ 📜HouseholdSize_DE.csv
    ┃ ┃ ┃ ┣ 📜I_DE.csv
    ┃ ┃ ┃ ┣ 📜MaxRefurbished_NonResidential_DE.csv
    ┃ ┃ ┃ ┣ 📜MaxRefurbished_Residential_DE.csv
    ┃ ┃ ┃ ┣ 📜SingleDwellingBuildings_DE.csv
    ┃ ┃ ┃ ┗ 📜Tamb_DE.csv
    ┃ ┃ ┗ 📂Unterhaching
    ┃ ┃ ┃ ┣ 📜ActiveHours_Unterhaching.csv
    ┃ ┃ ┃ ┣ 📜AverageDwellingSize_Unterhaching.csv
    ┃ ┃ ┃ ┣ 📜BuildingStock_NonResidential_Unterhaching.csv
    ┃ ┃ ┃ ┣ 📜BuildingStock_Residential_Unterhaching.csv
    ┃ ┃ ┃ ┣ 📜CurrentRefurbished_NonResidential_Unterhaching.csv
    ┃ ┃ ┃ ┣ 📜CurrentRefurbished_Residential_Unterhaching.csv
    ┃ ┃ ┃ ┣ 📜HouseholdSize_Unterhaching.csv
    ┃ ┃ ┃ ┣ 📜I_Unterhaching.csv
    ┃ ┃ ┃ ┣ 📜MaxRefurbished_NonResidential_Unterhaching.csv
    ┃ ┃ ┃ ┣ 📜MaxRefurbished_Residential_Unterhaching.csv
    ┃ ┃ ┃ ┣ 📜SingleDwellingBuildings_Unterhaching.csv
    ┃ ┃ ┃ ┗ 📜Tamb_Unterhaching.csv
    ┃ ┗ 📂Styles
    ┃ ┃ ┣ 📜TUM.mplstyle
    ┃ ┃ ┗ 📜presentation.mplstyle
    ┣ 📂results
    ┣ 📂settings
    ┃ ┣ 📜uhp_default_settings.yaml
    ┃ ┣ 📜uhp_settings_currently_used.yaml
    ┃ ┗ 📜uhp_settings_example.yaml
    ┣ 📜.gitignore
    ┣ 📜LICENSE
    ┣ 📜README.md
    ┣ 📜requirements.txt
    ┣ 📜runme.py
    ┗ 📜setup.py

.. short_tree_uhp

.. code-block:: text

    📦UrbanHeatPro                       The root directory of the UrbanHeatPro project
    ┣ 📂UrbanHeatPro                     The UrbanHeatPro library root directory
    ┃ ┣ 📂Classes                        Contains Python files related to classes
    ┃ ┃ ┣ 📜Building.py
    ┃ ┃ ┣ 📜City.py
    ┃ ┃ ┣ 📜HotWaterDemand.py
    ┃ ┃ ┣ 📜HotWaterDemand_D.py
    ┃ ┃ ┣ 📜Simulation.py
    ┃ ┃ ┣ 📜SpaceHeatingDemand.py
    ┃ ┃ ┗ 📜__init__.py
    ┃ ┣ 📂Functions                      Contains Python files related to functions
    ┃ ┃ ┣ 📜__init__.py
    ┃ ┃ ┣ 📜plot.py
    ┃ ┃ ┣ 📜probabilistic.py
    ┃ ┃ ┣ 📜to_tuple.py
    ┃ ┃ ┗ 📜uhp_utils.py
    ┃ ┣ 📜__init__.py                   An initialization file for UrbanHeatPro
    ┃ ┗ 📜run_uhp.py                    A Python module for running UrbanHeatPro
    ┣ 📂input                           Input data for UrbanHeatPro
    ┃ ┣ 📂Building Typology             Statistical data on the building typology
    ┃ ┣ 📂Buildings                     Buildings data
    ┃ ┣ 📂Domestic Hot Water            Statistical data on domestic hot water
    ┃ ┣ 📂Regional Data                 Regional data
    ┃ ┃ ┣ 📂DE
    ┃ ┃ ┗ 📂Unterhaching
    ┃ ┗ 📂Styles                       Styles for the plotting
    ┃ ┃ ┣ 📜TUM.mplstyle
    ┃ ┃ ┗ 📜presentation.mplstyle
    ┣ 📂results                        Output data from the UrbanHeatPro
    ┣ 📂settings                       YAML files related to project settings
    ┃ ┣ 📜uhp_default_settings.yaml    The default settings. Do not edit this file.
    ┃ ┣ 📜uhp_settings_currently_used.yaml
    ┃ ┗ 📜uhp_settings_example.yaml
    ┣ 📜.gitignore                     A file that specifies which files and directories should be ignored by Git
    ┣ 📜LICENSE                        The license file for the project
    ┣ 📜README.md                      A README file containing information about the project
    ┣ 📜requirements.txt               A file specifying the dependencies required by the project
    ┣ 📜runme.py                       A Python script for running the project
    ┗ 📜setup.py                       A Python script for setting up the project
    
.. explanation_of_the_tree

The directory structure of the UrbanHeatPro project is as follows:

UrbanHeatPro (root directory)
    - UrbanHeatPro
        - Classes: Contains Python files related to classes.
        - Functions: Contains Python files related to functions.
        - __init__.py: An initialization file for the UrbanHeatPro module.
        - run_uhp.py: A Python module for running the UrbanHeatPro project.
    - input: Contains input files for the project, including subdirectories such as Building Typology, Buildings, Domestic Hot Water, Regional Data, and Styles.
    - results: Contains output files and results of the project.
    - settings: Contains YAML files related to project settings, including uhp_default_settings.yaml, uhp_settings_currently_used.yaml, and uhp_settings_example.yaml.
    - .gitignore: A file that specifies which files and directories should be ignored by Git.
    - LICENSE: The license file for the project.
    - README.md: A README file containing information about the project.
    - requirements.txt: A file specifying the dependencies required by the project.
    - runme.py: A Python script for running the project.
    - setup.py: A setup script for the project.

    