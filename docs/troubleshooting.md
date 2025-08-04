# Troubleshooting Guide

This guide helps you resolve common issues when using the Alanube Python API.

## Table of Contents

- [Installation Issues](#installation-issues)
- [Authentication Issues](#authentication-issues)
- [API Connection Issues](#api-connection-issues)
- [Document Sending Issues](#document-sending-issues)
- [Validation Issues](#validation-issues)
- [Performance Issues](#performance-issues)
- [Country-Specific Issues](#country-specific-issues)
- [Getting Help](#getting-help)

## Installation Issues

### Import Error: No module named 'alanube'

**Symptoms:**
```python
ImportError: No module named 'alanube'
```

**Solutions:**

1. **Verify Installation:**
   ```bash
   pip list | grep alanube
   ```

2. **Reinstall the Package:**
   ```bash
   pip uninstall alanube
   pip install alanube
   ```

3. **Check Python Environment:**
   ```bash
   python --version
   which python
   pip --version
   ```

4. **Use Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install alanube
   ```

### Version Compatibility Issues

**Symptoms:**
```python
TypeError: 'module' object is not callable
```

**Solutions:**

1. **Check Python Version:**
   - Ensure you're using Python 3.10 or higher
   - The library requires Python 3.10+

2. **Update Python:**
   ```bash
   # On Ubuntu/Debian
   sudo apt update
   sudo apt install python3.10

   # On macOS with Homebrew
   brew install python@3.10

   # On Windows, download from python.org
   ```

## Authentication Issues

### Invalid Token Error

**Symptoms:**
```python
alanube.do.exceptions.AuthenticationError: Invalid API token
```

**Solutions:**

1. **Verify Token:**
   - Check your API token in the Alanube dashboard
   - Ensure the token is copied correctly (no extra spaces)
   - Verify the token hasn't expired

2. **Regenerate Token:**
   - Log into your Alanube account
   - Go to API settings
   - Generate a new token
   - Update your code with the new token

3. **Check Environment Variables:**
   ```python
   import os
   print(os.getenv('ALANUBE_TOKEN'))  # Should not be None
   ```

### Token Expired

**Symptoms:**
```python
alanube.do.exceptions.AuthenticationError: Token expired
```

**Solutions:**

1. **Generate New Token:**
   - Log into Alanube dashboard
   - Navigate to API settings
   - Generate a new token

2. **Update Your Code:**
   ```python
   # Update your token
   Alanube.connect("new_token_here", developer_mode=True)
   ```

3. **Use Environment Variables:**
   ```python
   import os
   from dotenv import load_dotenv

   load_dotenv()
   token = os.getenv('ALANUBE_TOKEN')
   Alanube.connect(token, developer_mode=True)
   ```

## API Connection Issues

### Connection Timeout

**Symptoms:**
```python
requests.exceptions.ConnectTimeout: HTTPSConnectionPool
```

**Solutions:**

1. **Check Internet Connection:**
   ```bash
   ping api.alanube.co
   ```

2. **Increase Timeout:**
   ```python
   import requests
   from alanube.do import Alanube

   # Set longer timeout
   requests.adapters.DEFAULT_RETRIES = 5
   ```

3. **Use Retry Logic:**
   ```python
   import time
   from alanube.do.exceptions import AlanubeException

   def send_with_retry(payload, max_retries=3):
       for attempt in range(max_retries):
           try:
               return Alanube.send_document(encf_type=31, payload=payload)
           except AlanubeException as e:
               if "timeout" in str(e).lower() and attempt < max_retries - 1:
                   time.sleep(2 ** attempt)  # Exponential backoff
                   continue
               raise
   ```

### SSL Certificate Issues

**Symptoms:**
```python
requests.exceptions.SSLError: SSL certificate verification failed
```

**Solutions:**

1. **Update Certificates:**
   ```bash
   # On Ubuntu/Debian
   sudo apt update
   sudo apt install ca-certificates

   # On macOS
   brew install ca-certificates
   ```

2. **Update Python:**
   ```bash
   pip install --upgrade certifi
   ```

3. **Temporary Workaround (Not Recommended for Production):**
   ```python
   import ssl
   import requests

   # Disable SSL verification (use only for testing)
   ssl._create_default_https_context = ssl._create_unverified_context
   ```

## Document Sending Issues

### Validation Errors

**Symptoms:**
```python
alanube.do.exceptions.ValidationError: Missing required field 'company_id'
```

**Solutions:**

1. **Check Payload Structure:**
   ```python
   # Ensure all required fields are present
   payload = {
       "company_id": "your_company_id",  # Required
       "customer": {
           "name": "Customer Name",      # Required
           "address": "Customer Address" # Required
       },
       "items": [                       # Required
           {
               "description": "Product", # Required
               "quantity": 1,           # Required
               "unit_price": 100.00,    # Required
               "tax_rate": 18.00        # Required
           }
       ]
   }
   ```

2. **Validate Data Types:**
   ```python
   # Ensure correct data types
   payload = {
       "company_id": str(company_id),    # Must be string
       "items": [
           {
               "quantity": float(quantity),    # Must be float
               "unit_price": float(price),     # Must be float
               "tax_rate": float(tax_rate)     # Must be float
           }
       ]
   }
   ```

### Document Type Not Supported

**Symptoms:**
```python
NotImplementedError: No implementation for eNCF type: 99
```

**Solutions:**

1. **Check Supported Types:**
   ```python
   # Supported document types
   SUPPORTED_TYPES = {
       31: "Fiscal Invoice",
       32: "Invoice",
       33: "Debit Note",
       34: "Credit Note",
       41: "Purchase",
       43: "Minor Expense",
       44: "Special Regime",
       45: "Governmental",
       46: "Export Support",
       47: "Payment Abroad Support"
   }
   ```

2. **Use Correct Type:**
   ```python
   # Use the correct document type
   response = Alanube.send_document(encf_type=31, payload=payload)  # Fiscal Invoice
   ```

## Validation Issues

### RNC Validation Failed

**Symptoms:**
```python
alanube.do.exceptions.ValidationError: Invalid RNC format
```

**Solutions:**

1. **Check RNC Format:**
   ```python
   # RNC must be 9 or 11 digits
   rnc = "123456789"  # 9 digits
   rnc = "12345678901"  # 11 digits
   ```

2. **Validate RNC:**
   ```python
   import re

   def validate_rnc(rnc):
       # Remove any non-digit characters
       rnc_clean = re.sub(r'\D', '', str(rnc))

       # Check length
       if len(rnc_clean) not in [9, 11]:
           raise ValueError("RNC must be 9 or 11 digits")

       return rnc_clean
   ```

### Tax Rate Validation

**Symptoms:**
```python
alanube.do.exceptions.ValidationError: Invalid tax rate
```

**Solutions:**

1. **Use Valid Tax Rates:**
   ```python
   # Valid tax rates for Dominican Republic
   VALID_TAX_RATES = [0.0, 18.0]  # 0% and 18%

   # Check tax rate
   if tax_rate not in VALID_TAX_RATES:
       raise ValueError(f"Tax rate must be one of {VALID_TAX_RATES}")
   ```

2. **Format Tax Rate:**
   ```python
   # Ensure tax rate is a float
   tax_rate = float(tax_rate)
   ```

## Performance Issues

### Slow Response Times

**Symptoms:**
- API calls taking longer than expected
- Timeout errors

**Solutions:**

1. **Optimize Payload Size:**
   ```python
   # Remove unnecessary fields
   payload = {
       "company_id": company_id,
       "customer": {
           "name": customer_name,
           "address": customer_address
           # Only include required fields
       },
       "items": items
   }
   ```

2. **Use Connection Pooling:**
   ```python
   import requests

   # Create a session for connection pooling
   session = requests.Session()
   session.mount('https://', requests.adapters.HTTPAdapter(
       pool_connections=10,
       pool_maxsize=10
   ))
   ```

3. **Implement Caching:**
   ```python
   import functools

   @functools.lru_cache(maxsize=128)
   def get_company_info(company_id):
       return Alanube.get_company(company_id)
   ```

### Rate Limiting

**Symptoms:**
```python
alanube.do.exceptions.RateLimitError: Rate limit exceeded
```

**Solutions:**

1. **Implement Exponential Backoff:**
   ```python
   import time
   import random

   def send_with_backoff(payload, max_retries=5):
       for attempt in range(max_retries):
           try:
               return Alanube.send_document(encf_type=31, payload=payload)
           except RateLimitError:
               if attempt < max_retries - 1:
                   wait_time = (2 ** attempt) + random.uniform(0, 1)
                   time.sleep(wait_time)
                   continue
               raise
   ```

2. **Batch Requests:**
   ```python
   # Instead of sending multiple requests quickly
   # Batch them or add delays
   import time

   for payload in payloads:
       response = Alanube.send_document(encf_type=31, payload=payload)
       time.sleep(1)  # Add delay between requests
   ```

## Country-Specific Issues

### Dominican Republic (DGII) Issues

**RNC Directory Issues:**
```python
# If RNC is not found in directory
try:
    Alanube.check_directory(rnc="123456789")
except AlanubeException as e:
    if "not found" in str(e).lower():
        print("RNC not found in DGII directory")
        # Handle accordingly
```

**NCF Generation Issues:**
```python
# If NCF generation fails
try:
    response = Alanube.send_document(encf_type=31, payload=payload)
    ncf = response['document_number']
except AlanubeException as e:
    if "ncf" in str(e).lower():
        print("NCF generation failed")
        # Check company configuration
```

### Environment Issues

**Production vs Sandbox:**
```python
# Use sandbox for testing
Alanube.connect(token, developer_mode=True)  # Sandbox

# Use production for live data
Alanube.connect(token, developer_mode=False)  # Production
```

## Getting Help

### Before Asking for Help

1. **Check the Documentation:**
   - Review the [API Reference](api-reference.md)
   - Check [Usage Examples](usage.md)
   - Read [Installation Guide](installation.md)

2. **Search Existing Issues:**
   - Check [GitHub Issues](https://github.com/wilmerm/alanube-python/issues)
   - Search for similar problems

3. **Reproduce the Issue:**
   - Create a minimal example
   - Include error messages
   - Specify your environment

### Creating a Good Bug Report

```markdown
## Environment
- Python version: 3.10.0
- Alanube version: 1.0.0
- Operating system: Windows 10
- Country: Dominican Republic

## Issue Description
Brief description of the problem

## Steps to Reproduce
1. Step 1
2. Step 2
3. Step 3

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Error Messages
```
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  ...
```

## Code Example
```python
from alanube.do import Alanube

Alanube.connect("your_token", developer_mode=True)
# Your code here
```

## Additional Context
Any other relevant information
```

### Support Channels

1. **GitHub Issues:** [Create an issue](https://github.com/wilmerm/alanube-python/issues)
2. **Documentation:** Check this troubleshooting guide
3. **Alanube Support:** [Contact Alanube](https://www.alanube.co/)
4. **Community:** Check discussions and existing issues

### Common Solutions Summary

| Issue | Quick Fix |
|-------|-----------|
| Import Error | `pip install alanube` |
| Authentication | Check/regenerate API token |
| Validation | Verify payload structure |
| Timeout | Check internet connection |
| Rate Limit | Add delays between requests |
| SSL Issues | Update certificates |
| RNC Issues | Validate RNC format |

Remember to always test in sandbox mode first before using production!