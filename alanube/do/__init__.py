"""
This module provides the Alanube API client, allowing interaction with the
Alanube API for various operations such as creating companies, sending
electronic documents, and checking their statuses.

Classes:
    Alanube: Main class to interact with the Alanube API.
"""

__version__ = "1.1.0"


from typing import Optional
import warnings

from . import exceptions
from .api import AlanubeAPI


class Alanube:
    """
    Class to interact with the Alanube API.

    This class provides static methods to connect to the Alanube API,
    as well as to perform common operations such as creating and updating
    companies, sending electronic documents, and checking the status of those
    documents.

    Methods:
    ----------
    - `connect`: Connect to the Alanube API using the provided authentication token.
    - `create_company`: Create a new company in the Alanube API.
    - `update_company`: Update an existing company in the Alanube API.
    - `get_company`: Get the details of a company from the Alanube API.
    - `check_dgii_status`: Check the status of a company with the DGII.
    - `check_directory`: Check the directory status of a company.
    - `get_received_document`: Get the details of a received document.
    - `get_received_documents`: Get a list of received documents.
    - `get_cancellation`: Get the details of a cancellation.
    - `get_cancellations`: Get a list of cancellations.
    - `send_cancellation`: Send a cancellation request to the Alanube API.
    - `send_document`: Send an electronic document of the specified type.
    - `get_document`: Retrieve the status of an electronic document of the specified type.
    - `get_documents`: Retrieve a list of electronic documents of the specified type.
    - `get_document_status`: (Deprecated) Retrieve the status of an electronic document.
    - `get_report_companies_documents_total`: Get a report of total documents for companies.
    - `get_report_users_documents_total`: Get a report of total documents for users.
    - `get_report_company_emitted_documents`: Get total emitted documents for a specific company.
    - `get_company_emitted_documents_monthly`: Get monthly emitted documents for a specific company.
    - `get_company_emitted_documents_15_days`: Get emitted documents for a specific company in the last 15 days.
    - `get_company_accepted_documents`: Get total accepted documents for a specific company.
    - `get_company_accepted_documents_monthly`: Get monthly accepted documents for a specific company.
    - `get_company_accepted_documents_15_days`: Get accepted documents for a specific company in the last 15 days.
    """
    exceptions = exceptions
    create_company = AlanubeAPI.create_company
    update_company = AlanubeAPI.update_company
    get_company = AlanubeAPI.get_company
    check_dgii_status = AlanubeAPI.check_dgii_status
    check_directory = AlanubeAPI.check_directory
    get_received_document = AlanubeAPI.get_received_document
    get_received_documents = AlanubeAPI.get_received_documents
    get_cancellation = AlanubeAPI.get_cancellation
    get_cancellations = AlanubeAPI.get_cancellations
    send_cancellation = AlanubeAPI.send_cancellation
    get_report_companies_documents_total = AlanubeAPI.get_report_companies_documents_total
    get_report_users_documents_total = AlanubeAPI.get_report_users_documents_total
    get_report_company_emitted_documents = AlanubeAPI.get_report_company_emitted_documents
    get_report_company_emitted_documents_monthly = AlanubeAPI.get_report_company_emitted_documents_monthly
    get_report_company_emitted_documents_15_days = AlanubeAPI.get_report_company_emitted_documents_15_days
    get_report_company_accepted_documents = AlanubeAPI.get_report_company_accepted_documents
    get_report_company_accepted_documents_monthly = AlanubeAPI.get_report_company_accepted_documents_monthly
    get_report_company_accepted_documents_15_days = AlanubeAPI.get_report_company_accepted_documents_15_days

    send_document_func_map = {
        31: AlanubeAPI.send_fiscal_invoice,
        32: AlanubeAPI.send_invoice,
        33: AlanubeAPI.send_debit_note,
        34: AlanubeAPI.send_credit_note,
        41: AlanubeAPI.send_purchase,
        43: AlanubeAPI.send_minor_expense,
        44: AlanubeAPI.send_special_regime,
        45: AlanubeAPI.send_gubernamental,
        46: AlanubeAPI.send_export_support,
        47: AlanubeAPI.send_payment_abroad_support,
    }

    get_document_func_map = {
        31: AlanubeAPI.get_fiscal_invoice,
        32: AlanubeAPI.get_invoice,
        33: AlanubeAPI.get_debit_note,
        34: AlanubeAPI.get_credit_note,
        41: AlanubeAPI.get_purchase,
        43: AlanubeAPI.get_minor_expense,
        44: AlanubeAPI.get_special_regime,
        45: AlanubeAPI.get_gubernamental,
        46: AlanubeAPI.get_export_support,
        47: AlanubeAPI.get_payment_abroad_support,
    }

    get_documents_func_map = {
        31: AlanubeAPI.get_fiscal_invoices,
        32: AlanubeAPI.get_invoices,
        33: AlanubeAPI.get_debit_notes,
        34: AlanubeAPI.get_credit_notes,
        41: AlanubeAPI.get_purchases,
        43: AlanubeAPI.get_minor_expenses,
        44: AlanubeAPI.get_special_regimes,
        45: AlanubeAPI.get_gubernamentals,
        46: AlanubeAPI.get_export_supports,
        47: AlanubeAPI.get_payment_abroad_supports,
    }

    @staticmethod
    def connect(token, developer_mode):
        """
        Connect to the Alanube API using the provided authentication token.

        This method configures the connection to the Alanube API by establishing
        the authentication token and the mode of development. The token is
        required for authentication in the API, and the mode Development
        determines whether you use the production environment or the sandbox
        environment.

        Args:
        ----------
        - `token` (str): The authentication token to access the Alanube API.
        - `developer_mode` (bool): Indicator of whether the sandbox should be used.
        """
        AlanubeAPI.connect(token, developer_mode=developer_mode)

    @staticmethod
    def send_document(encf_type: int, payload: dict):
        """
        Send an electronic document of the specified type to the Alanube API.

        This method sends a document with the provided payload based on the eNCF type.

        Args:
        ----------
        - `encf_type` (int): The type of the eNCF document.
        - `payload` (dict): The data required to send the document.

        Returns:
        ----------
        `dict`: The response from the Alanube API.
        """
        func = Alanube.send_document_func_map.get(encf_type)
        if func is None:
            raise NotImplementedError(f"No implementation for eNCF type: {encf_type}")
        return func(payload)

    @staticmethod
    def get_document(encf_type: int, document_id: str, company_id: Optional[str] = None):
        """
        Retrieve the status of an electronic document of the specified type
        from the Alanube API.

        This method sends a request to get the status of the document.

        Args:
        ----------
        - `encf_type` (int): The type of the eNCF document.
        - `document_id` (str): The ID of the document to retrieve the status for.
        - `company_id` (str): Optional, asociated company ID.

        Returns:
            `dict`: The response from the Alanube API.
        """
        func = Alanube.get_document_func_map.get(encf_type)
        if func is None:
            raise NotImplementedError(f"No implementation for eNCF type: {encf_type}")
        return func(document_id, company_id)

    @staticmethod
    def get_documents(
        encf_type: int,
        company_id: Optional[str] = None,
        status: Optional[str] = None,
        legal_status: Optional[str] = None,
        document_number: Optional[str] = None,
        limit: int = 25,
        page: int = 1,
        start: Optional[int] = None,
        end: Optional[int] = None,
    ):
        """
        Retrieve a list of electronic documents of the specified type from the Alanube API.

        This method sends a request to get a list of documents based on the provided parameters.

        Args:
        ----------
        - `encf_type` (int): The type of the eNCF document.
        - `company_id` (str): Optional, asociated company ID.
        - `status` (str): Optional, status of the document.
        - `legal_status` (str): Optional, legal status of the document.
        - `document_number` (str): Optional, document number.
        - `limit` (int): Optional, number of documents to retrieve per page.
        - `page` (int): Optional, page number.
        - `start` (int): Optional, start date.
        - `end` (int): Optional, end date.
        """
        func = Alanube.get_documents_func_map.get(encf_type)
        if func is None:
            raise NotImplementedError(f"No implementation for eNCF type: {encf_type}")
        return func(
            company_id=company_id,
            status=status,
            legal_status=legal_status,
            document_number=document_number,
            limit=limit,
            page=page,
            start=start,
            end=end,
        )

    @staticmethod
    def get_document_status(encf_type: int, document_id: str, company_id: Optional[str] = None):
        warnings.warn("This method is deprecated. Use `get_document` instead.", DeprecationWarning)
        return Alanube.get_document(encf_type, document_id, company_id)


__all__ = ['Alanube']
