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

### Dominican Republic API Methods

| Method | Description |
|--------|-------------|
| `create_company` | Create a new company. |
| `update_company` | Update company information. |
| `get_company` | Retrieve company info. |
| `send_fiscal_invoice` | Issue Fiscal Credit Invoice (31). |
| `get_fiscal_invoice` | Get status of a Fiscal Credit Invoice. |
| `get_fiscal_invoices` | List Fiscal Credit Invoices. |
| `send_invoice` | Issue Consumption Invoice (32). |
| `get_invoice` | Get status of a Consumption Invoice. |
| `get_invoices` | List Consumption Invoices. |
| `send_debit_note` | Issue Debit Note (33). |
| `get_debit_note` | Get status of a Debit Note. |
| `get_debit_notes` | List Debit Notes. |
| `send_credit_note` | Issue Credit Note (34). |
| `get_credit_note` | Get status of a Credit Note. |
| `get_credit_notes` | List Credit Notes. |
| `send_purchase` | Issue Purchase Document (41). |
| `get_purchase` | Get status of a Purchase Document. |
| `get_purchases` | List Purchase Documents. |
| `send_minor_expense` | Issue Minor Expense Document (43). |
| `get_minor_expense` | Get status of a Minor Expense Document. |
| `get_minor_expenses` | List Minor Expense Documents. |
| `send_special_regime` | Issue Special Regime Document (44). |
| `get_special_regime` | Get status of a Special Regime Document. |
| `get_special_regimes` | List Special Regime Documents. |
| `send_gubernamental` | Issue Government Document (45). |
| `get_gubernamental` | Get status of a Government Document. |
| `get_gubernamentals` | List Government Documents. |
| `send_export_support` | Issue Export Support Document (46). |
| `get_export_support` | Get status of an Export Support Document. |
| `get_export_supports` | List Export Support Documents. |
| `send_payment_abroad_support` | Issue Payment Abroad Support Document (47). |
| `get_payment_abroad_support` | Get status of a Payment Abroad Support Document. |
| `get_payment_abroad_supports` | List Payment Abroad Support Documents. |
| `send_cancellation` | Issue a cancellation document. |
| `get_cancellation` | Get status of a cancellation. |
| `get_cancellations` | List cancellations. |
| `get_received_document` | Retrieve a received document. |
| `get_received_documents` | List received documents. |
| `check_directory` | Check active companies in directory. |
| `check_dgii_status` | Check DGII service status and maintenance. |
| `get_report_companies_documents_total` | Get total documents issued by a company. |
| `get_report_users_documents_total` | Get total documents issued by the authenticated user. |
| `get_report_company_emitted_documents` | Get total documents emitted by a company. |
| `get_report_company_emitted_documents_monthly` | Monthly totals of emitted documents (12 months). |
| `get_report_company_emitted_documents_15_days` | Daily totals of emitted documents (last 15 days). |
| `get_report_company_accepted_documents` | Total documents accepted by DGII for a company. |
| `get_report_company_accepted_documents_monthly` | Monthly totals of accepted documents (12 months). |
| `get_report_company_accepted_documents_15_days` | Daily totals of accepted documents (last 15 days). |

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

## Used by

This library is trusted and used in production by:

<table>
  <tr>
    <td align="center" width="250">
      <a href="https://www.unolet.com" target="_blank">
        <img src="https://cdn.unolet.com/img/unolet/unolet-logo.svg" width="120px" alt="Unolet Logo"/><br/>
        <b>Unolet</b>
      </a>
      <br/>
      <sub><i>ERP and electronic invoicing platform for SMEs.</i></sub>
    </td>
  </tr>
</table>

If your company uses this library and would like to be listed here, feel free to [open a pull request](https://github.com/wilmerm/alanube-python/pulls) or [create an issue](https://github.com/wilmerm/alanube-python/issues).

## Developers

If you're contributing to the development of this library, here are the steps to set up your environment and run the tests:

### Setting Up the Environment

1. Clone the repository:

    ```sh
    git clone https://github.com/wilmerm/alanube-python.git
    cd alanube-python
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
        <td align="center">
            <a href="https://github.com/Bamidele123456">
                <img src="https://github.com/Bamidele123456.png" width="100px;" alt="Oriku Precious"/><br />
                <sub><b>Oriku Precious</b></sub>
            </a>
            <br/>Documentation Contributor
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

If you find this useful, consider supporting.

Your generosity helps us to continue improving and maintaining this project. We appreciate every contribution, however small. Thanks for being part of our community!

