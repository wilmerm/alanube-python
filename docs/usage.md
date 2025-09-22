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

---

For detailed information on each endpoint, refer to the official [Alanube API Documentation](https://developer.alanube.co/).