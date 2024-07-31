from types import SimpleNamespace

import requests

from .config import (
    API_URL,
    DEVELOPER_API_URL,
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
                try:
                    self.response.raise_for_status()
                except Exception as e:
                    return {'error': str(e)}
        return {}


class Session:
    __token = None
    __api_url = None

    def __init__(self, token: str, developer_mode=False):
        self.login(token, developer_mode)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.__token = None
        self.__api_url = None

    def login(self, token: str, developer_mode=False):
        self.__token = token
        if developer_mode is True:
            self.__api_url = DEVELOPER_API_URL
        else:
            self.__api_url = API_URL

    def logout(self):
        self.__token = None
        self.__api_url = None

    @property
    def is_authenticated(self):
        return self.__token is not None

    @property
    def headers(self):
        return {
            'accept': 'application/json',
            'content-type': 'application/json',
            'authorization': f'Bearer {self.__token}'
        }

    def get(self, url):
        response = requests.get(url, headers=self.headers)
        return Response(response)

    def post(self, url, data=None, json=None):
        response = requests.post(url, data=data, json=json, headers=self.headers)
        return Response(response)

    def patch(self, url, data=None, json=None):
        response = requests.patch(url, data=data, json=json, headers=self.headers)
        return Response(response)

    def build_url(self, endpoint: str, **query: dict):
        query_string = ''
        if query:
            query_string = '?' + '&'.join([f'{k}={v}' for k,v in query.items()])
        return f'{self.__api_url}{endpoint}{query_string}'

    def get_provider_info(self):
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
        url = self.build_url('provider-info')
        res = self.get(url)
        return res.json()

    def sign_document(self, id_company):
        """Firmado de XML de postulación.
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
        res = self.post(url)
        return res.json()


class Resource(SimpleNamespace):

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