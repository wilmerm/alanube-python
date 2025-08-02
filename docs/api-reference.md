# API Reference

This document provides comprehensive reference documentation for all methods available in the Alanube Python API.

## Table of Contents

- [Connection](#connection)
- [Company Management](#company-management)
- [Document Operations](#document-operations)
- [Cancellation Operations](#cancellation-operations)
- [Received Documents](#received-documents)
- [Status Checking](#status-checking)
- [Data Types](#data-types)
- [Error Handling](#error-handling)

## Connection

### `Alanube.connect(token, developer_mode)`

Establishes a connection to the Alanube API.

**Parameters:**
- `token` (str): Your Alanube API authentication token
- `developer_mode` (bool): Set to `True` for sandbox environment, `False` for production

**Example:**
```python
from alanube.do import Alanube

Alanube.connect("your_api_token", developer_mode=True)
```

## Company Management

### `Alanube.create_company(payload)`

Creates a new company in the Alanube system.

**Parameters:**
- `payload` (dict): Company information

**Payload Structure:**
```python
{
    "rnc": str,                    # Required: RNC number
    "name": str,                   # Required: Company name
    "commercial_name": str,        # Optional: Commercial name
    "address": str,                # Required: Company address
    "city": str,                   # Required: City
    "state": str,                  # Required: State/Province
    "country": str,                # Required: Country code (e.g., "DO")
    "phone": str,                  # Optional: Phone number
    "email": str,                  # Optional: Email address
    "tax_regime": str,             # Optional: Tax regime
    "economic_activity": str       # Optional: Economic activity
}
```

**Returns:** `dict` - Company information including the generated ID

**Example:**
```python
company_data = {
    "rnc": "123456789",
    "name": "My Company",
    "address": "123 Main St",
    "city": "Santo Domingo",
    "state": "Distrito Nacional",
    "country": "DO",
    "email": "contact@mycompany.com"
}

company = Alanube.create_company(company_data)
print(f"Company ID: {company['id']}")
```

### `Alanube.update_company(payload, company_id)`

Updates an existing company's information.

**Parameters:**
- `payload` (dict): Updated company information
- `company_id` (str, optional): Company ID (if not provided, uses default)

**Returns:** `dict` - Updated company information

### `Alanube.get_company(company_id)`

Retrieves company information.

**Parameters:**
- `company_id` (str, optional): Company ID (if not provided, uses default)

**Returns:** `dict` - Company information

## Document Operations

### `Alanube.send_document(encf_type, payload)`

Sends an electronic document of the specified type.

**Parameters:**
- `encf_type` (int): Document type code (see table below)
- `payload` (dict): Document data

**Document Types:**
| Type | Code | Method | Description |
|------|------|--------|-------------|
| Fiscal Invoice | 31 | `send_fiscal_invoice` | Electronic fiscal invoice (NCF-E) |
| Invoice | 32 | `send_invoice` | Regular invoice |
| Debit Note | 33 | `send_debit_note` | Debit note |
| Credit Note | 34 | `send_credit_note` | Credit note |
| Purchase | 41 | `send_purchase` | Purchase document |
| Minor Expense | 43 | `send_minor_expense` | Minor expense document |
| Special Regime | 44 | `send_special_regime` | Special regime document |
| Governmental | 45 | `send_gubernamental` | Governmental document |
| Export Support | 46 | `send_export_support` | Export support document |
| Payment Abroad Support | 47 | `send_payment_abroad_support` | Payment abroad support document |

**Common Payload Structure:**
```python
{
    "company_id": str,             # Required: Company ID
    "customer": {                  # Required: Customer information
        "rnc": str,               # Optional: Customer RNC
        "name": str,              # Required: Customer name
        "address": str,           # Required: Customer address
        "city": str,              # Optional: City
        "state": str,             # Optional: State
        "country": str,           # Optional: Country code
        "phone": str,             # Optional: Phone
        "email": str              # Optional: Email
    },
    "items": [                    # Required: List of items
        {
            "description": str,   # Required: Item description
            "quantity": float,    # Required: Quantity
            "unit_price": float,  # Required: Unit price
            "tax_rate": float,    # Required: Tax rate percentage
            "discount": float     # Optional: Discount amount
        }
    ],
    "payment_method": str,        # Optional: Payment method
    "payment_terms": str,         # Optional: Payment terms
    "notes": str                  # Optional: Additional notes
}
```

**Returns:** `DocumentResponse` - Document information including ID and status

**Example:**
```python
payload = {
    "company_id": "company_id_here",
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
print(f"Document ID: {response['id']}")
print(f"Document Number: {response['document_number']}")
```

### `Alanube.get_document(encf_type, document_id, company_id)`

Retrieves a specific document's information.

**Parameters:**
- `encf_type` (int): Document type code
- `document_id` (str): Document ID
- `company_id` (str, optional): Company ID (if not provided, uses default)

**Returns:** `DocumentResponse` - Document information

### `Alanube.get_documents(encf_type, **filters)`

Retrieves a list of documents with optional filtering.

**Parameters:**
- `encf_type` (int): Document type code
- `company_id` (str, optional): Filter by company ID
- `status` (str, optional): Filter by document status
- `legal_status` (str, optional): Filter by legal status
- `document_number` (str, optional): Filter by document number
- `limit` (int, optional): Number of documents per page (default: 25)
- `page` (int, optional): Page number (default: 1)
- `start` (int, optional): Start date timestamp
- `end` (int, optional): End date timestamp

**Returns:** `ListDocumentResponse` - Paginated list of documents

**Example:**
```python
# Get all approved fiscal invoices
documents = Alanube.get_documents(
    encf_type=31,
    company_id="company_id_here",
    status="approved",
    limit=50,
    page=1
)

print(f"Total documents: {documents['total']}")
for doc in documents['documents']:
    print(f"- {doc['document_number']}: {doc['status']}")
```

## Cancellation Operations

### `Alanube.send_cancellation(payload)`

Sends a cancellation request for a document.

**Parameters:**
- `payload` (dict): Cancellation information

**Payload Structure:**
```python
{
    "company_id": str,            # Required: Company ID
    "document_number": str,       # Required: Document number to cancel
    "reason": str,                # Required: Cancellation reason
    "document_type": int          # Required: Document type code
}
```

**Returns:** `dict` - Cancellation information including ID

### `Alanube.get_cancellation(cancellation_id, company_id)`

Retrieves cancellation information.

**Parameters:**
- `cancellation_id` (str): Cancellation ID
- `company_id` (str, optional): Company ID (if not provided, uses default)

**Returns:** `dict` - Cancellation information

### `Alanube.get_cancellations(**filters)`

Retrieves a list of cancellations.

**Parameters:**
- `company_id` (str, optional): Filter by company ID
- `limit` (int, optional): Number of cancellations per page (default: 25)
- `page` (int, optional): Page number (default: 1)
- `start` (int, optional): Start date timestamp
- `end` (int, optional): End date timestamp

**Returns:** `dict` - Paginated list of cancellations

## Received Documents

### `Alanube.get_received_document(document_id, company_id)`

Retrieves information about a received document.

**Parameters:**
- `document_id` (str): Received document ID
- `company_id` (str, optional): Company ID (if not provided, uses default)

**Returns:** `ReceivedDocumentsResponse` - Received document information

### `Alanube.get_received_documents(**filters)`

Retrieves a list of received documents.

**Parameters:**
- `company_id` (str, optional): Filter by company ID
- `limit` (int, optional): Number of documents per page (default: 25)
- `page` (int, optional): Page number (default: 1)
- `start` (int, optional): Start date timestamp
- `end` (int, optional): End date timestamp

**Returns:** `ListReceivedDocumentsResponse` - Paginated list of received documents

## Status Checking

### `Alanube.check_dgii_status(environment, maintenance, company_id)`

Checks the status of a company with the DGII.

**Parameters:**
- `environment` (int, optional): Environment type
- `maintenance` (bool, optional): Check maintenance status
- `company_id` (str, optional): Company ID (if not provided, uses default)

**Returns:** `dict` or `list` - DGII status information

### `Alanube.check_directory(rnc, company_id)`

Checks the directory status of a company.

**Parameters:**
- `rnc` (str, optional): RNC number to check
- `company_id` (str, optional): Company ID (if not provided, uses default)

**Returns:** `dict` - Directory status information

## Data Types

### DocumentResponse

```python
{
    "id": str,                    # Document ID
    "document_number": str,       # Document number
    "status": str,                # Document status
    "legal_status": str,          # Legal status
    "created_at": str,            # Creation timestamp
    "updated_at": str,            # Last update timestamp
    "company_id": str,            # Associated company ID
    "customer": dict,             # Customer information
    "items": list,                # Document items
    "totals": dict,               # Document totals
    "metadata": dict              # Additional metadata
}
```

### ListDocumentResponse

```python
{
    "documents": list,            # List of documents
    "total": int,                 # Total number of documents
    "page": int,                  # Current page
    "limit": int,                 # Documents per page
    "pages": int                  # Total number of pages
}
```

### ReceivedDocumentsResponse

```python
{
    "id": str,                    # Document ID
    "document_number": str,       # Document number
    "status": str,                # Document status
    "received_at": str,           # Reception timestamp
    "sender": dict,               # Sender information
    "items": list,                # Document items
    "totals": dict,               # Document totals
    "metadata": dict              # Additional metadata
}
```

### ListReceivedDocumentsResponse

```python
{
    "documents": list,            # List of received documents
    "total": int,                 # Total number of documents
    "page": int,                  # Current page
    "limit": int,                 # Documents per page
    "pages": int                  # Total number of pages
}
```

## Error Handling

The library uses custom exception classes for different types of errors:

### AlanubeException

Base exception class for all Alanube API errors.

### AuthenticationError

Raised when authentication fails (invalid token, expired token, etc.).

### ValidationError

Raised when request data validation fails (missing required fields, invalid format, etc.).

### RateLimitError

Raised when API rate limits are exceeded.

### ServerError

Raised when the Alanube API server returns an error.

**Example Error Handling:**
```python
from alanube.do.exceptions import (
    AlanubeException,
    AuthenticationError,
    ValidationError,
    RateLimitError,
    ServerError
)

try:
    response = Alanube.send_document(encf_type=31, payload=payload)
except AuthenticationError:
    print("Authentication failed - check your API token")
except ValidationError as e:
    print(f"Validation error: {e}")
except RateLimitError:
    print("Rate limit exceeded - wait before retrying")
except ServerError:
    print("Server error - try again later")
except AlanubeException as e:
    print(f"Alanube API error: {e}")
```

## Response Status Codes

The API returns standard HTTP status codes:

- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `429` - Too Many Requests
- `500` - Internal Server Error

## Rate Limiting

The API implements rate limiting to ensure fair usage. When rate limits are exceeded, the library will raise a `RateLimitError`. Implement exponential backoff for retries:

```python
import time
from alanube.do.exceptions import RateLimitError

def send_document_with_retry(payload, max_retries=3):
    for attempt in range(max_retries):
        try:
            return Alanube.send_document(encf_type=31, payload=payload)
        except RateLimitError:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                time.sleep(wait_time)
                continue
            else:
                raise
```

## Best Practices

1. **Always handle exceptions** - Use try-catch blocks for all API calls
2. **Validate data** - Ensure your payloads contain all required fields
3. **Use pagination** - When retrieving large lists, use the pagination parameters
4. **Cache responses** - Cache frequently accessed data to reduce API calls
5. **Monitor rate limits** - Implement proper retry logic for rate limit errors
6. **Log operations** - Log important operations for debugging and monitoring
7. **Use environment variables** - Store sensitive data like API tokens securely 