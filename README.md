# Alanube Python API

A lightweight Python client for connecting to the Alanube e-invoicing API across multiple countries.

[![PyPI version](https://img.shields.io/pypi/v/alanube.svg)](https://pypi.org/project/alanube/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)](#running-the-tests)


## 📚 Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Contents](#contents)
- [Developers](#developers)
- [Testing](#running-the-tests)
- [Build & Publish](#building-and-publishing-the-library)
- [Credits](#credits)
- [License](#licence)
- [Contribute](#contribution-💗)


## Instalation

To install the Alanube library, you can use pip:

```sh
pip install alanube
```

## Usage

```py
# Import the Alanube class specific to the country,
# in this case from `alanube.do` for the Dominican Republic
from alanube.do import Alanube

# Connect to the API
Alanube.connect("[TOKEN]")

payload = {...}

data = Alanube.send_document(encf_type=31, payload)
```

Now you can easily and efficiently use the Alanube API with this Python library!

## Contents

- `do`: Fully implemented for the Dominican Republic (DGII).
- `pa`, `cr`, `pe`, `bo`: Planned support. Follow the structure of the `do` module.

For the missing countries, you can use the `do` directory as a reference to build the required implementations, adapting the logic to meet the specific local requirements of each country.

### Links
* [Alanube Official Website](https://www.alanube.co/)
* [Alanube Documentation](https://developer.alanube.co/)

## Roadmap

- [x] 🇩🇴 Dominican Republic
- [ ] 🇵🇦 Panama
- [ ] 🇨🇷 Costa Rica
- [ ] 🇵🇪 Peru
- [ ] 🇧🇴 Bolivia

## Developers

If you're contributing to the development of this library, here are the steps to set up your environment and run the tests:

### Setting Up the Environment

1. Clone the repository:

    ```sh
    git clone https://github.com/wilmerm/alanube-python-api.git
    cd alanube-python-api
    ```

2. Create a virtual environment (optional but recommended):

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. Install the required dependencies:

    ```sh
    pip install -r requirements.txt
    pip install -r requirements-dev.txt
    ```

4. Install the library in editable mode:

    ```sh
    pip install -e .
    ```

5. **Code Style**. We follow PEP 8 for coding standards. Please ensure your code is formatted accordingly before submitting a pull request.

    ```sh
    flake8 alanube
    ```

### Running the Tests

1. Navigate to the project root directory.

2. Execute the tests with unittest:

    ```sh
    python -m unittest discover -s alanube/tests -p "*.py"
    ```

    * -s: Specifies the directory to look for tests (tests folder).
    * -p: Defines the pattern for test file names (e.g., *.py).

### Building and Publishing the Library

To compile and upload the library to PyPI, follow these steps:

1. Ensure you have the necessary dependencies:

    ```sh
    pip install build twine
    ```

2. Build the package:

    ```sh
    python -m build
    ```

3. (Optional) Verify the package:

    ```sh
    twine check dist/*
    ```

4. Upload the package to PyPI:

    ```sh
    python -m twine upload dist/*
    ```

## Credits

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/wilmerm">
        <img src="https://github.com/wilmerm.png" width="100px;" alt="Wilmer Martinez"/><br />
        <sub><b>Wilmer Martinez</b></sub>
      </a>
      <br/>Author & Maintainer
    </td>
  </tr>
</table>

If you contributed to this project and would like to be listed here, feel free to open a pull request adding yourself to the credits section.


## Licence

This project is licensed under the MIT License.

## Proyect Status

✅ This project is in production and actively maintained.

## Contributing

We welcome pull requests and suggestions. Please open an issue or submit a PR.

## Support 💗

If you find this useful, consider supporting:

[Donate on PayPal](https://paypal.me/martinezwilmer?country.x=DO&locale.x=es_XC)

Your generosity helps us to continue improving and maintaining this project. We appreciate every contribution, however small. Thanks for being part of our community!

