# Country Support

This document provides detailed information about country-specific features and implementations in the Alanube Python API.

## Table of Contents

- [Supported Countries](#supported-countries)
- [Dominican Republic (DGII)](#dominican-republic-dgii)
- [Planned Countries](#planned-countries)
- [Country-Specific Features](#country-specific-features)
- [Implementation Guidelines](#implementation-guidelines)

## Supported Countries

### 🇩🇴 Dominican Republic (DGII) - ✅ Fully Implemented

The Dominican Republic implementation is fully functional and supports all major e-invoicing operations through the DGII (Dirección General de Impuestos Internos) system.

**Module:** `alanube.do`

**Features:**
- ✅ Company registration and management
- ✅ All document types (NCF-E, invoices, credit/debit notes, etc.)
- ✅ Document cancellation
- ✅ Received documents handling
- ✅ DGII status checking
- ✅ Directory validation
- ✅ Comprehensive error handling

**Document Types Supported:**
| Type | Code | Description | DGII Name |
|------|------|-------------|-----------|
| Fiscal Invoice | 31 | Electronic fiscal invoice | NCF-E |
| Invoice | 32 | Regular invoice | Factura |
| Debit Note | 33 | Debit note | Nota de Débito |
| Credit Note | 34 | Credit note | Nota de Crédito |
| Purchase | 41 | Purchase document | Comprobante de Compra |
| Minor Expense | 43 | Minor expense document | Comprobante de Consumo |
| Special Regime | 44 | Special regime document | Comprobante de Régimen Especial |
| Governmental | 45 | Governmental document | Comprobante Gubernamental |
| Export Support | 46 | Export support document | Comprobante de Exportación |
| Payment Abroad Support | 47 | Payment abroad support document | Comprobante de Pago en el Exterior |

**Usage Example:**
```python
from alanube.do import Alanube

# Connect to DGII API
Alanube.connect("your_api_token", developer_mode=True)

# Send a fiscal invoice (NCF-E)
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
print(f"NCF-E generated: {response['document_number']}")
```

**DGII-Specific Features:**

1. **RNC Validation**
   - Automatic RNC (Registro Nacional de Contribuyentes) validation
   - Directory status checking
   - Company information retrieval

2. **Tax Calculations**
   - ITBIS (Impuesto sobre Transferencias de Bienes Industrializados y Servicios) calculation
   - Support for different tax rates (0%, 18%, etc.)
   - Automatic total calculations

3. **Document Numbering**
   - Automatic NCF (Número de Comprobante Fiscal) generation
   - Sequential numbering per company
   - Format validation

4. **Legal Compliance**
   - DGII format compliance
   - Required field validation
   - Legal status tracking

## Planned Countries

### 🇵🇦 Panama - 🚧 Planned

**Status:** Development planned
**Expected Features:**
- Company registration
- Electronic invoicing
- Tax calculations
- DGI (Dirección General de Ingresos) integration

**Document Types:**
- Electronic invoices
- Credit notes
- Debit notes
- Purchase receipts

### 🇨🇷 Costa Rica - 🚧 Planned

**Status:** Development planned
**Expected Features:**
- Company registration
- Electronic invoicing
- Hacienda integration
- Tax calculations

**Document Types:**
- Electronic invoices
- Credit notes
- Debit notes
- Purchase receipts

### 🇵🇪 Peru - 🚧 Planned

**Status:** Development planned
**Expected Features:**
- Company registration
- Electronic invoicing
- SUNAT integration
- Tax calculations

**Document Types:**
- Electronic invoices
- Credit notes
- Debit notes
- Purchase receipts

### 🇧🇴 Bolivia - 🚧 Planned

**Status:** Development planned
**Expected Features:**
- Company registration
- Electronic invoicing
- SIN integration
- Tax calculations

**Document Types:**
- Electronic invoices
- Credit notes
- Debit notes
- Purchase receipts

## Country-Specific Features

### Tax Systems

Each country has its own tax system and requirements:

**Dominican Republic (DGII):**
- ITBIS: 18% (standard), 0% (exempt)
- ISC: Selective consumption tax
- IT-1: Income tax withholding

**Panama (DGI):**
- ITBMS: 7% (standard), 0% (exempt)
- ISR: Income tax

**Costa Rica (Hacienda):**
- IVA: 13% (standard), 0% (exempt)
- ISR: Income tax

**Peru (SUNAT):**
- IGV: 18% (standard), 0% (exempt)
- ISC: Selective consumption tax

**Bolivia (SIN):**
- IVA: 13% (standard), 0% (exempt)
- ICE: Special consumption tax

### Document Numbering Systems

**Dominican Republic:**
- NCF (Número de Comprobante Fiscal)
- Format: A0100000001
- Sequential numbering per company

**Panama:**
- FEC (Factura Electrónica de Consumo)
- Format: TBD
- Sequential numbering

**Costa Rica:**
- FE (Factura Electrónica)
- Format: TBD
- Sequential numbering

**Peru:**
- CPE (Comprobante de Pago Electrónico)
- Format: TBD
- Sequential numbering

**Bolivia:**
- FE (Factura Electrónica)
- Format: TBD
- Sequential numbering

### Validation Requirements

Each country has specific validation requirements:

**Dominican Republic:**
- RNC validation
- Customer information validation
- Tax rate validation
- Document format validation

**Other Countries:**
- Tax ID validation
- Customer information validation
- Tax rate validation
- Document format validation

## Implementation Guidelines

### Adding New Country Support

To add support for a new country, follow these guidelines:

1. **Create Country Module**
   ```python
   # alanube/pa/__init__.py (for Panama)
   from .api import AlanubeAPI
   
   class Alanube:
       # Implement country-specific methods
       pass
   ```

2. **Implement Required Methods**
   - `connect()` - API connection
   - `create_company()` - Company registration
   - `send_document()` - Document sending
   - `get_document()` - Document retrieval
   - `get_documents()` - Document listing
   - Country-specific validation methods

3. **Add Configuration**
   ```python
   # alanube/pa/config.py
   class APIConfig:
       def __init__(self, token, developer_mode):
           self.token = token
           self.developer_mode = developer_mode
           # Country-specific configuration
   ```

4. **Implement Error Handling**
   ```python
   # alanube/pa/exceptions.py
   class PanamaException(AlanubeException):
       pass
   ```

5. **Add Type Definitions**
   ```python
   # alanube/pa/types.py
   from dataclasses import dataclass
   
   @dataclass
   class DocumentResponse:
       # Country-specific response structure
       pass
   ```

6. **Create Tests**
   ```python
   # alanube/pa/tests/test_api.py
   import unittest
   
   class TestPanamaAPI(unittest.TestCase):
       def test_send_document(self):
           # Test implementation
           pass
   ```

### Country-Specific Considerations

1. **API Endpoints**
   - Each country may have different API endpoints
   - Authentication methods may vary
   - Rate limiting policies may differ

2. **Data Formats**
   - Document structures may vary
   - Required fields may differ
   - Validation rules may be country-specific

3. **Tax Calculations**
   - Tax rates and rules vary by country
   - Calculation methods may differ
   - Exemptions and special cases

4. **Legal Requirements**
   - Document retention requirements
   - Reporting requirements
   - Compliance deadlines

### Testing Strategy

1. **Unit Tests**
   - Test individual methods
   - Mock API responses
   - Test error conditions

2. **Integration Tests**
   - Test with real API endpoints
   - Test end-to-end workflows
   - Test country-specific features

3. **Compliance Tests**
   - Test legal compliance
   - Test format validation
   - Test tax calculations

### Documentation Requirements

For each new country implementation:

1. **API Reference**
   - Document all methods
   - Provide usage examples
   - List country-specific parameters

2. **Installation Guide**
   - Country-specific setup instructions
   - Configuration requirements
   - Troubleshooting guide

3. **Usage Examples**
   - Common use cases
   - Best practices
   - Error handling examples

4. **Compliance Guide**
   - Legal requirements
   - Format specifications
   - Validation rules

## Migration Guide

When migrating from one country implementation to another:

1. **API Changes**
   - Different method signatures
   - Different parameter names
   - Different response formats

2. **Data Migration**
   - Company data format changes
   - Document format changes
   - Tax calculation changes

3. **Configuration Changes**
   - Different API endpoints
   - Different authentication methods
   - Different rate limits

## Support and Maintenance

### Current Support

- **Dominican Republic**: Full support with regular updates
- **Other Countries**: Development in progress

### Maintenance Schedule

- **Bug Fixes**: As needed
- **Feature Updates**: Quarterly
- **Compliance Updates**: As regulations change
- **Security Updates**: Monthly

### Contributing

To contribute to country implementations:

1. Fork the repository
2. Create a feature branch
3. Implement the country-specific code
4. Add comprehensive tests
5. Update documentation
6. Submit a pull request

For more information about contributing, see the [Contributing Guide](contributing.md). 