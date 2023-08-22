
from typing import List, Tuple
from types import SimpleNamespace

from alanube.api import Resource

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
    NCF_E_31,
    NCF_E_32,
    NCF_E_33,
    NCF_E_34,
    NCF_E_41,
    NCF_E_43,
    NCF_E_44,
    NCF_E_45,
)


class Company(Resource):

    def __init__(self):
        url = self.build_url('company')
        res = self.get(url)
        super().__init__(res)

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

    def check_set_tests(self):
        """consultar el set de pruebas asociado a la compañía principal."""
        url = self.build_url(f'check-set-tests/{self.id}')
        res = self.get(url)
        return Resource(res)


class Invoice(Resource):
    pass


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
