# Usage Examples

This guide provides practical examples of how to use the Alanube Python API for common e-invoicing tasks.

## Table of Contents

- [Basic Setup](#basic-setup)
- [Company Management](#company-management)
- [Sending Documents](#sending-documents)
- [Retrieving Documents](#retrieving-documents)
- [Document Cancellations](#document-cancellations)
- [Received Documents](#received-documents)
- [Status Checking](#status-checking)
- [Error Handling](#error-handling)

## Basic Setup

First, import the library and connect to the API:

```python
from alanube.do import Alanube

# Connect to the API (use developer_mode=True for sandbox)
Alanube.connect("your_api_token", developer_mode=True)
```

## Company Management

### Create a Company

```python
company_payload = {
    "rnc": "123456789",
    "name": "My Company Name",
    "commercial_name": "My Company",
    "address": "123 Main Street",
    "city": "Santo Domingo",
    "state": "Distrito Nacional",
    "country": "DO",
    "phone": "+1-809-555-0123",
    "email": "contact@mycompany.com",
    "tax_regime": "General",
    "economic_activity": "Software Development"
}

response = Alanube.create_company(company_payload)
print(f"Company created with ID: {response['id']}")
```

### Update a Company

```python
update_payload = {
    "name": "Updated Company Name",
    "phone": "+1-809-555-0124"
}

response = Alanube.update_company(update_payload, company_id="your_company_id")
print("Company updated successfully")
```

### Get Company Details

```python
company = Alanube.get_company("your_company_id")
print(f"Company: {company['name']}")
print(f"RNC: {company['rnc']}")
```

## Sending Documents

### Send a Fiscal Invoice (NCF-E)

```python
invoice_payload = {
    "company_id": "your_company_id",
    "customer": {
        "rnc": "123456789",
        "name": "Customer Name",
        "address": "Customer Address",
        "city": "Santo Domingo",
        "state": "Distrito Nacional",
        "country": "DO",
        "phone": "+1-809-555-0000",
        "email": "customer@example.com"
    },
    "items": [
        {
            "description": "Software Development Services",
            "quantity": 1,
            "unit_price": 1000.00,
            "tax_rate": 18.00,
            "discount": 0.00
        },
        {
            "description": "Consulting Services",
            "quantity": 2,
            "unit_price": 500.00,
            "tax_rate": 18.00,
            "discount": 50.00
        }
    ],
    "payment_method": "Cash",
    "payment_terms": "Immediate",
    "notes": "Thank you for your business!"
}

response = Alanube.send_document(encf_type=31, payload=invoice_payload)
print(f"Fiscal Invoice sent successfully: {response['document_number']}")
```

### Send a Regular Invoice

```python
regular_invoice_payload = {
    "company_id": "your_company_id",
    "customer": {
        "name": "Customer Name",
        "address": "Customer Address",
        "email": "customer@example.com"
    },
    "items": [
        {
            "description": "Product Description",
            "quantity": 5,
            "unit_price": 25.00,
            "tax_rate": 18.00
        }
    ]
}

response = Alanube.send_document(encf_type=32, payload=regular_invoice_payload)
print(f"Invoice sent successfully: {response['document_number']}")
```

### Send a Credit Note

```python
credit_note_payload = {
    "company_id": "your_company_id",
    "original_document": "B0100000001",  # Original invoice number
    "customer": {
        "rnc": "123456789",
        "name": "Customer Name",
        "address": "Customer Address"
    },
    "items": [
        {
            "description": "Returned Product",
            "quantity": 1,
            "unit_price": 100.00,
            "tax_rate": 18.00,
            "reason": "Customer return"
        }
    ]
}

response = Alanube.send_document(encf_type=34, payload=credit_note_payload)
print(f"Credit Note sent successfully: {response['document_number']}")
```

### Send a Debit Note

```python
debit_note_payload = {
    "company_id": "your_company_id",
    "original_document": "B0100000001",  # Original invoice number
    "customer": {
        "rnc": "123456789",
        "name": "Customer Name",
        "address": "Customer Address"
    },
    "items": [
        {
            "description": "Additional Services",
            "quantity": 1,
            "unit_price": 50.00,
            "tax_rate": 18.00,
            "reason": "Additional work performed"
        }
    ]
}

response = Alanube.send_document(encf_type=33, payload=debit_note_payload)
print(f"Debit Note sent successfully: {response['document_number']}")
```

## Retrieving Documents

### Get a Specific Document

```python
# Get a fiscal invoice
invoice = Alanube.get_document(encf_type=31, document_id="document_id_here")
print(f"Document Status: {invoice['status']}")
print(f"Document Number: {invoice['document_number']}")

# Get a credit note
credit_note = Alanube.get_document(encf_type=34, document_id="credit_note_id_here")
print(f"Credit Note Status: {credit_note['status']}")
```

### List Documents with Filters

```python
# Get all fiscal invoices for a company
invoices = Alanube.get_documents(
    encf_type=31,
    company_id="your_company_id",
    status="approved",
    limit=50,
    page=1
)

for invoice in invoices['documents']:
    print(f"Invoice: {invoice['document_number']} - Status: {invoice['status']}")

# Get documents within a date range
from datetime import datetime

start_date = int(datetime(2024, 1, 1).timestamp())
end_date = int(datetime(2024, 12, 31).timestamp())

documents = Alanube.get_documents(
    encf_type=31,
    company_id="your_company_id",
    start=start_date,
    end=end_date,
    limit=100
)
```

## Document Cancellations

### Send a Cancellation Request

```python
cancellation_payload = {
    "company_id": "your_company_id",
    "document_number": "B0100000001",
    "reason": "Customer request",
    "document_type": 31  # Fiscal invoice
}

response = Alanube.send_cancellation(cancellation_payload)
print(f"Cancellation request sent: {response['id']}")
```

### Get Cancellation Details

```python
cancellation = Alanube.get_cancellation("cancellation_id_here")
print(f"Cancellation Status: {cancellation['status']}")
```

### List Cancellations

```python
cancellations = Alanube.get_cancellations(
    company_id="your_company_id",
    limit=25,
    page=1
)

for cancellation in cancellations['cancellations']:
    print(f"Cancellation: {cancellation['document_number']} - Status: {cancellation['status']}")
```

## Received Documents

### Get Received Document Details

```python
received_doc = Alanube.get_received_document("received_document_id_here")
print(f"Received Document: {received_doc['document_number']}")
print(f"Sender: {received_doc['sender']['name']}")
```

### List Received Documents

```python
received_docs = Alanube.get_received_documents(
    company_id="your_company_id",
    limit=25,
    page=1
)

for doc in received_docs['documents']:
    print(f"Received: {doc['document_number']} from {doc['sender']['name']}")
```

## Status Checking

### Check DGII Status

```python
dgii_status = Alanube.check_dgii_status(company_id="your_company_id")
print(f"DGII Status: {dgii_status['status']}")
```

### Check Directory Status

```python
directory_status = Alanube.check_directory(
    rnc="123456789",
    company_id="your_company_id"
)
print(f"Directory Status: {directory_status['status']}")
```

## Error Handling

The library provides comprehensive error handling. Here's how to handle common errors:

```python
from alanube.do import Alanube
from alanube.do.exceptions import AlanubeException, AuthenticationError, ValidationError

try:
    response = Alanube.send_document(encf_type=31, payload=invoice_payload)
    print("Document sent successfully!")
    
except AuthenticationError as e:
    print(f"Authentication failed: {e}")
    # Check your API token
    
except ValidationError as e:
    print(f"Validation error: {e}")
    # Check your payload format
    
except AlanubeException as e:
    print(f"Alanube API error: {e}")
    # Handle other API errors
    
except Exception as e:
    print(f"Unexpected error: {e}")
    # Handle unexpected errors
```

### Common Error Scenarios

```python
# Handle missing required fields
try:
    incomplete_payload = {
        "company_id": "your_company_id",
        # Missing customer and items
    }
    Alanube.send_document(encf_type=31, payload=incomplete_payload)
except ValidationError as e:
    print(f"Missing required fields: {e}")

# Handle invalid document type
try:
    Alanube.send_document(encf_type=99, payload=payload)  # Invalid type
except NotImplementedError as e:
    print(f"Unsupported document type: {e}")

# Handle network issues
try:
    Alanube.get_document(encf_type=31, document_id="invalid_id")
except AlanubeException as e:
    if "404" in str(e):
        print("Document not found")
    elif "500" in str(e):
        print("Server error, try again later")
```

## Best Practices

1. **Always use try-catch blocks** for error handling
2. **Store your API token securely** (use environment variables)
3. **Use developer_mode=True** for testing
4. **Validate your data** before sending
5. **Handle pagination** when retrieving large lists
6. **Cache responses** when appropriate
7. **Log important operations** for debugging

## Complete Example

Here's a complete example that demonstrates the full workflow:

```python
import os
from datetime import datetime
from alanube.do import Alanube
from alanube.do.exceptions import AlanubeException

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Connect to API
token = os.getenv('ALANUBE_TOKEN')
Alanube.connect(token, developer_mode=True)

try:
    # Create a company
    company_payload = {
        "rnc": "123456789",
        "name": "Example Company",
        "address": "123 Main St",
        "city": "Santo Domingo",
        "state": "Distrito Nacional",
        "country": "DO",
        "email": "contact@example.com"
    }
    
    company = Alanube.create_company(company_payload)
    company_id = company['id']
    print(f"Company created: {company_id}")
    
    # Send a fiscal invoice
    invoice_payload = {
        "company_id": company_id,
        "customer": {
            "rnc": "987654321",
            "name": "Customer Company",
            "address": "456 Customer St",
            "city": "Santo Domingo",
            "state": "Distrito Nacional",
            "country": "DO"
        },
        "items": [
            {
                "description": "Consulting Services",
                "quantity": 10,
                "unit_price": 100.00,
                "tax_rate": 18.00
            }
        ]
    }
    
    invoice = Alanube.send_document(encf_type=31, payload=invoice_payload)
    document_id = invoice['id']
    print(f"Fiscal invoice sent: {invoice['document_number']}")
    
    # Check document status
    status = Alanube.get_document(encf_type=31, document_id=document_id)
    print(f"Document status: {status['status']}")
    
    # List all documents
    documents = Alanube.get_documents(
        encf_type=31,
        company_id=company_id,
        limit=10
    )
    
    print(f"Total documents: {documents['total']}")
    for doc in documents['documents']:
        print(f"- {doc['document_number']}: {doc['status']}")
        
except AlanubeException as e:
    print(f"Error: {e}")
```

This example shows the complete workflow from creating a company to sending documents and checking their status. 