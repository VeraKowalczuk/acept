# acept
ACEPT - Automated, communal energy planning tool

ACEPT is an open-source project that aims to provide an automated, communal energy planning tool. It allows users to model and analyze energy demand, supply, and distribution in a community or urban area. The tool takes into account factors such as building characteristics, regional data, and renewable energy sources to generate energy planning scenarios and evaluate their impact on sustainability and cost-effectiveness.

>  This is an Interdisciplinary Project (IDP) at the Chair of Renewable and Sustainable Energy Systems at TUM

<a href='https://acept.readthedocs.io/en/latest/?badge=latest'>
    <img src='https://readthedocs.org/projects/acept/badge/?version=latest' alt='Documentation Status' />
</a>
      

For a detailed documentation of the project, please refer to the [**Documentation**](https://acept.readthedocs.io/en/latest/index.html).

## Features

The ACEPT project aims to automate the process of sourcing input data for the linear optimization framework ``urbs``.
Additionally, it was integrated into the GUI of ``pylovo``, that allows a user to quickly visualize different grids and 
set parameters as well as results of the optimization of said grids.

``acept`` provides support to create timeseries profiles as an input for ``urbs`` for...

* the typical weather for a location or area,
* the ambient temperature for a location or area,
* heat demand profiles for all buildings in a specified area and the area as a whole,
* solar profiles, that give the PV capacity factor for all buildings in a specified area,
* the Coefficient of Performance (COP) for heat pumps,
* ...

These timeseries contain hourly data for one year.

To calculate the heat demand profiles, ``acept`` leverages an upgraded version of the existing 
tool ``UrbanHeatPro``. 

Additionally, ``acept`` complements the existing data on buildings with additional knowledge because the available
information on buildings is often incomplete, e.g. the postal code a building is in or its size.

Further information on the other projects that ``acept`` interacts with:
 - ``urbs``: Please refer to the [urbs documentation](https://urbs.readthedocs.io), or find the project on [GitHub](https://github.com/tum-ens/urbs).
 - ``pylovo``: Please refer to the [pylovo documentation](https://pylovo.readthedocs.io), or find the project on [Gitlab LRZ](https://pylovo.readthedocs.io/en/latest/).
 - ``UrbanHeatPro``: Check out the section on [the UrbanHeatPro dependency](https://acept.readthedocs.io/en/latest/uhp.html) in the documentation of ``acept``.

## Requirements

- Python 3.10

## Installation

_More details on how to install acept can be found 
in the [Installation Guide](https://acept.readthedocs.io/en/latest/installation.html) in the Documentation._

TLDR:
To install acept, follow these steps:

1. Clone the repository:

```sh
$ git clone --recurse-submodules https://github.com/VeraKowalczuk/acept.git
```

2. Navigate to the project directory:
```sh
$ cd acept
```

3. Setup and install the project

    - Linux & macOS: Use the setup script

        ```sh
        $ ./setup.sh
        ```

    - Windows: Follow the steps of the [Installation Guide for Windows](https://acept.readthedocs.io/en/latest/installation.html)

The documentation provides further help if you have problems during the installation.

## Additional requirements

For more information on the data setup, head to the [data setup section of the documentation](https://acept.readthedocs.io/en/latest/data_setup.html)

### src/acept/personal_settings.py
Place your Authorization Token for the [Renewables.ninja API](https://www.renewables.ninja) inside this file.

Your API token is displayed on your account page, where you can also generate a new random token in case your 
current token has been compromised.

The file should have the following structure:

```python
renewables_token = 'your_token_here'
```

### Weather data

ACEPT uses weather data from two sources:
- the Deutscher Wetterdienst (DWD) project TRY (Test Reference Years)
- the PVGIS API

The DWD data has to be downloaded and setup locally while the PVGIS API does not need any downloads.
Checkout the [documentation](https://acept.readthedocs.io/en/latest/data_setup.html#deutscher-wetterdienst-dwd-weather-data) for detailed information, when to use which data and how to set up the 
project to use your preferred data source.

## Usage

Check out the `acept.examples` package or the Jupyter notebooks in the `src/acept/acept_notebooks` directory for 
examples on how to use the project.

Alternatively, `acept` can be used in the GUI of the [`pylovo` project](https://pylovo.readthedocs.io).

_For more examples and usage instructions as well as details on the integration into the `pylovo` project, please refer to the [Documentation](https://acept.readthedocs.io/en/latest/usage.html)._

[//]: # (marker_text_contributing_start)


## Contributing

Contributions from the community are welcome. If you want to contribute to ACEPT, please follow these steps:

1. [Fork](<https://github.com/VeraKowalczuk/acept/fork>) the repository.
2. Create your feature branch
```sh
$ git checkout -b feature/my-feature
```
3. Make your changes and commit them (`git commit -am 'Add my feature'`)
```sh
$ git commit -am 'Add my feature'
```
4. Push to the branch
```sh
$ git push origin feature/my-feature
```
5. Create a new Pull Request

[//]: # (marker_text_contributing_end)

The documentation also provides some ideas for [further development of the project](https://acept.readthedocs.io/en/latest/development_future_work.html). You can use these ideas for inspiration.

## License

ACEPT is open-source software licensed under the MIT License. Check out the [LICENSE](LICENSE) file for more information.