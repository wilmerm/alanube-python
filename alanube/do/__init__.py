"""
This module provides the Alanube API client, allowing interaction with the
Alanube API for various operations such as creating companies, sending
electronic documents, and checking their statuses.

Classes:
    Alanube: Main class to interact with the Alanube API.
"""

__version__ = "1.2.2"


from . import exceptions
from .api import AlanubeAPI
from .utils import (
    check_directory,
    get_company,
    create_company,
    get_received_document,
    get_received_documents,
    update_company,
    send_fiscal_invoice,
    get_fiscal_invoice_status,
    send_invoice,
    get_invoice_status,
    send_debit_note,
    get_debit_note_status,
    send_credit_note,
    get_credit_note_status,
    send_purchase,
    get_purchase_status,
    send_minor_expense,
    get_minor_expense_status,
    send_special_regime,
    get_special_regime_status,
    send_gubernamental,
    get_gubernamental_status,
    send_export_support,
    get_export_support_status,
    send_payment_abroad_support,
    get_payment_abroad_support_status,
    send_cancellation,
    get_cancellation_status,
)


class Alanube:
    """
    Class to interact with the Alanube API.

    This class provides static methods to connect to the Alanube API,
    as well as to perform common operations such as creating and updating
    companies, sending electronic documents, and checking the status of those
    documents.

    Attributes:
        - `exceptions` (module): Custom exceptions module to handle specific
            Alanube errors.
        - `send_document_func_map` (dict): Map of eNCF types to corresponding
            functions for sending documents.
        - `get_status_func_map` (dict): Map of eNCF types to corresponding
            functions for retrieving document status.
    """
    exceptions = exceptions

    send_document_func_map = {
        31: send_fiscal_invoice,
        32: send_invoice,
        33: send_debit_note,
        34: send_credit_note,
        41: send_purchase,
        43: send_minor_expense,
        44: send_special_regime,
        45: send_gubernamental,
        46: send_export_support,
        47: send_payment_abroad_support,
    }
    get_status_func_map = {
        31: get_fiscal_invoice_status,
        32: get_invoice_status,
        33: get_debit_note_status,
        34: get_credit_note_status,
        41: get_purchase_status,
        43: get_minor_expense_status,
        44: get_special_regime_status,
        45: get_gubernamental_status,
        46: get_export_support_status,
        47: get_payment_abroad_support_status,
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
            `token` (str): The authentication token to access the Alanube API.
            `developer_mode` (bool): Indicator of whether the sandbox should be used.
        """
        AlanubeAPI.connect(token, developer_mode=developer_mode)

    @staticmethod
    def create_company(payload):
        """
        Create a new company in the Alanube API.

        This method sends a request to create a new company with the provided payload.

        Args:
            `payload` (dict): The data required to create a company.

        Returns:
            `dict`: The response from the Alanube API.
        """
        return create_company(payload)

    @staticmethod
    def update_company(payload, company_id: str = None):
        """
        Update the information of an existing company in the Alanube API.

        This method sends a request to update the company's information with
        the provided payload.

        Args:
            `payload` (dict): The data required to update the company.
            `company_id` (str, optional): The ID of the company to update.
            If not provided, the update will be applied to the default company.

        Returns:
            dict: The response from the Alanube API.
        """
        return update_company(payload, company_id)

    @staticmethod
    def get_company(company_id: str = None):
        """
        Retrieve the information of an existing company from the Alanube API.

        This method sends a request to get the company's information.

        Args:
            `company_id` (str, optional): The ID of the company to retrieve.
            If not provided, the default company's information will be retrieved.

        Returns:
            `dict`: The response from the Alanube API.
        """
        return get_company(company_id)

    @staticmethod
    def send_document(encf_type: int, payload: dict):
        """
        Send an electronic document of the specified type to the Alanube API.

        This method sends a document with the provided payload based on the eNCF type.

        Args:
            `encf_type` (int): The type of the eNCF document.
            `payload` (dict): The data required to send the document.

        Returns:
            `dict`: The response from the Alanube API.
        """
        func = Alanube.send_document_func_map.get(encf_type)
        if func is None:
            raise NotImplementedError(f"No implementation for eNCF type: {encf_type}")
        return func(payload)

    @staticmethod
    def get_document_status(encf_type: int, document_id: str, company_id: str = None):
        """
        Retrieve the status of an electronic document of the specified type
        from the Alanube API.

        This method sends a request to get the status of the document.

        Args:
            `encf_type` (int): The type of the eNCF document.
            `document_id` (str): The ID of the document to retrieve the status for.
            `company_id` (str): Optional, asociated company ID.

        Returns:
            `dict`: The response from the Alanube API.
        """
        func = Alanube.get_status_func_map.get(encf_type)
        if func is None:
            raise NotImplementedError(f"No implementation for eNCF type: {encf_type}")
        return func(document_id, company_id)

    @staticmethod
    def send_cancellation(payload: dict):
        """
        Send a document cancellation request to the Alanube API.

        This method sends a request to cancel a document with the provided payload.

        Args:
            `payload` (dict): The data required to cancel the document.

        Returns:
            `dict`: The response from the Alanube API.
        """
        return send_cancellation(payload)

    @staticmethod
    def get_cancellation_status(cancellation_id: str, company_id: str = None):
        """
        Retrieve the status of a document cancellation request from the Alanube API.

        This method sends a request to get the status of the cancellation.

        Args:
            `cancellation_id` (str): The ID of the cancellation to retrieve the status for.
            `company_id` (str): Optional, asociated company ID.

        Returns:
            `dict`: The response from the Alanube API.
        """
        return get_cancellation_status(cancellation_id, company_id)

    @staticmethod
    def get_received_document(received_document_id: str, company_id: str = None):
        """
        Retrieve the 'received document' from the Alanube API.

        This method sends a request to get the 'received document'.

        Args:
            `received_document_id` (str): The ID of the 'received document' to retrieve.
            `company_id` (str): Optional, asociated company ID.

        Returns:
            `dict`: The response from the Alanube API.
        """
        return get_received_document(received_document_id, company_id)

    @staticmethod
    def get_received_documents(
        company_id=None,
        limit=25,
        page=1,
        start=None,
        end=None,
    ):
        """
        Retrieve the 'received documents' from the Alanube API.

        Returns:
            `dict`: The response from the Alanube API.
        """
        return get_received_documents(company_id, limit, page, start, end)

    @staticmethod
    def check_directory(rnc=None, company_id=None):
        """
        Check the directory of a company in the Alanube API.
        """
        return check_directory(rnc, company_id)


__all__ = ['Alanube']