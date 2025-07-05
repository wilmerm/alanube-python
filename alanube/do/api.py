import logging
import requests
from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from typing import Any, Dict, List

from alanube.utils import build_url
from .exceptions import handle_response_error
from .types import (
    DocumentResponse,
    ListDocumentResponse,
    ListReceivedDocumentsResponse,
    ReceivedDocumentsResponse,
)


logger = logging.getLogger(__package__)


@dataclass(frozen=True)
class APIConfig:
    token: str
    developer_mode: bool
    api_version: str = "v1"

    @property
    def base_url(self):
        if self.developer_mode:
            return 'https://sandbox.alanube.co/dom'
        return 'https://api.alanube.co/dom'

    @property
    def api_url(self):
        return f"{self.base_url}/{self.api_version}"

    @property
    def endpoint_company(self):  # 31
        return f"{self.api_url}/company"

    @property
    def endpoint_fiscal_invoices(self):  # 31
        return f"{self.api_url}/fiscal-invoices"

    @property
    def endpoint_invoices(self):  # 32
        return f"{self.api_url}/invoices"

    @property
    def endpoint_debit_notes(self):  # 33
        return f"{self.api_url}/debit-notes"

    @property
    def endpoint_credit_notes(self):  # 34
        return f"{self.api_url}/credit-notes"

    @property
    def endpoint_purchases(self):  # 41
        return f"{self.api_url}/purchases"

    @property
    def endpoint_minorexpenses(self):  # 43
        return f"{self.api_url}/minor-expenses"

    @property
    def endpoint_special_regimes(self):  # 44
        return f"{self.api_url}/special-regimes"

    @property
    def endpoint_gubernamentals(self):  # 45
        return f"{self.api_url}/gubernamentals"

    @property
    def endpoint_export_supports(self):  # 46
        return f"{self.api_url}/export-supports"

    @property
    def endpoint_payment_abroad_supports(self):  # 47
        return f"{self.api_url}/payment-abroad-supports"

    @property
    def endpoint_cancellations(self):
        return f"{self.api_url}/cancellations"

    @property
    def endpoint_received_documents(self):
        """
        Constructs the URL for the received documents endpoint.

        Query parameters:
        -----------------
        - limit (int): The number of documents to retrieve.
        - page (int): The page number to retrieve.
        - start (str): The start date to filter the documents by.
        - end (str): The end date to filter the documents by.
        """
        return f"{self.api_url}/received-documents"

    @property
    def endpoint_check_directory(self):
        """
        Constructs the URL for the 'check-directory' endpoint.

        query parameters:
        -----------------
        - rnc (str): The RNC of the company to check in the directory.

        Returns:
            str: The full URL for the 'check-directory' endpoint.
        """
        return f"{self.api_url}/check-directory"

    @property
    def endpoint_check_dgii_status(self):
        """
        Constructs the URL for checking the DGII status.

        Optional query parameters:
        --------------------------------
        - environment (int): Specifies the environment to check the status for.
            - 1: PreCertificacion
            - 2: Producción
            - 3: Certificacion
        - maintenance (str): If set to 'yes', retrieves the maintenance windows
          for the electronic invoice services of the DGII. If the 'environment'
          parameter is also provided, it takes precedence over this parameter.
        """
        return f"{self.api_url}/check-dgii-status"


class AlanubeAPI:
    config: APIConfig = None

    @classmethod
    def connect(cls, token: str, developer_mode: bool = False, api_version: str = "v1"):
        """
        Connect to the Alanube API using the token, base_url and API version.
        """
        cls.config = APIConfig(token, developer_mode, api_version)

    @staticmethod
    def get_headers():
        if AlanubeAPI.config is None:
            raise RuntimeError("API not connected. Call AlanubeAPI.connect first.")
        return {
            "Authorization": f"Bearer {AlanubeAPI.config.token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    @staticmethod
    def request(endpoint, method='GET', params=None, data=None, expected_response_code=None):
        headers = AlanubeAPI.get_headers()
        logger.info(f"{method}: {endpoint} | Params: {params}")
        if data:
            logger.debug(f"Data: {data}")
        response = requests.request(method, endpoint, headers=headers, params=params, json=data)
        return response

    @staticmethod
    def get(endpoint, params=None, expected_response_code=None):
        response = AlanubeAPI.request(endpoint, "GET", params=params)
        return AlanubeAPI.process_response(response, expected_response_code=expected_response_code)

    @staticmethod
    def post(endpoint, params=None, data=None, expected_response_code=None):
        data = AlanubeAPI.serialize(data)
        response = AlanubeAPI.request(endpoint, "POST", params=params, data=data)
        return AlanubeAPI.process_response(response, expected_response_code=expected_response_code)

    @staticmethod
    def put(endpoint, params=None, data=None, expected_response_code=None):
        data = AlanubeAPI.serialize(data)
        response = AlanubeAPI.request(endpoint, "PUT", params=params, data=data)
        return AlanubeAPI.process_response(response, expected_response_code=expected_response_code)

    @staticmethod
    def patch(endpoint, params=None, data=None, expected_response_code=None):
        data = AlanubeAPI.serialize(data)
        response = AlanubeAPI.request(endpoint, "PATCH", params=params, data=data)
        return AlanubeAPI.process_response(response, expected_response_code=expected_response_code)

    @staticmethod
    def delete(endpoint, params=None, expected_response_code=None):
        response = AlanubeAPI.request(endpoint, "DELETE", params=params)
        return AlanubeAPI.process_response(response, expected_response_code=expected_response_code)

    @staticmethod
    def options(endpoint, expected_response_code=None):
        response = AlanubeAPI.request(endpoint, "OPTIONS")
        return AlanubeAPI.process_response(response, expected_response_code=expected_response_code)

    @staticmethod
    def process_response(response: requests.Response, expected_response_code: int = None):
        handle_response_error(response, expected_response_code=expected_response_code)
        logger.info(f"Response: {response.status_code}")
        try:
            logger.debug(f"JSON: {response.json()}")
        except ValueError:
            logger.error("Error parsing response as JSON")
            logger.debug(f"Text: {response.text}")
        return response

    @classmethod
    def serialize(cls, value):
        if value is None:
            return value
        elif isinstance(value, (date, datetime)):
            return value.isoformat()
        elif isinstance(value, Decimal):
            return float(value)  # Alanube require un número
        elif isinstance(value, (list, tuple)):
            return [cls.serialize(v) for v in value]
        elif isinstance(value, dict):
            return {k: cls.serialize(v) for k, v in value.items()}
        elif hasattr(value, '__dict__'):
            return {k: cls.serialize(v) for k, v in value.__dict__.items() if not k.startswith('_')}
        else:
            return value

    @classmethod
    def create_company(cls, payload: Dict) -> Dict[str, Any]:
        """
        Dar de alta a una empresa
        """
        url = cls.config.endpoint_company
        response = cls.post(url, data=payload, expected_response_code=201)
        return response.json()

    @classmethod
    def update_company(cls, payload: Dict, company_id: str = None) -> Dict[str, Any]:
        """
        Actualizar la información de una empresa

        Este endpoint permite actualizar la información un una empresa, ten en
        cuenta que únicamente se actualizará la información enviada y por lo
        tanto no es necesario enviar toda la información de la empresa.
        """
        url = cls.config.endpoint_company + (f"/{company_id}" if company_id else "")
        response = cls.patch(url, data=payload, expected_response_code=200)
        return response.json()

    @classmethod
    def get_company(cls, company_id: str = None) -> Dict[str, Any]:
        """
        Consultar la información de una empresa
        """
        url = cls.config.endpoint_company + (f"/{company_id}" if company_id else "")
        response = cls.get(url, expected_response_code=200)
        return response.json()

    @classmethod
    def send_fiscal_invoice(cls, payload: Dict) -> DocumentResponse:
        """
        Emitir Factura de Crédito Fiscal Electrónica (31)
        """
        url = cls.config.endpoint_fiscal_invoices
        response = cls.post(url, data=payload, expected_response_code=201)
        return response.json()

    @classmethod
    def get_fiscal_invoice(cls, id_: str, company_id: str = None) -> DocumentResponse:
        """
        Consultar el estado de la Factura de Crédito Fiscal Electrónica (31)
        """
        url = build_url(cls.config.endpoint_fiscal_invoices, company_id, id_)
        response = cls.get(url, expected_response_code=200)
        return response.json()

    @classmethod
    def get_fiscal_invoices(
        cls,
        company_id: str = None,
        status: str = None,
        legal_status: str = None,
        document_number: str = None,
        limit: int = 25,
        page: int = 1,
        start: int = None,
        end: int = None,
    ) -> ListDocumentResponse:
        """
        Consultar las Facturas de Crédito Fiscal Electrónicas (31)
        """
        url = build_url(
            cls.config.endpoint_fiscal_invoices,
            company_id,
            status=status,
            legal_status=legal_status,
            document_number=document_number,
            limit=limit,
            page=page,
            start=start,
            end=end,
        )
        response = cls.get(url, expected_response_code=200)
        return response.json()

    @classmethod
    def send_invoice(cls, payload: Dict) -> DocumentResponse:
        """
        Emitir Factura de Consumo Electrónica (32)
        """
        url = cls.config.endpoint_invoices
        response = cls.post(url, data=payload, expected_response_code=201)
        return response.json()

    @classmethod
    def get_invoice(cls, id_: str, company_id: str = None) -> DocumentResponse:
        """
        Consultar el estado de la Factura de Consumo Electrónica (32)
        """
        url = build_url(cls.config.endpoint_invoices, company_id, id_)
        response = cls.get(url, expected_response_code=200)
        return response.json()

    @classmethod
    def get_invoices(
        cls,
        company_id: str = None,
        status: str = None,
        legal_status: str = None,
        document_number: str = None,
        limit: int = 25,
        page: int = 1,
        start: int = None,
        end: int = None,
    ) -> ListDocumentResponse:
        """
        Consultar las Facturas de Consumo Electrónicas (32)
        """
        url = build_url(
            cls.config.endpoint_invoices,
            company_id,
            status=status,
            legal_status=legal_status,
            document_number=document_number,
            limit=limit,
            page=page,
            start=start,
            end=end,
        )
        response = cls.get(url, expected_response_code=200)
        return response.json()

    @classmethod
    def send_debit_note(cls, payload: Dict) -> DocumentResponse:
        """
        Emitir Nota de Débito Electrónica (33)
        """
        url = cls.config.endpoint_debit_notes
        response = cls.post(url, data=payload, expected_response_code=201)
        return response.json()

    @classmethod
    def get_debit_note(cls, id_: str, company_id: str = None) -> DocumentResponse:
        """
        Consultar el estado de la Nota de Débito Electrónica (33)
        """
        url = build_url(cls.config.endpoint_debit_notes, company_id, id_)
        response = cls.get(url, expected_response_code=200)
        return response.json()

    @classmethod
    def get_debit_notes(
        cls,
        company_id: str = None,
        status: str = None,
        legal_status: str = None,
        document_number: str = None,
        limit: int = 25,
        page: int = 1,
        start: int = None,
        end: int = None,
    ) -> ListDocumentResponse:
        """
        Consultar las Notas de Débito Electrónicas (33)
        """
        url = build_url(
            cls.config.endpoint_debit_notes,
            company_id,
            status=status,
            legal_status=legal_status,
            document_number=document_number,
            limit=limit,
            page=page,
            start=start,
            end=end,
        )
        response = cls.get(url, expected_response_code=200)
        return response.json()

    @classmethod
    def send_credit_note(cls, payload: Dict) -> DocumentResponse:
        """
        Emitir Nota de Crédito Electrónica (34)
        """
        url = cls.config.endpoint_credit_notes
        response = cls.post(url, data=payload, expected_response_code=201)
        return response.json()

    @classmethod
    def get_credit_note(cls, id_: str, company_id: str = None) -> DocumentResponse:
        """
        Consultar el estado de la Nota de Crédito Electrónica (34)
        """
        url = build_url(cls.config.endpoint_credit_notes, company_id, id_)
        response = cls.get(url, expected_response_code=200)
        return response.json()

    @classmethod
    def get_credit_notes(
        cls,
        company_id: str = None,
        status: str = None,
        legal_status: str = None,
        document_number: str = None,
        limit: int = 25,
        page: int = 1,
        start: int = None,
        end: int = None,
    ) -> ListDocumentResponse:
        """
        Consultar las Notas de Crédito Electrónicas (34)
        """
        url = build_url(
            cls.config.endpoint_credit_notes,
            company_id,
            status=status,
            legal_status=legal_status,
            document_number=document_number,
            limit=limit,
            page=page,
            start=start,
            end=end,
        )
        response = cls.get(url, expected_response_code=200)
        return response.json()

    @classmethod
    def send_purchase(cls, payload: Dict) -> DocumentResponse:
        """
        Emitir Documento de Compra Electrónico (41)
        """
        url = cls.config.endpoint_purchases
        response = cls.post(url, data=payload, expected_response_code=201)
        return response.json()

    @classmethod
    def get_purchase(cls, id_: str, company_id: str = None) -> DocumentResponse:
        """
        Consultar el estado del Documento de Compra Electrónico (41)
        """
        url = build_url(cls.config.endpoint_purchases, company_id, id_)
        response = cls.get(url, expected_response_code=200)
        return response.json()

    @classmethod
    def get_purchases(
        cls,
        company_id: str = None,
        status: str = None,
        legal_status: str = None,
        document_number: str = None,
        limit: int = 25,
        page: int = 1,
        start: int = None,
        end: int = None,
    ) -> ListDocumentResponse:
        """
        Consultar los documentos de Compra Electrónicos (41)
        """
        url = build_url(
            cls.config.endpoint_purchases,
            company_id,
            status=status,
            legal_status=legal_status,
            document_number=document_number,
            limit=limit,
            page=page,
            start=start,
            end=end,
        )
        response = cls.get(url, expected_response_code=200)
        return response.json()

    @classmethod
    def send_minor_expense(cls, payload: Dict) -> DocumentResponse:
        """
        Emitir Documento de Gasto Menor Electrónico (43)
        """
        url = cls.config.endpoint_minorexpenses
        response = cls.post(url, data=payload, expected_response_code=201)
        return response.json()

    @classmethod
    def get_minor_expense(cls, id_: str, company_id: str = None) -> DocumentResponse:
        """
        Consultar el estado del Documento de Gasto Menor Electrónico (43)
        """
        url = build_url(cls.config.endpoint_minorexpenses, company_id, id_)
        response = cls.get(url, expected_response_code=200)
        return response.json()

    @classmethod
    def get_minor_expenses(
        cls,
        company_id: str = None,
        status: str = None,
        legal_status: str = None,
        document_number: str = None,
        limit: int = 25,
        page: int = 1,
        start: int = None,
        end: int = None,
    ) -> ListDocumentResponse:
        """
        Consultar los documentos de Gasto Menor Electrónicos (43)
        """
        url = build_url(
            cls.config.endpoint_minorexpenses,
            company_id,
            status=status,
            legal_status=legal_status,
            document_number=document_number,
            limit=limit,
            page=page,
            start=start,
            end=end,
        )
        response = cls.get(url, expected_response_code=200)
        return response.json()

    @classmethod
    def send_special_regime(cls, payload: Dict) -> DocumentResponse:
        """
        Emitir Documento de Régimen Especial Electrónico (44)
        """
        url = cls.config.endpoint_special_regimes
        response = cls.post(url, data=payload, expected_response_code=201)
        return response.json()

    @classmethod
    def get_special_regime(cls, id_: str, company_id: str = None) -> DocumentResponse:
        """
        Consultar el estado del Documento de Régimen Especial Electrónico (44)
        """
        url = build_url(cls.config.endpoint_special_regimes, company_id, id_)
        response = cls.get(url, expected_response_code=200)
        return response.json()

    @classmethod
    def get_special_regimes(
        cls,
        company_id: str = None,
        status: str = None,
        legal_status: str = None,
        document_number: str = None,
        limit: int = 25,
        page: int = 1,
        start: int = None,
        end: int = None,
    ) -> ListDocumentResponse:
        """
        Consultar los documentos de Régimen Especial Electrónicos (44)
        """
        url = build_url(
            cls.config.endpoint_special_regimes,
            company_id,
            status=status,
            legal_status=legal_status,
            document_number=document_number,
            limit=limit,
            page=page,
            start=start,
            end=end,
        )
        response = cls.get(url, expected_response_code=200)
        return response.json()

    @classmethod
    def send_gubernamental(cls, payload: Dict) -> DocumentResponse:
        """
        Emitir Documento Gubernamental Electrónico (45)
        """
        url = cls.config.endpoint_gubernamentals
        response = cls.post(url, data=payload, expected_response_code=201)
        return response.json()

    @classmethod
    def get_gubernamental(cls, id_: str, company_id: str = None) -> DocumentResponse:
        """
        Consultar el estado del Documento Gubernamental Electrónico (45)
        """
        url = build_url(cls.config.endpoint_gubernamentals, company_id, id_)
        response = cls.get(url, expected_response_code=200)
        return response.json()

    @classmethod
    def get_gubernamentals(
        cls,
        company_id: str = None,
        status: str = None,
        legal_status: str = None,
        document_number: str = None,
        limit: int = 25,
        page: int = 1,
        start: int = None,
        end: int = None,
    ) -> ListDocumentResponse:
        """
        Consultar los documentos Gubernamentales Electrónicos (45)
        """
        url = build_url(
            cls.config.endpoint_gubernamentals,
            company_id,
            status=status,
            legal_status=legal_status,
            document_number=document_number,
            limit=limit,
            page=page,
            start=start,
            end=end,
        )
        response = cls.get(url, expected_response_code=200)
        return response.json()

    @classmethod
    def send_export_support(cls, payload: Dict) -> DocumentResponse:
        """
        Emitir Documento de Soporte de Exportación Electrónico (46)
        """
        url = cls.config.endpoint_export_supports
        response = cls.post(url, data=payload, expected_response_code=201)
        return response.json()

    @classmethod
    def get_export_support(cls, id_: str, company_id: str = None) -> DocumentResponse:
        """
        Consultar el estado del Documento de Soporte de Exportación Electrónico (46)
        """
        url = build_url(cls.config.endpoint_export_supports, company_id, id_)
        response = cls.get(url, expected_response_code=200)
        return response.json()

    @classmethod
    def get_export_supports(
        cls,
        company_id: str = None,
        status: str = None,
        legal_status: str = None,
        document_number: str = None,
        limit: int = 25,
        page: int = 1,
        start: int = None,
        end: int = None,
    ) -> ListDocumentResponse:
        """
        Consultar los documentos de Soporte de Exportación Electrónico (46)
        """
        url = build_url(
            cls.config.endpoint_export_supports,
            company_id,
            status=status,
            legal_status=legal_status,
            document_number=document_number,
            limit=limit,
            page=page,
            start=start,
            end=end,
        )
        response = cls.get(url, expected_response_code=200)
        return response.json()

    @classmethod
    def send_payment_abroad_support(cls, payload: Dict) -> DocumentResponse:
        """
        Emitir Documento de Soporte de Pagos al Exterior Electrónico (47)
        """
        url = cls.config.endpoint_payment_abroad_supports
        response = cls.post(url, data=payload, expected_response_code=201)
        return response.json()

    @classmethod
    def get_payment_abroad_support(cls, id_: str, company_id: str = None) -> DocumentResponse:
        """
        Consultar el estado del Documento de Soporte de Pagos al Exterior Electrónico (47)
        """
        url = build_url(cls.config.endpoint_payment_abroad_supports, company_id, id_)
        response = cls.get(url, expected_response_code=200)
        return response.json()

    @classmethod
    def get_payment_abroad_supports(
        cls,
        company_id: str = None,
        status: str = None,
        legal_status: str = None,
        document_number: str = None,
        limit: int = 25,
        page: int = 1,
        start: int = None,
        end: int = None,
    ) -> ListDocumentResponse:
        """
        Consultar los documentos de Soporte de Pagos al Exterior Electrónico (47)
        """
        url = build_url(
            cls.config.endpoint_payment_abroad_supports,
            company_id,
            status=status,
            legal_status=legal_status,
            document_number=document_number,
            limit=limit,
            page=page,
            start=start,
            end=end,
        )
        response = cls.get(url, expected_response_code=200)
        return response.json()

    @classmethod
    def send_cancellation(cls, payload: Dict) -> Dict[str, str]:
        """
        Este endpoint sirve para emitir anulaciones, las cuales se usan para
        anular rangos de numeración que no se usarán
        """
        url = cls.config.endpoint_cancellations
        response = cls.post(url, data=payload, expected_response_code=201)
        return response.json()

    @classmethod
    def get_cancellation(cls, id_: str, company_id: str = None) -> Dict[str, Any]:
        """
        Consultar el estado de la anulación
        """
        url = build_url(cls.config.endpoint_cancellations, company_id, id_)
        response = cls.get(url, expected_response_code=200)
        return response.json()

    @classmethod
    def get_cancellations(
        cls,
        company_id=None,
        limit=25,
        page=1,
        start=None,
        end=None,
    ):
        """
        Consultar el estado de las anulaciones
        """
        url = build_url(cls.config.endpoint_cancellations, company_id, limit=limit, page=page, start=start, end=end)
        response = cls.get(url, expected_response_code=200)
        return response.json()

    @classmethod
    def get_received_document(cls, id_: str, company_id: str = None) -> ReceivedDocumentsResponse:
        """
        Consultar un 'documento recibido'
        """
        url = build_url(cls.config.endpoint_received_documents, company_id, id_)
        response = cls.get(url, expected_response_code=200)
        return response.json()

    @classmethod
    def get_received_documents(
        cls,
        company_id=None,
        limit=25,
        page=1,
        start=None,
        end=None,
    ) -> ListReceivedDocumentsResponse:
        """
        Consultar varios 'documentos recibidos'

        Parámetros opcionales:
        ----------------------
        - `limit`: Límite de documentos consultados en cada request.
        - `page`: Página a ser consultada en el request actual.
        - `start`: Fecha de inicio de la consulta basada en la fecha de emisión
            del documento(s). Formato: YYYY-MM-DD. Si no se envía, se tomará
            la fecha actual menos 30 días en zona horaria UTC.
        - `end`: Fecha de fin de la consulta basada en la fecha de emisión del
            documento(s). Formato: YYYY-MM-DD. Si no se envía, se tomará la
            fecha actual en zona horaria UTC.
        """
        url = cls.config.endpoint_received_documents
        url = build_url(url, company_id=company_id, limit=limit, page=page, start=start, end=end)
        response = cls.get(url, expected_response_code=200)
        return response.json()

    @classmethod
    def check_directory(cls, rnc: str = None, company_id: str = None):
        """
        Consultar el directorio de compañías activas para facturación electrónica.

        Parámetros:
        -----------
        - rnc (str, opcional): El RNC de la compañía para consultar en el directorio.
        - company_id (str, opcional): El ID de la compañía para consultar en el directorio.

        Retorna:
        - data (dict o list): Los datos de la compañía o una lista de compañías.
        """
        url = cls.config.endpoint_check_directory
        url = build_url(url, company_id, rnc=rnc)

        response = cls.get(url, expected_response_code=200)
        data: List[Dict[str, str]] = response.json()

        if rnc and isinstance(data, list) and len(data) == 1:
            return data[0]

        return data

    @classmethod
    def check_dgii_status(
        cls,
        environment: int = None,
        maintenance: bool = False,
        company_id: str = None,
    ) -> List[Dict[str, Any]] | Dict[str, Any]:
        """
        Consultar el estado de los servicios de la DGII.

        Parámetros opcionales:
        ----------------------
        - environment (int): Ambiente para el cual se desea consultar el estado.
            - 1: PreCertificacion
            - 2: Producción
            - 3: Certificacion
        - maintenance (bool): Si es True, se recuperan las ventanas de
            mantenimiento para los servicios de factura electrónica de la DGII.
            Si también se proporciona el parámetro 'environment', este tiene
            prioridad sobre este parámetro.
        """
        url = cls.config.endpoint_check_dgii_status
        url = build_url(url, company_id, environment=environment, maintenance=maintenance)
        response = cls.get(url, expected_response_code=200)
        data = response.json()
        return data
