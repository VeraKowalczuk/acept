"""Main example for building the scenario profiles for a given PLZ and year.

To run the example use the following command with the venv activated:

.. code-block:: console

    $ source venv/bin/activate
    $ cd src/acept
    $ python examples/main_example.py


"""
import sys

import geopandas as gpd

from acept import plz_shape
from acept.acept_utils import absolute_path_from_relative_posix
from acept.bbd_plz_preprocessing import build_plz_munc_id_db, query_bbd_for_plz
from acept.demand_profiles import run_uhp_for_selected_buildings_year
from acept.pv_cap_api import PVQuery, PVCapacityFactorCreator
from acept.temperature_profiles import build_temperature_profile_for_year


def build_scenario_profiles_for_plz_year(plz: int, year: int = 2011) -> dict:
    """
    Build the scenario profiles for the given input

    The scenario profiles are built for the temperature profile and the PV capacity factor profiles
    The scenario profiles are saved in the:py:const:`acept.acept_constants.TEMP_PATH` directory

    :param plz: PLZ to search
    :param year: year to use for the scenario profiles
    :return: The paths to the created scenario profiles in a dictionary
    """
    print("Building the scenario profiles for the given input")
    selected_shape = plz_shape.get_single_plz_shape(str(plz))
    print("Selected PLZ shape read.")
    temp_profile = build_temperature_profile_for_year(plz, selected_shape=selected_shape, year=year, debug=True)

    # Using the PV capacity profile API of renewables.ninja for the PLZ region
    # Comment out the following two lines if you have set the renewables_token in personal_settings.py,
    # and you want to use the Renewables.ninja API
    pv_query = PVQuery(plz=str(plz), year=year)
    pcfc = PVCapacityFactorCreator()
    pv_profile = pcfc.create_pv_api_query(pv_query)

    return {"temperature_profile": temp_profile, "pv_profile": pv_profile}


if __name__ == "__main__":
    # download_dwd_data()
    #  read CLI parameters

    if len(sys.argv) != 3:
        # print("Usage: python main_example.py <plz> <year>")
        plz_cli = 91126  # Schwabach  # sys.argv[1]
        year_cli = 2011  # sys.argv[2]
        print("Using example PLZ and year:", plz_cli, year_cli)
    else:
        plz_cli = int(sys.argv[1])
        year_cli = int(sys.argv[2])

    # Use example PLZ and year commend out the following two lines if you want to use the CLI parameters
    plz_cli = 91126
    year_cli = 2011

    # uncomment the following if you want to build the PLZ mapping for all data for the BBD and use it with the CLI
    # parameters
    # build_plz_munc_id_db()
    # buildings_example = query_bbd_for_plz(str(plz_cli))
    print("Selected PLZ: ", plz_cli, "in year", year_cli)

    # Comment out the following two lines if you want to use the buildings read from the BBD
    buildings_example = gpd.read_file(
        absolute_path_from_relative_posix("../../data/bbd/TestBezirk/Res_9565000_10_buildings.shp"))

    scenarios = build_scenario_profiles_for_plz_year(plz_cli, year_cli)
    if scenarios["temperature_profile"] is not None:
        print("Temperature profile successfully created")
        if "temperature_tmy" in scenarios["temperature_profile"]:
            print("TMY used instead of DWD TRY for", year_cli)
            # set the year to None for UHP
            year_cli = None
    if scenarios["pv_profile"] is not None:
        print("PV profile successfully created")

    run_uhp_for_selected_buildings_year(plz_cli, buildings_example, year_cli, scenarios["temperature_profile"],
                                        demand_unit='W')

    # -----
    print("Finished running acept")
