# Alanube Python API

Python library to connect with Alanube API

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

- `do`: Implementation for the Dominican Republic (DGII). This is the only fully developed directory and contains all the necessary structure and logic to work with the Alanube API for this country.
- `pa`: Implementation for Panama (future). If you need to develop for Panama, create a directory named `pa` at the same level as `do` within `alanube` and replicate the internal structure of `do`.
- `cr`: Implementation for Costa Rica (future). Similarly, create a `cr` directory following the same structure as `do`.
- `bo`: Implementation for Bolivia (future). The `bo` directory should also follow the structure of `do`.

For the missing countries, you can use the `do` directory as a reference to build the required implementations, adapting the logic to meet the specific local requirements of each country.

### Links
* [Alanube Official Website](https://www.alanube.co/)
* [Alanube Documentation](https://developer.alanube.co/)

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

## Licence

This project is licensed under the MIT License.

## Proyect Status

This project is under development

## Contribution 💗

If you find value in this project and would like to show your support, please consider making a donation via PayPal:

[Donate on PayPal](https://paypal.me/martinezwilmer?country.x=DO&locale.x=es_XC)

Your generosity helps us to continue improving and maintaining this project. We appreciate every contribution, however small. Thanks for being part of our community!