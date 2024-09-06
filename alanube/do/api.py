from datetime import date, datetime
from dateutil import parser
from decimal import Decimal
import requests
from dataclasses import dataclass

from .exceptions import handle_response_error


@dataclass(frozen=True)
class APIConfig:
    token: str
    developer_mode: bool
    api_version: str = "v1"

    @property
    def base_url(self):
        if self.developer_mode:
            return f"https://sandbox.alanube.co/dom"
        return f"https://api.alanube.co/dom"

    @property
    def api_url(self):
        return f"{self.base_url}/{self.api_version}"

    @property
    def endpoint_company(self): # 31
        return f"{self.api_url}/company"

    @property
    def endpoint_fiscal_invoices(self): # 31
        return f"{self.api_url}/fiscal-invoices"

    @property
    def endpoint_fiscal_invoices_status(self): # 31 status
        return self.endpoint_fiscal_invoices + "/{id}"

    @property
    def endpoint_invoices(self): # 32
        return f"{self.api_url}/invoices"

    @property
    def endpoint_invoices_status(self): # 32 status
        return self.endpoint_invoices + "/{id}"

    @property
    def endpoint_debit_notes(self): # 33
        return f"{self.api_url}/debit-notes"

    @property
    def endpoint_debit_notes_status(self): # 33 status
        return self.endpoint_debit_notes + "/{id}"

    @property
    def endpoint_credit_notes(self): # 34
        return f"{self.api_url}/credit-notes"

    @property
    def endpoint_credit_notes_status(self): # 34 status
        return self.endpoint_credit_notes + "/{id}"

    @property
    def endpoint_purchases(self): # 41
        return f"{self.api_url}/purchases"

    @property
    def endpoint_purchases_status(self): # 41 status
        return self.endpoint_purchases + "/{id}"

    @property
    def endpoint_minorexpenses(self): # 43
        return f"{self.api_url}/minor-expenses"

    @property
    def endpoint_minorexpenses_status(self): # 43 status
        return self.endpoint_minorexpenses + "/{id}"

    @property
    def endpoint_special_regimes(self): # 44
        return f"{self.api_url}/special-regimes"

    @property
    def endpoint_special_regimes_status(self): # 44 status
        return self.endpoint_special_regimes + "/{id}"

    @property
    def endpoint_gubernamentals(self): # 45
        return f"{self.api_url}/gubernamentals"

    @property
    def endpoint_gubernamentals_status(self): # 45 status
        return self.endpoint_gubernamentals + "/{id}"

    @property
    def endpoint_export_supports(self): # 46
        return f"{self.api_url}/export-supports"

    @property
    def endpoint_export_supports_status(self): # 46 status
        return self.endpoint_export_supports + "/{id}"

    @property
    def endpoint_payment_abroad_supports(self): # 47
        return f"{self.api_url}/payment-abroad-supports"

    @property
    def endpoint_payment_abroad_supports_status(self): # 47 status
        return self.endpoint_payment_abroad_supports + "/{id}"

    @property
    def endpoint_cancellations(self):
        return f"{self.api_url}/cancellations"

    @property
    def endpoint_cancellations_status(self):
        return self.endpoint_cancellations + "/{id}"


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
        return {
            "Authorization": f"Bearer {AlanubeAPI.config.token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    @staticmethod
    def request(endpoint, method='GET', params=None, data=None, expected_response_code=None):
        url = AlanubeAPI.build_url(endpoint)
        headers = AlanubeAPI.get_headers()
        response = requests.request(method, url, headers=headers, params=params, json=data)
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
        return response

    @staticmethod
    def build_url(endpoint: str):
        return endpoint

    @classmethod
    def serialize(cls, value):
        if value is None:
            return value
        elif isinstance(value, (date, datetime)):
            return value.isoformat()
        elif isinstance(value, Decimal):
            return float(value) # Alanube require un número
        elif isinstance(value, (list, tuple)):
            return [cls.serialize(v) for v in value]
        elif isinstance(value, dict):
            return {k: cls.serialize(v) for k, v in value.items()}
        elif hasattr(value, '__dict__'):
            return {k: cls.serialize(v) for k, v in value.__dict__.items() if not k.startswith('_')}
        else:
            return value

    @classmethod
    def create_company(cls, payload):
        """
        Dar de alta a una empresa

        Este endpoint permite dar de alta empresas en la API con las
        configuraciones necesarias para enviar documentos a la DGII
        """
        url = cls.config.endpoint_company
        response = cls.post(url, data=payload, expected_response_code=201)
        return response.json()

    @classmethod
    def update_company(cls, payload, company_id: str = None):
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
    def get_company(cls, company_id: str = None):
        """
        Consultar la información de una empresa
        """
        url = cls.config.endpoint_company + (f"/{company_id}" if company_id else "")
        response = cls.get(url, expected_response_code=200)
        return response.json()

    @classmethod
    def send_fiscal_invoice(cls, payload):
        """
        Emitir Factura de Crédito Fiscal Electrónica (31)
        """
        url = cls.config.endpoint_fiscal_invoices
        response = cls.post(url, data=payload, expected_response_code=201)
        return response.json()

    @classmethod
    def get_fiscal_invoice_status(cls, fiscal_invoice_id: str, company_id: str = None):
        """
        Consultar el estado de la Factura de Crédito Fiscal Electrónica (31)
        """
        url = cls.config.endpoint_fiscal_invoices_status.format(id=fiscal_invoice_id)
        if company_id:
            url += f'/idCompany/{company_id}'

        response = cls.get(url, expected_response_code=200)
        return response.json()

    @classmethod
    def send_invoice(cls, payload):
        """
        Emitir Factura de Consumo Electrónica (32)
        """
        url = cls.config.endpoint_invoices
        response = cls.post(url, data=payload, expected_response_code=201)
        return response.json()

    @classmethod
    def get_invoice_status(cls, invoice_id: str, company_id: str = None):
        """
        Consultar el estado de la Factura de Consumo Electrónica (32)
        """
        url = cls.config.endpoint_invoices_status.format(id=invoice_id)
        if company_id:
            url += f'/idCompany/{company_id}'
        response = cls.get(url, expected_response_code=200)
        return response.json()

    @classmethod
    def send_debit_note(cls, payload):
        """
        Emitir Nota de Débito Electrónica (33)
        """
        url = cls.config.endpoint_debit_notes
        response = cls.post(url, data=payload, expected_response_code=201)
        return response.json()

    @classmethod
    def get_debit_note_status(cls, debit_note_id: str, company_id: str = None):
        """
        Consultar el estado de la Nota de Débito Electrónica (33)
        """
        url = cls.config.endpoint_debit_notes_status.format(id=debit_note_id)
        if company_id:
            url += f'/idCompany/{company_id}'
        response = cls.get(url, expected_response_code=200)
        return response.json()

    @classmethod
    def send_credit_note(cls, payload):
        """
        Emitir Nota de Crédito Electrónica (34)
        """
        url = cls.config.endpoint_credit_notes
        response = cls.post(url, data=payload, expected_response_code=201)
        return response.json()

    @classmethod
    def get_credit_note_status(cls, credit_note_id: str, company_id: str = None):
        """
        Consultar el estado de la Nota de Crédito Electrónica (34)
        """
        url = cls.config.endpoint_credit_notes_status.format(id=credit_note_id)
        if company_id:
            url += f'/idCompany/{company_id}'
        response = cls.get(url, expected_response_code=200)
        return response.json()

    @classmethod
    def send_purchase(cls, payload):
        """
        Emitir Documento de Compra Electrónico (41)
        """
        url = cls.config.endpoint_purchases
        response = cls.post(url, data=payload, expected_response_code=201)
        return response.json()

    @classmethod
    def get_purchase_status(cls, purchase_id: str, company_id: str = None):
        """
        Consultar el estado del Documento de Compra Electrónico (41)
        """
        url = cls.config.endpoint_purchases_status.format(id=purchase_id)
        if company_id:
            url += f'/idCompany/{company_id}'
        response = cls.get(url, expected_response_code=200)
        return response.json()

    @classmethod
    def send_minor_expense(cls, payload):
        """
        Emitir Documento de Gasto Menor Electrónico (43)
        """
        url = cls.config.endpoint_minorexpenses
        response = cls.post(url, data=payload, expected_response_code=201)
        return response.json()

    @classmethod
    def get_minor_expense_status(cls, minor_expense_id: str, company_id: str = None):
        """
        Consultar el estado del Documento de Gasto Menor Electrónico (43)
        """
        url = cls.config.endpoint_minorexpenses_status.format(id=minor_expense_id)
        if company_id:
            url += f'/idCompany/{company_id}'
        response = cls.get(url, expected_response_code=200)
        return response.json()

    @classmethod
    def send_special_regime(cls, payload):
        """
        Emitir Documento de Régimen Especial Electrónico (44)
        """
        url = cls.config.endpoint_special_regimes
        response = cls.post(url, data=payload, expected_response_code=201)
        return response.json()

    @classmethod
    def get_special_regime_status(cls, special_regime_id: str, company_id: str = None):
        """
        Consultar el estado del Documento de Régimen Especial Electrónico (44)
        """
        url = cls.config.endpoint_special_regimes_status.format(id=special_regime_id)
        if company_id:
            url += f'/idCompany/{company_id}'
        response = cls.get(url, expected_response_code=200)
        return response.json()

    @classmethod
    def send_gubernamental(cls, payload):
        """
        Emitir Documento Gubernamental Electrónico (45)
        """
        url = cls.config.endpoint_gubernamentals
        response = cls.post(url, data=payload, expected_response_code=201)
        return response.json()

    @classmethod
    def get_gubernamental_status(cls, gubernamental_id: str, company_id: str = None):
        """
        Consultar el estado del Documento Gubernamental Electrónico (45)
        """
        url = cls.config.endpoint_gubernamentals_status.format(id=gubernamental_id)
        if company_id:
            url += f'/idCompany/{company_id}'

        response = cls.get(url, expected_response_code=200)
        return response.json()

    @classmethod
    def send_export_support(cls, payload):
        """
        Emitir Documento de Soporte de Exportación Electrónico (46)
        """
        url = cls.config.endpoint_export_supports
        response = cls.post(url, data=payload, expected_response_code=201)
        return response.json()

    @classmethod
    def get_export_support_status(cls, export_support_id: str, company_id: str = None):
        """
        Consultar el estado del Documento de Soporte de Exportación Electrónico (46)
        """
        url = cls.config.endpoint_export_supports_status.format(id=export_support_id)
        if company_id:
            url += f'/idCompany/{company_id}'
        response = cls.get(url, expected_response_code=200)
        return response.json()

    @classmethod
    def send_payment_abroad_support(cls, payload):
        """
        Emitir Documento de Soporte de Pagos al Exterior Electrónico (47)
        """
        url = cls.config.endpoint_payment_abroad_supports
        response = cls.post(url, data=payload, expected_response_code=201)
        return response.json()

    @classmethod
    def get_payment_abroad_support_status(cls, payment_abroad_support_id: str, company_id: str = None):
        """
        Consultar el estado del Documento de Soporte de Pagos al Exterior Electrónico (47)
        """
        url = cls.config.endpoint_payment_abroad_supports_status.format(id=payment_abroad_support_id)
        if company_id:
            url += f'/idCompany/{company_id}'
        response = cls.get(url, expected_response_code=200)
        return response.json()

    @classmethod
    def send_cancellation(cls, payload):
        """
        Este endpoint sirve para emitir anulaciones, las cuales se usan para
        anular rangos de numeración que no se usarán
        """
        url = cls.config.endpoint_cancellations
        response = cls.post(url, data=payload, expected_response_code=201)
        return response.json()

    @classmethod
    def get_cancellation_status(cls, cancellation_id: str, company_id: str = None):
        """
        Consultar el estado de la anulación
        """
        url = cls.config.endpoint_cancellations_status.format(id=cancellation_id)
        if company_id:
            url += f'/idCompany/{company_id}'
        response = cls.get(url, expected_response_code=200)
        return response.json()