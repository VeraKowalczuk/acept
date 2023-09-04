# acept
ACEPT - Automated, communal energy planning tool

ACEPT is an open-source project that aims to provide an automated, communal energy planning tool. It allows users to model and analyze energy demand, supply, and distribution in a community or urban area. The tool takes into account factors such as building characteristics, regional data, and renewable energy sources to generate energy planning scenarios and evaluate their impact on sustainability and cost-effectiveness.

>  This is a Interdisciplinary Project (IDP) at the Chair of Renewable and Sustainable Energy Systems at TUM

## Requirements

- Python 3.10

## Installation

To install ACEPT, follow these steps:

1. Clone the repository:

```sh
$ git clone https://github.com/VeraKowalczuk/acept.git
```

2. Navigate to the project directory:
```sh
$ cd acept
```

3. Setup and install the project

    - Linux & macOS: Use the setup script

        ```sh
        $ setup.sh
        ```

    - Windows: Follow the steps of the setup script

_More details on how to install acept can be found in the [Documentation](TODO)._


## Additional requirements
### src/acept/personal_settings.py
```python
# https://www.renewables.ninja Authorization Token
# Your API token is displayed on your account page, where you can also generate a new random token in case your 
# current token has been compromised.
renewables_token = 'your_token_here'
```

## Usage example

[//]: # (To run ACEPT, use the following command:)


_For more examples and usage insturctions, please refer to the [Documentation](TODO)._

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

## License

ACEPT is open-source software licensed under the MIT License. See the ``LICENSE`` file for more information.