# Alanube Python API Documentation

Welcome to the official documentation for the Alanube Python API client. This library provides a lightweight and easy-to-use interface for connecting to the Alanube e-invoicing API across multiple countries.

[![PyPI version](https://img.shields.io/pypi/v/alanube.svg)](https://pypi.org/project/alanube/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

## 🚀 Quick Start

```python
from alanube.do import Alanube

# Connect to the API
Alanube.connect("your_api_token", developer_mode=True)

# Send a fiscal invoice
payload = {
    "company_id": "your_company_id",
    "customer": {
        "rnc": "123456789",
        "name": "Customer Name",
        "address": "Customer Address"
    },
    "items": [
        {
            "description": "Product Description",
            "quantity": 1,
            "unit_price": 100.00,
            "tax_rate": 18.00
        }
    ]
}

response = Alanube.send_document(encf_type=31, payload=payload)
print(response)
```

## 📚 Documentation Sections

### [Installation Guide](installation.md)
Complete setup instructions for getting started with the Alanube Python API.

### [Usage Examples](usage.md)
Practical examples showing how to use the library for common tasks.

### [API Reference](api-reference.md)
Comprehensive documentation of all available methods and parameters.

### [Country Support](countries.md)
Information about supported countries and their specific features.

## 🌍 Supported Countries

- 🇩🇴 **Dominican Republic (DGII)** - ✅ Fully implemented
- 🇵🇦 Panama - 🚧 Planned
- 🇨🇷 Costa Rica - 🚧 Planned
- 🇵🇪 Peru - 🚧 Planned
- 🇧🇴 Bolivia - 🚧 Planned

## 🤝 Used by

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

## 🔧 Features

- **Easy Integration**: Simple and intuitive API design
- **Multiple Document Types**: Support for invoices, credit notes, debit notes, and more
- **Country-Specific**: Tailored implementations for each country's requirements
- **Error Handling**: Comprehensive error handling and validation
- **Type Safety**: Full type hints for better development experience
- **Documentation**: Extensive documentation and examples

## 📋 Document Types Supported

| Type | Code | Description |
|------|------|-------------|
| Fiscal Invoice | 31 | Electronic fiscal invoice (NCF-E) |
| Invoice | 32 | Regular invoice |
| Debit Note | 33 | Debit note |
| Credit Note | 34 | Credit note |
| Purchase | 41 | Purchase document |
| Minor Expense | 43 | Minor expense document |
| Special Regime | 44 | Special regime document |
| Governmental | 45 | Governmental document |
| Export Support | 46 | Export support document |
| Payment Abroad Support | 47 | Payment abroad support document |

## 🛠️ Development

This project is actively maintained and welcomes contributions. See our [Contributing Guide](contributing.md) for more information.

## 📞 Support

- **Documentation**: This site
- **Issues**: [GitHub Issues](https://github.com/wilmerm/alanube-python/issues)
- **Website**: [Alanube Official Site](https://www.alanube.co/)
- **API Documentation**: [Alanube Developer Docs](https://developer.alanube.co/)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Ready to get started?** Check out our [Installation Guide](installation.md) to begin using the Alanube Python API!