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
The `do` directory contains the following files and directories.

### Links
* [Alanube Official Website](https://www.alanube.co/)
* [Alanube Documentation](https://developer.alanube.co/)

## Licence

This project is licensed under the MIT License.

## Proyect Status

This project is under development

## Contribution 💗

If you find value in this project and would like to show your support, please consider making a donation via PayPal:

[Donate on PayPal](https://paypal.me/martinezwilmer?country.x=DO&locale.x=es_XC)

Your generosity helps us to continue improving and maintaining this project. We appreciate every contribution, however small. Thanks for being part of our community!