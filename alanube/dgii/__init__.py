
from typing import Any, Dict, List, Tuple
from types import SimpleNamespace
import requests

from .utils import count_ncf_sequence, split_ncf
from .forms import (
    CancellationHeaderForm,
    CancellationItemForm,
    CancellationItemRangeCancelledEnfcForm,
    CreditNoteForm,
    InvoiceForm,
    CancellationForm,
)
from .config import (
    API_URL,
    NCF_E_31,
    NCF_E_32,
    NCF_E_33,
    NCF_E_34,
    NCF_E_41,
    NCF_E_43,
    NCF_E_44,
    NCF_E_45,
)


class Response:
    ok: bool
    url: str
    status_code: int

    def __init__(self, response: requests.Response):
        self.response = response

    def __getattr__(self, __name: str):
        return getattr(self.response, __name)

    def __str__(self):
        return f'Response(ok: {self.ok}, status_code: {self.status_code}, url: {self.url} errors: {self.errors})'

    @property
    def errors(self):
        if self.status_code >= 400:
            try:
                return self.json()
            except ValueError as e:
                return {'error': f'Failed to parse response as JSON. {e}'}
        return {}


class Session:
    __token = None

    @classmethod
    def login(cls, token):
        cls.__token = token

    @classmethod
    def logout(cls):
        cls.__token = None

    @classmethod
    def is_authenticated(cls):
        return cls.__token is not None

    @classmethod
    def headers(cls, token=None):
        token = token or cls.__token
        
        return {
            'accept': 'application/json',
            'content-type': 'application/json',
            'authorization': f'Bearer {token}'
        }

    @classmethod
    def get(cls, url, token=None):
        response = requests.get(url, headers=cls.headers(token))
        response.raise_for_status()
        return Response(response)

    @classmethod
    def post(cls, url, data=None, json=None, token=None):
        response = requests.post(url, data=data, json=json, headers=cls.headers(token))
        response.raise_for_status()
        return Response(response)

    @classmethod
    def patch(cls, url, data=None, json=None, token=None):
        response = requests.patch(url, data=data, json=json, headers=cls.headers(token))
        response.raise_for_status()
        return Response(response)

    @classmethod
    def build_url(cls, endpoint: str, api_url = API_URL, **query: dict):
        query_string = ''
        if query:
            query_string = '?' + '&'.join([f'{k}={v}' for k,v in query.items()])
        return f'{api_url}{endpoint}{query_string}'

    @classmethod
    def check_dgii_status(cls, environment: int = None):
        """Consulta de salud a los servicios de la API DGII

        Los servicios de facturación electrónica de la DGII brinda una seria de
        recursos para poder conocer el estado actual de sus servicios, de esta
        forma estar siempre actualizado y alerta ante cualquier caída. Por esta
        razón, la API de Alanube pone a disposición de sus usuarios un endpoint
        que facilita obtener toda esta información en un solo recurso.

        https://developer.alanube.co/docs/consulta-de-salud-a-los-servicios-de-la-api-dgii

        Args:
        ------------
        * `environment` (int, optional):
            1. PreCertificacion
            2. Producción
            3. Certificacion

        Return:
        ------------
        ```
        [
            {
                "servicio": "Autenticación",
                "estatus": "Disponible"
            },
            {
                "servicio": "Recepción",
                "estatus": "Disponible"
            },
            {
                "servicio": "Consulta Resultado",
                "estatus": "Disponible"
            },
            {
                "servicio": "Consulta Estado",
                "estatus": "Disponible"
            },
            {
                "servicio": "Consulta Directorio",
                "estatus": "Disponible"
            },
            {
                "servicio": "Consulta TrackIds",
                "estatus": "Disponible"
            },
            {
                "servicio": "Aprobación Comercial",
                "estatus": "Disponible"
            },
            {
                "servicio": "Anulación Rangos",
                "estatus": "Disponible"
            },
            {
                "servicio": "Recepción FC",
                "estatus": "Disponible"
            }
        ]
        ```
        """
        url = cls.build_url('check-dgii-status', environment=environment)
        return cls.get(url)

    @classmethod
    def get_company(cls):
        url = cls.build_url('company')
        res = cls.get(url)
        return Company(res)

    @classmethod
    def get_provider_info(cls):
        """Obtener la información necesaria para la postulación

        Para iniciar el proceso de certificación, se debe comenzar con la
        postulación y para esto es necesario obtener la información de Alanube
        y la información de las url de recepción.
        https://developer.alanube.co/docs/proceso-de-certificaci%C3%B3n

        Return:
        -------------
        ```json
        {
            "data": {
                "softwareType": {
                    "description": "Tipo de software",
                    "value": "EXTERNO"
                },
                "softwareName": {
                    "description": "Nombre del software",
                    "value": "Alanube"
                },
                "softwareVersion": {
                    "description": "version",
                    "value": 1
                },
                "providerData": {
                    "description": "Datos del proveedor",
                    "rnc": {
                        "description": "RNC/Cedula del proveedor",
                        "value": 132109122
                    },
                    "name": {
                        "description": "Nombre/Razón social del proveedor",
                        "value": "Alanube Soluciones SRL"
                    },
                    "tradeName": {
                        "description": "Nombre comercial",
                        "value": "Alanube Soluciones"
                    }
                }
            }
        }
        ```
        """
        url = cls.build_url('provider-info')
        res = cls.get(url)
        return res.json()

    @classmethod
    def sign_document(cls, id_company):
        """Firmado de XML de postulación.

        Esto retornará un link para descargar el archivo XML firmado, el cual
        deberá ser cargado en la DGII para activar el ambiente de certificación
        el cual es necesario para iniciar el set de pruebas.
        https://developer.alanube.co/docs/proceso-de-certificaci%C3%B3n

        Return:
        ----------
        ```json
        {
            "signedDocumentUrl": "http:/api-alanube-e-provider-dom-prod/..."
        }
        ```

        """
        url = f'https://ap.alanube.co/dom/v1/sign-document/idCompany/{id_company}'
        res = cls.post(url)
        return res.json()


class Resource(SimpleNamespace, Session):

    def __init__(self, response: requests.Response):
        data = response.json()
        super().__init__(**data)
        self._meta = SimpleNamespace(**{
            'response': response,
            'url': response.url,
            'data': data,
        })

    def __repr__(self):
        def parse(dic):
            if isinstance(dic, dict):
                return '  ' + '  '.join([f'{k}: {parse(v)}\n' for k,v in dic.items()])
            return dic
        return parse(self.as_dict())

    def save(self):
        data = self.as_dict()
        if data.get('id'):
            return self.patch(self._meta.url, data)
        return self.post(self._meta.url, data)

    def as_dict(self):
        data = self.__dict__.copy()
        data.pop('_meta', None)
        return data


class Company(Resource):

    def __init__(self):
        url = self.build_url('company')
        res = self.get(url)
        super().__init__(res)

    def check_set_tests(self):
        """consultar el set de pruebas asociado a la compañía principal."""
        url = self.build_url(f'check-set-tests/{self.id}')
        res = self.get(url)
        return Resource(res)


class Invoice(Resource):

    @classmethod
    def create(cls, form: InvoiceForm | CreditNoteForm):
        """
        Returns:
            ```
            {
                "id": "01H22Z1JS88EWQCB4HZ9499TZ3",
                "stampDate": "1990-12-31",
                "status": "REGISTERED",
                "companyIdentification": 133109124,
                "encf": "E310000000005"
            }
            ```
        """
        encf = form.id_doc.encf
        url = cls.get_url_from_encf(encf)
        response = cls.post(url, json=form.data)
        return response

    @classmethod
    def get_url_from_encf(cls, encf: str):
        endpoint = cls.get_endpoint_from_ncf(encf)
        return cls.build_url(endpoint)

    @classmethod
    def get_endpoint_from_ncf(cls, encf: str):
        serie, code, sequence = split_ncf(encf)

        encf_code_endpoint_map = {
            NCF_E_31: 'fiscal-invoices',
            NCF_E_32: 'invoices',
            NCF_E_33: 'debit-notes',
            NCF_E_34: 'credit-notes',
            NCF_E_41: 'purchases',
            NCF_E_43: 'minor-expenses',
            NCF_E_44: 'special-regimes',
            NCF_E_45: 'gubernamentals',
            # NCF_E_46: 'export-supports' FIXME: No hay información de esto en la DGII
            # NCF_E_47: 'payment-abroad-supports', FIXME: No hay información de esto en la DGII
        }
        return encf_code_endpoint_map[code]

    @classmethod
    def check_status(cls, encf: str, status_id: str):
        """Consulta el estado de la factura electrónica"""
        url = cls.get_url_from_encf(encf) + f'/{status_id}'
        res = cls.get(url)
        return InvoiceStatus(res)


class InvoiceStatus(Resource):
    pass


class Cancellation(Resource):

    @classmethod
    def create(cls, form: CancellationForm):
        """
        Returns:
            ```
            {
                "id": "01H22Z1JS88EWQCB4HZ9499TZ3",
                "stampDate": "1990-12-31",
                "status": "REGISTERED",
                "companyIdentification": 133109124,
                "encf": "E310000000005"
            }
            ```
        """
        url = cls.build_url('cancellations')
        response = cls.post(url, json=form.data)
        return response

    @classmethod
    def check_status(cls, status_id: str):
        """Consulta el estado de la anulación"""
        url = cls.build_url(f'cancellations/{status_id}')
        res = cls.get(url)
        return CancellationStatus(res)


class CancellationStatus(Resource):
    pass


def create_simple_cancellation(rnc_sender: int, sequences: List[Tuple[str, str]]):
    """
    Crea una cancelacción de NCF de manera simple.

    Args:
    ---------
    * `rnc_sender` (int): Corresponde al Número de Registro Nacional del
        contribuyente que emite la factura electrónica.
    * `sequences` (List[Tuple[str, str]]): Una lista de rangos
        (secuencia_inicial, secuencia_final) de los comprobantes que se van a anular.

    Returns:
    ---------
    (CancellationForm, Response): Retorna una tupla.

    Example:
    ---------
    >>> create_simple_cancellation(
        rnc_sender='132000000',
        sequences=[
            ('E310000000001', 'E310000000010'),
            ('E320000000004', 'E310000000005'),
        ]
    )
    (CancellationForm, Response)

    """
    cancelled_encf_quantity = 0
    items = []
    line_number = 1
    for sequence in sequences:
        item_cancelled_encf_quantity = count_ncf_sequence(*sequence)
        cancelled_encf_quantity += item_cancelled_encf_quantity
        ncf_from_parts = split_ncf(sequence[0])
        ncf_until_parts = split_ncf(sequence[1])

        item = CancellationItemForm(
            line_number=line_number,
            ecf_type=int(ncf_from_parts[1]),
            range_cancelled_enfc=[
                CancellationItemRangeCancelledEnfcForm(
                    encf_from=sequence[0],
                    encf_until=sequence[1],
                )
            ],
            cancelled_encf_quantity=item_cancelled_encf_quantity,
        )

        line_number += 1
        items.append(item)

    header_form = CancellationHeaderForm(
        rnc_sender=rnc_sender,
        cancelled_encf_quantity=cancelled_encf_quantity,
    )

    cancellation_form = CancellationForm(
        header=header_form,
        cancellations=items,
    )

    response = Cancellation.create(cancellation_form)
    return (cancellation_form, response)


class DirectoryAndStatus(Resource):

    def check_directory(self, id_company=None) -> List[SimpleNamespace]:
        """Consultar el directorio de compañías activas para facturación electrónica."""
        url = self.build_url('check-directory')
        if id_company:
            url += f'/idCompany/{id_company}'
        res = self.get(url)
        return [SimpleNamespace(data) for data in res.json()]

    def check_dgii_status(self, id_company = None) -> SimpleNamespace:
        url = self.build_url('check-dgii-status')
        if id_company:
            url += f'/idCompany/{id_company}'
        res = self.get(url)
        return SimpleNamespace(res.json())
