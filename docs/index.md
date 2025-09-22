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
  "company": {
    "id": "FAKE-01FV0123456789000000"
  },
  "idDoc": {
    "encf": "E310000000001",
    "sequenceDueDate": "1990-12-31",
    "deferredDeliveryIndicator": 1,
    "taxAmountIndicator": 1,
    "incomeType": 1,
    "paymentType": 1,
    "paymentDeadline": "1990-12-31",
    "paymentTerm": "72 horas",
    "paymentFormsTable": [
      {
        "paymentMethod": 1,
        "paymentAmount": 24300
      }
    ],
    "paymentAccountType": "CT",
    "paymentAccountNumber": 1212453611324,
    "bankPayment": "Banco estatal",
    "dateFrom": "1990-12-31",
    "dateUntil": "1990-12-31",
    "totalPages": 3
  },
  "sender": {
    "rnc": "133109124",
    "companyName": "Mi compañía",
    "tradename": "Mi compañía S.A.",
    "branchOffice": "Mi sucursal",
    "address": "30 De Marzo 9 Sd",
    "municipality": "020101",
    "province": "020000",
    "phoneNumber": [
      [
        "809-123-4567",
        "809-123-4570"
      ]
    ],
    "mail": "user@example.com",
    "webSite": "example.com",
    "economicActivity": "Componenetes electrónicos",
    "sellerCode": "A10002121",
    "internalInvoiceNumber": "2023",
    "internalOrderNumber": "202",
    "saleArea": "Ventas",
    "saleRoute": "Principal",
    "additionalInformationIssuer": "Información adicional de emisor...",
    "stampDate": "1990-12-31"
  },
  "buyer": {
    "rnc": "133109124",
    "companyName": "Su compañía",
    "contact": "David Pérez",
    "mail": "user@example.com",
    "address": "30 De Marzo 9 Sd",
    "municipality": "020101",
    "province": "020000",
    "deliverDate": "1990-12-31",
    "contactDelivery": "30 De Marzo 9 Sd",
    "deliveryAddress": "30 De Marzo 9 Sd",
    "additionalPhone": "333-222-2454",
    "purchaseOrderDate": "1990-12-31",
    "purchaseOrderNumber": 420,
    "internalCode": "A0001212",
    "responsibleForPayment": 101215465,
    "additionalInformation": "Informacion adicional del comprador..."
  },
  "additionalInformation": {
    "shippingDate": "1990-12-31",
    "shipmentNumber": "A24000000126",
    "containerNumber": 1000025,
    "referenceNumber": 1234,
    "grossWeight": 228,
    "netWeight": 227,
    "grossWeightUnit": 10,
    "unitNetWeight": 10,
    "bulkQuantity": 1000,
    "bulkUnit": 10,
    "bulkVolume": 1000,
    "unitVolume": 10
  },
  "transport": {
    "driver": "A20020",
    "transportDocument": 20020,
    "file": "AZ100200",
    "licensePlate": "ED00168",
    "transportationRoute": "Principal",
    "transportationZone": "Zona de transporte",
    "albaranNumber": 20023
  },
  "totals": {
    "totalTaxedAmount": 4000,
    "i1AmountTaxed": 1000,
    "i2AmountTaxed": 1000,
    "i3AmountTaxed": 1000,
    "exemptAmount": 1000,
    "itbisS1": 18,
    "itbisS2": 16,
    "itbisS3": 0,
    "itbisTotal": 340,
    "itbis1Total": 180,
    "itbis2Total": 160,
    "itbis3Total": 0,
    "additionalTaxAmount": 270,
    "additionalTaxes": [
      {
        "taxType": 6,
        "additionalTaxRate": 632.58,
        "selectiveTaxAmountSpecificConsumption": 24300,
        "amountSelectiveConsumptionTaxAdvalorem": 24300,
        "otherAdditionalTaxes": 24300
      }
    ],
    "totalAmount": 88757.68,
    "nonBillableAmount": 88757.68,
    "amountPeriod": 88757.68,
    "previousBalance": 88757.68,
    "amountAdvancePayment": 88757.68,
    "payValue": 2000,
    "itbisTotalRetained": 2000,
    "isrTotalRetention": 2000,
    "itbisTotalPerception": 2000,
    "isrTotalPerception": 2000
  },
  "otherCurrency": {
    "currencyType": "USD",
    "exchangeRate": 100.8,
    "totalTaxedAmountOtherCurrency": 2000,
    "amountTaxed1OtherCurrency": 2000,
    "amountTaxed2OtherCurrency": 2000,
    "amountTaxed3OtherCurrency": 2000,
    "exemptAmountOtherCurrency": 2000,
    "itbisTotalOtherCurrency": 2000,
    "itbis1TotalOtherCurrency": 2000,
    "itbis2TotalOtherCurrency": 2000,
    "itbis3TotalOtherCurrency": 2000,
    "additionalTaxAmountOtherCurrency": 2000,
    "additionalTaxesOtherCurrency": [
      {
        "taxTypeOtherCurrency": 6,
        "additionalTaxRateOtherCurrency": 632.58,
        "selectiveTaxAmountSpecificConsumptionOtherCurrency": 24300,
        "amountSelectiveConsumptionTaxAdvaloremOtherCurrency": 24300,
        "otherAdditionalTaxesOtherCurrency": 24300
      }
    ],
    "totalAmountOtherCurrency": 24300
  },
  "itemDetails": [
    {
      "lineNumber": 1,
      "itemCodeTable": [
        {
          "codeType": "Interna",
          "itemCode": "A001212"
        }
      ],
      "billingIndicator": 0,
      "retention": {
        "indicatorAgentWithholdingPerception": 1,
        "itbisAmountWithheld": 24300,
        "isrAmountWithheld": 24300
      },
      "itemName": "Caja de madera",
      "goodServiceIndicator": 1,
      "itemDescription": "Fabricado con madera de arce canadience",
      "quantityItem": 24300,
      "unitMeasure": 0,
      "quantityReference": 24300,
      "referenceUnit": 4,
      "subquantityTable": [
        {
          "subquantity": 24300,
          "codeSubquantity": 3
        }
      ],
      "degreesAlcohol": 0,
      "unitPriceReference": 24300,
      "elaborationDate": "1990-12-31",
      "expirationDateItem": "1990-12-31",
      "unitPriceItem": 24300,
      "discountAmount": 24300,
      "subDiscounts": [
        {
          "subDiscountRate": "$",
          "subDiscountPercentage": 0,
          "subDiscountAmount": 24300
        }
      ],
      "surchargeAmount": 24300,
      "subSurcharge": [
        {
          "subSurchargeType": "$",
          "subSurchargePercentage": 0,
          "subSurchargeAmount": 24300
        }
      ],
      "additionalTaxes": [
        {
          "taxType": 6
        }
      ],
      "otherCurrencyDetail": {
        "priceOtherCurrency": 24300,
        "discountOtherCurrency": 24300,
        "surchargeAnotherCurrency": 24300,
        "amountItemOtherCurrency": 24300
      },
      "itemAmount": 24300
    }
  ],
  "subtotals": [
    {
      "subTotalNumber": 1,
      "subtotalDescription": "Subtotal 1",
      "order": 1,
      "subTotalAmountTaxedTotal": 24300,
      "subTotalAmountTaxedI1": 24300,
      "subTotalAmountTaxedI2": 24300,
      "subTotalAmountTaxedI3": 24300,
      "itbisSubTotal": 24300,
      "itbis1SubTotal": 24300,
      "itbis2SubTotal": 24300,
      "itbis3SubTotal": 24300,
      "subTotalAdditionalTax": 24300,
      "subTotalExempt": 24300,
      "subTotalAmount": 24300,
      "lines": 1
    }
  ],
  "discountsOrSurcharges": [
    {
      "lineNumber": 1,
      "fitType": "D",
      "norma1007Indicator": 1,
      "descriptionDiscountOrSurcharge": "Descuendo por el día de la madre",
      "typeValue": "%",
      "discountValueOrSurcharge": 0,
      "discountAmountOrSurcharge": 24300,
      "discountAmountOrSurchargeOtherCurrency": 24300,
      "indicatorBillingDiscountOrSurcharge": 1
    }
  ],
  "pagination": [
    {
      "pageNo": 1,
      "noLineFrom": 1,
      "noLineUntil": 1,
      "subtotalAmountTaxedPage": 24300,
      "subtotalAmountTaxed1Page": 24300,
      "subtotalAmountTaxed2Page": 24300,
      "subtotalAmountTaxed3Page": 24300,
      "exemptSubtotalPage": 24300,
      "itbisSubtotalPage": 24300,
      "itbis1SubtotalPage": 24300,
      "itbis2SubtotalPage": 24300,
      "itbis3SubtotalPage": 24300,
      "subtotalAdditionalTaxPage": 24300,
      "subtotalAdditionalTax": {
        "subtotalSelectiveTaxForSpecificConsumptionPage": 24300,
        "subtotalOtherTax": 24300
      },
      "subtotalAmountPage": 24300,
      "subtotalNonBillableAmountPage": 24300
    }
  ],
  "informationReference": {
    "ncfModified": 1090012500,
    "rncOtherTaxpayer": "101212154",
    "ncfModifiedDate": "1990-12-31",
    "modificationCode": 4
  },
  "config": {
    "pdf": {
      "type": "generic",
      "note": "Nota de prueba"
    }
  }
}

data = Alanube.send_document(encf_type=31, payload=payload)
print(data)

# Output
{
  "id": "01G021Z3QSRZ58GSTBH7TPGD2J",
  "stampDate": "1990-12-31",
  "status": "REGISTERED",
  "companyIdentification": 132109122,
  "encf": "E310000000001",
  "xml": "https://api-alanube-e-provider-dom-test.s3.amazonaws.com/users/...",
  "pdf": "https://api-alanube-e-provider-dom-test.s3.amazonaws.com/users/...",
  "documentStampUrl": "https://ecf.dgii.gov.do/testecf/ConsultaTimbre?...",
  "signatureDate": "2025-09-22T13:46:23.350Z",
  "securityCode": "MYUVCT",
  "sequenceConsumed": False
}
```

## 📚 Documentation Sections

### [Installation Guide](installation.md)
Complete setup instructions for getting started with the Alanube Python API.

### [Usage Examples](usage.md)
Practical examples showing how to use the library for common tasks.

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